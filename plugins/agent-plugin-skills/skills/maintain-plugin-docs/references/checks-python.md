# Python Checks

## Detection

Treat repository as Python when any is present:
- `pyproject.toml`
- `uv.lock`
- `.python-version`
- `requirements.txt` / `requirements-*.txt`

## Tooling Preference

- If `uv.lock` exists, commands should use uv-centric workflow where applicable.
- Canonical examples:
  - `uv sync`
  - `uv run <command>`

## Alignment Expectations

- Avoid contradictory guidance that defaults to raw `pip install -r requirements.txt` when uv signals are strong.
- Keep instructions internally consistent across README and other in-scope docs.

## Safe Fix Scope

- Replace clearly contradictory install/run snippets with uv equivalents only when intent is deterministic.
- Do not alter dependency model narratives or packaging architecture sections.
