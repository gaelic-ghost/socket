# Socket Steward

Socket Steward is a repo-local OpenAI Agents SDK prototype for maintaining this
repository's docs, guidance, plugin catalog, and release workflow notes.

The first version is intentionally read-only by default. It can run deterministic
audits without `OPENAI_API_KEY`, and it only calls the OpenAI Agents SDK when the
`ask` command is used.

## Commands

Run deterministic audits:

```bash
uv run socket-steward audit guidance
uv run socket-steward audit marketplace
uv run socket-steward audit docs
uv run socket-steward plan docs-sync
```

Ask the agent a repo-maintenance question:

```bash
OPENAI_API_KEY=... uv run socket-steward ask "What Socket docs look stale?"
```

## Validation

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run mypy .
```

## Boundaries

- Audit commands do not call the OpenAI API.
- The agent is read-only in this first slice.
- Write, apply, commit, push, release, LaunchAgent, and app behavior are future
  slices after the repo-local contract proves useful.
