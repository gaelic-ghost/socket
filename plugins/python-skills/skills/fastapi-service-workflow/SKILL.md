---
name: fastapi-service-workflow
description: Maintain existing uv-managed FastAPI services, including route and dependency composition, typed settings, lifespan, async and integration testing, OpenAPI review, deployment-readiness handoff, and service-specific diagnostics.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients maintaining FastAPI services on macOS with uv, typed configuration, async Python, and the repository's existing deployment tools.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-fastapi
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# FastAPI Service Workflow

## Purpose

Maintain an existing FastAPI service without turning routing, application
lifecycle, domain logic, deployment, and MCP integration into one layer. Keep
HTTP adapters thin around typed domain behavior and make startup, shutdown,
configuration, and public API changes explicit.

## Workflow

1. Inspect `pyproject.toml`, app entrypoint, routers, dependencies, settings,
   lifespan, tests, OpenAPI output, CI, and deployment configuration.
2. Classify the requested change as route composition, request/response model,
   dependency, settings, lifecycle, async boundary, public OpenAPI contract, or
   deployment-readiness work.
3. Keep route handlers focused on HTTP translation. Put reusable behavior in
   domain modules or existing service boundaries rather than duplicating it
   across routes, CLI commands, or MCP tools.
4. Keep settings typed and injectable. Store safe defaults separately from
   machine-local or deployment secrets; use dependency overrides in tests.
5. Use one lifespan contract for resources such as pools, clients, queues, and
   background workers. Combine lifespans deliberately when mounting another
   ASGI application instead of silently replacing startup or shutdown work.
6. Review the OpenAPI effect of public routes, models, status codes, operation
   IDs, security requirements, and deprecations. Treat incompatible changes as
   an API compatibility decision.
7. Run focused HTTP and async tests, then the repository's configured checks:
   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy .
   ```
8. Report deployment readiness separately: configuration source, migrations,
   health endpoint, logs, timeouts, workers, and external dependencies. Do not
   deploy unless the user asks for that operation.

## Testing And Diagnostics

Use dependency overrides for paid, privileged, or nondeterministic services and
clear them after each test. Use an async client for async behavior, and make
lifespan execution explicit when tests depend on startup resources.

Diagnose service failures in this order: import or app factory, settings,
lifespan, route/dependency resolution, response validation, async boundary,
then external integration. Hand generic lockfile, package, CI, or tool failures
to their existing Python workflows.

## Handoffs

- New service scaffolding: `bootstrap-python-service`.
- Generic implementation and package structure: `build-python-project`.
- FastAPI plus FastMCP in one codebase: `integrate-fastapi-fastmcp`.
- MCP service maintenance: `fastmcp-service-workflow`.
- Package, CI, testing, tooling, and upgrade work: their corresponding Python
  workflows.

## Output Shape

Return the service boundary changed, HTTP/OpenAPI impact, settings and
lifespan effect, tests and commands run, deployment-readiness evidence, and
residual risk.

## Guardrails

- Do not add a repository, manager, or service wrapper when a route can call an
  existing typed domain boundary directly.
- Do not run a service, migration, external write, or deployment merely to
  validate static guidance without user approval.
- Do not change public OpenAPI behavior silently.

## References

- [FastAPI lifespan events](https://fastapi.tiangolo.com/advanced/events/)
- [FastAPI settings](https://fastapi.tiangolo.com/advanced/settings/)
- [FastAPI dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [FastAPI async tests](https://fastapi.tiangolo.com/advanced/async-tests/)
