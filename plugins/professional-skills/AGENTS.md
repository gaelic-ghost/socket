# AGENTS.md

This plugin owns professional workflows such as career and job-search guidance.
Follow root Socket guidance for general Git, release, dependency, privacy, and
documentation rules.

## Scope

- Keep professional-service integrations, career workflows, privacy boundaries,
  and application-state guidance here.
- Do not absorb generic personal productivity, repository maintenance, or
  agent-system engineering work.
- Root `skills/` is the authored source of truth; plugin metadata is packaging.

## Validation

Run from the Socket repository root so the shared maintainer environment and
cache policy apply:

```bash
uv run python -B -m pytest \
  plugins/professional-skills/skills/dice-job-search-workflow/tests \
  -o cache_dir=.codex/.cache/pytest
```
