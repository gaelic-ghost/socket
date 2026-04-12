# Reality Audit Guide

## Purpose

Use this audit when changing root docs, skill contracts, scripts, references, or metadata. The goal is to keep the shipped repo surface aligned with what the skills actually do.

## Root Doc Audit

Check that:

- `README.md` uses the canonical `*-skills` section schema
- `README.md` presents root `skills/` as the canonical workflow-authoring surface
- `README.md` presents the repo as a shared authored skill surface with thin packaging rooted under `plugins/python-skills/`
- `README.md` names `plugins/python-skills/` as the plugin packaging root
- `README.md` states plainly that `productivity-skills` is the default baseline layer for general repo-doc and maintenance work, while this repo is the Python-specific specialization layer
- `README.md` includes accurate direct skill install guidance from the shared `skills/` tree as well as plugin install guidance
- `README.md` distinguishes repo-local plugin development from personal installs under `~/.codex/plugins/python-skills`
- `README.md` documents local Claude development through `claude --plugin-dir ./plugins/python-skills`
- the active skill inventory matches the actual `skills/*/SKILL.md` directories
- the repository layout snippet matches the real repo
- `plugins/python-skills/.codex-plugin/plugin.json` exists and points at `./skills/`
- `plugins/python-skills/.claude-plugin/plugin.json` exists
- `.agents/plugins/marketplace.json` exists and points at the packaged plugin root
- `.claude-plugin/marketplace.json` exists and points at the packaged plugin root
- `.agents/skills`, `.claude/skills`, and `plugins/python-skills/skills` are the expected POSIX mirrors
- `ROADMAP.md` uses checklist-style sections and milestone progress

## Skill Contract Audit

For each skill directory:

- frontmatter `name` matches the directory name
- frontmatter includes the repo-required open-standard fields: `license`, `compatibility`, `metadata`, and `allowed-tools`
- `SKILL.md` describes the actual entrypoint and supported modes
- every referenced file under `scripts/`, `references/`, `assets/`, and `agents/` exists
- runtime defaults in docs match the scripts
- fallback or handoff guidance reflects the real current surface

## Metadata Audit

For each `agents/openai.yaml`:

- `display_name` is readable and stable
- `short_description` matches the skill’s actual scope
- `brand_color` is present and valid
- `default_prompt` names the canonical skill and primary behavior accurately
- `policy.allow_implicit_invocation` is present and reflects intended triggering behavior
- any listed dependencies or policy knobs reflect real usage

For repo-level packaging policy:

- OpenAI packaging files are present, valid, and described as the active release surface
- Claude packaging is present, thin, and never described as a second authored skill tree
- shared skill content is still described as the single-source workflow surface
- Root `skills/` is the canonical workflow-authoring surface.
- The packaged plugin root is described consistently as `plugins/python-skills/`.

## Script Audit

Check that:

- developer-facing shell entrypoints use the repo’s current shell policy
- help text matches actual supported flags
- docs use `uv run ...` for Python commands
- maintainer guidance names `uv tool install ruff` and `uv tool install mypy`
- generated next-step commands match what the scaffold really creates
- generated projects include the committed `.env`, ignored `.env.local`, and `pydantic-settings`-based config surface described in the docs

## Maintainer Validation Commands

Run these from repo root:

```bash
uv run scripts/validate_repo_metadata.py
uv run pytest
```

If these commands and the docs disagree, the docs are stale until updated in the same pass.
