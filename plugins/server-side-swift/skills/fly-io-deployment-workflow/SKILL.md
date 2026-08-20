---
name: fly-io-deployment-workflow
description: Configure a GitHub Actions-only Fly.io deployment adapter for an exact prebuilt Swift service image, with protected environments, scoped credentials, health verification, and rollback.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Fly.io, fly.toml, immutable OCI images, and GitHub Actions.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-fly-io
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Fly.io Deployment Workflow

## Purpose

Own Fly-specific configuration and the GitHub Actions adapter that deploys an
exact image produced by an earlier GitHub build job. This workflow never builds
from a developer Mac, launches apps interactively, or deploys from a local
checkout.

## When To Use

- Use this skill for reviewed `fly.toml`, process groups, internal ports,
  health checks, release commands, scoped secret names, protected GitHub
  environments, exact-image deployment, verification, and rollback.
- Use it only after the cloud release workflow records an immutable registry
  identity for the image.
- Diagnose Fly state from GitHub deployment logs and provider read-only evidence.
- Do not offer interactive app creation, developer-session deployment, local
  image validation, remote source builds, or direct developer credential use.
- Use `docker-workflow` for image definition and the framework workflows for
  route, binding, lifecycle, and readiness behavior.

## Source Check

Use current official Fly sources before changing provider behavior:

- [Deploy an app](https://fly.io/docs/launch/deploy/)
- [App configuration](https://fly.io/docs/reference/configuration/)
- [Managing prebuilt images](https://fly.io/docs/blueprints/using-the-fly-docker-registry/)
- [GitHub Actions deployment](https://fly.io/docs/launch/continuous-deployment-with-github-actions/)
- [Access tokens](https://fly.io/docs/security/tokens/)
- [Health checks](https://fly.io/docs/reference/health-checks/)

Fly currently documents app-scoped deploy tokens for GitHub automation rather
than GitHub OIDC. Record that provider limitation and use the narrowest app-only
token with the shortest practical expiry; never substitute a broad personal or
organization token.

## Single-Path Workflow

1. Inspect the service manifest, executable, Dockerfile contract, `fly.toml`,
   internal port, binding, process groups, secrets names, release command,
   health checks, and existing GitHub workflows.
2. Require a completed GitHub build job that published an image and recorded its
   registry digest. The deployment job consumes that exact identity; it does not
   check out source to rebuild it.
3. Keep non-secret configuration in `fly.toml`; keep credentials and sensitive
   runtime values in the appropriate protected GitHub environment and Fly secret
   surface.
4. Authenticate only inside GitHub Actions with an app-scoped Fly deploy token.
   Record its app, purpose, expiry, and rotation owner.
5. Run `flyctl deploy --app <app> --image <immutable-image-reference>` only in
   the protected GitHub deployment job. Reject `latest`, branch tags, or any
   reference whose digest cannot be reconciled to the release manifest.
6. Verify the resulting Fly release reports the expected image identity, then
   prove the configured health check and required external behavior.
7. Record the previous healthy image/release before deployment. Rollback deploys
   that recorded immutable identity through the same protected GitHub job.
8. Use separate live-test and production GitHub environments, concurrency
   controls, approval rules, and audit logs.

## Inputs

- Fly app and reviewed `fly.toml`
- exact image reference plus recorded digest
- protected GitHub environment
- app-scoped deploy-token secret name and expiry record
- health URL/check and previous healthy rollback identity

## Outputs

- GitHub-only Fly provider job
- exact deployed image and Fly release identity
- health evidence and rollback identity
- explicit credential limitation and rotation record

## Guards and Stop Conditions

- Stop if the image was not built, smoke-tested, published, and digest-recorded
  by GitHub Actions.
- Stop if deployment would rebuild source or use a mutable tag.
- Stop if a protected environment, exact app target, health signal, rollback
  identity, or app-scoped credential is missing.
- Do not create apps, attach databases, set secrets, scale, deploy, or destroy
  Fly resources from a local developer session.
- Do not expose Fly tokens, runtime secrets, or private registry credentials in
  logs, artifacts, summaries, issues, or commits.

## Fallbacks and Handoffs

- Use `cloud-deployment-skills:dockerized-service-release-deployment-workflow`
  for build-once artifact ownership and release manifests.
- Use `docker-workflow` for Dockerfile/runtime definition.
- Use `vapor-server-workflow` or `hummingbird-server-workflow` for process
  command, binding, routes, and readiness endpoints.
- Use `persistence-workflow` for migration and database design; deployment may
  invoke only an already-reviewed non-destructive migration contract.
- If Fly cannot consume and report the exact GitHub-built identity, block the
  provider adapter instead of rebuilding.

## Customization

Repository-specific app names, regions, ports, health checks, and secret names
belong in reviewed repository configuration. No customization may enable local
deployment or source rebuilding.

## References

- [Fly deploy image selection](https://fly.io/docs/launch/deploy/)
- [Fly prebuilt-image deployment](https://fly.io/docs/blueprints/using-the-fly-docker-registry/)
- [Fly app-scoped access tokens](https://fly.io/docs/security/tokens/)
- [GitHub deployment environments](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment)
