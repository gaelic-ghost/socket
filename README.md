# things-app

Focused Things.app skills for reminder management and planning digests.

## Active Skills

- `things-reminders-manager`
  - Deterministic create and update workflows for Things reminders and scheduled todos.
- `things-digest-generator`
  - Week-ahead planning digests built from Things MCP reads or equivalent JSON exports.

## Repository Layout

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
└── skills/
    ├── things-digest-generator/
    └── things-reminders-manager/
```

## Maintainer Notes

- Keep active skill runtime assets self-contained inside each skill directory.
- Prefer `uv run pytest` for the Python-backed digest skill test surface.
- Treat `things-app` as the canonical repo home for the two Things skills.
