# Canonical Swift Workspace Adoption And Legacy Removal Plan

## Status

Implemented on `docs/unify-swift-server-workflow`. This plan records the gaps
closed after the first unified-workspace pass and remains the acceptance contract
for review.

Do not merge, release, or close GitHub issues #183, #185, #186, or #187 as fully
remediated until this plan's definition of done passes on the reviewed branch.

## Decision

Socket will expose one Swift repository lifecycle through
`apple-dev-skills:bootstrap-xcode-workspace`:

1. `create` creates a new canonical workspace.
2. `adopt` migrates any existing Swift repository into that workspace.
3. `add-component` adds an app, app extension, library, or service without
   changing repository shape.
4. `align` refreshes the already-canonical workspace and managed guidance.

There is no separate app-project migration entrypoint, standalone Swift-package
bootstrap, repository-shape classifier, mixed-root compatibility mode, or broad
legacy routing skill. Build and test workflows remain operation-specific: they
use the nearest `Package.swift` for SwiftPM work and the root workspace for
Xcode-owned state.

## Canonical Target Architecture

```text
Product/
  Product.xcworkspace/
  Product.xcodeproj/                 # generated; never hand-edited
  project.yml
  Configurations/
  Apps/
    apps-shared.yml
    Apps-shared.xcconfig
    ProductiOS/                      # application target
      target.yml
      Sources/
      Resources/
      Configurations/
    ProductShareExtension/           # extension target; peer of the app
      target.yml
      Sources/
      Resources/
      Configurations/
    ProductiOSTests/                 # test target; peer Xcode target
    ProductiOSUITests/
  Packages/
    packages-shared.yml
    ProductCore/
      Package.swift
  Services/
    services-shared.yml
    ProductAPI/
      Package.swift
  Scripts/
  docs/
  .github/workflows/
```

### Extension Placement

- There is no root `Extensions/` directory.
- Every app extension is a first-class Xcode target directly under `Apps/`,
  adjacent to its host application and test targets.
- The extension owns its own `target.yml`, sources, resources, entitlements,
  Info.plist state, configurations, and tests when applicable.
- The host app's target graph owns embedding and signing the extension. The
  adoption map records the host-target relationship explicitly; name proximity
  is not sufficient evidence.
- `app-extension-architecture-workflow` owns extension-point behavior and target
  requirements. `bootstrap-xcode-workspace` owns placement, XcodeGen registration,
  host embedding, and the permanent workspace graph.

## Non-Negotiable Invariants

- One root `.xcworkspace` and one generated root `.xcodeproj` exist for every
  Gale-owned Swift repository.
- `Apps/`, `Packages/`, and `Services/` always exist, even when one is empty.
- All Xcode-native targets, including app extensions and test bundles, live as
  peers under `Apps/`.
- SwiftPM remains authoritative for library and executable packages under
  `Packages/` and `Services/`.
- The workflow inventories concrete components and operations. It never asks
  whether the whole repository is an Xcode repo, SwiftPM repo, plain repo, or
  mixed repo.
- Local service work uses native Swift and installed Homebrew services only.
- Linux artifacts, OCI builds, image smoke tests, live tests, and production
  deployments run only in GitHub Actions.
- Soto is the default AWS SDK for new Swift work, with one client lifecycle owner
  and a recorded exception required for the official SDK.
- No compatibility wrapper or alternate entrypoint remains after adoption.

## Current Gaps

| Surface | Current problem | Required outcome |
| --- | --- | --- |
| XcodeGen migrator | Classifies `xcode-managed-to-xcodegen` versus `modernize-xcodegen` and emits the old flat `Sources/`, `Tests/`, `Shared/`, and root `Extensions/` layout. | Fold safe audit/promotion behavior into workspace `adopt`; emit `Apps/`, `Packages/`, and `Services/`. |
| SwiftPM-only/service-only adoption | The migrator blocks repositories without Xcode project evidence. | Inventory manifests and executable/library products directly and create the permanent workspace around them. |
| App extensions | Legacy guidance treats `Extensions/` as a root. | Put every extension target directly under `Apps/` and record its host relationship. |
| Workspace align | `align` assumes the canonical shape already exists. | Keep `align` idempotent; add a distinct reviewed `adopt` operation for noncanonical repositories. |
| Creation entrypoints | `bootstrap-swift-package` remains a second repository bootstrap. | Delete it; library-first repositories use workspace `create --component-kind library`. |
| Compatibility routers | `swift-package-workflow` and `xcode-app-project-workflow` exist only for old names. | Delete both and route metadata/docs directly to focused build, test, and extension workflows. |
| Maintainer profiles | `maintain-project-repo` still classifies and exposes `swift-package` and `xcode-app`. | Remove both profiles and classification prose; Swift workspace callers pass `xcode-workspace` explicitly. |
| Docker guidance | Active steps still offer local development images, Compose stacks, and obsolete bootstrap behavior. | Make the server Docker skill definition-only locally and GitHub-execution-only. Remove Compose from Gale-product guidance. |
| Fly.io guidance | Active guidance runs local image checks plus direct `fly launch` and `fly deploy`. | Replace it with a GitHub-only provider adapter or remove the Fly surface if exact immutable deployment cannot be proved. |
| Framework workflows | Hummingbird/Vapor still list Docker/Compose and direct Fly handoffs. | Route deployment only through the GitHub artifact/deployment contract. |
| Local environment templates | Standalone package templates duplicate generated workspace commands and omit the shared Homebrew readiness gate. | Delete them; generated workspace `Justfile` and service scripts own local commands. |
| Apple container/VM routing | Server-side skills still expose local Linux/container-machine routes that can be selected despite the product override. | Remove the server-side Apple containerization surface and all inbound Swift-product handoffs; retain generic Apple virtualization research only outside product workflows. |
| Metadata and history | Prompts, profile descriptions, README inventories, checked roadmap history, and maintainer audits retain old names or optional-Services wording. | Align live metadata; mark retained history explicitly superseded and collapse stale planning docs after moving durable conclusions. |

## Target Public Workflow

### Create

`bootstrap-xcode-workspace --operation create` supports these first components:

- `--component-kind app`
- `--component-kind extension --host-target <AppTarget>` only after a host exists
- `--component-kind library`
- `--component-kind service --framework hummingbird|vapor`

All variants create the same root workspace and all three component roots.

### Adopt

`bootstrap-xcode-workspace --operation adopt --repo-root <root>` is the only
existing-repository migration path. It accepts any combination of:

- hand-managed `.xcodeproj` targets;
- existing Xcode workspaces or multiple project files;
- old or partial XcodeGen specs;
- root or nested SwiftPM libraries;
- root or nested Hummingbird/Vapor executables;
- app extensions, test targets, schemes, and test plans;
- repositories already combining several of those surfaces.

The operation does not assign a repository type. It inventories component owners
and produces one explicit adoption map.

### Add Component

`add-component` supports `app`, `extension`, `library`, and `service`.

For an extension it requires:

- target name;
- extension kind/product type grounded in current Apple/Xcode documentation;
- host app target;
- supported platform;
- bundle identifier and signing inputs when they cannot be derived safely.

Unknown or ambiguous extension product types block instead of becoming generic
application targets.

### Align

`align` remains safe and idempotent only for an already-canonical workspace. It
refreshes managed guidance, component registries, maintainer tooling, and
generated project output without discovering or converting a legacy layout.

## Adoption Design

### Phase A: Read-Only Inventory

The first pass is always non-mutating. It records concrete evidence:

- root and nested workspaces, projects, XcodeGen specs, and Swift manifests;
- every PBX native target and product type;
- app-to-extension embedding relationships;
- test-host and UI-test target relationships;
- SwiftPM products and targets, distinguishing libraries from executables;
- Hummingbird/Vapor dependency and executable evidence;
- sources, resources, build phases, package dependencies, configurations,
  schemes, test plans, Info.plist files, entitlements, asset catalogs, and
  build settings;
- existing Dockerfiles and deployment files as cloud inputs only;
- tracked `.pbxproj` differences that require promotion before regeneration.

The output is `components[]`, not `repo_shape`. Each component includes its
current owner, proposed canonical destination, dependencies, host relationship,
and unresolved evidence.

### Phase B: Reviewed Adoption Map

The workflow emits a reviewable mapping artifact before moving files or replacing
project state. It must explicitly map:

- application and extension targets to `Apps/<Target>/`;
- test targets to peer `Apps/<TargetTests>/` directories;
- library packages to `Packages/<Package>/`;
- server executables to `Services/<Service>/`;
- shared source to an owning package or named target rather than a root `Shared/`
  dumping ground;
- configurations, entitlements, plists, assets, schemes, and test plans to their
  canonical owners;
- every extension to one host app target.

Ambiguous ownership blocks adoption. The workflow must not infer an extension
host, collapse multiple products, rename public modules, or choose a service
framework from directory names alone.

### Phase C: Staged Canonical Sources

Apply the reviewed map on a named feature branch/worktree:

1. Create root XcodeGen and workspace source files.
2. Create `Apps/`, `Packages/`, and `Services/` registries.
3. Move component source with history-preserving Git operations where practical.
4. Promote GUI-owned `.pbxproj` state into XcodeGen, `.xcconfig`, entitlements,
   Info.plist files, resources, schemes, and test plans.
5. Register extension targets as `Apps/` peers and wire host embedding.
6. Preserve SwiftPM manifests as the owners of packages and services.
7. Remove generated Compose files from adopted Gale-owned services while
   retaining reviewed Dockerfiles only as GitHub cloud-build inputs.
8. Generate the candidate root project without deleting the old project yet.

### Phase D: Equivalence Validation

Compare pre-adoption and candidate state:

- target, product, scheme, and test-plan inventory;
- build configurations and material build settings;
- package/product dependencies;
- source and resource membership;
- app-extension host embedding, entitlements, bundle identifiers, and signing;
- app entrypoints and service executable entrypoints;
- `xcodebuild -list` against the permanent workspace;
- representative Debug builds and tests when the fixture supports them;
- native service build/test and Homebrew readiness commands;
- GitHub workflow syntax and immutable artifact/deployment contract.

Any unexplained target loss, ownership change, signing change, or scheme loss
blocks finalization.

### Phase E: Finalize Without Compatibility Paths

Only after equivalence passes:

1. Remove superseded hand-managed/generated project files.
2. Remove obsolete flat source roots after every file has a canonical owner.
3. Install the `xcode-workspace` maintainer profile.
4. Run workspace `align` twice and prove no second-pass diff.
5. Run the full Apple, server, repository, root, Hermes, and Claude/Cowork gates.

Do not leave forwarding scripts, duplicate project files, duplicate source trees,
alternate profiles, or migration-only wrappers in the adopted repository.

## Legacy Surface Removal Matrix

### Delete After Ownership Moves

- `apple-dev-skills:migrate-xcode-project-to-xcodegen`; move its safe PBX audit,
  promotion, and equivalence logic into workspace `adopt`.
- `apple-dev-skills:bootstrap-swift-package`; workspace library-first creation is
  the replacement.
- `apple-dev-skills:swift-package-workflow`; focused SwiftPM workflows remain.
- `apple-dev-skills:xcode-app-project-workflow`; focused Xcode build/test
  workflows remain, and the direct `.pbxproj` guard moves to the mutation owner.
- `repository-skills` `swift-package` and `xcode-app` profiles, assets, CLI
  choices, tests, and migration branches.
- Server-Side Swift standalone Codex local-environment templates.
- `server-side-swift:apple-containerization-workflow` and its Hermes export as a
  server development route.
- The existing direct/local `fly-io-deployment-workflow`; replace it only with a
  compliant GitHub provider adapter after current provider capability is proved.

### Rewrite In Place

- `bootstrap-xcode-workspace`: add `adopt` and `extension`, make the component
  model shared by create/adopt/add/align, and correct prompts to include Services
  and extensions.
- `app-extension-architecture-workflow`: require peer placement under `Apps/`
  and host embedding through XcodeGen.
- `maintain-project-repo`: remove repository classification; retain `generic` for
  non-Swift repositories and explicit `xcode-workspace` for Swift repositories.
- SwiftPM build/test/extension workflows: retain operation routing only and
  remove handoffs to deleted broad/creation skills.
- Xcode build/test workflows: absorb the `.pbxproj` mutation guard and remove
  handoffs to the deleted compatibility router.
- Docker workflow: own Dockerfile/runtime definition, while GitHub owns every
  build, smoke test, registry push, and deployment artifact.
- Hummingbird, Vapor, persistence, and deployment handoffs: native Homebrew local
  work only; GitHub cloud path only.
- Fly provider guidance, if retained: GitHub environment plus OIDC/short-lived
  credentials, prebuilt immutable artifact, exact deployment identity, health,
  and rollback. No local build, `fly launch`, or direct developer deployment.
- Root and child `AGENTS.md`, plugin manifests, README inventories, prompts,
  generated guidance, roadmap, architecture inventory, and portability exports.

### Preserve Only As Explicit History

- Checked ROADMAP accomplishments may retain deleted skill names only when the
  entry says they were superseded by the canonical workspace.
- Historical maintainer plans may remain only when labeled superseded and still
  useful. Otherwise move their durable conclusions into this plan/ROADMAP and
  delete them in the reviewed cleanup pass.
- Generic virtualization skills may remain for explicit OS, platform, or security
  research, but no Swift product skill may route local development or cloud
  artifact work into them.

## Implementation Slices

### Slice 1: Canonical Component Model

- Extract one component type/mapping model shared by create, adopt, add, align,
  validation, and tests.
- Add extension component support and `Apps/` peer placement.
- Update root/project/registry generation and workspace findings.
- Prove library-first, service-first, app-first, extension addition, and repeated
  alignment through generated fixtures.

### Slice 2: Existing-Repository Adoption

- Port PBX/XcodeGen audit logic into workspace adoption.
- Add SwiftPM library/service discovery without requiring Xcode markers.
- Emit the reviewed component map and block ambiguity.
- Stage canonical files, generate the candidate project, compare equivalence,
  and finalize only after validation.

### Slice 3: Delete Apple Compatibility Surfaces

- Remove the old migrator, standalone package bootstrap, and both broad routers.
- Redirect every prompt, README entry, test, customization inventory, and skill
  handoff to the canonical or focused owner.
- Move the `.pbxproj` safety guard before deleting its compatibility owner.

### Slice 4: Collapse Maintainer Profiles

- Remove `swift-package` and `xcode-app` profile choices and assets.
- Remove profile classification from skill prose and runtime.
- Keep explicit `generic` and `xcode-workspace` contracts only.
- Update installed profile migrations so adoption ends directly at
  `xcode-workspace`, without preserving old profile wrappers.

### Slice 5: Remove Local Linux And Direct Deployment Paths

- Purge obsolete Compose/local-image instructions from Server-Side Swift.
- Delete duplicated local environment templates and use generated workspace
  commands plus the shared Homebrew readiness script.
- Remove the server Apple-container route and inbound VM/container handoffs.
- Replace or delete direct Fly deployment guidance after a current official-docs
  capability check.
- Require GitHub environments, immutable identity, hosted smoke tests, health,
  and rollback for every retained provider adapter.

### Slice 6: Consolidate Docs, Metadata, And Exports

- Update all plugin manifests, prompts, READMEs, root/child guidance, and managed
  assets to the same four workspace operations.
- Remove deleted skills from validators, customization counts, inventories,
  Hermes allowlists, `skills.sh.json`, and generated tap output.
- Mark or collapse historical docs and annotate superseded ROADMAP entries.
- Regenerate architecture inventory only after the final skill graph is stable.

### Slice 7: Full Contract Validation

- Add negative scans that reject retired skill names and active legacy wording.
- Run child suites, root compatibility validation, metadata, type/lint,
  architecture, Hermes, and Claude/Cowork validation.
- Confirm the feature branch is clean and account for every unmerged branch before
  PR/release work begins.

## Required Fixture Matrix

| Fixture | Required proof |
| --- | --- |
| Hand-managed single app | PBX settings/resources/schemes preserved; app lands under `Apps/`. |
| Existing XcodeGen app | Old flat roots become target-owned `Apps/` content; second alignment is clean. |
| SwiftPM library-only | Workspace is created without Xcode-project prerequisites; package lands under `Packages/`. |
| Hummingbird service-only | Service lands under `Services/`; local commands are native/Homebrew; app can be added later unchanged. |
| Vapor service-only | Same boundary as Hummingbird, with framework-owned package structure preserved. |
| Existing mixed repository | Apps, packages, and services are inventoried independently; no whole-repo classification appears. |
| App plus one extension | Extension is `Apps/<ExtensionTarget>`, host embedding is preserved, and no root `Extensions/` exists. |
| Multiple apps/extensions | Every extension host relationship is explicit; ambiguous hosts block. |
| Tests and test plans | Test hosts, UI-test targets, schemes, and `.xctestplan` references survive. |
| Already-canonical workspace | `adopt` reports no migration; `align` twice produces no diff. |
| Ambiguous/unsupported target | Adoption blocks before writes and names the missing ownership/product evidence. |

## Negative Contract Tests

Active skills, scripts, metadata, templates, and generated exports must contain:

- no `repo_shape`, `mixed_root`, or Xcode-versus-SwiftPM repo classifier;
- no root `Extensions/` recommendation;
- no retired migration/bootstrap/router skill;
- no `swift-package` or `xcode-app` maintainer profile;
- no local Compose, Colima, VM, container-machine, LocalStack, Docker build, image
  smoke test, or direct cloud deployment path for Gale-owned Swift products;
- no service framework workflow that bypasses the workspace component entrypoint;
- no cloud deployment that rebuilds source or consumes a mutable image tag.

Allowed references must be narrowly scoped:

- generic virtualization research outside Swift product workflows;
- Docker/OCI definitions as GitHub build inputs;
- historical docs explicitly marked superseded;
- provider CLI commands inside reviewed GitHub Actions adapters, never as local
  developer commands.

## Release And Issue Boundary

This cleanup removes public skills and maintainer profiles, so it is a breaking
plugin-contract change. Prepare it as a major Socket release unless the release
policy supplies a stronger documented reason otherwise.

Before release:

- map GitHub issues #183, #185, #186, and #187 to final tests and guidance;
- decide whether a separate issue should own the adoption/legacy-removal gap;
- do not close the existing issues merely because the first implementation commit
  exists;
- use the normal protected-main PR, CI, review, branch-accounting, tag, release,
  marketplace-upgrade, and cleanup lifecycle.

No PR, issue mutation, merge, version bump, tag, or release belongs to the
planning pass.

## Risks And Controls

- **PBX state loss:** audit and promote before generation; compare candidate and
  original state before deleting anything.
- **Incorrect extension host:** require explicit PBX evidence or reviewed mapping;
  block ambiguity.
- **Source-history loss:** use Git-aware moves and review rename detection.
- **SwiftPM semantic drift:** preserve manifest products, target names, and public
  module names; movement must not imply a package rewrite.
- **Service framework damage:** preserve framework-generated package structure;
  change only workspace placement and local/cloud ownership files.
- **Provider limitation:** if a provider cannot deploy the exact GitHub-built
  immutable artifact, block that adapter rather than reintroducing a local build.
- **Public plugin breakage:** enumerate every deleted skill/profile reference and
  ship the removal through the required major-release notes.
- **Historical confusion:** retain history only when explicitly labeled
  superseded; active guidance has no compatibility language.

## Definition Of Done

- `bootstrap-xcode-workspace` is the sole Swift repository create/adopt/add/align
  entrypoint.
- Existing app-only, package-only, service-only, and mixed repositories adopt the
  same permanent workspace without whole-repo classification.
- Extensions are peer Xcode targets under `Apps/`; no active guidance or fixture
  creates root `Extensions/`.
- The old migrator, standalone package bootstrap, broad SwiftPM/Xcode routers,
  old maintainer profiles, server Apple-container route, direct/local Fly path,
  and duplicate local templates are removed with no forwarding shims.
- Focused SwiftPM and Xcode build/test/extension skills route only by requested
  operation and component owner.
- Local server commands are native Swift plus Homebrew services only.
- Every Linux artifact and live-test/production deployment is GitHub-built,
  immutable, environment-gated, OIDC-authenticated where supported, health
  checked, and rollback-addressable.
- Soto remains the only default new Swift AWS path.
- Fixture and negative-contract matrices pass.
- Root and child docs, plugin metadata, generated guidance, maintainer tooling,
  architecture, roadmap, Hermes exports, and Claude/Cowork compatibility all
  describe the same one-way workflow.
