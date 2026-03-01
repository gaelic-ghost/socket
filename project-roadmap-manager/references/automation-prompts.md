# Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Conditional` - useful for recurring roadmap consistency checks and bounded updates.
- Codex CLI: `Conditional` - useful for scripted check/apply workflows when edits stay limited to `ROADMAP.md`.

## Codex App Automation Prompt Template

```markdown
Use $project-roadmap-manager.

Scope:
- Project root: <PROJECT_ROOT_ABS_PATH>
- Target file: <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD>
- Run mode: <UPDATE_MODE_CHECK_ONLY_OR_APPLY>

Execution policy:
- Restrict all edits to <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> only.
- Preserve existing roadmap content; update sections in place instead of duplicating.
- Keep `Current Milestone`, `Milestones`, `Plan History`, and `Change Log` internally consistent.
- If sub-milestones are enabled in skill config, keep parent/child linkage, child ID uniqueness, and child status values consistent.
- Never edit unrelated files.
- Never commit, push, or open PRs.

Output contract:
- Report whether roadmap is consistent.
- If updates were applied, summarize section-level changes and why.
- If check-only, report required changes without editing.

No-findings handling:
- If no updates are needed, output exactly `No findings.` and archive the run.
- Otherwise keep the run in inbox triage with a concise change summary.

Failure handling:
- If roadmap file is missing in check-only mode, report that it is missing and required path.
- If apply mode is blocked by permissions/sandbox, report minimum required access.
```

## Codex CLI Automation Prompt Template (codex exec)

### Variant A: Check-only

- Recommended sandbox: `read-only`

Prompt template:

```markdown
Use $project-roadmap-manager.

Check roadmap consistency at <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> for project <PROJECT_ROOT_ABS_PATH>.
Do not edit files.

Validate:
- Current Milestone matches active milestone row.
- Milestone statuses are non-conflicting.
- Plan History and Change Log are consistent with current state.
- If sub-milestones are enabled, child IDs are deterministic for configured style and unique within parent scope.
- If sub-milestones are enabled, child statuses follow `subMilestoneStatusValues` (or inherited `statusValues`).

If no updates are needed, output exactly `No findings.`.
Otherwise output a concise required-changes report.
```

### Variant B: Apply bounded updates

- Recommended sandbox: `workspace-write`

Prompt template:

```markdown
Use $project-roadmap-manager.

Apply bounded updates to <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> for project <PROJECT_ROOT_ABS_PATH>.
Edit this file only.
Synchronize Current Milestone, Milestones, Plan History, and Change Log per skill rules.
If sub-milestones are enabled, also synchronize child entries and parent/child linkage per skill rules.
Keep edits minimal and deterministic.
Never edit other files.
Never commit or push.

If no updates are needed, output exactly `No findings.`.
If blocked by permissions/sandbox, report minimum required access.
```

Optional command wrappers:

```bash
codex exec --sandbox read-only --output-last-message <FINAL_MESSAGE_PATH> "<PASTE_PROMPT_TEXT>"
```

```bash
codex exec --sandbox workspace-write --output-last-message <FINAL_MESSAGE_PATH> "<PASTE_PROMPT_TEXT>"
```

## Placeholders

- `<PROJECT_ROOT_ABS_PATH>`: Absolute project path.
- `<ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD>`: Absolute path to `ROADMAP.md`.
- `<UPDATE_MODE_CHECK_ONLY_OR_APPLY>`: `check-only` or `apply`.
- `<FINAL_MESSAGE_PATH>`: File path for final assistant output.
- `<PASTE_PROMPT_TEXT>`: Fully expanded prompt text for `codex exec`.

## Customization Points

- Run mode (`check-only` vs `apply`).
- Allowed status vocabulary and milestone naming conventions.
- Optional sub-milestone settings (enablement, ID style, delimiter, and child status vocabulary).
- Change-log verbosity requirements.
- Date/target conventions (version-based or calendar-based).
