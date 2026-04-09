---
name: maintain-project-contributing
description: Maintain canonical CONTRIBUTING.md files for ordinary software projects through deterministic audit and bounded apply modes. Use when a project contribution guide needs auditing, normalization, or bounded fixes for contributor workflow, local setup, naming conventions, verification, or pull request expectations.
---

# Maintain Project Contributing

Maintain canonical `CONTRIBUTING.md` files for ordinary software projects through one deterministic contribution-guide workflow.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--contributing-path <path>`

## Workflow

1. Validate the project root and resolve the target `CONTRIBUTING.md`.
2. Detect the repo profile from repo signals such as package metadata, workspace manifests, runtime dependencies, or build files.
3. In `check-only`, audit the required section schema, the required `Local Setup > Runtime Config` and `Local Setup > Runtime Behavior` subsections, naming-conventions coverage, and grounded command integrity.
4. In `apply`, keep edits bounded to the target `CONTRIBUTING.md` while creating or normalizing the canonical section order and filling missing sections with grounded, non-invented guidance.
5. Re-run the same audit to confirm post-fix status.

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
- Never invent commands, setup steps, environment variables, branch rules, or review policies that are not grounded in the repo.
- Never edit files other than the target `CONTRIBUTING.md`.
- Keep `CONTRIBUTING.md` as the canonical contribution-guide filename for this skill.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/project-contributing-maintenance-automation-prompts.md`
