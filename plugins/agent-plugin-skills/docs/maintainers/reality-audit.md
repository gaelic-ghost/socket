# Repo Reality Audit

Use this document as the source-of-truth checklist when auditing `agent-plugin-skills`.

For the durable map of Codex plugin catalogs, staged payloads, installed cache paths, and config enabled-state, see [codex-plugin-install-surfaces.md](./codex-plugin-install-surfaces.md).

## Source Of Truth Order

1. root `skills/`
2. skill-local runtime files inside each skill directory
3. repo docs: `README.md`, `AGENTS.md`, `ROADMAP.md`
4. maintainer docs under `docs/maintainers/`
5. local discovery mirrors only: `.agents/skills`, `.claude/skills`

## Hard Boundaries

- Treat `productivity-skills` as the default baseline owner for general repo-doc and maintenance workflows.
- Treat this repository as the specialist override only for skills-export and plugin-export repo shapes.
- This repository ships root `.codex-plugin` packaging and does not track a nested staged plugin directory for itself.
- This repository does not track a repo-local Codex marketplace file for itself.
- This repository does not ship `install-plugin-to-socket`.
- This repository does not ship `validate-plugin-install-surfaces`.
- If docs or skills imply otherwise, treat that as a real defect.

## Audit Checklist

- Root `skills/` is canonical.
- `.agents/skills` and `.claude/skills` are POSIX symlink mirrors to `../skills`.
- README and AGENTS say plainly that this repo exports installable skills and that OpenAI documents marketplace-based plugin discovery rather than a richer repo-private plugin scope.
- ROADMAP matches the live exported skill set.
- Maintainer tooling guidance includes `uv sync --dev`, repo-local `pyproject.toml` dev dependencies for `pytest`, `ruff`, and `mypy`, plus the corresponding `uv run pytest`, `uv run ruff check .`, and `uv run mypy .` commands when those checks are part of the shipped workflow.
- No tracked file reintroduces nested staged plugin directories, repo-marketplace guidance for this repo, installer workflows, or install-validation workflows.

## Specialist Owners

- `bootstrap-skills-plugin-repo`
- `sync-skills-repo-guidance`
