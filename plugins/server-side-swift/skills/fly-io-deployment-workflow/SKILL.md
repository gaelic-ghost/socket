---
name: fly-io-deployment-workflow
description: Plan, configure, deploy, and diagnose Fly.io deployments for server-side Swift services, including Vapor and Hummingbird apps, Dockerfile handoffs, fly.toml settings, environment variables, secrets, health checks, Postgres attachment, process groups, and deployment validation.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Fly.io, flyctl, Dockerfile-based Swift services, Vapor, Hummingbird, and server-side Swift projects on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-fly-io
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(docker:*) Bash(fly:*) Bash(flyctl:*) Bash(curl:*)
---

# Fly.io Deployment Workflow

## Purpose

Prepare, deploy, or diagnose a Fly.io deployment for a server-side Swift service without confusing platform configuration with framework routing, Docker image construction, persistence design, or local development workflow.

The practical decision is which Swift executable runs in the Fly Machine, which Dockerfile builds it, which `fly.toml` settings expose it, how secrets and non-secret environment variables reach the process, which health checks prove readiness, and which command proves the deployed app is serving the expected behavior.

## When To Use

- Use this skill when adding or changing `fly.toml`, Fly app configuration, Fly secrets, Fly Postgres attachment, Fly process groups, Fly health checks, or deployment validation for a Vapor or Hummingbird service.
- Use this skill when diagnosing `fly launch`, `fly deploy`, remote builder, Machine rollout, health-check, app binding, `DATABASE_URL`, secret, region, scaling, or deployed HTTP failures.
- Use this skill when deciding whether a server-side Swift service is ready for Fly.io deployment or should first receive Docker, Vapor, Hummingbird, persistence, or observability work.
- Use this skill when preparing handoff guidance for a Dockerfile-based hosted deployment on Fly.io.
- Do not use this skill for ordinary route, middleware, model, migration, request-context, or SwiftPM package changes unless Fly deployment behavior is the reason for the change.
- Do not use this skill for generic Dockerfile design without Fly-specific configuration. Use `docker-workflow` for Docker image structure.
- Do not use this skill for Apple Containerization local development. Use `apple-containerization-workflow` for Apple's `container` CLI or Containerization APIs.

## Source Check

Use repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Fly.io or Swift framework docsets, and then official docs when Dash/local coverage is missing or stale. Check one of those source-specific paths before claiming Fly.io or framework deployment behavior:

- [Fly.io Dockerfile deployment](https://fly.io/docs/languages-and-frameworks/dockerfile/)
- [Fly.io app configuration reference](https://fly.io/docs/reference/configuration/)
- [Fly.io fly launch reference](https://fly.io/docs/flyctl/launch/)
- [Fly.io secrets](https://fly.io/docs/apps/secrets/)
- [Fly.io health checks](https://fly.io/docs/reference/health-checks/)
- [Vapor Fly deployment](https://docs.vapor.codes/deploy/fly/)
- [Vapor server configuration](https://docs.vapor.codes/advanced/server/)
- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird GitHub organization](https://github.com/hummingbird-project)

Use Vapor, Hummingbird, SwiftPM, Docker, Swift Docker image, or persistence documentation when the deployment depends on app commands, package targets, image shape, runtime assets, migrations, database drivers, or framework-specific binding behavior.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - executable target and local `swift run` command
   - Vapor or Hummingbird app entry point, host binding, port binding, and graceful shutdown behavior
   - `Dockerfile`, `.dockerignore`, Compose files, and existing deployment files
   - `fly.toml`, Fly app name, primary region, service or `http_service` shape, process groups, release command, checks, scaling, and volumes
   - environment variable names, secret names, database URL handling, and migration commands
2. Identify the deployment job:
   - first deployment
   - redeploy an existing Fly app
   - add database-backed behavior
   - split web and worker processes
   - fix health checks, port binding, or startup failures
   - validate production readiness
3. Check official Fly docs before recommending CLI flags, config keys, secrets behavior, or health-check behavior.
4. Check framework docs before changing the app's run command, host, port, migration timing, or background-worker command.
5. Keep Docker image structure in `docker-workflow` unless the Fly change only needs to verify that the existing image exposes and runs the right process.
6. Keep app routes and readiness endpoints in `vapor-server-workflow` or `hummingbird-server-workflow` unless they are already present and only need Fly wiring.
7. Keep database schema and migration design in `persistence-workflow`; this skill owns when Fly should run or require those commands, not what schema they create.
8. Validate in the narrowest useful order: local SwiftPM or Docker check, Fly config check through `fly deploy` or documented Fly commands, deployed health or HTTP check.

## First Launch

For a service that already has a production-ready `Dockerfile`, prefer Fly's Dockerfile flow:

```bash
fly launch --no-deploy
```

Use `--no-deploy` when the app needs secrets, database attachment, region choice, process groups, health checks, or port review before the first release.

After reviewing config and secrets:

```bash
fly deploy
```

Use plain `fly launch` only when immediate deployment is acceptable and the repository's Dockerfile, port, env, and health behavior are already ready.

Do not commit credentials, generated local tokens, or machine-local paths while adding Fly files.

## fly.toml Shape

Prefer the `fly.toml` generated by `fly launch` as the starting point. Edit it deliberately instead of replacing it wholesale.

Check these fields for Swift services:

- `app`: Fly app name, not a package module name unless they intentionally match
- `primary_region`: chosen operator region for the app
- `[build]`: only when the repository needs a non-default Dockerfile path, build target, or build arguments
- `[env]`: non-secret runtime values only
- `[deploy]`: release commands, rollout strategy, wait timeout, or other deploy behavior only when the app needs them
- `[processes]`: separate web, worker, queue, migration, or job processes only when the service has real process boundaries
- `[http_service]` or `[[services]]`: the internal port must match the container's listening port
- checks: TCP checks for basic binding, HTTP checks for real readiness, and Machine checks only for deploy-time behavior that cannot be proven by port or HTTP readiness

Do not add a readiness endpoint only to satisfy Fly config if the app does not have a real readiness signal. Hand route design to the Vapor or Hummingbird skill.

## Ports And Binding

Fly routes traffic to the app's configured internal service port. The Swift process must listen on the same port inside the Machine.

For Vapor:

- confirm whether the image runs `App serve`, `App serve --hostname 0.0.0.0 --port <port>`, or an equivalent entry point
- make sure Vapor does not bind only to `127.0.0.1` in production
- keep Fluent migration commands separate from the web process unless the repository intentionally uses a release command

For Hummingbird:

- confirm the executable target and any command-line options exposed by the package
- confirm the service binds to a container-reachable host and the same port named in Fly config
- preserve template-generated host, port, and log-level flags unless the user explicitly wants a different configuration model
- if the repository was generated as an `hb` Lambda app, stop and choose an appropriate Lambda deployment workflow instead of forcing the Fly.io long-running process model onto it

When diagnosing failures, report the exact Fly internal port, container `EXPOSE` port when present, framework port, host binding, process command, and health-check path involved.

## Secrets And Environment

Use `[env]` only for non-sensitive strings that are safe to commit.

Use Fly secrets for credentials, API keys, database URLs, JWT signing keys, cookie/session secrets, OAuth client secrets, SMTP credentials, and service tokens:

```bash
fly secrets set NAME=value
fly secrets list
```

Use `fly secrets set NAME=value --stage` when secrets should be staged for a later deploy.

Do not print secret values in logs, deploy summaries, diagnostics, issue comments, or commit messages. When reporting secret state, name only the variable and whether it is missing, staged, listed, or expected by the app.

## Databases And Migrations

For Vapor with Fluent and Postgres, Fly's Vapor docs describe creating or attaching Postgres so the app receives `DATABASE_URL`.

Use Fly Postgres attachment only when it matches the user's target deployment:

```bash
fly pg create
fly pg attach <postgres-app-name>
```

Treat migration timing as an explicit deployment decision:

- one-off manual migration command
- Fly release command
- application startup migration, only when the project already documents that risk tradeoff
- separate migration Machine or process group

Do not run destructive migration reverts, database resets, or production data repair commands without explicit user approval.

## Health Checks And Rollouts

Use service-level TCP checks when the platform only needs to know whether the process is listening.

Use service-level HTTP checks when the app exposes a real readiness endpoint that returns a 2xx response after required dependencies are ready.

Use Machine checks only when deploy-time validation needs to run a command inside an ephemeral Machine, such as a dependency or background-service check that a simple HTTP endpoint cannot prove.

When health checks fail, inspect:

- the deployed process command
- startup logs
- host and port binding
- health-check path and expected status
- missing secrets or env
- database connectivity
- migration or startup ordering
- image architecture and Linux runtime dependencies

Do not claim a deploy succeeded until `fly deploy` completes and the relevant Fly output, health checks, or external HTTP check confirms the expected state.

## Vapor And Hummingbird Handoffs

Use `vapor-server-workflow` for:

- Vapor route, controller, middleware, command, environment, server, and Fluent migration behavior
- deciding whether a health route belongs in the app
- Vapor 5 alpha posture or migration readiness

Use `hummingbird-server-workflow` for:

- Hummingbird router, middleware, request context, application lifecycle, command-line options, and framework testing behavior
- deciding whether a readiness route belongs in the app

Use `docker-workflow` for:

- Dockerfile stage design, Swift builder/runtime images, `.dockerignore`, entry point, runtime assets, non-root execution, and local container validation

Use `persistence-workflow` for:

- schema changes, migrations, database query behavior, migration tests, seed data, and local dependency setup

Use observability guidance, when available, for:

- log levels, metrics, traces, alerting, health signal design, and production diagnostic dashboards

## Testing And Validation

Prefer this order:

1. Run the repository's SwiftPM build or tests when the deploy depends on compiled app behavior.
2. Validate Docker image behavior locally when startup, port binding, runtime assets, Linux dependencies, or entry point are the risk.
3. Review `fly.toml` and secret names before first deploy.
4. Run `fly launch --no-deploy` for a new app when configuration needs review.
5. Run `fly deploy` for deployment validation.
6. Use `fly logs`, `fly status`, `fly checks list`, or Fly's monitoring page when deploy or runtime checks fail.
7. Use `curl https://<app>.fly.dev/...` only when public HTTP behavior is part of the expected result.

When a Fly command fails, report the exact app, region, command, process group, Machine, image, port, check, secret name, environment variable, or route involved. Include the likely cause, such as missing Dockerfile, wrong executable name, failed remote build, wrong host binding, wrong internal port, missing secret, failed migration, database not attached, health endpoint returning non-2xx, or a readiness check that depends on unavailable infrastructure.

## Output Shape

Return:

1. `Deployment shape`: Fly app, package root, executable target, Dockerfile, `fly.toml` service/process shape, port, environment, secrets, database, checks, and public URL when known.
2. `Docs used`: Fly.io, Vapor, Hummingbird, Docker, SwiftPM, or persistence docs consulted.
3. `Command path`: exact `fly`, Docker, SwiftPM, migration, log, status, check, or HTTP commands run or recommended.
4. `Runtime behavior`: entry point, arguments, binding, health checks, release commands, process groups, migrations, and secrets.
5. `Validation`: deploy result, checks, logs, status, or HTTP result.
6. `Handoffs`: Vapor, Hummingbird, Docker, persistence, observability, CI, or release follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not commit secrets, `.env` files, Fly access tokens, machine-local paths, private image credentials, or generated local auth state.
- Do not add Fly deployment files to an ordinary route or model change unless deployment scope was requested.
- Do not claim Fly CLI, config, health-check, secret, or Machine behavior from memory when current official docs can be checked.
- Do not run production-affecting Fly commands such as deploys, secret changes, database attachment, scaling, or app destruction without confirming the target app and intent.
- Do not use Fly deployment success as proof that route behavior is correct unless the route was checked directly or covered by tests.
- Do not let Fly-specific process groups or release commands become a hidden substitute for explicit app lifecycle and migration design.
