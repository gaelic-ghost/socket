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
uv run socket-steward propose docs-sync
uv run socket-steward propose docs-sync --output
uv run socket-steward prepare docs-sync --output
uv run socket-steward apply docs-sync --confirm
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

- Audit, plan, and proposal commands do not call the OpenAI API.
- The steward does not apply proposed documentation edits in this slice.
- Proposal report writes are limited to `docs/agents/`.
- `prepare docs-sync --output` runs audits, planning, and proposal report writing
  in order.
- `apply docs-sync --confirm` is guarded and currently refreshes the proposal
  report only. It reports `NEEDS-REVIEW` instead of mutating durable docs when
  the docs-sync plan has TODO items.
- Durable docs writes, commits, pushes, releases, LaunchAgent, and app behavior
  are future slices after the repo-local contract proves useful.
