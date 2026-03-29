# Roadmap Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Conditional` - useful for recurring checklist-roadmap consistency checks and bounded updates.
- Codex CLI: `Conditional` - useful for scripted check/apply workflows when edits stay limited to `ROADMAP.md`.

## Codex App Automation Prompt Template

```markdown
Use $project-docs-maintainer with mode=roadmap_maintenance.

Scope:
- Project root: <PROJECT_ROOT_ABS_PATH>
- Target file: <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD>
- Run mode: <UPDATE_MODE_CHECK_ONLY_OR_APPLY>

Execution policy:
- Restrict all edits to <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> only.
- Preserve useful roadmap content and update sections in place.
- Enforce checklist-standard roadmap structure:
  - `Milestone Progress`
  - Milestone sections with `Scope`, `Tickets`, and `Exit criteria`
- Ensure each milestone has checklist items and valid checkbox syntax.
- Mark parallelizable ticket items with `[P]` only when genuinely parallel.
- If legacy table-style format is detected:
  - In `apply` mode: migrate in-place to checklist standard while preserving useful history.
  - In `check-only` mode: report required migration changes without editing.
- Never edit unrelated files.
- Never commit, push, or open PRs.

Output contract:
- Report whether roadmap is checklist-consistent.
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
Use $project-docs-maintainer with mode=roadmap_maintenance.

Check roadmap consistency at <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> for project <PROJECT_ROOT_ABS_PATH>.
Do not edit files.

Validate:
- `Milestone Progress` exists and matches milestone-level reality.
- Each milestone section includes `Tickets` and `Exit criteria`.
- Ticket and exit criteria items use valid markdown checkbox syntax.
- `[P]` appears only on ticket items where parallel work is plausible.
- If legacy table-style sections are present, report migration required.

If no updates are needed, output exactly `No findings.`.
Otherwise output a concise required-changes report.
```

### Variant B: Apply bounded updates

- Recommended sandbox: `workspace-write`

Prompt template:

```markdown
Use $project-docs-maintainer with mode=roadmap_maintenance.

Apply bounded updates to <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> for project <PROJECT_ROOT_ABS_PATH>.
Edit this file only.

Enforce checklist-standard roadmap structure and consistency:
- `Milestone Progress`
- Milestone sections with `Scope`, `Tickets`, and `Exit criteria`
- Valid checkbox syntax and deterministic milestone ordering

If legacy table-style format is present, migrate in-place and preserve useful history/context without duplicated conflicting state.
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
- Ticket granularity conventions and `[P]` usage expectations.
- History/changelog verbosity behavior.
- Legacy migration strictness for preserving historical sections.
