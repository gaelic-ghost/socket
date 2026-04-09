---
name: sync-skills-repo-guidance
description: Audit and reconcile guidance across README.md, AGENTS.md, ROADMAP.md, maintainer docs, discovery mirrors, and plugin metadata in an existing skills repository. Use when a skills repo may have stale guidance, missing plugin or discovery wiring, or outdated references to the Agent Skills standard, OpenAI Codex docs, or Claude Code docs. Defer narrow README-only or roadmap-only requests to the specialized maintainer skills.
---

# Sync Skills Repo Guidance

Audit and reconcile an existing skills repository against the current house guidance and upstream standards.

Current scope note:

- This skill currently owns ongoing guidance alignment for this repo pattern.
- The script-backed audit is narrower than the full maintainer workflow.
- Today, the script checks local guidance snippets and discovery mirrors, while broader docs-link review, wording updates, and cross-doc reconciliation remain maintainer-driven.

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
4. Run `scripts/sync_skills_repo_guidance.py` in `check-only` mode to detect current local guidance-snippet and symlink drift.
5. Interpret that audit together with the current repo docs and any upstream guidance reviewed in step 3.
6. Keep Codex install guidance consistent across repo docs:
   - repo-local packaged plugin surface: `plugins/<plugin-name>/`
   - repo-local marketplace: `.agents/plugins/marketplace.json`
   - personal installs live outside the repo at `~/.codex/plugins/<plugin-name>` with `~/.agents/plugins/marketplace.json`
7. Keep Claude guidance consistent across repo docs:
   - local Claude development should point `claude --plugin-dir` at the tracked plugin source root
   - if the repo itself is shareable as a Claude marketplace, it should track `.claude-plugin/marketplace.json` at the repo root
   - Claude marketplace relative paths must stay inside the marketplace root
8. Keep git-tracking guidance consistent across repo docs:
   - canonical plugin source trees and shared marketplace catalogs belong in git
   - install copies, caches, and local-only runtime state do not
   - the shared `.gitignore` snippet for local runtime state is present unless stricter ignores already cover it
9. Make repo guidance explicit about which workflow owns what:
   - bootstrap and sync own repo-local structure and guidance
   - `install-plugin-to-socket` owns local Codex install lifecycle work such as install, update, uninstall, verify, enable, disable, and promote
10. Apply bounded maintainer fixes to repo docs and related guidance surfaces when the request includes changes.
11. Ensure repo-level maintainer Python guidance stays explicit about `uv sync --dev`, `uv tool install ruff`, `uv tool install mypy`, and `uv run --group dev pytest` where that baseline is documented.
12. Re-run the same audit to confirm remaining findings.
13. Record any upstream-docs findings with dates when behavior appears changed or ambiguous.

## Output Contract

- Return a short summary plus JSON with:
  - `run_context`
  - `findings`
  - `errors`
- If there are no findings and no errors, output exactly `No findings.`

## Guardrails

- Never use this skill for ordinary software-project repos.
- Never replace specialized `maintain-plugin-docs` work when the request is narrow and docs-focused.
- Never claim upstream guidance is timeless. Date the audit when official docs were consulted.
- Never flatten repo-specific maintainer policy while syncing missing shared guidance.
- Never describe the current script as if it already performs full repo-wide remediation, plugin-metadata drift repair, or automated upstream-doc intake.

## References

- `references/sync-checklist.md`
- `references/source-order.md`
