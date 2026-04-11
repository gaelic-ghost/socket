---
name: maintain-project-readme
description: Maintain ordinary software-project README.md files against a hard-enforced canonical base schema with deterministic check-only and bounded apply modes. Use when a project README needs a durable baseline structure that downstream plugins can extend or customize without weakening the shared README contract.
---

# Maintain Project README

Maintain ordinary software-project `README.md` files through one deterministic base-template workflow.

This skill is the general template layer for README maintenance. It defines the canonical shared README contract that downstream language-, framework-, or stack-specific plugins can adapt through explicit customization instead of ad hoc structure drift.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--readme-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `README.md`.
2. Load the canonical README schema from the built-in template config, then merge any explicit customization override.
3. In `check-only`, audit title and summary requirements, top-level section names and order, required subsection names, the required table of contents, and placeholder-style content.
4. In `apply`, keep edits bounded to the target `README.md` while normalizing the README into the configured canonical structure.
5. Preserve preamble material such as badges, callouts, screenshots, and extra intro prose before the first H2 while normalizing the structural contract around it.
6. Use the bundled README template when bootstrapping a missing `README.md` or when a downstream workflow needs a canonical starter document.
7. Re-run the same audit to confirm post-fix status.
8. If the repository is a skills or plugin repo with specialized install and discoverability conventions, use the dedicated `maintain-skills-readme` skill from `/Users/galew/Workspace/agent-plugin-skills` instead.

## Writing Expectations

- `Overview > Status` should be very short and plain: one simple statement about whether the project is just starting out, exploratory, in early development, stable enough to try, actively available, or superseded/inactive.
- `Overview > What This Project Is` should be written by the user in the user's own words.
- `Overview > Motivation` should be written by the user in the user's own words.
- `Quick Start` should stay human-focused and end-user friendly, or explicitly say the project is still too early for a real quick start and direct curious readers to `Development`.
- `Usage` should stay human-focused, concise, and informative. Prefer fenced code blocks with info strings when examples help.
- `Repo Structure` should be a small directory tree or outline diagram, not a long prose section.

## Canonical Base Contract

The authoritative default shared README structure lives in:

- `config/readme-customization.template.yaml`
- `assets/README.template.md`

Treat those two files as the source of truth for the canonical base schema and the canonical bootstrap document. Downstream plugins may extend or change that structure through explicit customization, but this base skill treats the required table of contents plus the configured section block as hard-enforced.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `customization_state`
  - `schema_contract`
  - `schema_violations`
  - `content_quality_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, setup steps, or product claims that are not grounded in the repo.
- Never edit files other than the target `README.md`.
- Keep the README schema hard-enforced against the configured contract instead of inferring structure from repo profile heuristics.
- Do not use this skill for agent-skills, Codex plugin, Claude plugin, or similar skills/plugin repositories. Use the dedicated `maintain-skills-readme` skill from `/Users/galew/Workspace/agent-plugin-skills` instead.

## References

- `agents/openai.yaml`
- `config/readme-customization.template.yaml`
- `assets/README.template.md`
- `references/section-schema.md`
- `references/readme-customization.md`
- `references/readme-config-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/verification-checklist.md`
- `references/project-readme-maintenance-automation-prompts.md`
