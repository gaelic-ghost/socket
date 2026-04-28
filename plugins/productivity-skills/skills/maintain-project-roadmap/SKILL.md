---
name: maintain-project-roadmap
description: Maintain checklist-style ROADMAP.md files against a hard-enforced canonical base schema with deterministic check-only and bounded apply modes. Use when a project roadmap needs a durable checklist baseline that downstream plugins can extend or customize without weakening the shared roadmap contract.
---

# Maintain Project Roadmap

Maintain checklist-style `ROADMAP.md` files through one deterministic base-template workflow.

This skill is the general template layer for roadmap maintenance. It defines the canonical shared checklist-roadmap contract that downstream language-, framework-, stack-, or repository-specific customization can adapt through explicit configuration instead of ad hoc structure drift.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--roadmap-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `ROADMAP.md`.
2. Load the canonical roadmap schema from the built-in template config, then merge any explicit customization override.
3. In `check-only`, audit title requirements, top-level section names and order, the required table of contents, milestone ordering, milestone subsection names, milestone status values, milestone progress consistency, checkbox syntax, and legacy format.
4. In `apply`, keep edits bounded to the target `ROADMAP.md` while normalizing the roadmap into the configured canonical checklist structure.
5. Preserve useful preamble material before the first H2 when normalizing the structural contract around it.
6. Use the bundled roadmap template when bootstrapping a missing `ROADMAP.md`.
7. Re-run the same audit to confirm post-fix status.

## Writing Expectations

- `Vision` should describe the long-term outcome the roadmap is meant to deliver, not restate what the project already is.
- `Product Principles` should capture a small set of planning and delivery rules that shape roadmap decisions, not general branding or philosophy.
- `Milestone Progress` should stay a concise rollup of milestone names and statuses, not a second task-management surface.
- `Milestone > Status` should be one plain allowed status value.
- `Milestone > Scope` should describe boundary and intended outcome, not duplicate the ticket list.
- `Milestone > Tickets` should be the actionable checklist for work inside the milestone.
- `Milestone > Exit Criteria` should define what must be true before the milestone counts as complete.
- `Backlog Candidates` should hold plausible future work that is not yet committed to a milestone.
- `History` should record only notable roadmap changes such as milestone additions, scope cuts, resets, or major replans.

## Codex Subagent Fit

When the user explicitly asks for subagents or parallel agent work, use subagents only for read-heavy roadmap discovery before the main workflow edits or reports. Good jobs include checking one milestone family per worker, comparing roadmap claims against release notes, or gathering evidence from docs and issues for backlog triage.

Keep `apply` edits in the main thread because this skill owns one target roadmap and must preserve one coherent planning structure. Ask workers for concise findings, candidate changes, and references instead of direct roadmap rewrites.

## Canonical Base Contract

The authoritative default shared roadmap structure lives in:

- `config/roadmap-customization.template.yaml`
- `assets/ROADMAP.template.md`

Treat those two files as the source of truth for the canonical base schema and the canonical bootstrap document. Downstream plugins may extend or change that structure through explicit customization, but this base skill treats the required table of contents plus the configured checklist roadmap section block as hard-enforced.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `customization_state`
  - `schema_contract`
  - `findings`
  - `apply_actions`
  - `errors`
- If there are no findings, no apply actions, and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent roadmap status, milestone names, or ticket details that are not grounded in the existing file or the canonical template scaffolding.
- Never edit files other than the target `ROADMAP.md`.
- Keep checklist-style `ROADMAP.md` as the canonical format.
- Treat legacy table-style roadmap layouts as migration sources, not as an alternate canonical output mode.

## References

- `agents/openai.yaml`
- `config/roadmap-customization.template.yaml`
- `assets/ROADMAP.template.md`
- `references/roadmap-automation-prompts.md`
- `references/roadmap-customization.md`
- `references/roadmap-config-schema.md`
