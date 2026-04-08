# Validation Surface

## Canonical Authored Surface

- root `skills/`
- one directory per skill
- each skill directory should own:
  - `SKILL.md`
  - `agents/openai.yaml`
  - optional `scripts/`, `references/`, and `assets/`

## Metadata Overlays

- `SKILL.md` frontmatter:
  - `name`
  - `description`
- `agents/openai.yaml`:
  - `interface.display_name`
  - `interface.short_description`
  - `interface.default_prompt`

## Plugin Packaging Surfaces

- `plugins/*/.codex-plugin/plugin.json`
- `plugins/*/.claude-plugin/plugin.json`
- `plugins/*/skills/` bundled plugin skills directory
- `.agents/plugins/marketplace.json`

## Discovery Mirrors

- `.agents/skills -> ../skills`
- `.claude/skills -> ../skills`

## Bundled Plugin Skills Contract

- `plugins/<plugin>/skills/` must be a real directory, not a symlink
- the bundled plugin tree must stay in sync with root `skills/`

## Install-Surface Checks

- README install examples should point at real repo surfaces.
- `npx skills add <owner/repo> --skill <skill-name>` should reference real skill directories.
- When Codex or Claude plugin packaging exists, README install guidance should reference Codex local plugin installs and Claude Code plugin usage explicitly.
