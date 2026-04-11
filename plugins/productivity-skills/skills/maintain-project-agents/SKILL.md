---
name: maintain-project-agents
description: Maintain ordinary project-local AGENTS.md files through deterministic audit and bounded apply modes. Use when a repository's AGENTS.md needs auditing, normalization, or bounded fixes for durable repo guidance, grounded commands, review expectations, or safety boundaries.
---

# Maintain Project Agents

Maintain ordinary project-local `AGENTS.md` files through one deterministic AGENTS workflow.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--agents-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `AGENTS.md`.
2. Load the canonical AGENTS schema from `config/agents-customization.template.yaml`, then merge any explicit override or project-local customization file.
3. In `check-only`, audit the required AGENTS sections, required subsection structure, command formatting, workflow routing guidance, and safety boundaries.
4. In `apply`, keep edits bounded to the target `AGENTS.md` while creating a missing file from the bundled template and normalizing the document to the canonical structure.
5. Re-run the same audit to confirm post-fix status.

## Canonical Base Contract

The source of truth for the base AGENTS contract lives in:

- `config/agents-customization.template.yaml`
- `assets/AGENTS.template.md`

The base contract requires:

- a top-level title and short preamble
- canonical top-level sections for repo scope, working rules, commands, review and delivery, safety boundaries, and local overrides
- required subsection structure for those sections where specific guidance needs to be easy to scan and maintain

## Writing Expectations

- Keep the file compact, practical, and repo-specific.
- `Repository Scope > Where To Look First` should route Codex toward the few highest-value files or directories, not try to summarize the whole repo.
- `Commands` should prefer fenced code blocks with language info strings for setup and validation commands.
- `Review and Delivery` should explain what good handoff looks like and what “done” means in this repo, including grounded verification and nearby updates when they matter.
- `Safety Boundaries` should stay concrete, high-signal, and easy to scan.
- `Local Overrides` should briefly explain whether more specific AGENTS files or fallback instruction files exist below this root, and make clear that closer guidance refines this root file later in the instruction chain.

## Alignment With Official Codex Guidance

The base contract is shaped to match the official Codex `AGENTS.md` guidance:

- keep repo-local guidance small and practical
- encode durable repo rules, commands, review expectations, and constraints
- add routing guidance when Codex reads too broadly
- update `AGENTS.md` when repeated mistakes or recurring review feedback reveal missing guidance
- acknowledge that more specific nested instruction files can refine the root guidance

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `schema_contract`
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
- Preserve intentional repo-specific policy when it is already coherent and grounded.
- Treat `AGENTS.md` as maintainer and agent guidance, not as public README content.
- Treat this skill as a hard-enforced base template. Downstream plugins may specialize the schema, but the base skill should not do repo-profile inference.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/agents-customization.md`
- `references/agents-config-schema.md`
- `references/project-agents-maintenance-automation-prompts.md`
