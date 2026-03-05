---
name: project-workspace-cleaner
description: Scan workspace repositories for cleanup opportunities using a read-only hygiene audit. Use when users ask to detect build/cache artifact buildup, stale large transient files, and prioritized cleanup chores by repository and directory.
---

# Project Workspace Cleaner

Run a read-only scan over repositories in `~/Workspace` and rank cleanup chores by severity.

## Workflow

1. Load active customization config:
   - Prefer `config/customization.yaml`.
   - Fall back to `config/customization.template.yaml`.
2. Run `scripts/scan_workspace_cleanup.py`.
3. Review top-ranked findings first.
4. Report findings with severity, repo, directory, category, size, and reason.
5. Provide cleanup recommendations as text only.

## Commands

Default scan:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py
```

Custom workspace root:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py --workspace ~/Workspace
```

Machine-readable output:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py --json
```

Tuned thresholds:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py --min-mb 100 --stale-days 90
```

Configuration precedence:

1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. script defaults

## Output Contract

Each finding includes:

- `severity`
- `repo`
- `directory`
- `category`
- `size_human`
- `score`
- `why_flagged`
- `suggested_cleanup`

Report includes:

- top findings (sorted by severity then size)
- repo summary (ranked by total flagged size)

## Read-Only Rules

- Never run destructive commands.
- Never remove artifacts automatically.
- Never write into scanned repositories.
- Provide recommendations only.

## Customization Workflow

1. Read `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm:
   - workspace root
   - thresholds (`minMb`, `staleDays`, `maxFindings`)
   - severity cutoffs
   - override rules
3. Propose 2-4 option bundles with one recommended default.
4. Write `config/customization.yaml` with `schemaVersion: 1`, `isCustomized: true`, and profile.
5. Validate with a scan run and report behavior deltas.

## Automation Templates

Use `$project-workspace-cleaner` in automation prompts.

- `references/automation-prompts.md`

## References

- `references/patterns.md`
- `references/customization.md`
- `references/config-schema.md`
- `references/automation-prompts.md`
