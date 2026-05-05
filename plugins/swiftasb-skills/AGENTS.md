# AGENTS.md

This file is the SwiftASB Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `swiftasb-skills` ships Codex skills for explaining and integrating [SwiftASB](https://github.com/gaelic-ghost/SwiftASB).
- Treat root [`skills/`](./skills/) as the authored skill source of truth.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as plugin packaging metadata.
- Keep this plugin focused on SwiftASB-specific explanation, decision support, and integration workflows.

## Local Rules

- Use the current SwiftASB repository, README, DocC docs, release notes, and public Swift API as the source of truth for package behavior.
- SwiftASB `v1.0.0` is the first supported public API baseline, but active development may move ahead of the latest release; verify local or GitHub package state before writing exact API guidance.
- Do not copy SwiftASB source, generated wire models, or schema files into this plugin.
- Do not describe generated `CodexWire...` models as the intended public integration surface; SwiftASB's public surface is the hand-owned Swift API.
- Use `apple-dev-skills` for Apple framework behavior, SwiftUI/AppKit lifecycle rules, Xcode workflow selection, DocC, build, and test execution guidance.

## Validation

For Socket marketplace and packaging changes:

```bash
uv run scripts/validate_socket_metadata.py
```

When these skills change, inspect authored Markdown for stale SwiftASB symbol names and verify links still point at the current source-of-truth docs.
