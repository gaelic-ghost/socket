---
name: maintain-project-contributing
description: Maintain canonical CONTRIBUTING.md files for ordinary software projects through deterministic audit and bounded apply modes. Use when a project contribution guide needs auditing, normalization, or bounded fixes for contributor workflow, local setup, development expectations, review handoff, or communication guidance.
---

# Maintain Project Contributing

Maintain canonical `CONTRIBUTING.md` files for ordinary software projects through one deterministic contribution-guide workflow.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--contributing-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `CONTRIBUTING.md`.
2. Load the canonical contributing-guide schema from `config/contributing-customization.template.yaml`, then merge any explicit override or project-local customization file.
3. In `check-only`, audit the required section schema, required subsection schema, required table of contents, placeholder content, and verification-command formatting.
4. In `apply`, keep edits bounded to the target `CONTRIBUTING.md` while creating a missing file from the bundled template and normalizing the document to the canonical structure.
5. Re-run the same audit to confirm post-fix status.

## Canonical Base Contract

The source of truth for the base contributing-guide contract lives in:

- `config/contributing-customization.template.yaml`
- `assets/CONTRIBUTING.template.md`

The base contract requires:

- a top-level title and short summary
- a required `## Table of Contents`
- canonical top-level sections for overview, workflow, setup, development expectations, PR expectations, communication, and contribution terms
- required subsection structure for `Overview`, `Contribution Workflow`, `Local Setup`, and `Development Expectations`

## Writing Expectations

- `Overview > Who This Guide Is For` should stay short and plainly explain who this guide serves.
- `Overview > Before You Start` should call out the most important prerequisites before someone begins work.
- `Contribution Workflow` should describe how contributors choose work, make changes, and ask for review without drifting into repo history or product overview prose.
- `Local Setup > Runtime Config` should be explicit about config files, env vars, secrets, and local services.
- `Local Setup > Runtime Behavior` should explain what needs to be running locally and how contributors can tell the project is actually working.
- `Development Expectations > Verification` should prefer fenced code blocks with language info strings when commands help contributors validate changes.
- `Communication` should stay practical and concise, focused on how contributors surface uncertainty or larger-scope questions.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `schema_contract`
  - `schema_violations`
  - `command_integrity_issues`
  - `content_quality_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, setup steps, environment variables, branch rules, review policies, or contribution terms that are not grounded in the repo.
- Never edit files other than the target `CONTRIBUTING.md`.
- Keep `CONTRIBUTING.md` as the canonical contribution-guide filename for this skill.
- Treat this skill as a hard-enforced base template. Downstream plugins may specialize the schema, but the base skill should not do repo-profile inference.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/contributing-customization.md`
- `references/contributing-config-schema.md`
- `references/project-contributing-maintenance-automation-prompts.md`
