# AGENTS.md

Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or workflow surfaces in this repository.

## Repository Scope

### What This File Covers

- `agent-plugin-skills` is the canonical home for maintainer skills that target skills-export and plugin-export repositories.
- This root file governs the repo-wide maintainer docs, the source-first plugin packaging surface at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json), and the authored skill surface under [`skills/`](./skills/).

### Where To Look First

- Start with [README.md](./README.md), [CONTRIBUTING.md](./CONTRIBUTING.md), and [ROADMAP.md](./ROADMAP.md).
- For Codex packaging or install-surface questions, read [`docs/maintainers/codex-plugin-install-surfaces.md`](./docs/maintainers/codex-plugin-install-surfaces.md).
- For current repo-shape and inventory expectations, read [`docs/maintainers/reality-audit.md`](./docs/maintainers/reality-audit.md) and [`docs/maintainers/workflow-atlas.md`](./docs/maintainers/workflow-atlas.md).

## Working Rules

### Change Scope

- Keep work bounded to the repo surface that actually changed.
- When a skill contract changes, update the nearby maintainer docs and tests in the same pass.
- Do not widen work into installer revival, nested packaging, or repo-shape experiments unless Gale explicitly asks for that scope change.

### Source of Truth

- Root [`skills/`](./skills/) is the canonical authored and exported surface.
- Treat maintainer docs under [`docs/maintainers/`](./docs/maintainers/) as the durable explanation layer for repo policy and packaging boundaries.
- Keep Codex plugin guidance aligned with the current OpenAI docs: only `plugin.json` belongs in `.codex-plugin/`, while `skills/` stays at the plugin root.
- Keep Codex plugin-boundary wording factual and explicit: repo-visible plugins come from the documented marketplace model, and OpenAI does not document a richer repo-private scoping model beyond that.
- For Python-backed maintainer repositories, require `uv` plus repo-local dev dependencies in `pyproject.toml` for the tools the repo expects to run.
- Do not teach or rely on machine-global `uv tool install` as the primary baseline for repo validation when the repo can declare `pytest`, `ruff`, and `mypy` directly in its dev dependency group.

### Communication and Escalation

- Surface scope expansion before adding new maintainer workflows, new packaging layers, or new repo families.
- If docs and shipped skill behavior diverge, fix the skill or narrow the docs so they match instead of preserving soft ambiguity.
- When a wording choice could overstate Codex packaging behavior, prefer the narrower documented claim and name the exact surface involved.

### Sync And Branch Accounting Gates

- Treat repo-sync verification and local-branch accounting as hard gates before cleanup or "done" claims.
- When work in this repository is performed from the `socket` superproject or is expected to ship back through `socket`, verify whether `socket` now needs an explicit subtree or nested-repo sync step and either complete it or say plainly why no sync is required.
- Before saying work is merged, preserved, or safe to delete, verify the exact commit reachability in the repo and remote being discussed.
- Before deleting local branches, remote branches, worktrees, or rescue refs, enumerate every local branch not contained by `main` and account for each one explicitly as preserved elsewhere, intentionally in progress, newly archived, newly merged, or safe to delete.
- Do not treat branch cleanup as routine hygiene that can happen before that accounting pass.

## Commands

### Setup

```bash
uv sync --dev
```

### Validation

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

### Optional Project Commands

There are no additional repo-level commands worth calling out beyond the `uv` sync and test flow.

## Review and Delivery

### Review Expectations

- Keep edits compact, repo-specific, and grounded in the shipped skill surface.
- When changing docs, preserve the split between public-facing project docs, contributor workflow docs, maintainer reference docs, and agent guidance.
- When changing skill behavior or audit logic, include the nearest tests or validation updates in the same pass.

### Definition of Done

- The changed surface is consistent across the relevant skill, maintainer doc, and test coverage.
- README, CONTRIBUTING, AGENTS, and ROADMAP stay aligned with the current repo shape when one of them materially changes.
- `uv run pytest` passes after changes that touch shipped skills, maintainer automation, or docs-backed audit expectations.
- Any required superproject or nested-repo sync has been completed or surfaced explicitly before cleanup.
- Local branches not contained by `main` have been accounted for explicitly before deleting anything.

## Safety Boundaries

### Never Do

- Do not recreate nested staged plugin directories or repo-local installer workflows in this repository.
- Do not invent hidden plugin install surfaces, undocumented scoping behavior, or stale packaging overlays.
- Do not treat maintainer docs as a substitute for the actual shipped skill contract.

### Ask Before

- Ask before adding new maintainer workflows, new repo-family support, or new packaging layers.
- Ask before turning this repo into a broader plugin-management surface beyond its current maintainer-skill role.
- Ask before deleting a maintainer reference doc unless its durable conclusions have been moved somewhere still-live.

## Local Overrides

There are no deeper `AGENTS.md` files in this repository today. If one is added later, that narrower file should refine this root guidance for the subtree where it lives.
