# python-skills plugin surface

Thin packaged plugin root for the `python-skills` repository.

This directory exists so Codex can install the packaged `python-skills` surface while the canonical authored workflow content remains at the repository root under [`../../skills/`](../../skills/).

Use the repository root README for the actual project overview and maintainer workflow:

- [Repository README](../../README.md)
- [Root skills directory](../../skills/)
- [Plugin manifest](./.codex-plugin/plugin.json)

This packaged surface is intentionally thin:

- `skills` is a symlink back to the canonical root skill tree
- `.codex-plugin/plugin.json` defines the packaged Codex plugin metadata
- `.claude-plugin/` carries the Claude-side packaging metadata for this nested surface
