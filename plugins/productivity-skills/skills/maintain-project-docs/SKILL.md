---
name: maintain-project-docs
description: Coordinate project documentation maintenance across README.md, CONTRIBUTING.md, AGENTS.md, ACCESSIBILITY.md, and ROADMAP.md by delegating to the owner document skills and auditing cross-document responsibility drift. Use when a repo needs a complete docs sweep, doc-boundary audit, repeated-content cleanup, or a single umbrella pass over project-maintenance documentation.
---

# Maintain Project Docs

Coordinate a complete project-docs sweep without collapsing the document-specific skills into one oversized workflow.

This skill is the umbrella layer for repository documentation maintenance. It delegates canonical file audits and bounded edits to the owner skills, then checks whether content responsibilities are drifting across files.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--include <readme,contributing,agents,accessibility,roadmap>`
- Optional: `--skip <readme,contributing,agents,accessibility,roadmap>`
- Optional: `--collect-source-tickets`
- Optional: `--collect-github-issues`
- Optional: `--github-repo <owner/repo>`

## Workflow

1. Validate the project root and choose the included document workflows.
2. Run the owner workflows serially in this order: README, CONTRIBUTING, AGENTS, ACCESSIBILITY, ROADMAP.
3. Pass `--collect-source-tickets`, `--collect-github-issues`, and `--github-repo` only to the roadmap workflow.
4. In `check-only`, report each owner workflow's findings plus cross-document responsibility issues.
5. In `apply`, let each owner workflow make only its own bounded file edits, then audit the resulting document set again.
6. Keep any cross-document moves, wording rewrites, or repeated-content cleanup in the main thread unless a future deterministic fixer owns those edits.

## Responsibility Boundaries

- `README.md`: product overview, status, quick start, usage, and short development pointer.
- `CONTRIBUTING.md`: human contributor workflow, setup, development expectations, PR expectations, and communication rules.
- `AGENTS.md`: durable agent-facing repo scope, routing, commands, review and delivery rules, and safety boundaries.
- `ACCESSIBILITY.md`: accessibility standards, architecture expectations, known gaps, support paths, and verification evidence.
- `ROADMAP.md`: milestones, small tickets, TODO/FIXME imports, backlog planning, and notable roadmap history.

When content belongs in another file, report the mismatch instead of copying or rewriting it silently.

## Codex Subagent Fit

When the user explicitly requests subagents, `repo-docs-auditor`, review-packet planning, or asks to keep working while broad repo-doc discovery happens in parallel, use the `repo-docs-auditor` custom-agent role for bounded read-heavy discovery before this skill coordinates owner docs workflows. Good jobs include checking docs for stale commands, comparing roadmap claims against repo evidence, inventorying nested `AGENTS.md` overrides, and finding cross-document responsibility drift.

Keep `apply` edits in the main thread. The auditor may return proposed patch-set entries, but the main agent should review them with the user before saving, editing, or applying any documentation edits.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `document_order`
  - `document_reports`
  - `responsibility_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent project claims, commands, accessibility evidence, roadmap scope, or agent policy.
- Never make broad cross-file rewrites as a side effect of running the umbrella workflow.
- Do not duplicate detailed rules across README, CONTRIBUTING, AGENTS, ACCESSIBILITY, and ROADMAP just to make each file self-contained.
- Treat this skill as an orchestrator. The owner document skills keep their own schemas, templates, and bounded apply behavior.

## References

- `agents/openai.yaml`
- `references/document-boundaries.md`
- `references/project-docs-maintenance-automation-prompts.md`
- `scripts/maintain_project_docs.py`
