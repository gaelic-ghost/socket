# python-skills

A plugin with some skills I use for Python stuff. Includes skills for `uv`-first bootstrapping, `pytest` unit-testing, FastAPI service setup, FastMCP scaffolding, and FastAPI/FastMCP integration guidance.

For standards and maintainer operating guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [Bundled Skill Guide](#bundled-skill-guide)
- [Platform Direction](#platform-direction)
- [Install As Skills](#install-as-skills)
- [Plugin Structure](#plugin-structure)
- [Maintainer Workflow](#maintainer-workflow)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## Bundled Skill Guide

- `bootstrap-python-mcp-service`
  - Bootstrap `uv` FastMCP projects and workspaces, plus optional OpenAPI or FastAPI mapping guidance.
- `bootstrap-python-service`
  - Bootstrap `uv` FastAPI projects and workspaces with consistent app, test, and quality-tool defaults.
- `integrate-fastapi-fastmcp`
  - Combine FastAPI and FastMCP in existing or evolving `uv` projects, including mounted MCP apps, generated MCP surfaces, and promotion from auto-generated to curated MCP design.
- `bootstrap-uv-python-workspace`
  - Create the shared `uv` package or workspace scaffolds used directly or as the basis for the higher-level bootstrap skills.
- `uv-pytest-unit-testing`
  - Standardize pytest setup, package-targeted runs, and troubleshooting for `uv` projects and workspaces.

## Platform Direction

This repository is OpenAI-first today, with the active distribution surface centered on Codex plugin packaging and Codex-specific optimizations.

The shared long-term direction across skills repositories is broader:

- keep the actual skill content portable and rooted in the open Agent Skills format
- keep OpenAI support and optimizations strong wherever they are applicable and useful
- add Claude Code support and optimizations wherever they are applicable and useful
- add vendor plugin packaging as a thin layer on top of the shared `skills/` tree instead of duplicating the skills themselves

That means root `skills/` stays canonical, while `plugins/python-skills/` is the plugin packaging root for this repository. OpenAI Codex Skills and Claude Code Plugins should remain thin vendor layers over the same skill bodies rather than separate skill trees.

## Install As Skills

OpenAI's skills docs still support direct skill installation and local discovery through standard `.agents/skills` locations:

- [OpenAI Codex Skills](https://developers.openai.com/codex/concepts/customization/#skills)
- [Where to save skills](https://developers.openai.com/codex/concepts/customization/#skills)

This repository supports that path too. The shared skills live under `./skills/`, so you can install one, several, or all of them by symlinking or copying those skill directories into a supported skill location such as `~/.agents/skills/`.

Install one skill:

```bash
mkdir -p ~/.agents/skills
ln -sfn "$PWD/skills/bootstrap-python-service" ~/.agents/skills/bootstrap-python-service
```

Install multiple named skills:

```bash
mkdir -p ~/.agents/skills
ln -sfn "$PWD/skills/bootstrap-python-service" ~/.agents/skills/bootstrap-python-service
ln -sfn "$PWD/skills/bootstrap-python-mcp-service" ~/.agents/skills/bootstrap-python-mcp-service
```

Install all shipped skills at once:

```bash
mkdir -p ~/.agents/skills
for skill_dir in "$PWD"/skills/*; do
  ln -sfn "$skill_dir" "$HOME/.agents/skills/$(basename "$skill_dir")"
done
```

Codex supports symlinked skill folders, so symlinks are a good fit while developing or iterating on this repository. If a newly installed skill does not appear right away, restart Codex.

For repo-local Codex plugin development, use the tracked plugin source root at `plugins/python-skills/` together with `.agents/plugins/marketplace.json`. For personal Codex installs, stage the plugin outside the repo at `~/.codex/plugins/python-skills` and register it in `~/.agents/plugins/marketplace.json`.

For Claude development, point the CLI at the tracked plugin source root:

```bash
claude --plugin-dir ./plugins/python-skills
```

If this repository is shared as a Claude marketplace, keep `.claude-plugin/marketplace.json` in git and keep plugin-relative paths inside that marketplace root.

## Plugin Structure

```text
.
├── README.md
├── ROADMAP.md
├── AGENTS.md
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── .claude-plugin/
│   └── marketplace.json
├── docs/
│   └── maintainers/
│       ├── reality-audit.md
│       └── workflow-atlas.md
├── .github/
│   └── scripts/
│       └── validate_repo_docs.sh
├── scripts/
│   └── validate_repo_metadata.py
├── plugins/
│   └── python-skills/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills -> ../../skills
└── skills/
    ├── bootstrap-python-mcp-service/
    ├── bootstrap-python-service/
    ├── integrate-fastapi-fastmcp/
    ├── bootstrap-uv-python-workspace/
    └── uv-pytest-unit-testing/
```

This repository ships the maintained skills under `skills/`, and root `skills/` is the canonical workflow-authoring surface.

The active packaged plugin surface lives under `plugins/python-skills/`, while shared marketplace catalogs live at `.agents/plugins/marketplace.json` for Codex and `.claude-plugin/marketplace.json` for Claude sharing.

Current scaffold defaults now include typed configuration via `pydantic-settings`, a committed `.env` for safe defaults, and an ignored `.env.local` for local or secret overrides.

## Maintainer Workflow

Keep the repo packaging and skill metadata consistent:

- Keep root `skills/` as the canonical workflow-authoring surface.
- Maintain `plugins/python-skills/.codex-plugin/plugin.json` and `plugins/python-skills/.claude-plugin/plugin.json` as the packaged plugin manifests.
- Maintain `.agents/plugins/marketplace.json` for repo-local Codex install and smoke testing.
- Maintain `.claude-plugin/marketplace.json` for repo-shared Claude marketplace wiring.
- Keep `skills/` vendor-neutral by default, and localize vendor-specific packaging to thin top-level surfaces.
- Keep direct skill install guidance accurate too; this repo supports both plugin installs and direct skill installs from the shared `skills/` tree.
- Keep bundled skills under `skills/` only; do not reintroduce a flat top-level skill layout.
- Treat each skill's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair.
- Route ongoing install, update, uninstall, verify, enable, disable, and promote workflows through `install-plugin-to-socket` rather than implying the repo-sync workflow owns those lifecycle actions.
- Track canonical plugin source trees and shared marketplace catalogs in git.
- Do not track consumer-side install copies, caches, or machine-local runtime state.
- Keep maintainer Python tooling explicit and repo-local:

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
uv run scripts/validate_repo_metadata.py
uv run pytest
```

## Notes

- Root docs are the canonical installation and discovery surface.
- Active bundled skills live under `skills/`.
- `plugins/python-skills/` is the plugin packaging root for this repository.
- `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json` are maintained shared catalogs, not generated throwaways.
- Direct skill installs remain supported from the shared `skills/` tree through the standard `.agents/skills` locations.
- OpenAI packaging is the active release surface today, and Claude packaging is kept as a thin additive surface over the same shared skills.
- Each skill’s maintained contract lives in `SKILL.md` plus `agents/openai.yaml`; per-skill `README.md` files are intentionally retired.
- Generated bootstrap projects now ship `pydantic-settings`, a committed `.env`, and an ignored `.env.local`.
- Maintainer-side validation is standardized on `uv run pytest` and `uv run scripts/validate_repo_metadata.py`.

## Keywords

Codex skills, Python skills, `uv`, FastAPI, FastMCP, pytest, FastAPI integration, MCP integration, workspace bootstrap, automation workflows, documentation alignment.

## License

Apache-2.0. See [LICENSE](./LICENSE).
