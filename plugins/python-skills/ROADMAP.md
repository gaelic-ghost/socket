# Project Roadmap

## Vision

- Keep `python-skills` as a focused, durable skills repository with one shared `skills/` surface, deterministic local helpers, and thin packaging layers on top.

## Product principles

- Keep the active public surface constrained to one shared `skills/` tree with thin vendor packaging layers.
- Prefer deterministic local scripts and validation over implied behavior.
- Keep skill docs, metadata, and script behavior synchronized.

## Milestone Progress

- [ ] Milestone 7: Claude Code skill optimizations

## Milestone 7: Claude Code skill optimizations

Scope:

- Audit the shared `skills/` content for Claude Code compatibility and additive Claude-oriented improvements.

Tickets:

- [ ] Review each shipped `SKILL.md` against Claude Code skill behavior and supported frontmatter.
- [ ] Make shared skill wording more vendor-neutral where that improves portability.
- [ ] Define a maintainer policy for Claude-only optimizations so they stay additive rather than invasive.
- [ ] Update maintainer docs to explain the shared-core versus vendor-layer split.

Exit criteria:

- [ ] Shared skills remain single-source and intentionally portable.
- [ ] Claude-specific skill optimizations are documented or implemented without duplicating the skill tree.

## History

- Completed Milestones 1 through 6 by establishing the repository, adding the Python bootstrap, FastAPI, FastMCP, and pytest workflows, aligning the maintainer contract, and adding Codex plugin packaging.
- Completed Milestone 8 by adding Claude plugin and marketplace support without duplicating the shared skill tree.
- Completed Milestones 9 and 10 by aligning the repo with the shared skills and plugin standards and adding the dedicated FastAPI and FastMCP integration workflow.
- Added GitHub Actions validation so the documented repo-metadata and pytest checks now run automatically on `main` and pull requests.
