---
name: workspace-cleanup-audit
description: Read-only repository hygiene scanner for directories under ~/Workspace. Use when asked to audit cleanup chores, detect build or cache artifact buildup, find large transient files, or rank cleanup issues by severity with the repo and directory where each issue is found.
---

# Workspace Cleanup Audit

## Overview

Run a read-only scan over repositories in `~/Workspace` and report cleanup chores ranked by severity. Never delete, move, or modify files.

## Workflow

1. Load active customization config:
   - Prefer `<skill_root>/config/customization.yaml`.
   - Fall back to `<skill_root>/config/customization.template.yaml`.
2. Run `scripts/scan_workspace_cleanup.py`.
3. Review top-ranked findings first.
4. Report findings with severity, repo, directory, category, size, and reason.
5. Suggest cleanup actions as text only.

## Commands

Use the default workspace scan:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py
```

Scan a custom workspace root:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py --workspace ~/Workspace
```

Return machine-readable output:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py --json
```

Tune noise floor and stale threshold:

```bash
uv run --with pyyaml python scripts/scan_workspace_cleanup.py --min-mb 100 --stale-days 90
```

Configuration precedence:

1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. Script hardcoded defaults

## Customization Workflow

When a user asks to customize this skill, use this deterministic flow:

1. Read active config from `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm desired behavior for:
   - workspace root
   - thresholds (`minMb`, `staleDays`, `maxFindings`)
   - severity cutoffs
   - directory/file override rules
3. Propose 2-4 option bundles with one recommended default.
4. Create or update `config/customization.yaml` from template and set:
   - `schemaVersion: 1`
   - `isCustomized: true`
   - `profile: <selected-profile>`
5. Validate with a scan run and report changed keys plus behavior deltas.

## Customization Reference

- Detailed knobs and examples: `references/customization.md`
- YAML schema and allowed values: `references/config-schema.md`

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

The report also includes:

- Top findings sorted by severity then size
- Repo summary ranked by total flagged size

## Read-Only Rules

- Never run destructive commands.
- Never remove artifacts automatically.
- Never write into scanned repositories.
- Provide recommendations only.

## Automation Templates

Use `$workspace-cleanup-audit` inside automation prompts so Codex consistently loads this skill behavior.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including placeholders, safety defaults, and output handling, use:
- `references/automation-prompts.md`

## References

- Pattern and threshold notes: `references/patterns.md`
- Automation prompt templates: `references/automation-prompts.md`
- Customization guide: `references/customization.md`
- Customization schema: `references/config-schema.md`
