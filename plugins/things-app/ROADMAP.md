# Project Roadmap

## Vision

- Keep `things-app` as the canonical home for Gale's Things-oriented skills plus the bundled Things MCP server, with packaging that stays honest about the mixed skills-and-server repository model.

## Product Principles

- Keep root `skills/` as the canonical skill-authoring surface.
- Keep the bundled MCP server self-contained under `mcp/things-app-mcp/`.
- Keep plugin packaging thin and explicit under `plugins/things-app/`.
- Keep root docs, server docs, and packaging metadata aligned with the same mixed-repo model.

## Milestone Progress

- [x] Milestone 1: canonical Things skill repo
- [x] Milestone 2: bundled MCP server import
- [x] Milestone 3: plugin-first packaging
- [ ] Milestone 4: docs and validation consolidation
- [ ] Milestone 5: future Things workflow expansion

## Milestone 1: canonical Things skill repo

Scope:

- Establish the repository as the canonical home for Gale's Things-oriented skills.

Tickets:

- [x] Keep the active Things skills together under root `skills/`.
- [x] Align repo docs with the repository's Things-focused role.

Exit criteria:

- [x] The repository clearly owns the Things skills it ships today.

## Milestone 2: bundled MCP server import

Scope:

- Vendor the standalone Things MCP server into this repository without hiding its own package and test surface.

Tickets:

- [x] Import `things-app-mcp` under `mcp/things-app-mcp/`.
- [x] Preserve the server as a self-contained FastMCP package with its own docs and tests.

Exit criteria:

- [x] The MCP server lives in this repository with its own maintainable local surface.

## Milestone 3: plugin-first packaging

Scope:

- Keep one packaged plugin surface for Codex and Claude while leaving root `skills/` canonical.

Tickets:

- [x] Add the packaged plugin root under `plugins/things-app/`.
- [x] Keep the marketplace and discovery surfaces aligned with the same authored skill tree.

Exit criteria:

- [x] The packaged plugin surface and the canonical skill-authoring surface describe the same shipped repo model.

## Milestone 4: docs and validation consolidation

Scope:

- Tighten the mixed-repo maintainer contract now that the repository ships skills, server code, and plugin packaging together.

Tickets:

- [ ] Add a dedicated roadmap and keep it aligned with the root README.
- [ ] Clarify which validations run from repo root versus from `mcp/things-app-mcp/`.
- [ ] Keep root docs and bundled server docs consistent when packaging or server layout changes.

Exit criteria:

- [ ] Public docs and maintainer guidance explain the same mixed-repository validation and packaging story.

## Milestone 5: future Things workflow expansion

Scope:

- Expand the Things workflow surface deliberately instead of adding ad hoc helpers.

Tickets:

- [ ] Decide whether the next addition should be another skill, MCP server capability, or both.
- [ ] Keep any new workflow aligned with the repository's canonical mixed-repo model.

Exit criteria:

- [ ] New Things workflow additions fit the same skills-plus-server repository contract.
