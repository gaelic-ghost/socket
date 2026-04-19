# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 11: Documentation and maintainer-surface alignment](#milestone-11-documentation-and-maintainer-surface-alignment)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

Keep `python-skills` as a focused Python workflow repository with one shared `skills/` surface, repo-root plugin metadata, and docs that make the authored-versus-packaged split obvious.

## Product Principles

- Keep root `skills/` as the only authored workflow surface.
- Keep repo-root plugin metadata thin, explicit, and aligned with the real install surfaces.
- Keep public docs, maintainer docs, and validation behavior synchronized.
- Keep general-purpose maintainer workflow guidance in `productivity-skills` unless Python-specific behavior truly changes the workflow.

## Milestone Progress

- Milestone 11: Documentation and maintainer-surface alignment - Active

## Milestone 11: Documentation and maintainer-surface alignment

### Status

Active

### Scope

- [ ] Align the root docs and maintainer guidance around the real source-of-truth split between root `skills/` and the repo-root plugin metadata.

### Tickets

- [ ] Tighten `README.md` so it owns the public overview, install surfaces, active inventory, and packaging shape.
- [ ] Add a root `CONTRIBUTING.md` that owns maintainer workflow, validation habits, and contributor expectations.
- [ ] Normalize `AGENTS.md` to the canonical repo-guidance structure without losing the repo-specific packaging rules.
- [ ] Clean up `ROADMAP.md` so the current planning surface and completed-history notes no longer compete with each other.
- [ ] Confirm the repo validation path still passes after the docs-alignment pass.

### Exit Criteria

- [ ] `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, and `ROADMAP.md` have clear non-overlapping roles.
- [ ] The docs describe root `skills/` as the source of truth and the repo root as the Codex plugin root.
- [ ] The repo validation path passes after the documentation update.

## Backlog Candidates

- [ ] Revisit the older Claude Code optimization plan as additive portability work once the core maintainer docs are aligned again.

## History

- Completed Milestones 1 through 6 by establishing the repository, adding the Python bootstrap, FastAPI, FastMCP, and pytest workflows, and aligning the initial maintainer contract.
- Completed Milestones 8 through 10 by adding Claude-compatible packaging, aligning the repo with the shared skills and plugin standards, and adding the dedicated FastAPI and FastMCP integration workflow.
- Added GitHub Actions validation so the documented repo-metadata and pytest checks now run automatically on `main` and pull requests.
- Reframed the stale planned Claude optimization milestone into backlog work and made documentation alignment the active planning surface.
