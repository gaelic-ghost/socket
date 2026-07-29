---
name: dockerized-service-release-deployment-workflow
description: "Create a Dockerized-service release contract with clean GitHub Actions builds, main-anchored tags, immutable digest manifests, published-release deployments, production approval, health checks, and exact-digest rollback."
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Docker or OCI images, GitHub Actions, GitHub Releases, container registries, and provider-specific deployment adapters.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: cloud-deployment-release
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(docker:*) Bash(gh:*) Bash(curl:*) Bash(uv:*) Bash(uvx:*)
---

# Dockerized Service Release and Deployment Workflow

## Purpose

Create or audit a durable release contract for a Dockerized backend or cloud service without treating a developer worktree or a production host as a build machine.

The default contract is:

1. Feature worktrees are development-only and may run local tests or image checks.
2. A clean GitHub Actions checkout of a version tag validates the release commit and builds the published OCI image.
3. The tag must resolve to a commit reachable from `origin/main`.
4. The registry digest, tag, commit, image reference, build run, and provenance/SBOM choices are written into a release manifest.
5. The workflow creates a draft GitHub Release with that manifest attached.
6. Publishing the GitHub Release is the production deployment trigger.
7. The deployment job is gated by the protected `production` GitHub environment and invokes a provider-specific adapter with `image@sha256:...`.
8. The adapter verifies service health and records the prior manifest/digest so rollback deploys a previous exact digest rather than rebuilding source.

This is a durable building-block change: it removes the ambiguity between a developer build, a CI artifact, and a deployed artifact. A project can later change registries or providers without weakening the tag-to-digest deployment contract.

## When To Use

- Use this skill when adding or reviewing Dockerized-service release automation, an OCI registry publication path, GitHub Release deployment triggers, production approval gates, image-digest deployment, release manifests, health checks, or rollback guidance.
- Use it for backend services and cloud workloads regardless of application language when Docker or OCI images are the release artifact.
- Use `server-side-swift:docker-workflow` for Swift Dockerfile, Compose, Linux runtime, and image-entrypoint work.
- Use the official provider plugin or provider documentation for the final deployment adapter. This skill does not create cloud resources, configure a cloud account, or guess a provider command.

## Source Check

Inspect the repository's Dockerfile, CI workflows, release process, registry settings, deployment files, health endpoint, provider configuration, and rollback procedures first. Then verify the current platform behavior against these official sources:

- [GitHub Actions environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub Actions release-event triggers](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [GitHub Actions token-trigger behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [GitHub Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker GitHub Actions image publishing](https://docs.docker.com/build/ci/github-actions/push-multi-registries/)
- [Docker BuildKit attestations](https://docs.docker.com/build/metadata/attestations/)

Translate those sources into the actual project choices: registry, tag policy, environment policy, provider identity, health URL, and rollback command.

## Required Decisions Before Editing

Confirm these decisions. Stop rather than silently choosing a production target:

- registry and image name
- supported target platform or platforms
- tag pattern and the protected integration branch, normally `main`
- repository validation command and image smoke-test command
- GitHub Release draft/publish ownership
- GitHub `production` environment reviewers, permitted tags, and bypass policy
- cloud account, project, region, workload, and OIDC trust policy for the deployment adapter
- health endpoint, expected response, timeout, and failure diagnostics
- source of the prior successful release manifest for rollback

## Template Set

Copy these template assets into the target repository and replace every `{{...}}` placeholder before enabling them:

- [`release-container.yml.tmpl`](./assets/release-container.yml.tmpl): tag-anchored validation, immutable image publication, manifest creation, and draft release creation.
- [`deploy-production.yml.tmpl`](./assets/deploy-production.yml.tmpl): a GitHub Release `published` trigger, protected production environment, manifest download, exact-digest adapter call, health verification, and failure guidance.
- [`release-manifest.json.tmpl`](./assets/release-manifest.json.tmpl): the release-record schema.
- [`deploy-production-image.sh.tmpl`](./assets/deploy-production-image.sh.tmpl): a deliberately blocked provider-adapter seam.
- [`verify-production-health.sh.tmpl`](./assets/verify-production-health.sh.tmpl): a deliberately blocked health-check seam.

The shell templates fail closed until a project replaces their placeholders. Do not treat the template itself as a deploy command.

## Release Workflow

1. Create feature work in a branch-backed worktree. Use local checks for feedback only; do not publish a release image from that worktree.
2. Open and merge the reviewed change into `main` through the repository's normal CI and review gates.
3. Create an annotated SemVer tag from the reviewed `main` commit and push it.
4. The tag workflow checks out the tag in a clean hosted runner, fetches `origin/main`, and rejects a tag commit that is not reachable from it.
5. Run the repository validation from that clean checkout.
6. Build and push the image once. Capture the registry output digest, then run the container smoke test against that exact published digest. Publish provenance and SBOM attestations where the chosen registry supports them.
7. Create `release-manifest.json` from the tag, resolved commit, immutable image reference, workflow run URL, and attestations. Attach it to a **draft** GitHub Release.
8. Review the draft release and publish it through the GitHub UI or an explicitly approved GitHub App/PAT release publisher. Draft-first release creation means all manifest assets exist before an immutable-release policy locks the release. A release created with the first workflow's `GITHUB_TOKEN` does not trigger another workflow, which is why the template creates a draft and requires a later publish action.

The deployment workflow must listen only for `release: [published]`. It must not deploy directly on a tag push, a push to `main`, or a pull request.

## Production Deployment and Rollback

1. The release-published workflow downloads `release-manifest.json` from the exact release event.
2. It validates that the manifest tag matches the release event and that `image` is a fully qualified `name@sha256:digest` reference.
3. The job enters the GitHub `production` environment. Configure required reviewers, tag restrictions, and no-administrator-bypass where the repository plan supports them.
4. Authenticate to the provider using short-lived OIDC credentials when supported. Do not put long-lived cloud credentials in repository secrets merely to run this workflow.
5. Pass only the exact digest reference to the provider deployment adapter. The adapter must not run `docker build`, clone source, or reinterpret a mutable tag.
6. Run the repository-defined health check against the deployed release. On failure, preserve deployment logs and stop; do not silently roll forward or rebuild.
7. Roll back by selecting the prior successful GitHub Release manifest and rerunning the same exact-digest deployment path after the required production approval. Do not rebuild an old commit on a host.

## Security and Supply-Chain Rules

- Scope workflow permissions minimally. The release workflow normally needs `contents: write`, `packages: write`, and `attestations: write`; the deploy workflow should have read-only contents plus `id-token: write` only when the provider adapter uses OIDC.
- Keep registry write access in the release workflow. Production deployment should normally need only pull/read access plus provider authorization.
- Do not place secrets in Docker build arguments, image layers, caches, release manifests, logs, or committed environment files.
- Treat restored CI caches as untrusted input; do not cache secrets or make a release depend on an unrebuildable cache.
- Use mutable version tags only as discovery aliases. The release manifest and deployment adapter must use the immutable digest.
- Require a real health signal. A TCP connection alone is not a readiness guarantee unless the service explicitly documents it as one.

## Validation

Before enabling the workflow:

1. Validate YAML and shell syntax after template substitution.
2. Run the repository test suite and a local image smoke test for fast feedback.
3. Use a non-production tag or staging environment to prove that the Actions runner produces the manifest, registry digest, and digest-based smoke-test evidence.
4. Inspect the manifest against the registry and release tag before publishing the GitHub Release.
5. Confirm the `production` environment pauses for approval and that the deployment adapter receives `image@sha256:...`, not a tag.
6. Exercise the health-check failure path and a rollback drill using a known prior release digest before treating the workflow as release-ready.

## Guardrails

- Do not deploy or modify a cloud account while creating this reusable guidance or template set.
- Do not use a worktree, developer laptop, or production host to build the image that a release deploys.
- Do not publish a GitHub Release from a tag that is not anchored to the protected integration branch.
- Do not use a GitHub Release `created` event as the deployment trigger; draft releases need a later explicit publish action.
- Do not deploy from `latest`, a branch name, a short SHA tag, or any other mutable image identifier.
- Do not substitute an SSH host copy, `docker compose build`, or remote source checkout for the provider deployment adapter.
- Do not claim rollback readiness until a prior release manifest and exact-digest adapter path have both been verified.

## Output Shape

Return:

1. `Release contract`: branch, tag pattern, registry, image platforms, validation, manifest location, and GitHub Release ownership.
2. `Deployment contract`: provider adapter, OIDC/credential boundary, production environment policy, health signal, and rollback source.
3. `Templates`: copied assets and every required substitution.
4. `Validation`: local, CI, registry, release, environment-approval, health, and rollback evidence.
5. `Risk`: unresolved provider commands, approval policy, plan limitations, health semantics, or rollback gaps.
