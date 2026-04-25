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
- For Python-backed maintainer work, require `uv` plus repo-local dev dependencies in `pyproject.toml` for the tools the repo expects to run.
- Do not rely on machine-global installs as the primary maintainer baseline when the repository can declare `pytest`, `ruff`, and `mypy` directly in its dev dependency group.

### Dependency Provenance

- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch.
- Do not commit dependency declarations, lockfiles, scripts, docs, examples, generated project files, or CI config that point at machine-local paths such as `/Users/...`, `~/...`, `../...`, local worktrees, or private checkout paths.
- Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly. If local integration is needed, keep it uncommitted or convert it to a tagged release, branch, or registry dependency before sharing.

### Validation Discipline

- Keep user-facing and maintainer-facing Python command examples expressed with `uv`.
- Run the repo validation path before landing documentation or metadata changes.
- If docs and validator behavior disagree, update them in the same pass instead of leaving a split-brain repo state.

### Sync And Branch Accounting Gates

- Treat repo-sync verification and local-branch accounting as hard gates before cleanup, release closeout, or "done" claims.
- When work in this repository is performed from the `socket` superproject or is expected to ship back through `socket`, verify whether `socket` now needs an explicit subtree sync and either complete it or say plainly why no sync is required.
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
uv run scripts/validate_repo_metadata.py
uv run pytest
uv run ruff check .
uv run mypy .
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
- `uv run scripts/validate_repo_metadata.py`, `uv run pytest`, `uv run ruff check .`, and `uv run mypy .` pass when the touched work should affect them.
- Any required superproject or subtree sync has been completed or surfaced explicitly before cleanup.
- Local branches not contained by `main` have been accounted for explicitly before deleting anything.

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
