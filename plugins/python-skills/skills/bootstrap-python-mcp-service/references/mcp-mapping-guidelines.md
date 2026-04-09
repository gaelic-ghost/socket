# MCP Mapping Guidelines

Use this file when converting an existing HTTP API surface to MCP capabilities.

## Primitive selection heuristics

- `Resource`: Prefer for read-oriented, stable, side-effect-free access patterns.
- `Tool`: Prefer for mutations, workflow actions, asynchronous jobs, or operations with side effects.
- `Prompt`: Prefer for reusable operator workflows, request templates, or guided usage patterns.

## Naming conventions

- Use concise, action-oriented names for tools.
- Use domain nouns for resources.
- Remove transport-specific details (for example `/api/v1/`) from exposed MCP names when possible.

## RouteMap heuristics

Use custom RouteMaps when one or more are true:

- Endpoint naming is transport-centric rather than user-centric.
- URL version prefixes leak into capability names.
- Endpoint depth or path nesting hurts discoverability.
- Multiple endpoints represent one conceptual capability and should be grouped.

## Transform heuristics

Use Transforms when one or more are true:

- Request bodies are deeply nested wrappers around a few meaningful fields.
- Response envelopes are inconsistent across similar endpoints.
- Pagination or metadata structures differ and should be normalized.
- You need to hide transport-only fields from MCP clients.

## Workspace mapping considerations

When bootstrapping MCP workspaces, establish service boundaries before detailed mapping:

- Map MCP Tools/Resources to service members by domain ownership.
- Keep shared models/utilities in package members and avoid duplicating mapping logic across services.
- Start with per-service primitive naming, then normalize cross-service naming during RouteMap review.
- Produce one mapping report per service member for large workspaces.

## Bootstrap policy

- Keep initial bootstrap minimal and deterministic.
- Emit a concrete RouteMap/Transform recommendation report.
- Defer implementation of heavy custom mapping unless explicitly requested.
