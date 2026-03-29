---
name: maintain-project-readme
description: Maintain ordinary software-project README.md files through deterministic audit and bounded apply modes. Use when a project README needs clearer overview, motivation, setup, usage, development, or verification guidance. Do not use this for agent-skills, Codex plugin, Claude plugin, or similar skills or plugin repositories with specialized install and discoverability sections.
---

# Maintain Project README

Maintain ordinary software-project `README.md` files through one deterministic README workflow.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--readme-path <path>`

## Workflow

1. Validate the project root and resolve the target `README.md`.
2. Detect the repo profile from repo signals such as package metadata, CLI entrypoints, app/service manifests, or workspace files.
3. In `check-only`, audit title/value proposition, common README sections, the required `Overview > Motivation` structure, and command integrity.
4. In `apply`, keep edits bounded to the target `README.md` while repairing missing structure and grounded wording.
5. Re-run the same audit to confirm post-fix status.
6. If the repository is a skills or plugin repo with specialized install and discoverability conventions, use `maintain-skills-readme` instead.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `profile_assignment`
  - `schema_violations`
  - `command_integrity_issues`
  - `content_quality_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, setup steps, or support claims that are not grounded in the repo.
- Never edit files other than the target `README.md`.
- Do not use this skill for agent-skills, Codex plugin, Claude plugin, or similar skills/plugin repositories. Use `maintain-skills-readme` instead.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/profile-model.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/verification-checklist.md`
