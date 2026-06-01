# Socket Steward Local Evals

These evals exercise the live Socket Steward `ask` path against small behavior
contracts.

They are not a replacement for unit tests. Unit tests prove deterministic code.
These evals check whether the model-backed agent chooses the right repo workflow,
uses existing skills or scripts, and avoids unsupported actions.

## Run

```bash
uv run python evals/run_local.py
```

`OPENAI_API_KEY` must be set in the shell environment. The runner never prints
or stores the key.

Results are written to `evals/results/latest.json`, which is ignored by git.

## Case Shape

Each JSONL case includes:

- `id`: stable case name
- `prompt`: user prompt sent to Socket Steward
- `required`: case-insensitive substrings that must appear
- `required_any`: case-insensitive substring groups where at least one item per group must appear
- `forbidden`: case-insensitive substrings that must not appear

Keep cases small and behavior-focused. Promote manual smoke-test failures into
this suite when they represent behavior we want to preserve.
