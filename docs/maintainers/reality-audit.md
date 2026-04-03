# Repo Reality Audit

This document is maintainer-only. It is the operating guide for verifying that repo docs match the code and that skill runtime resources stay self-contained.

## Source Of Truth Order

Use this order when checking any behavior claim:

1. skill `scripts/*` or the actual MCP or tool sequence
2. skill `agents/openai.yaml`
3. skill `SKILL.md`
4. skill-local `references/*`
5. repo-level maintainer docs in `docs/maintainers/*`

If two layers disagree, fix the lower-trust layer or narrow its claims.

## Audience Boundaries

- `README.md` is user-facing only.
- `AGENTS.md` is repo-maintainer guidance only.
- Installed skills must be understandable from their own directories.
- Skill runtime docs must not depend on `../docs/...`.
- Repo-level maintainer docs may describe patterns and audits, but they are not part of installed skill operation.

## Roadmap Accuracy Rule

- Do not present `ROADMAP.md` as authoritative if you have evidence it is behind completed repo work.
- When asked to report roadmap status, reconcile `ROADMAP.md` first or explicitly state that it is stale before summarizing it.
- After finishing milestone work, update `ROADMAP.md` in the same change unless explicitly asked not to.

## Current Repo Reality

### Skill Runtime Surfaces

All active repo-authored skills live under `skills/`.

- `bootstrap-skills-plugin-repo`
  - Script: `scripts/bootstrap_skills_plugin_repo.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `maintain-skills-readme`
  - Script: `scripts/maintain_skills_readme.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `sync-skills-repo-guidance`
  - Script: `scripts/sync_skills_repo_guidance.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`

### Packaging Surfaces

- `plugins/agent-plugin-skills/.codex-plugin/plugin.json`
- `plugins/agent-plugin-skills/.claude-plugin/plugin.json`
- `plugins/agent-plugin-skills/skills`
- `plugins/agent-plugin-skills/hooks/hooks.json`
- `.agents/skills`
- `.claude/skills`
- `.agents/plugins/marketplace.json`

### Maintainer Surfaces

- `AGENTS.md`
- `docs/maintainers/reality-audit.md`
- `docs/maintainers/workflow-atlas.md`
- `ROADMAP.md`

## Audit Procedure

For each skill:

1. Read the implementation source of truth.
2. Check `agents/openai.yaml` for trigger and output wording.
3. Check `SKILL.md` for inputs, workflow, output contract, and guardrails.
4. Check every referenced file for stale, orphaned, or cross-boundary guidance.
5. Confirm every referenced path exists.

Required checks:

- inputs match actual accepted flags or actual MCP or tool inputs
- workflow steps match real implementation order
- output contracts match text and JSON emitted by code
- exact phrases like `No findings.` match actual output
- trigger wording is broad enough to match intended natural-language request shapes
- packaging docs distinguish canonical authored surfaces from symlink mirrors and plugin metadata

## Current Invariants

- `bootstrap-skills-plugin-repo` reserves exact `No findings.` for complete clean runs with no remaining findings, apply actions, or errors.
- `maintain-skills-readme` and `sync-skills-repo-guidance` reserve exact `No findings.` for clean runs that finish without remaining issues or errors.
- `maintain-skills-readme` is currently the canonical owner of README-only maintenance for skills and plugin repositories.
- `bootstrap-skills-plugin-repo` is the canonical owner of repo bootstrap and structural alignment for this repo pattern.
- `sync-skills-repo-guidance` is the canonical owner of repo-wide guidance synchronization for this repo pattern.
- Root `skills/` is the canonical workflow-authoring surface.
- `plugins/agent-plugin-skills/` is the plugin packaging root for Codex and Claude scaffolding.
- `.agents/skills` and `.claude/skills` are POSIX symlink mirrors into root `skills/`.
- `plugins/agent-plugin-skills/skills` is a POSIX symlink mirror into root `skills/`.
- `.agents/plugins/marketplace.json` points local Codex plugin discovery at `plugins/agent-plugin-skills/`.
