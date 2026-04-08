---
name: maintain-plugin-repo
description: Maintain plugin-development repositories through one audit-first, repo-level orchestrator that classifies packaging, docs, and local install drift, routes bounded fixes to the existing specialist skills, and returns one combined maintainer report. Use when a skills or plugin repo feels drifted overall and a maintainer wants one entrypoint instead of manually coordinating multiple specialist skills.
---

# Maintain Plugin Repo

Maintain a plugin-development repository through one audit-first, repo-level workflow.

Current scope note:

- This skill is the repo-level maintainer orchestrator for this repo family.
- It does not replace the existing specialists.
- It coordinates:
  - `validate-plugin-install-surfaces` for audit-only packaging and install-surface drift
  - `maintain-plugin-docs` for README and ROADMAP maintenance
  - `install-plugin-to-socket` for bounded local Codex install-surface repair when explicit install inputs are provided
- Version 1 stays conservative by design:
  - audit first
  - docs fixes in apply mode
  - optional install-surface repair only when the maintainer explicitly provides the local plugin install inputs
  - no direct manifest rewriting beyond what the specialist scripts already support

## Inputs

- Required: `--repo-root <path>`
- Optional: `--plugin-name <name>`
- Optional: `--workflow <audit-only|apply-safe-fixes>`
  - default: `audit-only`
- Optional: `--doc-scope <readme|roadmap|all>`
  - default: `all`
- Optional: `--source-plugin-root <path>`
  - required only when local install repair should be orchestrated
- Optional: `--install-scope <personal|repo>`
  - default: `repo`
- Optional: `--target-repo-root <path>`
  - default: same as `--repo-root`
- Optional: `--install-mode <copy|symlink>`
  - default: `copy`
- Optional: `--apply-install-repairs`
- Optional: `--print-md`
- Optional: `--print-json`
- Optional: `--fail-on-issues`

## Workflow

1. Confirm the request is overall plugin-repo maintenance, not a narrow docs-only, bootstrap-only, or install-only task.
2. Run the install-surface validator first through `scripts/maintain_plugin_repo.py`.
3. Run the docs maintainer audit for the same repository.
4. Classify findings by owner:
   - validator findings stay attributed to `validate-plugin-install-surfaces`
   - README and ROADMAP findings stay attributed to `maintain-plugin-docs`
   - local install-lifecycle repair stays attributed to `install-plugin-to-socket`
5. In `audit-only` mode:
   - stop after classification
   - return the grouped repo-health report
6. In `apply-safe-fixes` mode:
   - apply docs fixes through `maintain-plugin-docs`
   - only attempt local install repair when `--apply-install-repairs` and the explicit install inputs were provided
   - treat missing install inputs as deferred work, not as permission to guess
7. Re-run the validator after apply behavior so the final report reflects the current repo state.
8. Keep install-surface repair bounded:
   - do not invent broader package or manifest surgery
   - do not claim to fix everything automatically
9. Return one combined report with fixes applied, deferred work, unresolved findings, and owner assignments.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `repo_root`
  - `workflow`
  - `owner_assignments`
  - `validation_findings`
  - `docs_findings`
  - `install_findings`
  - `fixes_applied`
  - `deferred_findings`
  - `post_fix_status`
  - `errors`
- If there are no findings, no deferred work, no fixes applied, and no errors, output exactly `No findings.`

## Guardrails

- Never replace `bootstrap-skills-plugin-repo` for first-time repo creation or structural bootstrap.
- Never replace `maintain-plugin-docs` for narrow docs-only maintenance requests.
- Never replace `install-plugin-to-socket` for narrow local install lifecycle work.
- Never pretend local install repair can proceed safely without an explicit `--source-plugin-root`.
- Never silently widen apply mode into arbitrary manifest or source edits.
- Never flatten owner boundaries in the final report. Preserve which specialist owns which finding class.

## References

- `references/owner-routing.md`
- `references/output-contract.md`
