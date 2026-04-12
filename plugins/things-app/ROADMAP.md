# Project Roadmap

## Vision

- Keep `things-app` as the canonical home for Gale's Things-oriented skills plus the bundled Things MCP server, with packaging that stays honest about the mixed skills-and-server repository model.

## Product principles

- Keep root `skills/` as the canonical skill-authoring surface.
- Keep the bundled MCP server self-contained under `mcp/things-app-mcp/`.
- Keep plugin packaging thin and explicit.
- Keep root docs, server docs, and packaging metadata aligned with the same mixed-repo model.

## Milestone Progress

- [ ] Milestone 5: future Things workflow expansion

## Milestone 5: future Things workflow expansion

Scope:

- Expand the Things workflow surface deliberately instead of adding ad hoc helpers.

Tickets:

- [ ] Decide whether the next addition should be another skill, MCP server capability, or both.
- [ ] Keep any new workflow aligned with the repository's canonical mixed-repo model.

Exit criteria:

- [ ] New Things workflow additions fit the same skills-plus-server repository contract.

## History

- Completed Milestones 1 through 3 by establishing this repo as the canonical Things skill home, importing the bundled MCP server, and aligning the plugin packaging story around the shared authored surface.
- Completed Milestone 4 by tightening the repo docs, clarifying which validation runs from repo root versus `mcp/things-app-mcp/`, and keeping the mixed-repo packaging story consistent across the root docs.
