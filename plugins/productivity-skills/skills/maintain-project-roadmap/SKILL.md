---
name: maintain-project-roadmap
description: Maintain checklist-style ROADMAP.md files against a hard-enforced canonical base schema with deterministic check-only and bounded apply modes. Use when a project roadmap needs milestone planning, small-ticket tracking for issue-sized fixes or TODO/FIXME imports, and a durable checklist baseline that downstream plugins can extend or customize without weakening the shared roadmap contract.
---

# Maintain Project Roadmap

Maintain checklist-style `ROADMAP.md` files through one deterministic base-template workflow.

This skill is the general template layer for roadmap maintenance. It defines the canonical shared checklist-roadmap contract that downstream language-, framework-, stack-, or repository-specific customization can adapt through explicit configuration instead of ad hoc structure drift. It also owns small planning tickets that are too small or too unplanned for a milestone, so ordinary bug-fix TODOs do not need a separate `TODO.md` surface by default.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--roadmap-path <path>`
- Optional: `--config <path>`
- Optional: `--collect-source-tickets`
- Optional: `--collect-github-issues`
- Optional: `--github-repo <owner/repo>`
- Optional: `--ticket-section <Small Tickets|Backlog Candidates|Milestone N: Tickets>`
- Optional: `--ticket-text <checklist item text>`
- Optional: `--ticket-state <open|done>`
- Optional: `--ticket-source <repo-relative source>`
- Optional: `--ticket-match <existing checklist item text>`
- Optional: `--allow-duplicate`

## Workflow

1. Validate the project root and resolve the target `ROADMAP.md`.
2. Load the canonical roadmap schema from the built-in template config, then merge any explicit customization override.
3. In `check-only`, audit title requirements, top-level section names and order, the required table of contents, milestone ordering, milestone subsection names, milestone status values, milestone progress consistency, small-ticket placement, checkbox syntax, and legacy format.
4. When requested, collect small-ticket candidates from source TODO/FIXME comments or open GitHub issues and report them under `small_ticket_candidates`.
5. In `apply`, keep edits bounded to the target `ROADMAP.md` while normalizing the roadmap into the configured canonical checklist structure. If source or GitHub ticket collection was requested, append new candidates to `Small Tickets` without rewriting source files.
6. If an explicit roadmap ticket mutation was requested, add or update one checklist item in `Small Tickets`, `Backlog Candidates`, or a milestone `Tickets` subsection. Dedupe by default, and use `--allow-duplicate` only when the duplicate is intentional.
7. Preserve useful preamble material before the first H2 when normalizing the structural contract around it.
8. Use the bundled roadmap template when bootstrapping a missing `ROADMAP.md`.
9. Re-run the same audit to confirm post-fix status.

## Writing Expectations

- `Vision` should describe the long-term outcome the roadmap is meant to deliver, not restate what the project already is.
- `Product Principles` should capture a small set of planning and delivery rules that shape roadmap decisions, not general branding or philosophy.
- `Milestone Progress` should stay a concise rollup of milestone names and statuses, not a second task-management surface.
- `Milestone > Status` should be one plain allowed status value.
- `Milestone > Scope` should describe boundary and intended outcome, not duplicate the ticket list.
- `Milestone > Tickets` should be the actionable checklist for work inside the milestone.
- `Milestone > Exit Criteria` should define what must be true before the milestone counts as complete.
- `Small Tickets` should hold issue-sized fixes, TODO/FIXME imports, and cleanup work that is not substantial enough for a milestone yet. Keep these as checklist items that can be linked to GitHub issues, source comments, or milestone tickets when the evidence exists.
- `Backlog Candidates` should hold plausible future work that is not yet committed to a milestone.
- `History` should record only notable roadmap changes such as milestone additions, scope cuts, resets, or major replans.

## Codex Subagent Fit

When the user explicitly requests subagents, or applicable workflow guidance tells the agent to ask and the user grants explicit permission, use them for read-heavy roadmap discovery before the main workflow edits or reports. Good jobs include checking one milestone family per worker, comparing roadmap claims against release notes, or gathering evidence from docs and issues for backlog triage.

Keep `apply` edits in the main thread because this skill owns one target roadmap and must preserve one coherent planning structure. Ask workers for concise findings, candidate changes, and references instead of direct roadmap rewrites.

## Small Ticket Collection

- Use `--collect-source-tickets` to scan ordinary source and documentation files for TODO/FIXME comments and report candidate `Small Tickets` entries with repo-relative file and line references.
- Use `--collect-github-issues` to call `gh issue list` for open issues. Pass `--github-repo <owner/repo>` when the current checkout's GitHub remote is not the intended issue source.
- In `check-only`, collection is report-only and does not mutate files.
- In `apply`, collection appends new entries to `Small Tickets` in `ROADMAP.md`. It does not rewrite source comments yet; source comment rewrites need a separate explicit mode so code files are not changed as a side effect of roadmap normalization.

## Explicit Ticket Mutation

Use explicit ticket mutation when another agent, skill, report, or maintainer
workflow has one known checklist item to add or update in `ROADMAP.md`.

Examples:

```bash
scripts/maintain_project_roadmap.py \
  --project-root . \
  --run-mode apply \
  --ticket-section "Backlog Candidates" \
  --ticket-text "Add guarded Socket Steward roadmap apply support" \
  --ticket-source "docs/agents/socket-steward-docs-sync.md"
```

```bash
scripts/maintain_project_roadmap.py \
  --project-root . \
  --run-mode apply \
  --ticket-section "Small Tickets" \
  --ticket-text "Add guarded Socket Steward roadmap apply support" \
  --ticket-state done
```

```bash
scripts/maintain_project_roadmap.py \
  --project-root . \
  --run-mode apply \
  --ticket-section "Milestone 2: Tickets" \
  --ticket-text "Wire roadmap ticket mutation into Socket Steward apply"
```

Rules:

- Ticket mutation requires `--run-mode apply`.
- Ticket mutation requires both `--ticket-section` and `--ticket-text`.
- Supported sections are `Small Tickets`, `Backlog Candidates`, and `Milestone N: Tickets`.
- `--ticket-state open` writes `[ ]`; `--ticket-state done` writes `[x]`.
- `--ticket-source` must be repo-relative or inside the project root when passed as an absolute path.
- Existing matching checklist items are updated by default instead of duplicated.
- Use `--ticket-match` when the existing item text differs from the replacement text.
- Use `--allow-duplicate` only when an intentional duplicate checklist item is needed.

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
  - `small_ticket_candidates`
  - `apply_actions`
  - `errors`
- If there are no findings, no small-ticket candidates, no apply actions, and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent roadmap status, milestone names, or ticket details that are not grounded in the existing file or the canonical template scaffolding.
- Never edit files other than the target `ROADMAP.md`.
- Never use explicit ticket mutation as a generic prose editor; it may only add or update one checklist item per run.
- Never rewrite source TODO/FIXME comments unless a future explicit source-rewrite mode is implemented and requested.
- Keep checklist-style `ROADMAP.md` as the canonical format.
- Treat legacy table-style roadmap layouts as migration sources, not as an alternate canonical output mode.

## References

- `agents/openai.yaml`
- `config/roadmap-customization.template.yaml`
- `assets/ROADMAP.template.md`
- `references/roadmap-automation-prompts.md`
- `references/roadmap-customization.md`
- `references/roadmap-config-schema.md`
