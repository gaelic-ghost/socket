# POSIX Symlink Policy

This repo pattern assumes local development on macOS or Linux.

Preferred local mirrors:

- `.agents/skills -> ../skills`
- `.claude/skills -> ../skills`
- `plugins/<plugin-name>/skills -> ../../skills`

Why symlinks:

- Git preserves them explicitly.
- Humans and coding agents can inspect them directly.
- They keep one authored skill tree instead of divergent copies.

Why not hardlinks:

- Git does not preserve hardlink relationships as repo structure.
- They are opaque to humans and agents.
- They are filesystem-local implementation details, not a durable repository contract.

Windows note:

- Assume WSL 2 or another Linux environment when Windows is involved.
- Do not promise native Windows symlink behavior.
