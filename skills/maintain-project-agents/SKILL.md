---
name: maintain-project-agents
description: Maintain ordinary project-local AGENTS.md files through deterministic audit and bounded apply modes. Use when a repository's AGENTS.md needs auditing, normalization, or bounded fixes for workflow guidance, validation commands, architecture boundaries, or agent safety rules.
---

# Maintain Project Agents

Maintain ordinary project-local `AGENTS.md` files through one deterministic AGENTS workflow.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--agents-path <path>`

## Workflow

1. Validate the project root and resolve the target `AGENTS.md`.
2. Detect repo signals that affect agent guidance, such as package-manager files, validation commands, packaging layout, or workflow boundaries.
3. In `check-only`, audit the required AGENTS sections, workflow accuracy, validation-command grounding, and safety or boundary guidance.
4. In `apply`, keep edits bounded to the target `AGENTS.md` while repairing missing canonical sections, stale workflow guidance, or missing validation and boundary coverage.
5. Re-run the same audit to confirm post-fix status.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `schema_violations`
  - `workflow_drift_issues`
  - `validation_drift_issues`
  - `boundary_and_safety_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, toolchains, packaging surfaces, or project policy that are not grounded in the repo.
- Never edit files other than the target `AGENTS.md`.
- Preserve intentional structure and repo-specific policy when it is already coherent and grounded.
- Treat `AGENTS.md` as maintainer and agent guidance, not as public README content.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/project-agents-maintenance-automation-prompts.md`
