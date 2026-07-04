---
name: integrate-fastapi-fastmcp
description: Integrate FastAPI and FastMCP applications in existing or evolving uv-managed Python projects. Use when adding a FastMCP server to an existing FastAPI app, folding an existing FastMCP server into a FastAPI project, serving both REST and MCP interfaces from one codebase, or graduating an auto-generated FastAPI-to-FastMCP server into a curated FastMCP application.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients on macOS with uv-managed Python projects, FastAPI and FastMCP application code, shell access for uv commands, and access to the fastmcp_docs MCP server for current framework guidance.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-integration
allowed-tools: Bash(uv:*) Read
---

# Integrate FastAPI and FastMCP

## Purpose

Guide integration and restructuring work when a project needs both a conventional FastAPI surface and an MCP surface, without treating FastAPI-to-FastMCP auto-conversion as the final architecture by default.

## When To Use

- Use this skill when an existing FastAPI app needs a mounted or generated FastMCP server.
- Use this skill when an existing FastMCP project needs to live inside a FastAPI application or alongside one in the same `uv` project or workspace.
- Use this skill when a FastAPI-derived FastMCP server needs to be promoted from prototype output into a maintained, curated FastMCP application.
- Hand off to `bootstrap-python-service` or `bootstrap-python-mcp-service` only when the main task is creating fresh scaffolding rather than integrating existing code.

## Core Guidance

- Treat FastAPI-to-FastMCP generation as a bootstrap or discovery step, not proof that the generated server is already the right long-term MCP surface.
- Keep one source of truth for business logic and typed configuration, then expose it through both HTTP and MCP layers where that actually helps.
- Preserve `uv` as the package and command surface:
  - use `uv add ...` for dependency changes
  - use `uv run ...` for local execution
  - use workspace-aware commands when the repo already uses `[tool.uv.workspace]`
- Keep safe defaults in committed `.env`, local or secret overrides in `.env.local`, and typed settings in a shared config module.

## Integration Decision Guide

1. Start by identifying the actual goal:
   - add MCP to an existing API
   - add FastAPI hosting around an existing MCP server
   - serve both API and MCP from one process
   - replace auto-generated MCP pieces with curated tools and resources
2. Choose the lightest integration pattern that satisfies that goal:
   - mount an MCP ASGI app into FastAPI when the MCP server already exists or is intentionally separate
   - generate an MCP server from FastAPI when bootstrapping from an API surface
   - build a combined app when one process should serve both interfaces from the same codebase
3. Before keeping an auto-generated server, review whether the generated tool names, parameters, and endpoint coverage are actually LLM-friendly.
4. If the generated server is too broad or awkward, keep the shared domain logic and replace the MCP surface with explicit curated FastMCP components.

## Recommended Patterns

### Pattern A: Mount an existing MCP server into FastAPI

Use this when FastMCP is already curated or intentionally distinct from the REST API.

```python
from fastapi import FastAPI
from fastmcp import FastMCP

mcp = FastMCP("Analytics Tools")

@mcp.tool
def analyze_pricing(category: str) -> dict:
    ...

mcp_app = mcp.http_app(path="/mcp")
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/analytics", mcp_app)
```

Guardrails:

- Always pass the MCP lifespan into FastAPI.
- If FastAPI already has its own lifespan, combine both lifespans instead of replacing one with the other.
- Avoid top-level `CORSMiddleware` on a combined app when the mounted FastMCP server uses OAuth flows; prefer separate sub-apps if custom CORS is needed.

### Pattern B: Generate FastMCP from an existing FastAPI app

Use this when the API already exists and you need a quick MCP bootstrap surface.

```python
from fastmcp import FastMCP

mcp = FastMCP.from_fastapi(app=app, name="Project MCP")
```

Then immediately review:

- operation IDs and resulting MCP names
- whether GET endpoints should remain tools or become resources/resource templates
- whether authentication headers or client config must be supplied through `httpx_client_kwargs`

Do not stop after generation if the resulting surface is verbose, repetitive, or mirrors REST too literally.

### Pattern C: Serve both API and MCP from one FastAPI process

Use this when one deployment should expose both REST and MCP interfaces.

```python
from fastapi import FastAPI
from fastmcp import FastMCP

mcp = FastMCP.from_fastapi(app=app, name="Project MCP")
mcp_app = mcp.http_app(path="/mcp")

combined_app = FastAPI(
    title="Project API with MCP",
    routes=[*mcp_app.routes, *app.routes],
    lifespan=mcp_app.lifespan,
)
```

This is a good intermediate architecture when the MCP surface is still close to the API, but it still needs the same curation review as Pattern B.

### Pattern D: Promote an auto-generated FastMCP server into a curated MCP app

Use this when `FastMCP.from_fastapi(...)` got you started but the resulting server needs stronger MCP ergonomics.

Promotion steps:

1. Keep the shared FastAPI domain logic, models, and config modules.
2. Retain only the generated pieces that still provide good MCP ergonomics.
3. Add explicit FastMCP tools, resources, and prompts for the high-value tasks LLM clients actually need.
4. Use route maps only when they improve the MCP shape clearly.
5. Give FastAPI routes explicit `operation_id` values anywhere generated names would be poor MCP names.
6. Add client-based MCP tests so the MCP surface is verified directly instead of only through REST tests.

## UV Workflow Expectations

- In a single-project repo:
  - add dependencies with `uv add`
  - run local app flows with `uv run fastapi dev` or the project’s chosen entrypoint
  - run checks with `uv run pytest`, `uv run ruff check .`, and `uv run mypy .` when configured
- In a workspace repo:
  - add dependencies to the right member with `uv add --package <member> ...`
  - run targeted commands with `uv run --package <member> ...`
  - keep shared libraries and service members separated when that improves ownership and import clarity

When a combined FastAPI/FastMCP setup starts demanding separate service members, call that out explicitly as an architectural pivot rather than silently introducing another package boundary.

## Validation Checklist

1. Confirm the chosen integration pattern matches the intended deployment shape.
2. Verify configuration loading still comes from one typed settings path.
3. Run HTTP-side checks.
4. Run MCP-side checks with a FastMCP client or equivalent integration test.
5. Confirm lifespan and startup/shutdown behavior are correct.
6. If FastAPI generated the MCP surface, review names, parameter shapes, and auth behavior before accepting the result.

## References

- `references/integration-patterns.md`
- `references/official-docs.md`

