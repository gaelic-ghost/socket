---
name: maintain-skills-readme
description: Maintain README.md files for agent-skills, Codex plugin, Claude plugin, and similar skills or plugin repositories with specialized install, discoverability, and catalog sections. Use when a skills or plugin repo README needs auditing or bounded fixes. Do not use this for ordinary software project READMEs.
---

# Maintain Skills README

Maintain specialized README.md files for skills and plugin repositories through one deterministic workflow.

Current scope note:

- This skill is intentionally README-only today.
- It is the current stack-specific docs-maintenance entrypoint for this repo family, but only for `README.md`.
- The roadmap may replace or widen it into a broader stack-specific docs maintainer, likely `maintain-plugin-docs`, after the wider workflow and boundaries are defined.

## Inputs

- Required: `--workspace <path>`
- Optional: `--repo-glob <glob>`
- Optional: repeatable `--exclude <path>`
- Optional: `--apply-fixes`
- Treat `skills_readme_alignment` as compatibility-only when handling legacy prompts.

## Workflow

1. Validate the workspace path and discover matching repositories.
2. Run the read-only audit first.
3. Check README sections, install commands, skill inventory wording, and skills/plugin discoverability rules.
4. If the user requested edits, apply bounded fixes with `--apply-fixes`.
5. Re-run the same audit to confirm remaining issues.
6. Return the Markdown plus JSON report shape.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `repos_scanned`
  - `profile_assignments`
  - `schema_violations`
  - `command_integrity_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never edit source code, manifests, lockfiles, or CI files.
- Keep edits bounded to `README.md` and explicitly approved snippet insertions into `AGENTS.md`.
- Do not use this skill for ordinary software project READMEs. Use `maintain-project-readme` instead.

## References

- `references/output-contract.md`
- `references/skills-readme-maintenance-automation-prompts.md`
- `references/profile-model.md`
- `references/section-schema.md`
- `references/discoverability-rules.md`
- `references/fix-policies.md`
