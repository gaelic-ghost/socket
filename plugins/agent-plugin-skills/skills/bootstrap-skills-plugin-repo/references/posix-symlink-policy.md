# POSIX Symlink Policy

This repo pattern assumes local development on macOS or Linux.

Preferred local discovery mirrors:

- `.agents/skills -> ../skills`
- `.claude/skills -> ../skills`

Bundled plugin packaging surface:

- `plugins/<plugin-name>/skills/` is a real directory that stays in sync with root `skills/`.

Why symlinks for repo-level discovery:

- Git preserves them explicitly.
- Humans and coding agents can inspect them directly.
- They keep one authored skill tree instead of divergent repo-level discovery copies.

Why the plugin bundle should not use a symlinked `skills/` tree:

- Codex installs and loads a cached copy of the plugin, so the shipped plugin surface must carry its own bundled `skills/` directory.
- A real plugin-root directory keeps the distribution boundary explicit for end users and for marketplace-based installs.

Why not hardlinks:

- Git does not preserve hardlink relationships as repo structure.
- They are opaque to humans and agents.
- They are filesystem-local implementation details, not a durable repository contract.

Windows note:

- Assume WSL 2 or another Linux environment when Windows is involved.
- Do not promise native Windows symlink behavior.
