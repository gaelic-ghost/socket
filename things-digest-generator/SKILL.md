---
name: things-digest-generator
description: Generate a week-ahead Things planning digest with recent activity, upcoming deadlines, and concrete next actions. Use when users request Things check-ins, weekly planning summaries, or prioritized planning recommendations.
---

# Things Digest Generator

Build a repeatable Things planning digest with four sections:

- Snapshot
- Recently Active
- Week/Weekend Ahead
- Suggestions

## Inputs

Collect data with Things MCP tools:

1. `things_read_areas`
2. `things_read_projects` with `status="open"`
3. `things_read_todos` with `status="open"`
4. `things_read_todos` with `status="completed"` and `completed_after=<today-7d>`
5. Optional `things_read_todo` for detailed notes/checklist signals

If any call fails due to permissions, report the missing permission and continue with best available data.

## Workflow

1. Load active customization config:
   - Prefer `config/customization.yaml`.
   - Fall back to `config/customization.template.yaml`.
2. Build urgency buckets from open todos.
3. Score recent activity by project and area.
4. Identify top active projects/areas.
5. Generate configured number of concrete suggestions.
6. Format output using `references/output-format.md`.

## Script Usage

Use `scripts/build_digest.py` for deterministic scoring/formatting:

```bash
uv run --with pyyaml python scripts/build_digest.py \
  --areas areas.json \
  --projects projects.json \
  --open-todos open_todos.json \
  --recent-done recent_done.json
```

Configuration precedence:

1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. script defaults

## Customization Workflow

1. Read `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm:
   - planning windows
   - top project/area counts
   - scoring weights
   - suggestion cap/style
3. Propose 2-4 option bundles with one recommended default.
4. Write `config/customization.yaml` with `schemaVersion: 1`, `isCustomized: true`, and profile.
5. Validate by generating a sample digest and reporting behavior deltas.

## Automation Templates

Use `$things-digest-generator` in automation prompts.

- `references/automation-prompts.md`

## References

- `references/suggestion-rules.md`
- `references/output-format.md`
- `references/customization.md`
- `references/config-schema.md`
- `references/automation-prompts.md`
