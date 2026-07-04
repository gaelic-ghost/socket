---
name: sync-hummingbird-service-guidance
description: Sync repo guidance for an existing Hummingbird server-side Swift repository when the user wants to add, merge, refresh, or align AGENTS.md, hb CLI, Server or Lambda, OpenAPI, swift-configuration, Docker, and SwiftPM workflow guidance. Use for existing Hummingbird repos. Do not use for brand-new service bootstrap or non-Hummingbird Swift packages.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with existing Hummingbird, hb, SwiftPM, OpenAPIHummingbird, hummingbird-lambda, swift-configuration, Docker, and server-side Swift repositories on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-sync
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(hb:*) Bash(curl:*)
---

# Sync Hummingbird Service Guidance

## Purpose

Bring an existing Hummingbird repository up to the current Socket guidance baseline without treating the repo as a fresh scaffold.

This skill owns repo-local guidance alignment for existing Hummingbird services: `AGENTS.md`, `.codex/environments/hummingbird.toml`, `hb` CLI expectations, generated Server versus Lambda shape, generated `swift-configuration` assumptions, OpenAPI transport distinctions, Docker baseline notes, and SwiftPM-first validation. It is a conscious guidance-sync surface, not a package-rewrite or template-overwrite workflow.

## Companion Plugin Requirement

When a repository also needs shared maintenance scripts, GitHub Actions, branch-protection guidance, or release helpers refreshed, compose this skill with the companion `productivity-skills:maintain-project-repo` workflow using the closest server-side Swift or Swift package profile exposed in the current session. If the companion skill is not exposed, tell the user to add the Socket marketplace with `codex plugin marketplace add gaelic-ghost/socket` so future sessions expose both plugins.

## When To Use

- Use this skill when an existing Hummingbird repo needs `AGENTS.md` added, refreshed, or merged with the current Hummingbird service baseline.
- Use this skill when the repository already contains `Package.swift` plus Hummingbird dependencies, imports, generated files, or app construction.
- Use this skill when an older Hummingbird repo needs guidance updated for the current `hb` CLI Server or Lambda prompts, generated `swift-configuration`, OpenAPIHummingbird, or `hummingbird-lambda` behavior.
- Use this skill when a repo-local `.codex/environments/hummingbird.toml` should be added or checked against the executable target name.
- Use this skill when downstream repos should catch up after Socket updates Hummingbird bootstrap, OpenAPI, deployment, auth, or command guidance.
- Do not use this skill for brand-new service creation from nothing. Use `bootstrap-hummingbird-service`.
- Do not use this skill for ordinary route, middleware, request-context, persistence, OpenAPI contract, Docker, auth, or deployment implementation unless guidance sync is the reason for the task.
- Do not use this skill for Vapor, Xcode app, Apple-platform client, or plain Swift package repos.

## Source Check

Use repo-local files first, then current Hummingbird and package sources before making CLI, generated-shape, package, or command claims:

- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird hb CLI](https://github.com/hummingbird-project/hb)
- [Hummingbird template](https://github.com/hummingbird-project/template)
- [Hummingbird Lambda package](https://github.com/hummingbird-project/hummingbird-lambda)
- [Swift OpenAPI Hummingbird package](https://github.com/hummingbird-project/swift-openapi-hummingbird)
- [Swift OpenAPI Lambda package](https://github.com/swift-server/swift-openapi-lambda)
- [Swift Package Manager documentation](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/)

Do not claim current `hb` prompt names, generated package dependencies, generated file layout, or template defaults from memory. Check `hb init --help`, `hb --version`, the template `metadata.json`, or generated scaffold files when that detail affects the guidance.

## Single-Path Workflow

1. Collect the required inputs:
   - `repo_root`
   - optional `skip_validation`
   - optional `dry_run`
2. Classify the request as existing Hummingbird guidance sync before continuing:
   - continue only when the repo already contains `Package.swift`
   - detect Hummingbird through package dependencies, imports, `Application`, `Router`, `HummingbirdLambda`, `OpenAPIHummingbird`, or generated Hummingbird template paths
   - stop if the request is really fresh bootstrap, Vapor guidance sync, Xcode app guidance sync, or plain SwiftPM package guidance sync
   - stop if the repo boundary is ambiguous because multiple unrelated app roots are present
3. Inspect the existing service shape:
   - executable target name
   - `Package.swift` dependency style and Swift tools version
   - Server app entry point, Lambda entry point, or both
   - `swift-configuration` providers and runtime settings
   - OpenAPI document, generated API target, and `OpenAPIHummingbird` registration when present
   - `hummingbird-lambda` adapter and selected Lambda event type when present
   - Dockerfile, Compose, local database, and Codex local environment files
   - current `AGENTS.md`, README, CONTRIBUTING, and repo-maintenance scripts when present
4. Apply the current Hummingbird guidance baseline:
   - fresh project creation belongs to `hb init`, not a hand-written SwiftPM scaffold
   - existing repos should not have the template copied over them without explicit replacement approval
   - preserve the repo's current Server, Lambda, or dual-adapter shape
   - preserve generated `swift-configuration` when it fits
   - for generated Lambda + OpenAPI projects, keep `hummingbird-lambda` as the deployment adapter and `OpenAPIHummingbird` as the generated handler registration transport
   - mention `swift-openapi-lambda` only as a separate valid transport when the repository intentionally chose it
   - when a repo may need both long-running server and Lambda deployments, keep generated `APIProtocol` implementations transport-neutral and isolate adapter differences in thin executable or adapter targets
5. Apply the sync path:
   - if `AGENTS.md` is missing, copy `assets/AGENTS.md`
   - if `AGENTS.md` exists and already contains the managed Hummingbird sync section, keep the file unchanged except for deliberate user-requested edits
   - if `AGENTS.md` exists but lacks the managed section, append `assets/append-section.md` as a bounded section
   - preserve existing repo-specific instructions and formatting
6. Install or verify Codex GUI local environment guidance when useful:
   - copy `templates/codex-local-environments/hummingbird.toml` into `.codex/environments/hummingbird.toml` when missing
   - replace `EXECUTABLE_NAME` with the actual executable target
   - leave customized matching files in place
7. Validate the synced guidance:
   - verify `AGENTS.md` exists
   - verify the synced file mentions `bootstrap-hummingbird-service`
   - verify the synced file mentions `sync-hummingbird-service-guidance`
   - verify the synced file preserves `swift build` and `swift test` as default validation paths
   - verify generated Lambda + OpenAPI guidance distinguishes `OpenAPIHummingbird` plus `hummingbird-lambda` from `swift-openapi-lambda`
   - verify `.codex/environments/hummingbird.toml`, when present, uses the actual executable target name
8. Refresh shared repo maintenance only when requested or already part of the repo's workflow:
   - use the companion repo-maintenance workflow rather than inventing a Hummingbird-specific release script
   - preserve repo-specific extra scripts that are not part of the managed file set
   - keep protected-branch, GitHub settings, and release-helper changes in the maintainer workflow rather than this skill
9. Hand off ongoing service work cleanly:
   - use `hummingbird-server-workflow` for routes, middleware, request contexts, app lifecycle, and Hummingbird tests
   - use `openapi-rpc-workflow` for OpenAPI documents, generated stubs, and transport registration
   - use `persistence-workflow` for Fluent, direct Postgres, migrations, repositories, and database-backed tests
   - use `docker-workflow`, `fly-io-deployment-workflow`, or a Lambda-specific deployment workflow for deployment changes

## Inputs

- `repo_root`: optional absolute or relative path to the repository root; defaults to `.`
- `skip_validation`: optional flag to skip post-sync file validation
- `dry_run`: optional flag to emit the planned contract without writing files
- Defaults:
  - `repo_root=.` when omitted
  - `writeMode=sync-if-needed`
  - validation runs unless `skip_validation` is requested
  - successful mutating runs install `.codex/environments/hummingbird.toml` from `templates/codex-local-environments/hummingbird.toml` when missing, replace `EXECUTABLE_NAME`, leave matching files unchanged, and preserve customized existing files

## Outputs

- `status`
  - `success`: guidance sync completed or was already satisfied
  - `blocked`: prerequisites, repo classification, or sync policy prevented completion
  - `failed`: the sync path started but did not complete successfully
- `path_type`
  - `primary`: the documented sync path completed
  - `fallback`: a non-mutating guided result was returned
- `output`
  - resolved repo root
  - detected Hummingbird shape
  - executable target
  - Server, Lambda, or dual-adapter classification
  - `AGENTS.md` path
  - actions applied or planned
  - installed or preserved `.codex/environments/hummingbird.toml`
  - validation result
  - one concise next step or handoff

## Guards And Stop Conditions

- Stop with `blocked` if the repo root cannot be resolved.
- Stop with `blocked` if the repo does not contain `Package.swift`.
- Stop with `blocked` if Hummingbird cannot be detected from package dependencies, imports, generated files, or app construction.
- Stop with `blocked` if the repo is a Vapor app, Xcode app, or plain Swift package rather than a Hummingbird service.
- Stop with `blocked` if the chosen write mode does not allow the mutation the repo still needs, such as creating missing `AGENTS.md` or appending the bounded Hummingbird section.
- Stop with `blocked` if the target `AGENTS.md` path exists but is not a regular file.
- Fail with a clear message if the Codex local environment template is missing or the target `.codex/environments/hummingbird.toml` path exists but is not a regular file.
- Do not rewrite `Package.swift`, rename targets, replace configuration systems, convert Server apps to Lambda, convert Lambda apps to Server, or copy a new template over an existing service as part of guidance sync.

## Fallbacks And Handoffs

- The only current fallback is a non-mutating dry run or guided result that explains what the sync would do.
- After a successful sync, use `hummingbird-server-workflow` for active Hummingbird implementation.
- After a successful sync, use `openapi-rpc-workflow` for OpenAPI contract or transport work.
- After a successful sync, use `persistence-workflow` for database behavior.
- After a successful sync, use `docker-workflow` for container runtime changes and `fly-io-deployment-workflow` for Fly.io long-running service deployment.
- Recommend `bootstrap-hummingbird-service` when the repository still needs to be created from scratch.
- Recommend `sync-swift-package-guidance` when the repo is really a plain Swift package rather than a Hummingbird service.

## References

### Support References

- `assets/AGENTS.md`
- `assets/append-section.md`
- `templates/codex-local-environments/hummingbird.toml`
