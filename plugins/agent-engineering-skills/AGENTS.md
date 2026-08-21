# AGENTS.md

This plugin owns reusable agent-system design and operating workflows. Follow
root Socket guidance for general Git, release, dependency, safety, and
documentation rules.

## Scope

- Own coordinator/worker contracts, external-agent handoffs, scheduling,
  orchestration, and agent-system evaluation.
- Keep host compatibility adapters in `agent-portability-skills` and language
  implementation in the owning stack plugin.
- Root `skills/` is the authored source of truth; plugin metadata is packaging.

## Validation

Run from the Socket repository root so the shared maintainer environment and
cache policy apply:

```bash
uv run python -B -m pytest \
  plugins/agent-engineering-skills/skills/design-agent-automation-workflow/tests \
  plugins/agent-engineering-skills/skills/design-agent-eval-workflow/tests \
  -o cache_dir=.codex/.cache/pytest
```
