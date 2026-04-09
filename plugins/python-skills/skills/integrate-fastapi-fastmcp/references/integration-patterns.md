# Integration Patterns

Use this reference after the skill triggers and the repo shape is known.

## Pattern Selection

- Existing FastAPI app, new MCP surface needed:
  - start with `FastMCP.from_fastapi(app=app)` if you need a quick bootstrap
  - move to explicit FastMCP tools/resources if the generated interface is too REST-shaped
- Existing curated FastMCP app, FastAPI host needed:
  - build `mcp_app = mcp.http_app(path="/mcp")`
  - mount it into FastAPI and wire lifespan correctly
- One process should serve both REST and MCP:
  - combine routes deliberately or mount the MCP sub-app
  - choose the approach that keeps routing, auth, and middleware behavior easiest to reason about

## Lifespan Rules

- Always carry FastMCP lifespan into the FastAPI app when mounting or combining.
- If the FastAPI app already owns startup and shutdown work, create a combined lifespan context instead of replacing one side.

## Naming Rules

- FastAPI `operation_id` values become MCP component names during conversion.
- Add explicit `operation_id` values before or during the promotion pass whenever generated names would be noisy or unstable.

## Promotion Heuristics

Replace generated MCP pieces with explicit FastMCP components when:

- a tool name mirrors REST path syntax instead of the task the user wants
- a single endpoint exposes too many parameters for an LLM-friendly tool
- related REST endpoints should really collapse into one higher-value MCP tool
- read-heavy GET routes should become resources or resource templates

## Shared Configuration Rules

- Prefer one typed settings module shared by both FastAPI and FastMCP layers.
- Keep `.env` committed for non-secret defaults and `.env.local` ignored for machine-local overrides.
- In FastAPI, prefer a cached settings dependency so the settings object is created once and remains easy to override in tests.

## UV Workspace Rules

- Use `uv add --package <member>` when the repo is already workspace-based.
- Keep service-specific dependencies scoped to the owning member instead of flattening everything into the root.
- Only split FastAPI and FastMCP into separate workspace members when that unlocks a real ownership or deployment need.

