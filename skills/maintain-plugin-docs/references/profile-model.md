# Profile Model

## Public Curated

- `apple-dev-skills`
- `productivity-skills`
- `python-skills`

Requirements:

- core README schema
- compact `## Table of Contents` required
- `## Install individually by Skill or Skill Pack` required
- `## Update Skills` required
- discoverability sections
- release highlights/history section(s)
- `## Keywords` section

## Private/Internal

- `private-skills`

Requirements:

- concise core schema
- discoverability and release sections optional

## Bootstrap

- `a11y-skills`

Requirements:

- create minimal complete README if missing
- release history optional until first release cadence

## Plugin Maintainer

- repos with canonical `skills/` authoring plus plugin packaging under `plugins/*/.codex-plugin` or `plugins/*/.claude-plugin`

Requirements:

- maintainer-facing README schema, not the public skill-pack schema
- `## Active Skills`
- `## Repo Purpose`
- `## Packaging And Discovery`
- `## Standards And Docs`
- `## Maintainer Python Tooling`
- `## Install`
- `## Repository Layout`
- `## License`
- `## Maintainer Python Tooling` should document `uv sync --dev`, `uv tool install ruff`, `uv tool install mypy`, and `uv run --group dev pytest`
- primary Codex Plugin and Claude Code Plugin install surfaces documented before secondary Vercel `skills` CLI examples
