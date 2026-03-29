# python-skills

Codex plugin bundle for Python bootstrapping, testing, FastAPI service setup, and FastMCP scaffolding with `uv`-first workflows.

For standards and maintainer operating guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [What This Codex Plugin Includes](#what-this-codex-plugin-includes)
- [Bundled Skill Guide](#bundled-skill-guide)
- [Platform Direction](#platform-direction)
- [Install As Skills](#install-as-skills)
- [Plugin Structure](#plugin-structure)
- [Maintainer Workflow](#maintainer-workflow)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What This Codex Plugin Includes

This repository ships the maintained skills under `skills/` and also includes Codex plugin packaging metadata at the repo root.

Current scaffold defaults now include typed configuration via `pydantic-settings`, a committed `.env` for safe defaults, and an ignored `.env.local` for local or secret overrides.

## Bundled Skill Guide

- `bootstrap-python-mcp-service`
  - Bootstrap `uv` FastMCP projects and workspaces, plus optional OpenAPI or FastAPI mapping guidance.
- `bootstrap-python-service`
  - Bootstrap `uv` FastAPI projects and workspaces with consistent app, test, and quality-tool defaults.
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

That means `skills/` is the shared workflow surface, while `.codex-plugin/` is the current active packaging layer. Future Claude support should add Claude-specific packaging and optimizations without forking the real skill bodies unless a genuine platform-specific divergence forces it.

## Install As Skills

OpenAI's skills docs still support direct skill installation and local discovery through standard `.agents/skills` locations:

- [Agent Skills](https://developers.openai.com/codex/skills/)
- [Where to save skills](https://developers.openai.com/codex/skills/#where-to-save-skills)

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

## Plugin Structure

```text
.
├── README.md
├── ROADMAP.md
├── AGENTS.md
├── .codex-plugin/
│   └── plugin.json
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── docs/
│   └── maintainers/
│       ├── reality-audit.md
│       └── workflow-atlas.md
├── .github/
│   └── scripts/
│       └── validate_repo_docs.sh
├── scripts/
│   └── validate_repo_metadata.py
└── skills/
    ├── bootstrap-python-mcp-service/
    ├── bootstrap-python-service/
    ├── bootstrap-uv-python-workspace/
    └── uv-pytest-unit-testing/
```

## Maintainer Workflow

Keep the repo packaging and skill metadata consistent:

- Maintain `.codex-plugin/plugin.json` as the plugin distribution contract.
- Maintain `.agents/plugins/marketplace.json` for local Codex install and smoke testing.
- Keep `skills/` vendor-neutral by default, and localize vendor-specific packaging to thin top-level surfaces.
- Treat OpenAI support as the current release target, while preserving a structure that can later add Claude Code skill and plugin support cleanly.
- Keep direct skill install guidance accurate too; this repo supports both plugin installs and direct skill installs from the shared `skills/` tree.
- Keep bundled skills under `skills/` only; do not reintroduce a flat top-level skill layout.
- Treat each skill's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair.
- Run repo validation before commits:

```bash
uv run scripts/validate_repo_metadata.py
uv run pytest
```

## Notes

- Root docs are the canonical installation and discovery surface.
- Active bundled skills live under `skills/`.
- `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` are maintained surfaces, not generated throwaways.
- Direct skill installs remain supported from the shared `skills/` tree through the standard `.agents/skills` locations.
- OpenAI packaging is the active release surface today; Claude Code packaging is a planned follow-on surface, not a second live contract yet.
- Each skill’s maintained contract lives in `SKILL.md` plus `agents/openai.yaml`; per-skill `README.md` files are intentionally retired.
- Generated bootstrap projects now ship `pydantic-settings`, a committed `.env`, and an ignored `.env.local`.
- Maintainer-side validation is standardized on `uv run pytest` and `uv run scripts/validate_repo_metadata.py`.

## Keywords

Codex skills, Python skills, `uv`, FastAPI, FastMCP, pytest, workspace bootstrap, automation workflows, documentation alignment.

## License

Apache-2.0. See [LICENSE](./LICENSE).
