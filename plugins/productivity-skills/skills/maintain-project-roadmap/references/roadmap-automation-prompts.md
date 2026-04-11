# Roadmap Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Conditional` - useful for recurring checklist-roadmap audits, bounded updates, and legacy migrations that stay limited to `ROADMAP.md`
- Codex CLI: `Conditional` - useful for scripted check/apply workflows when roadmap edits stay limited to one file

## Codex App Automation Prompt Template

```markdown
Use $maintain-project-roadmap.

Scope:
- Project root: <PROJECT_ROOT_ABS_PATH>
- Target file: <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD>
- Run mode: <UPDATE_MODE_CHECK_ONLY_OR_APPLY>

Execution policy:
- Restrict all edits to <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> only.
- Preserve useful roadmap content while normalizing it into the canonical checklist roadmap structure.
- Enforce the required table of contents.
- Enforce canonical top-level sections and configured milestone subsection headings.
- Ensure milestone progress matches the actual milestone sections, order, and milestone status values.
- Ensure checklist items use valid markdown checkbox syntax.
- Allow `[P]` only inside milestone `Tickets` subsections.
- If legacy table-style format is detected:
  - In `apply` mode: migrate in-place to checklist standard while preserving useful milestone identity.
  - In `check-only` mode: report migration required without editing.
- Never edit unrelated files.
- Never commit, push, or open PRs.

Output contract:
- Report whether the roadmap matches the configured checklist contract.
- If updates were applied, summarize structural changes and why.
- If check-only, report required changes without editing.

No-findings handling:
- If no updates are needed, output exactly `No findings.` and archive the run.
- Otherwise keep the run in inbox triage with a concise change summary.

Failure handling:
- If roadmap file is missing in check-only mode, report the missing required path.
- If apply mode is blocked by permissions or sandboxing, report the minimum required access.
```

## Codex CLI Automation Prompt Template (codex exec)

### Variant A: Check-only

- Recommended sandbox: `read-only`

Prompt template:

```markdown
Use $maintain-project-roadmap.

Check roadmap consistency at <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> for project <PROJECT_ROOT_ABS_PATH>.
Do not edit files.

Validate:
- the roadmap has a title and the required table of contents
- canonical top-level sections are present and ordered correctly
- milestone sections are ordered deterministically
- each milestone includes the configured required subsections
- milestone statuses use allowed status values
- milestone progress matches the actual milestone headings and statuses
- checklist items use valid markdown checkbox syntax
- `[P]` appears only in milestone `Tickets` subsections
- if legacy table-style sections are present, report that migration is required

If no updates are needed, output exactly `No findings.`.
Otherwise output a concise required-changes report.
```

### Variant B: Apply bounded updates

- Recommended sandbox: `workspace-write`

Prompt template:

```markdown
Use $maintain-project-roadmap.

Apply bounded updates to <ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD> for project <PROJECT_ROOT_ABS_PATH>.
Edit this file only.

Enforce the configured checklist roadmap structure:
- required table of contents
- canonical top-level sections
- milestone sections in deterministic order
- required milestone subsections
- milestone progress aligned with milestone sections and statuses
- valid checkbox syntax

If legacy table-style format is present, migrate in-place using the canonical checklist template as the target structure.
Keep edits minimal, deterministic, and grounded in the existing roadmap plus bundled scaffold wording.
Never edit other files.
Never commit or push.

If no updates are needed, output exactly `No findings.`.
If blocked by permissions or sandboxing, report the minimum required access.
```

## Placeholders

- `<PROJECT_ROOT_ABS_PATH>`: absolute project path
- `<ROADMAP_PATH_DEFAULT_PROJECT_ROOT_ROADMAP_MD>`: absolute path to `ROADMAP.md`
- `<UPDATE_MODE_CHECK_ONLY_OR_APPLY>`: `check-only` or `apply`

## Customization Points

- top-level section set and ordering
- milestone subsection set and ordering
- heading alias migrations
- scaffolding text for base sections and milestone subsections
- additional-section preservation policy
