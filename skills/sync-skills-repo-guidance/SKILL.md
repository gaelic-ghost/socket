---
name: sync-skills-repo-guidance
description: Audit and reconcile guidance across README.md, AGENTS.md, ROADMAP.md, maintainer docs, discovery mirrors, and plugin metadata in an existing skills repository. Use when a skills repo may have stale guidance, missing plugin or discovery wiring, or outdated references to the Agent Skills standard, OpenAI Codex docs, or Claude Code docs. Defer narrow README-only or roadmap-only requests to the specialized maintainer skills.
---

# Sync Skills Repo Guidance

Audit and reconcile an existing skills repository against the current house guidance and upstream standards.

## Inputs

- Required: target repository root
- Optional: plugin name when it differs from the repository directory name
- Optional: whether the request is audit-only or audit-plus-fixes

## Workflow

1. Confirm the task is repo-wide guidance synchronization, not narrow README-only or roadmap-only maintenance.
2. Read the local repo surfaces:
   - `README.md`
   - `AGENTS.md`
   - `ROADMAP.md`
   - `docs/maintainers/reality-audit.md`
   - `docs/maintainers/workflow-atlas.md`
3. Refresh upstream guidance from the relevant official sources before making policy claims:
   - Agent Skills standard
   - OpenAI Codex Skills and Plugins docs
   - Claude Code Skills and Plugins docs
4. Run `scripts/sync_skills_repo_guidance.py` in `check-only` mode to detect local structure or wording drift.
5. Apply bounded fixes to repo docs, manifests, and symlink mirrors when the request includes changes.
6. Re-run the same audit to confirm remaining findings.
7. Record any upstream-docs findings with dates when behavior appears changed or ambiguous.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
  - `findings`
  - `errors`
- If there are no findings and no errors, output exactly `No findings.`

## Guardrails

- Never use this skill for ordinary software-project repos.
- Never replace specialized README-only or roadmap-only maintenance skills when the request is narrow.
- Never claim upstream guidance is timeless. Date the audit when official docs were consulted.
- Never flatten repo-specific maintainer policy while syncing missing shared guidance.

## References

- `references/sync-checklist.md`
- `references/source-order.md`
