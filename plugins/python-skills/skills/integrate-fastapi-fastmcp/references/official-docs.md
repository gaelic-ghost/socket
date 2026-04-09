# Official Docs

Use these as the primary sources for current behavior and examples.

## FastMCP

- FastAPI integration guide:
  - https://gofastmcp.com/v2/integrations/fastapi
- HTTP deployment and FastAPI mounting details:
  - https://gofastmcp.com/v2/deployment/http#fastapi-integration

FastMCP guidance this skill relies on:

- `FastMCP.from_fastapi(app=app)` is good for bootstrapping and prototyping, not automatically the best final MCP surface.
- Mounting requires carrying the MCP lifespan into FastAPI.
- If FastAPI already has a lifespan, both contexts should be combined explicitly.
- FastAPI `operation_id` values become MCP component names.

## FastAPI

- Settings and environment variables:
  - https://fastapi.tiangolo.com/advanced/settings/
- Bigger applications and multi-file structure:
  - https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Advanced path operation configuration:
  - https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/

FastAPI guidance this skill relies on:

- Typed settings should live in a shared config module and can be provided through dependencies.
- `@lru_cache` is the documented pattern for creating settings once while keeping tests override-friendly.
- Explicit `operation_id` values are available when default route naming would produce poor OpenAPI names.

## uv

- FastAPI integration guide:
  - https://docs.astral.sh/uv/guides/integration/fastapi/
- Working on projects:
  - https://docs.astral.sh/uv/guides/projects/
- Workspaces:
  - https://docs.astral.sh/uv/concepts/projects/workspaces/

uv guidance this skill relies on:

- `uv init --app` plus `uv add fastapi --extra standard` is the documented FastAPI project path.
- `uv run` creates and uses the project environment, lockfile, and dependency context automatically.
- Use workspace-aware dependency and run commands once the repo uses `[tool.uv.workspace]`.
