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

- This repository does not track a nested plugin directory for itself.
- This repository does not track a repo-local Codex marketplace file for itself.
- This repository does not ship `install-plugin-to-socket`.
- This repository does not ship `validate-plugin-install-surfaces`.
- If docs or skills imply otherwise, treat that as a real defect.

## Audit Checklist

- Root `skills/` is canonical.
- `.agents/skills` and `.claude/skills` are POSIX symlink mirrors to `../skills`.
- README and AGENTS say plainly that this repo exports installable skills and does not pretend Codex has proper repo-private plugin scope.
- ROADMAP matches the live exported skill set.
- Maintainer tooling guidance includes `uv sync --dev`, `uv tool install ruff`, `uv tool install mypy`, and `uv run --group dev pytest`.
- No tracked file reintroduces nested plugin directories, repo-marketplace guidance for this repo, installer workflows, or install-validation workflows.

## Specialist Owners

- `maintain-plugin-docs`
- `maintain-plugin-repo`
- `bootstrap-skills-plugin-repo`
- `sync-skills-repo-guidance`
