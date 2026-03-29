# Repo Reality Audit

This document is maintainer-only. It is the operating guide for verifying that repo docs match the code and that skill runtime resources stay self-contained.

## Source Of Truth Order

Use this order when checking any behavior claim:

1. skill `scripts/*` or the actual MCP/tool sequence
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
- After finishing milestone work, update `ROADMAP.md` in the same change unless the user explicitly asks you not to.

## Current Repo Reality

### Skill Runtime Surfaces

All active repo-authored skills live under `skills/`.

- `code-slice-explainer`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `maintain-project-readme`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`
- `maintain-project-roadmap`
  - Script: `scripts/maintain_project_roadmap.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `maintain-skills-readme`
  - Script: `scripts/maintain_skills_readme.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `project-workspace-cleaner`
  - Script: `scripts/scan_workspace_cleanup.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `things-digest-generator`
  - Script: `scripts/build_digest.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `things-reminders-manager`
  - MCP sequence is the source of truth
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`

### Maintainer Surfaces

- `AGENTS.md`
- `docs/maintainers/reality-audit.md`
- `docs/maintainers/workflow-atlas.md`

## Audit Procedure

For each skill:

1. Read the implementation source of truth.
2. Check `agents/openai.yaml` for trigger and output wording.
3. Check `SKILL.md` for inputs, workflow, output contract, and guardrails.
4. Check every referenced file for stale, orphaned, or cross-boundary guidance.
5. Confirm every referenced path exists.

Required checks:

- inputs match actual accepted flags or actual MCP/tool inputs
- workflow steps match real implementation order
- output contracts match text and JSON emitted by code
- exact phrases like `No findings.` match actual output
- blocked/error branches are documented only if they really exist
- compatibility aliases stay secondary
- trigger wording is broad enough to match the intended natural-language request shapes for the skill

## Review Rubric

Use these criteria when closing a maintainer doc or a skill runtime surface.

### Pass 1: Accurate and Current

- Trigger clarity: `SKILL.md` frontmatter and `agents/openai.yaml` describe the same capability and trigger conditions.
- Canonical naming: mode names, script names, config paths, and compatibility notes match the current repo.
- Command accuracy: every documented command, flag, and file path exists.
- Contract accuracy: documented outputs match the actual report fields, section order, or mutation result shape.
- Deprecation accuracy: compatibility paths are clearly labeled as non-canonical and redirect to the right place.
- Reference integrity: every referenced file exists and is the right source for the claim it supports.
- Trigger coverage: if a skill depends on wide natural-language activation, its references include realistic should-trigger and should-not-trigger examples.

### Pass 2: Simplified and Durable

- Single-path workflow: `SKILL.md` has one clear main path, not a menu of competing flows.
- Section consistency: prefer `Inputs`, `Workflow`, `Output Contract`, `Guardrails`, and `References`.
- Minimal primary surface: keep customization, automation templates, schemas, and examples in references unless they are first-class runtime behavior.
- Naming consistency: use the same term everywhere for the same thing.
- Input contract clarity: state required inputs, optional overrides, defaults, and config precedence without ambiguity.
- Output contract clarity: state exactly what the user gets back and when exact clean-run text such as `No findings.` is valid.
- Reference modularity: skill runtime docs stay inside the skill directory; repo-level docs stay maintainer-only.
- Deprecated-path handling: compatibility notes stay brief and never overshadow the canonical path.
- Trigger realism: frontmatter descriptions bias toward user intent and real phrasing, not only internal terminology.

## Trigger Audit Workflow

Use this when a skill depends heavily on natural-language routing.

1. Read the `SKILL.md` frontmatter description first.
2. Check `agents/openai.yaml` to confirm the UI metadata matches the same trigger surface.
3. Review the skill-local trigger-eval prompts when present.
4. Confirm the description covers:
   - direct domain terms
   - indirect natural-language asks
   - terse phrasing
   - comparison asks when comparison is part of the skill
5. If the skill is intentionally wide-trigger, prefer false-positive tolerance over missed intended activations.

### Completion Rule

Mark a surface complete only when:

- Pass 1 has no known drift against scripts, config files, current metadata, or current references.
- Pass 2 leaves one clear primary workflow and removes unnecessary duplication from the main path.

## Maintainer Conventions

Use these conventions when editing repo-maintainer guidance.

### Python execution baseline

- Use `uv run` for Python commands. In this repository, prefer the root dev baseline for maintainer workflows (`uv run --group dev pytest`, `uv run --group dev python`) unless project docs explicitly require otherwise.

### Safety defaults

- Never auto-commit changes.
- Never auto-install dependencies or tools without explicit user confirmation.
- Keep edits bounded to the requested scope.
- When blocked, report the exact blocker and the next required user action.

### Config precedence template

1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. tool/script defaults

### Output contract defaults

- Provide a short human-readable summary.
- Provide machine-readable JSON output when the workflow supports it.
- Include touched files, unresolved issues, and explicit error details.

### Relative date normalization default

- Resolve relative date terms (`today`, `tomorrow`, `next Monday`) against current local date/time first.
- Confirm scheduled dates in absolute form with timezone in user-visible output.

## Current Invariants

- `project-workspace-cleaner` reserves exact `No findings.` for complete clean runs with no skipped paths.
- `things-digest-generator` uses deterministic `Input error:` failures for missing or invalid JSON fallback inputs.
- `maintain-project-roadmap` is the canonical owner of checklist-style `ROADMAP.md` maintenance.
- `maintain-skills-readme` is the canonical owner of skills/plugin repository `README.md` maintenance.
- The repository root is the Codex plugin root, and active repo-authored skills are discovered from `skills/`.
