# Unified Swift Workspace And Cloud Boundary Plan

## Status

Partially implemented on `docs/unify-swift-server-workflow`. The follow-up
[canonical adoption and legacy-removal plan](./canonical-swift-workspace-adoption-and-legacy-removal-plan.md)
owns the remaining existing-repository migration, extension placement, legacy
surface deletion, and contradictory deployment cleanup. Release and issue closure
remain separate lifecycle work. This plan coordinates GitHub issues [#183](https://github.com/gaelic-ghost/socket/issues/183), [#185](https://github.com/gaelic-ghost/socket/issues/185), [#186](https://github.com/gaelic-ghost/socket/issues/186), and [#187](https://github.com/gaelic-ghost/socket/issues/187).

Issue [#182](https://github.com/gaelic-ghost/socket/issues/182) remains a separate bootstrap-runner discovery fix. The current `bootstrap-xcode-workspace` implementation and regression test appear to cover its versioned-cache failure mode; verify that issue independently and do not widen this plan to carry unrelated compatibility cleanup.

## Outcome

Socket will teach one default Swift product workflow:

1. Create one root Xcode workspace at the beginning of the repository's life.
2. Add Apple apps, shared packages, and server executables to that workspace without later project conversion.
3. Run and test server code natively on macOS, using already-installed Homebrew services for local dependencies.
4. Use Soto by default for AWS access from Swift.
5. Build Linux deployment artifacts and perform test or production cloud deployments only in GitHub Actions.

This is a durable product-workspace and deployment-boundary change. It is not a compatibility wrapper around the current standalone-service, Docker-Compose-local, or local-Linux-build paths.

## Why The Current Model Fails

The current guidance makes each decision in isolation:

- `bootstrap-xcode-workspace` assumes at least one Apple app target and treats packages as app-support modules.
- `bootstrap-hummingbird-service` and `bootstrap-vapor-service` create standalone SwiftPM repositories with separate generated guidance.
- package workflows run a repo-wide “Xcode or SwiftPM” classifier and treat the intended mixed root as an exceptional state requiring handoff or opt-in.
- server bootstraps require Docker Compose PostgreSQL and preserve local container validation.
- deployment guidance still permits bounded local image checks even when GitHub owns the release artifact.
- no server-side Swift skill owns the AWS SDK choice, so a generic AWS handoff can select the official AWS SDK without applying Gale's Soto default.

The practical failure is predictable: a repository starts in one shape, a new target forces a migration, local integration tests start container infrastructure, and a Linux deployment requirement turns Gale's Mac into an unofficial CI runner.

The simpler option considered was to add warnings to the existing independent workflows. That would leave multiple bootstrap entry points, multiple guidance-sync surfaces, and multiple locally valid deployment paths. It would not make the intended workflow mechanically easier or the conflicting workflow invalid, so it is rejected.

## Target Architecture

### Repository Shape

```text
Product/
  Product.xcworkspace/              # permanent human and agent entry point
  Product.xcodeproj/                # generated from XcodeGen sources
  project.yml                       # root XcodeGen project graph
  Apps/                             # Apple application and test targets
  Packages/                         # shared SwiftPM library packages
  Services/                         # deployable SwiftPM executable packages
  Configurations/
  Scripts/
  .github/workflows/
  AGENTS.md  CONTRIBUTING.md  Justfile
```

The directory roots express deployment and ownership boundaries, not different repository types:

| Surface | Owner | Contract |
| --- | --- | --- |
| Root workspace | `apple-dev-skills:bootstrap-xcode-workspace` | Permanent entry point for every Gale-owned Swift product repository. |
| Root project and Apple targets | XcodeGen sources | `project.yml`, included target fragments, and `.xcconfig` files are authoritative; generated project data is never hand-edited. |
| Shared libraries | SwiftPM under `Packages/` | `Package.swift` owns products, targets, dependencies, and tests. |
| Server executables | SwiftPM under `Services/` | Each service package owns its executable/library/test targets and server dependencies. |
| Framework-specific service content | `server-side-swift` component adapters | Hummingbird or Vapor code, configuration, persistence, and framework handoffs. |
| Local dependency lifecycle | Native macOS plus Homebrew services | No Compose, Colima, Lima, Docker Desktop, QEMU, or local Linux VM in the standard path. |
| Cloud artifact and deployment lifecycle | GitHub Actions | Clean hosted build, immutable artifact identity, protected environment, OIDC, deploy, health verification, and rollback record. |

### Workspace Composition

The root workspace remains the stable opening surface while SwiftPM remains the service build-graph source of truth.

- Extend the generated workspace composition to include local package roots that need first-class Xcode schemes.
- Extend the workspace bootstrap so a repository may begin as app-only, service-only, package-only, or mixed without changing its root shape later.
- Add an idempotent `add-component` operation for Apple apps, shared packages, Hummingbird services, and Vapor services.
- Keep framework adapters behind the workspace entry point. Apple Dev Skills owns repository/workspace composition; Server-Side Swift owns the contents of `Services/<Service>`.
- Prove the generated service scheme with `xcodebuild -list -workspace` and a native macOS build/run/test. Do not duplicate service sources into an XcodeGen command-line target merely to make them visible.
- Keep standalone package bootstrap only for a deliberately standalone published library or CLI that is not a Gale-owned product repository. Make that exception explicit at creation time.

There is no repository-wide “Xcode or SwiftPM” classification in the target model. Every Gale-owned Swift product repository is intentionally both:

- use the workspace when the operation needs a scheme, destination, preview, simulator/device, Xcode diagnostics, or generated-project state;
- use the nearest `Package.swift` when the operation changes or executes a package, library, plugin, macro, or service target;
- route by the requested operation and component path, never by treating the presence of both Xcode and SwiftPM markers as ambiguity.

Delete `mixed_root`, `mixed_root_opt_in`, `--mixed-root-opt-in`, plain-versus-mixed root results, and repo-level handoff branches. Replace duplicated `repo-shape-detection.md` and `xcode-handoff-conditions.md` references with one operation-based execution-surface contract. A deliberately standalone third-party or published package is an explicit repository contract, not something inferred because Xcode files are absent.

### One Public Bootstrap And Alignment Surface

- Make `bootstrap-xcode-workspace` the only public fresh-repository and component-addition entry point for Gale-owned Swift products.
- Replace the public standalone `bootstrap-hummingbird-service` and `bootstrap-vapor-service` surfaces with workspace component adapters. Do not leave duplicate compatibility paths.
- Retire `sync-hummingbird-service-guidance`. Extend the workspace's managed `just align` contract to cover `Services/AGENTS.md`, native service commands, and CI-owned deployment wording.
- Stop asking guidance-sync, DocC, source-structure, package build/run, package testing, and package-extension workflows to classify the entire repository as Xcode or SwiftPM. They should locate the requested component and select the execution surface required by the operation.
- Preserve focused Hummingbird, Vapor, persistence, OpenAPI, authentication, and runtime skills for ongoing implementation after the component exists.

## Non-Negotiable Development And Deployment Contract

### Local macOS

Local work may:

- resolve Swift packages;
- build, run, and test Swift code natively for macOS;
- use Xcode or `swift build`, `swift run`, and `swift test` against the same SwiftPM service targets;
- inspect already-installed Homebrew service formulae with `brew services list`;
- start a required installed PostgreSQL, Redis, or other declared native service with `brew services start <formula>`;
- run native integration tests against isolated test databases or namespaces;
- validate deployment configuration statically without creating the Linux artifact.

Local work must not:

- run Docker Compose as the normal dependency path;
- start or resize Colima, Lima, Docker Desktop, QEMU, Apple container machines, or another Linux VM for development or deployment packaging;
- build, cross-compile, or package a Linux cloud artifact;
- perform a test, staging, live, or production cloud deployment;
- represent native unit/integration success as evidence that a Linux artifact or live deployment succeeded.

Generated repo commands should make the allowed path shorter than the forbidden path. Provide explicit native recipes such as service status/start, service run, unit test, and integration test. If a required Homebrew formula is absent, stop with an actionable prerequisite; do not silently install it or switch to a container.

### GitHub Actions

GitHub owns every cloud-bound build and deployment:

- pull-request validation may include hosted Linux compilation and tests;
- a reviewed `main` commit produces the immutable artifact for the protected `test` environment;
- a reviewed SemVer release produces or promotes the immutable production artifact according to the repository's release contract;
- test and production deployments use GitHub environments, scoped OIDC identity, environment protection, concurrency, health verification, and recorded rollback identity;
- OCI deployments use an image digest; archive/Lambda deployments use an artifact checksum and release manifest;
- production hosts and developer machines consume artifacts but never rebuild source.

The provider-neutral cloud contract belongs in `cloud-deployment-skills`. Server-Side Swift supplies framework/package validation and artifact inputs. The official AWS plugin supplies AWS account, IAM, and provider-adapter details without overriding the repository's GitHub-only build boundary.

## Soto AWS Standard

Add a focused Server-Side Swift AWS integration workflow because no current owner applies a Swift-specific SDK decision before the generic AWS handoff.

The workflow contract is:

- Soto is the default for new Swift AWS integrations.
- Add fetchable, versioned SwiftPM dependencies from `soto-project/soto`; add only the service products the target consumes.
- Create one `AWSClient` per long-running application process or Lambda execution environment, share it across service clients, and shut it down once at lifecycle termination.
- Prefer the default credential-provider chain and workload identity. Never commit static AWS credentials.
- Keep the client outside a per-request or per-invocation handler so warm Lambda invocations reuse it.
- The official AWS SDK for Swift is an exception only when a required service/API, compatibility constraint, upstream defect, or existing repository contract makes Soto unsuitable.
- Every exception records the missing capability or constraint, the checked Soto version, and why a narrower adapter is insufficient.
- Do not migrate an existing repository's SDK merely because the default changed; migration remains a separate requested task.

The official AWS plugin continues to own infrastructure and provider operations. It does not own the Swift package dependency choice.

## Consolidation Workstreams

### 1. Strengthen The Workspace Primitive

Primary owner: `plugins/apple-dev-skills`.

- Expand `bootstrap-xcode-workspace` inputs from an Apple-platform list into a component model that can represent app, shared-package, Hummingbird-service, and Vapor-service components.
- Support `create`, `align`, and idempotent `add-component` operations.
- Permit service-only and package-only initial roots; remove the validator requirement for at least one `Apps/**/target.yml` when another valid component exists.
- Generate and maintain `Services/`, `Services/services-shared.yml` or an equivalent declarative registry, and `Services/AGENTS.md`.
- Extend workspace generation so local service package schemes appear without duplicating the SwiftPM graph.
- Extend `Justfile`, validation, pre-commit, and `maintain-project-repo`'s `xcode-workspace` profile for Apps, Packages, and Services.
- Narrow the package workflow's mixed-root handoff: workspace presence should select the root workspace for Xcode state, but must not make ordinary SwiftPM manifest/build/test work invalid inside `Packages/` or `Services/`.
- Remove the package workflow's repo-shape classifier and mixed-root handoff system entirely. Workspace presence is normal; ordinary SwiftPM work inside `Packages/` or `Services/` remains valid without opt-in.
- Remove the same repo-wide classifier from Swift DocC authoring, Swift source-structure, and guidance-sync paths. Route DocC generation/export and source validation from the requested target/component instead.
- Replace the `swift-package` versus `xcode-workspace` automatic maintenance-profile choice for Gale-owned products with the workspace profile. Keep a standalone-package profile only behind an explicit standalone package contract.
- Update Apple plugin metadata, README, managed guidance, Hermes export decision, and tests together.

Acceptance tests:

1. Create a service-only Hummingbird workspace and list its service scheme.
2. Add an iOS app to that repository without moving or converting the service package.
3. Create an app-only workspace, add a Vapor service, and retain the original app schemes.
4. Re-run `add-component` and fail safely without duplicate targets or overwritten local guidance.
5. Run `just align` twice and produce no second-pass diff.
6. Run package build, test, extension, DocC, and source-structure workflows inside a workspace without a mixed-root handoff or opt-in flag.

### 2. Replace Standalone Server Bootstrap And Sync Paths

Primary owner: `plugins/server-side-swift`.

- Replace standalone bootstrap skills with Hummingbird and Vapor workspace component adapters.
- Remove Docker Compose as a generated local dependency and validation surface.
- Keep a generated Dockerfile only when the chosen GitHub deployment artifact is OCI; mark it CI-only.
- Generate native macOS configuration defaults for `localhost` Homebrew services and isolated tests.
- Replace separate Hummingbird guidance sync with the root `just align` managed surface.
- Update `AGENTS.md`, plugin metadata/prompts, local environment templates, generated assets, ongoing framework workflows, Docker/Containerization handoffs, and root roadmap wording.
- Add child validation; the server plugin currently has no focused behavior test suite for these bootstrap contracts.

Acceptance tests:

1. Generated server guidance contains native Homebrew service commands and contains no local Compose startup command.
2. A stopped installed service may be started deliberately; a missing formula blocks instead of installing or creating a VM.
3. Hummingbird Server, Hummingbird Lambda, and Vapor shapes remain framework-correct inside `Services/`.
4. Generated local environment actions invoke native Swift and Homebrew commands only.

### 3. Add The Soto Decision Owner

Primary owner: `plugins/server-side-swift`.

- Add one AWS integration skill or equivalently focused owner surface; do not scatter the default independently through every framework skill.
- Link Hummingbird, Vapor, Lambda, and persistence workflows to that owner when AWS access is requested.
- Add Soto dependency, client-lifecycle, credential, retry/observability, test-double, and shutdown examples grounded in current Soto documentation.
- Add an explicit, machine-testable deviation record template for the official AWS SDK exception.
- Update plugin metadata and Hermes compatibility/export records.

Acceptance tests:

1. A new DynamoDB/SSM server fixture selects Soto products.
2. A long-running service fixture creates one shared client and shuts it down once.
3. A Lambda fixture keeps the client outside the invocation handler and reuses it across warm invocations.
4. An official-SDK fixture is rejected without a concrete exception reason.
5. An existing official-SDK repository is preserved unless migration was explicitly requested.

### 4. Make GitHub The Enforced Cloud Build Boundary

Primary owner: `plugins/cloud-deployment-skills`, with Server-Side Swift handoffs.

- Extract one provider-neutral GitHub-built artifact contract shared by OCI and archive/Lambda deployment workflows.
- Remove local release-image smoke builds from the standard contract. Local verification ends at native tests and static deployment checks.
- Make repository-declared `github-only` build/deploy ownership override generic Docker, SAM, containerization, cross-compilation, and VM recommendations.
- Add or generalize guidance for immutable archive checksums as well as OCI digests.
- Provide test and production GitHub environment patterns with OIDC, concurrency, approval, health, and rollback requirements.
- Update cloud routing so a Linux architecture requirement selects a hosted runner, not local virtualization.
- Update the server Docker, Apple Containerization, and Linux VM handoffs to respect the boundary.

Acceptance tests:

1. A GitHub-only Swift Lambda request produces no local Linux build, SAM package, Docker build, Colima, or VM command.
2. A test deployment is built from a clean hosted checkout and records the immutable artifact checksum or digest.
3. Production pauses at the protected environment and uses OIDC-scoped provider credentials.
4. Rollback selects a previously recorded immutable artifact and never rebuilds an old commit locally or on the host.
5. Reports distinguish native local tests, hosted artifact build, test deployment, and production deployment as four separate evidence states.

### 5. Put The Rule In Durable Guidance And Validation

Primary owners: root Socket guidance and each affected child plugin.

- Add the high-level one-workspace, native-local, Soto-default, and GitHub-only-cloud rules to root `AGENTS.md`.
- Keep detailed commands in their owning skills and generated repo assets; do not duplicate command matrices in root guidance.
- Update `ROADMAP.md` and retire this plan after the behavior, tests, and live guidance become authoritative.
- Add root compatibility validation that rejects reintroduced local Compose defaults, local Linux cloud builds, standalone Gale-product server bootstrap, or unqualified official AWS SDK defaults.
- Validate Codex and Hermes surfaces in the same pass. Mark Xcode-specific workspace mutation as Codex/Apple-host-specific while exporting portable policy and server/cloud guidance to Hermes.

## Implementation Sequence

The ordering prevents new guidance from pointing at incomplete runtime support.

1. Add failing contract tests for the target workspace shapes, native-local boundary, Soto choice, and GitHub-only deployment behavior.
2. Delete the repo-wide Xcode-versus-SwiftPM classifier, mixed-root flags, handoff branches, duplicate references, and tests; replace them with component/operation routing tests.
3. Extend the workspace model, generator, alignment runtime, and repository-maintenance profile.
4. Add Hummingbird and Vapor workspace component adapters; remove standalone bootstrap and separate sync surfaces.
5. Add the Soto AWS integration owner and fixtures.
6. Generalize the cloud artifact/deployment contract and enforce the repository override in Docker, container, VM, and AWS handoffs.
7. Regenerate/update plugin metadata, managed guidance assets, Hermes exports, root docs, and roadmap wording.
8. Run child tests, root compatibility validation, and end-to-end generated-repository scenarios.
9. Review issue acceptance criteria, close only the issues fully proven by the evidence, and keep #182 separate unless its own reproduction is rerun.

## Validation Matrix

| Layer | Required evidence |
| --- | --- |
| Apple workspace unit tests | Component normalization, service-only roots, add-component idempotence, declarative service registration, alignment preservation. |
| Execution-surface routing | No mixed-root flags or repo classifiers; package operations use the nearest manifest and Xcode-only operations use the root workspace. |
| Generated workspace integration | `xcodegen generate`, `xcodebuild -list -workspace`, native service build, native service tests. |
| Server child tests | Hummingbird/Vapor component output, Homebrew-only local commands, no Compose default, CI-only Dockerfile classification. |
| Soto fixtures | Dependency products, one-client lifecycle, Lambda warm reuse, shutdown, exception record. |
| Cloud contract tests | No local Linux build path, hosted artifact identity, `test` and `production` environment separation, OIDC, rollback identity. |
| Metadata and portability | Plugin manifests, prompts, skill inventory, Hermes tap export/validation, host-specific boundary notes. |
| Root validation | `just repo-validate`, then the relevant full profile before release. |

Build and test tools must run serially on Gale's machine. The end-to-end tests must not start containers, create VMs, deploy AWS resources, or mutate Homebrew installations.

## Migration And Compatibility

- New Gale-owned Swift product repositories use the workspace shape immediately, including server-only products.
- Existing canonical workspaces gain Services support through `align` and `add-component` without moving existing Apps or Packages.
- Existing standalone server repositories require one explicit adoption operation that creates the permanent workspace around their existing package without rewriting its manifest or source tree. After adoption, all future targets use `add-component`.
- Existing third-party or deliberately standalone published Swift packages remain package-first and do not gain a workspace unless requested.
- Existing repositories keep their chosen AWS SDK until a separate migration request.
- Remove retired Socket skill surfaces in the same release that updates metadata and routing. Do not leave duplicate shims or contradictory prompts.

## Risks And Controls

- **Xcode scheme visibility:** prove local service schemes in a generated fixture before settling the workspace registration format. Keep SwiftPM authoritative; reject any solution that copies service targets into the XcodeGen graph.
- **Cross-plugin orchestration:** keep workspace structure in Apple Dev Skills and framework content in Server-Side Swift. Use an explicit adapter handoff and fail clearly when the companion plugin is unavailable.
- **Homebrew service naming/version drift:** discover installed formula names at runtime and keep project configuration explicit. Do not hard-code one global PostgreSQL formula version as universal.
- **Shared local service state:** use project-specific test databases/namespaces and never stop or remove a user-managed service as automatic cleanup.
- **Cloud artifact variation:** share the GitHub ownership and evidence contract while keeping OCI digest and archive checksum adapters explicit.
- **Generic skill regressions:** preserve Docker, containerization, and VM workflows for explicitly requested unrelated work, but make the repository's deployment-boundary declaration a hard routing override.

## Definition Of Done

- Issues #183, #185, #186, and #187 have acceptance evidence mapped to committed tests and authoritative guidance.
- A new server-only repository starts with the same permanent workspace entry point as a mixed Apple/server product.
- Adding any supported new app, package, or service component does not require repository conversion.
- No shipped Gale-product workflow asks whether the repository is “an Xcode repo” or “a SwiftPM repo,” emits a mixed-root state, or requires mixed-root opt-in.
- Local generated commands are macOS-native and Homebrew-service-based, with no standard container or VM path.
- No Socket guidance permits Gale's Mac to build a Linux artifact for a repository whose cloud boundary is GitHub Actions.
- Test and production cloud deployments are GitHub-hosted, immutable-artifact-based, environment-gated, and OIDC-authenticated.
- Soto is the default new Swift AWS stack, and deviations are explicit and testable.
- Duplicate standalone server bootstrap and guidance-sync surfaces are removed.
- Child validation, root compatibility validation, metadata, managed guidance, and Hermes exports agree.
- The detailed plan is retired into concise `ROADMAP.md` history after implementation and release.

## Evidence Consulted

- [Apple: Organizing your code with local packages](https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages) establishes same-repository local Swift packages as a supported modular code shape.
- [Apple: Projects and workspaces](https://developer.apple.com/documentation/xcode/projects-and-workspaces) establishes the workspace as the place to manage related projects and dependencies.
- [XcodeGen Project Spec](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html) is the declarative project-generation contract already adopted by Socket.
- [Soto `AWSClient`](https://soto.codes/user-guides/awsclient.html) documents one shared application client in ordinary use and explicit shutdown ownership.
- [Soto on AWS Lambda](https://soto.codes/user-guides/using-soto-on-aws-lambda.html) documents keeping the client outside the invocation handler and tying shutdown to the Lambda handler lifecycle.
- [AWS SDK for Swift](https://github.com/awslabs/aws-sdk-swift) is the explicit alternative SDK whose use now requires a concrete exception.
- [Homebrew `brew(1)` services documentation](https://docs.brew.sh/Manpage#services-subcommand) owns the native service command behavior.
- [GitHub Actions deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments) documents protected environments, approval, branch restrictions, secrets, and deployment concurrency.
- [GitHub Actions OIDC for AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) documents short-lived AWS authentication and environment-bound trust conditions.
