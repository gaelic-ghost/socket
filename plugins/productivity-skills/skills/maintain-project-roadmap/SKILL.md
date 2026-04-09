---
name: maintain-project-roadmap
description: Maintain checklist-style ROADMAP.md files for projects through deterministic validation and bounded apply modes. Use when a project roadmap needs auditing, normalization, or legacy-format migration.
---

# Maintain Project Roadmap

Maintain checklist-style `ROADMAP.md` files through one deterministic roadmap workflow.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--roadmap-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root.
2. Resolve the roadmap path.
3. In `check-only`, audit sections, checkboxes, milestone ordering, and legacy format.
4. In `apply`, create, migrate, or normalize the target `ROADMAP.md`.
5. Re-run the same checks to confirm remaining findings.
6. Return the Markdown plus JSON roadmap report.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `findings`
  - `apply_actions`
  - `errors`
- If there are no findings, no apply actions, and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never edit files other than the target `ROADMAP.md` in `apply` mode.
- Keep checklist-style `ROADMAP.md` as the canonical format.

## References

- `references/roadmap-automation-prompts.md`
- `references/roadmap-customization.md`
- `references/roadmap-config-schema.md`
