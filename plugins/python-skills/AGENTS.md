# AGENTS.md

Use this file for durable repo-local guidance before changing code, docs, metadata, or packaging in this repository.

## Repository Scope

### What This File Covers

- `python-skills` is the canonical source of truth for the shipped Python workflow skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Treat `productivity-skills` as the default baseline maintainer layer for general repo-doc and maintenance work. Use this repo when Python-specific behavior should materially change the workflow.

### Where To Look First

- Start with [`README.md`](./README.md), [`CONTRIBUTING.md`](./CONTRIBUTING.md), and [`ROADMAP.md`](./ROADMAP.md).
- Use [`docs/maintainers/workflow-atlas.md`](./docs/maintainers/workflow-atlas.md) for the maintained map of the active repo surface.
- Use [`docs/maintainers/reality-audit.md`](./docs/maintainers/reality-audit.md) when checking whether docs, metadata, and packaging still match shipped reality.
- Use [`scripts/validate_repo_metadata.py`](./scripts/validate_repo_metadata.py) and [`tests/test_validate_repo_metadata.py`](./tests/test_validate_repo_metadata.py) as the mechanical source of truth for the current metadata contract.

## Working Rules

### Change Scope

- Keep changes focused on one coherent repo outcome.
- When the shipped skill surface changes, update the affected skill docs, root docs, and packaging metadata in the same pass.
- Do not broaden this repo into the general-purpose maintainer baseline when the work belongs in `productivity-skills`.

### Source Of Truth

- Treat each skill directory's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair.
- Do not reintroduce a nested packaged plugin subtree for Codex.
- Do not reintroduce maintained per-skill `README.md` files unless Gale explicitly asks for that public-doc surface again.
- Keep direct skill-install guidance accurate alongside repo-root plugin guidance.

### Validation Discipline

- Keep user-facing and maintainer-facing Python command examples expressed with `uv`.
- Run the repo validation path before landing documentation or metadata changes.
- If docs and validator behavior disagree, update them in the same pass instead of leaving a split-brain repo state.

## Commands

### Setup

```bash
uv sync --dev
```

### Validation

```bash
uv run scripts/validate_repo_metadata.py
uv run pytest
```

## Review and Delivery

### Review Expectations

- Explain whether the change affects the authored `skills/` surface, the repo-root plugin metadata, or only repo documentation.
- Keep install guidance, active skill inventory, and packaging language aligned across root docs and metadata.
- Prefer small, focused commits over broad mixed maintenance passes.

### Definition Of Done

- The changed surface still preserves root `skills/` as the source of truth.
- Root docs reflect the current active skill inventory and packaging shape.
- The repo root still reads as the plugin root for Codex without a second packaged subtree.
- `uv run scripts/validate_repo_metadata.py` and `uv run pytest` pass when the touched work should affect them.

## Safety Boundaries

### Never Do

- Do not add back a second packaged subtree that duplicates the repo-root plugin surface.
- Do not invent install paths, marketplace surfaces, or packaging metadata that are not present in the repo.
- Do not silently widen this repo to own stack-neutral maintainer workflows that belong in `productivity-skills`.

### Ask Before

- Ask before adding a second authored documentation surface for each skill.
- Ask before changing the packaging split between root `skills/` and repo-root plugin metadata.
- Ask before introducing new vendor-specific packaging layers beyond the current thin plugin roots.

## Local Overrides

- There are no deeper repo-local `AGENTS.md` files below this root today.
- If a future nested instruction file is added under a narrower subpath, treat it as refining this root guidance for that subtree.
