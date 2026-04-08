# Reality Audit Guide

Use this guide when reconciling repository documentation with the actual shipped skill surface, local scripts, and tests.

## Source-of-Truth Order

Use the highest-confidence artifact first and only fall back when the higher layer is silent.

Root `skills/` is the canonical workflow-authoring surface.

1. Runtime behavior proven by tests under `tests/`
2. Active shipped skill assets under `skills/<skill>/`
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/`
   - `scripts/`
2.5. Vendored shared maintainer-toolkit snapshot under `shared/repo-maintenance-toolkit/` for Apple bootstrap and guidance-sync integrations
3. Plugin packaging metadata under the plugin packaging root `plugins/apple-dev-skills/`, `.agents/plugins/marketplace.json`, and `.claude-plugin/marketplace.json`
   - `.codex-plugin/plugin.json`
   - `.claude-plugin/plugin.json`
   - plugin-only packaging directories such as `hooks/`, `bin/`, and `assets/`
   - documented local install flow for `plugins/apple-dev-skills/`
4. Repository validation rules in `.github/scripts/validate_repo_docs.sh`
5. Root maintainer and discoverability docs
   - `README.md`
   - `AGENTS.md`
   - `ROADMAP.md`
   - `docs/maintainers/`

Deprecated compatibility skills that remain on disk do not count as part of the active public skill surface unless the validator and root docs explicitly say otherwise.

## Audit Procedure

1. Confirm the active public skill surface from `.github/scripts/validate_repo_docs.sh` and the matching sections in `README.md` and `docs/maintainers/workflow-atlas.md`.
2. Check each active skill for the documented contract:
   - required headings in `SKILL.md`
   - `agents/openai.yaml`
   - `references/customization.template.yaml`
   - `references/`
   - the skill-appropriate local snippet copy under `references/snippets/`
3. Check plugin packaging metadata for drift:
   - root `skills/` still define the canonical workflow behavior
   - Codex plugin metadata does not claim unsupported plugin capabilities
   - Claude-only extras remain optional and clearly separated
   - repo-root `.claude-plugin/marketplace.json` still points at the tracked in-repo plugin root
   - local install guidance still points at `plugins/apple-dev-skills/` and keeps the official marketplace-based plugin install path canonical
4. Run `bash .github/scripts/validate_repo_docs.sh` and treat failures as documentation-contract drift unless code assets prove otherwise.
   - for repo-maintenance toolkit drift, compare the Apple skill copies against `shared/repo-maintenance-toolkit/`, not against an active top-level skill directory in this repo
5. Run `uv run --group dev pytest` and treat failures as runtime drift.
6. Reconcile root docs to the tested, shipped state instead of preserving stale historical wording.
7. Update `ROADMAP.md` in the same change when milestone or status text is no longer truthful.

## Durable Review Criteria

- Root docs must describe the same active skill surface.
- Root docs must describe the current plugin packaging shape without treating plugin wrappers as the workflow source of truth.
- Root docs must distinguish repo-local Codex packaging, personal Codex installs, and Git-backed Claude marketplace sharing.
- Maintainer-doc links in root docs must resolve on disk.
- Validation rules must check the canonical maintainer-doc paths, not legacy locations.
- Historical notes may mention retired or deprecated skills only in migration context.
- Maintainer docs must not imply that repo-root files are required when the canonical files live under `docs/maintainers/`.
- Plugin docs must keep the Codex common denominator and Claude-only extras explicit.
- Local install docs must name the packaged plugin root and the supported automated wiring path.
- Maintainer Python tooling guidance should stay explicit about `uv tool install` for optional tools such as `ruff` and `mypy`.

## Current Canonical Maintainer Docs

- Workflow diagrams and UX maps: `docs/maintainers/workflow-atlas.md`
- Audit procedure and source-of-truth order: `docs/maintainers/reality-audit.md`
- Customization-surface decision and follow-up plan: `docs/maintainers/customization-consolidation-review.md`
- Execution-skill split, inference plan, and guidance-preservation contract: `docs/maintainers/execution-split-and-inference-plan.md`

## Reporting Shape

A maintainer audit report should summarize:

- documentation drift found
- validation health
- test health
- roadmap credibility or staleness
- local plugin install guidance health
- remaining follow-up items
