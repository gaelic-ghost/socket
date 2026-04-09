# AGENTS.md

## Repository Policy

- This repository is the source of truth for skill development.
- Do all skill authoring, refactoring, testing, and maintenance only in this repository.
- Treat managed production skills at `~/.agents/skills` as read-only deployment artifacts.
- Never edit files under `~/.agents/skills` directly; make changes here and promote through the normal sync/release flow.

## Durable Skill Customization

- Global durable customization path for shipped skills: `~/.config/gaelic-ghost/python-skills/<skill-name>/customization.yaml`.
- Repo-local override path: `.codex/profiles/<skill-name>/customization.yaml`.
- Repo-local override files are user-local and must remain untracked.
- Built-in script defaults remain canonical fallback when no profile exists or when bypass flags are used.

## Maintainer Defaults

- Keep the active public surface limited to the five bundled skills shipped under `skills/` in this repository's plugin root.
- Treat the root `README.md` as the canonical install and discovery surface for the repository.
- Treat root `skills/` as the canonical workflow-authoring surface.
- Treat `plugins/python-skills/` as the plugin packaging root for this repository.
- Treat `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json` as the canonical shared local marketplace catalogs for this repository.
- Keep `skills/` as the shared, vendor-neutral workflow surface wherever practical. Prefer thin vendor packaging layers over duplicated skill trees.
- Keep direct skill install guidance accurate as a first-class supported path alongside plugin installation. Users should be able to install one skill, multiple skills, or all shipped skills from the shared `skills/` tree.
- Treat each skill's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair.
- When building or updating skills in this repository, always use every applicable field, option, and feature from the open Agent Skills standard and the OpenAI Codex skill extensions. Treat "applicable" as "materially useful and accurate for the shipped skill", not as permission to add decorative or misleading metadata.
- OpenAI support and optimizations are required wherever they are applicable and useful in this repository's current release surface.
- Claude Code support and optimizations should be added as thin additive layers instead of forking or duplicating the core `skills/` content.
- Do not introduce a generalized cross-platform compatibility framework, wrapper layer, or packaging abstraction unless the simpler shared-skills-plus-thin-vendor-layers structure has clearly failed. Such a new layer would add real complexity and should be treated with strong caution and extra review.
- Do not reintroduce per-skill `README.md` files as maintained public docs unless a later repo decision explicitly restores that surface.
- Track canonical plugin source trees and shared marketplace catalogs in git.
- Do not track consumer-side install copies, caches, or machine-local runtime state such as `.codex/plugins/` and `.claude/settings.local.json`.
- Keep maintainer Python tooling explicit through uv-managed tools, including `uv sync --dev`, `uv tool install ruff`, `uv tool install mypy`, and validation runs from `uv`.
- Run repo validation with `uv run scripts/validate_repo_metadata.py` and `uv run pytest` before committing documentation or metadata changes.
