# AGENTS.md

Use this file for durable guidance that applies inside the `swiftasb-skills` child plugin.

## Repository Scope

- `swiftasb-skills` is a Socket child plugin that ships Codex skills for explaining and integrating [SwiftASB](https://github.com/gaelic-ghost/SwiftASB).
- Treat root [`skills/`](./skills/) as the authored skill source of truth.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) as plugin packaging metadata.
- Keep this plugin focused on SwiftASB-specific explanation, decision support, and integration workflows.

## Source Of Truth

- Use the current SwiftASB repository, README, DocC docs, release notes, and public Swift API as the source of truth for package behavior.
- SwiftASB `v1.0.0` is the first supported public API baseline, and `v1.0.1` is the current released baseline. Active development may move ahead of that release, so verify the local or GitHub package state before writing exact API guidance.
- Do not copy SwiftASB source, generated wire models, or schema files into this plugin.
- Do not describe generated `CodexWire...` models as the intended public integration surface. SwiftASB's public surface is the hand-owned Swift API.

## Skill Boundaries

- Use this plugin for SwiftASB-specific choices: whether to adopt SwiftASB, which SwiftASB owner should own the work, how to expose observable companions, and how to explain tradeoffs to a user.
- Use `apple-dev-skills` for Apple framework behavior, SwiftUI/AppKit lifecycle rules, Xcode workflow selection, DocC, build, and test execution guidance.
- When a task involves SwiftUI, AppKit, Observation, SwiftPM, or Xcode behavior, read the relevant Apple documentation before making framework claims.
- Keep user-facing explanations plain and decision-oriented before moving into symbol names.

## Validation

For root Socket marketplace and packaging changes, run from the Socket root:

```bash
uv run scripts/validate_socket_metadata.py
```

When these skills are changed, also inspect the authored Markdown for stale SwiftASB symbol names and ensure links still point at the current source-of-truth docs.
