# Reality Audit Guide

Use this guide when reconciling repository documentation with the actual shipped top-level export surface, local scripts, and tests.

## Source-of-Truth Order

Use the highest-confidence artifact first and only fall back when the higher layer is silent.

Root `skills/` is the canonical workflow-authoring surface.

1. Runtime behavior proven by tests under `tests/`
2. Active shipped skill assets under `skills/<skill>/`
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/`
   - `scripts/`
2.5. Shared repo-maintenance behavior from `productivity-skills/skills/maintain-project-repo/`
   - `productivity-skills` owns the reusable `maintain-project-repo` toolkit contract
   - this repository's Apple bootstrap and guidance-sync flows call that sibling skill with the `swift-package` or `xcode-app` profile
   - this repository owns only the Apple-specific profile selection and Xcode MCP registration contract
2.6. Packaged plugin metadata under `.codex-plugin/plugin.json` and `.mcp.json`
   - `.codex-plugin/plugin.json` is the Codex plugin entrypoint
   - `.mcp.json` registers Xcode's built-in `xcrun mcpbridge` server for external Codex sessions
   - the Xcode MCP server remains Xcode-owned; this repo does not bundle a separate Xcode MCP server package
3. Repository validation rules in `.github/scripts/validate_repo_docs.sh`
4. Root maintainer and discoverability docs
   - `README.md`
   - `AGENTS.md`
   - `ROADMAP.md`
   - `docs/maintainers/`
   - especially `execution-split-and-inference-plan.md` when validating compatibility surfaces and guidance-preservation rules

Deprecated compatibility skills that remain on disk do not count as part of the active public skill surface unless the validator and root docs explicitly say otherwise.

## Audit Procedure

1. Confirm the active public skill surface from `.github/scripts/validate_repo_docs.sh` and the matching sections in `README.md` and `docs/maintainers/workflow-atlas.md`.
2. Check each active skill for the documented contract:
   - required headings in `SKILL.md`
   - `agents/openai.yaml`
   - `references/customization.template.yaml`
   - `references/`
   - the skill-appropriate local snippet copy under `references/snippets/`
3. Check export-surface docs for drift:
   - root `skills/` still define the canonical workflow behavior
   - docs do not reintroduce a nested packaged plugin tree or any other second export surface under `plugins/`
   - docs do not tell maintainers to use removed installer or install-validator skills
   - docs describe top-level `skills/` as the active export surface today, with top-level `mcps/` or `apps/` only if those directories are added later
4. Run `bash .github/scripts/validate_repo_docs.sh` and treat failures as documentation-contract drift unless code assets prove otherwise.
   - for repo-maintenance drift inside this repo, compare Apple behavior against `productivity-skills/skills/maintain-project-repo/`
   - when intentionally syncing ideas from another repo, reconcile them into `maintain-project-repo` first, then keep this repo limited to Apple guidance and profile selection
   - for Xcode MCP drift, compare the plugin metadata against Apple's documented `codex mcp add xcode -- xcrun mcpbridge` setup
5. Run `uv run --group dev pytest` and treat failures as runtime drift.
6. Reconcile root docs to the tested, shipped state instead of preserving stale historical wording.
7. Update `ROADMAP.md` in the same change when milestone or status text is no longer truthful.

## Local Discovery Smoke Test Flow

Use this flow when validating the current top-level export surface and local discovery mirrors instead of checking a nested packaged plugin tree.

1. Run `bash .github/scripts/validate_repo_docs.sh`.
2. Run `uv run --group dev pytest`.
3. Confirm `.agents/skills` and `.claude/skills` still point at `../skills`.
4. Confirm root docs, skill docs, and the roadmap all describe top-level `skills/` as the active export surface and do not mention a nested packaged plugin tree or removed installer workflows.
5. If discovery or docs drift remains, update the docs to match the tested top-level export surface instead of preserving stale packaging language.

## Durable Review Criteria

- Root docs should say plainly that `productivity-skills` remains the default baseline layer for general repo-doc and maintenance work, while this repo is the Apple-specific specialization layer.
- Root docs must describe the same active skill surface.
- Root docs must describe the current top-level export shape without treating deleted nested packaging experiments as active.
- Codex plugin docs must describe Xcode MCP registration as Xcode-owned `xcrun mcpbridge` wiring, not as a bundled third-party server package.
- Maintainer-doc links in root docs must resolve on disk.
- Validation rules must check the canonical maintainer-doc paths, not legacy locations.
- Historical notes may mention retired or deprecated skills only in migration context.
- Maintainer docs must not imply that repo-root files are required when the canonical files live under `docs/maintainers/`.
- Docs and skill guidance must not mention removed installer or install-validator skills as if they still exist.
- Maintainer Python tooling guidance should stay explicit about repo-local `pyproject.toml` dev dependencies and `uv run` commands for tools such as `pytest`, `ruff`, and `mypy`, rather than relying on machine-global installs.

## Current Canonical Maintainer Docs

- Workflow diagrams and UX maps: `docs/maintainers/workflow-atlas.md`
- Audit procedure and source-of-truth order: `docs/maintainers/reality-audit.md`
- Customization-surface decision and follow-up plan: `docs/maintainers/customization-consolidation-review.md`
- Execution-skill split, inference plan, and guidance-preservation contract: `docs/maintainers/execution-split-and-inference-plan.md`
- Historical milestone planning decisions that no longer need standalone docs should live in `ROADMAP.md` under the milestone body or `History`.

## Reporting Shape

A maintainer audit report should summarize:

- documentation drift found
- validation health
- test health
- roadmap credibility or staleness
- top-level export-surface guidance health
- remaining follow-up items
