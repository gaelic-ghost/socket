# MCP Failure Fallback Contract

Use this payload shape when `xcode-testing-workflow` falls back from an MCP attempt to the official CLI path.

## Inputs

- `intent`: `build`, `test`, `run`, `package`, `toolchain`, `docs`, `mutation`, or `read-search`
- `workspace_path`: absolute path when known
- `tab_identifier`: resolved MCP tab identifier or `unknown`
- `mcp_failure_reason`: `timeout`, `transport`, `unsupported`, or `precondition`
- `attempts`: number of MCP attempts already made

## Output

```text
status: <success|blocked>
path_type: <primary|fallback>
intent: <build|test|run|package|toolchain|docs|mutation|read-search>
workspace_path: <absolute-path-or-unknown>
tab_identifier: <resolved-or-unknown>
mcp_failure_reason: <timeout|transport|unsupported|precondition>
attempts: <count>
fallback_commands:
  - <official-command-1>
  - <official-command-2>
next_step: <short-text>
```

## Notes

- Retry once on `timeout` or `transport`.
- Do not retry on `unsupported` beyond the first determination.
- Use `status: success` with `path_type: fallback` when the official CLI path completes successfully.
- Continue to official CLI fallback after the documented retry policy is exhausted.
