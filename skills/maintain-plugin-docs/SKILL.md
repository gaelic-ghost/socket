---
name: maintain-plugin-docs
description: Maintain docs for agent-skills, Codex plugin, Claude Code plugin, and similar agent-plugin repositories through deterministic audits and bounded fixes. Use when a stack-specific plugin or skills repo needs README or roadmap maintenance. Do not use this for ordinary software project docs.
---

# Maintain Plugin Docs

Maintain specialized docs for skills and plugin repositories through one deterministic docs workflow.

Current scope note:

- This is the stack-specific docs-maintenance entrypoint for this repo family.
- It is meant to be installed repo-locally into a plugin-development repository and used there by Gale, another coding agent, or an automation-oriented subagent.
- The intended long-term scope combines the README-oriented behavior from the old `maintain-skills-readme` skill with the checklist-style roadmap maintenance shape from `maintain-project-roadmap`.
- The current implementation supports `README.md`, `ROADMAP.md`, and combined docs passes through explicit scope selection.
- For install guidance in this repo family, Codex Plugin and Claude Code Plugin installation should be treated as the primary path. Individual and `--all` installs via the Vercel `skills` CLI are the secondary path.

## Inputs

- Required: `--workspace <path>`
- Optional: `--repo-glob <glob>`
- Optional: `--doc-scope <readme|roadmap|all>`
- Optional: repeatable `--exclude <path>`
- Optional: `--apply-fixes`
- Treat `maintain_skills_readme` and `skills_readme_alignment` as compatibility-only when handling legacy prompts.

## Workflow

1. Validate the workspace path and discover matching repositories.
2. Run the read-only audit first.
3. In `readme` scope, check README structure, plugin and skills install guidance, skill inventory wording, and repo discoverability rules.
4. In `roadmap` scope, validate checklist-style `ROADMAP.md` structure, milestone ordering, checkbox syntax, and legacy-format migration needs.
5. In `all` scope, run both audits and report cross-doc consistency findings together.
6. Treat plugin-level install guidance for Codex Plugin and Claude Code Plugin as the primary install surface when describing or evolving this repo pattern.
7. Treat Vercel `skills` CLI per-skill and `--all` installs as the secondary install surface.
8. If the user requested edits, apply bounded fixes with `--apply-fixes`.
9. Re-run the same audit to confirm remaining issues.
10. Return the Markdown plus JSON report shape.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `repos_scanned`
  - `profile_assignments`
  - `readme_findings`
  - `roadmap_findings`
  - `cross_doc_findings`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never edit source code, manifests, lockfiles, or CI files.
- Keep edits bounded to `README.md`, `ROADMAP.md`, and explicitly approved snippet insertions into `AGENTS.md`.
- Do not use this skill for ordinary software project docs. Use `maintain-project-readme` or `maintain-project-roadmap` instead.
- Leave repo-wide policy reconciliation, broad maintainer-doc alignment, and packaging-surface drift beyond docs wording to `sync-skills-repo-guidance`.

## References

- `references/output-contract.md`
- `references/plugin-docs-maintenance-automation-prompts.md`
- `references/profile-model.md`
- `references/section-schema.md`
- `references/discoverability-rules.md`
- `references/fix-policies.md`
