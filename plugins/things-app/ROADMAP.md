# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 5: guidance and maintenance modernization](#milestone-5-guidance-and-maintenance-modernization)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `things-app` as the canonical home for Gale's Things-oriented skills plus the bundled Things MCP server, with documentation and packaging that stay honest about the mixed skills-and-server repository model.

## Product Principles

- Keep root `skills/` as the canonical skill-authoring surface.
- Keep the bundled MCP server self-contained under `mcp/`.
- Keep plugin packaging thin and explicit.
- Keep root docs, server docs, and packaging metadata aligned in the same pass when shared behavior changes.

## Milestone Progress

- Milestone 5: guidance and maintenance modernization - In Progress

## Milestone 5: guidance and maintenance modernization

### Status

In Progress

### Scope

- [ ] Refresh the root maintainer docs so `README.md`, `ROADMAP.md`, and `AGENTS.md` describe the same mixed repo model and the same source-of-truth boundaries, with shared contribution workflow owned by Socket root docs.
- [ ] Tighten the split between root-skill maintenance guidance and bundled-server guidance so contributors can tell which validation path applies to which surface.

### Tickets

- [ ] Keep the root README focused on project shape, usage, packaging, and high-level validation entrypoints.
- [ ] Keep root README and AGENTS guidance grounded about setup, workflow, and review expectations for root skills, plugin packaging, and the bundled MCP server.
- [ ] Keep AGENTS guidance explicit about source-of-truth boundaries, validation commands, and scope-escalation triggers.
- [ ] Re-run the maintainer guidance audits after doc updates so the subtree stays on the canonical schemas.

### Exit Criteria

- [ ] The root guidance files pass the maintainer-schema checks without placeholder text or contradictory claims.
- [ ] A contributor can tell, from the root docs alone, whether their change belongs in `skills/`, `mcp/`, or the thin plugin metadata.

## Backlog Candidates

- [ ] Expand the repo-root maintainer tooling once more than one root skill needs Python-backed verification.
- [ ] Add broader bundled-server smoke coverage when new Things tool families or auth-sensitive update flows are introduced.
- [ ] Revisit packaging mirrors if the repo starts shipping additional Codex discovery surfaces.

## History

- Completed Milestones 1 through 3 by establishing this repo as the canonical Things skill home, importing the bundled MCP server, and aligning the plugin packaging story around the shared authored surface.
- Completed Milestone 4 by tightening the repo docs, clarifying which validation runs from repo root versus `mcp/`, and keeping the mixed-repo packaging story consistent across the root docs.
- Opened Milestone 5 to modernize the root guidance contract around a cleaner README, AGENTS, and Socket-root contribution split plus explicit maintainer-schema alignment.
