# Interactive Customization

## Checklist

1. Confirm `mode` (`project` or `workspace`).
2. Gather `name`, `path`, and `python`.
3. If workspace mode, gather `members` and optional `profile_map`.
4. Confirm `force`, `initial_commit`, and `no_git_init`.
5. Return both YAML profile and exact command.

## Schema

- `name` (string, required)
- `mode` (string: `project|workspace`, default `project`)
- `path` (string, default `./<name>`)
- `python` (string, default `3.13`)
- `members` (string CSV, workspace only)
- `profile_map` (string mapping CSV, workspace only)
- `force` (bool, default `false`)
- `initial_commit` (bool, default `false`)
- `no_git_init` (bool, default `false`)

## Source Precedence

1. CLI flags
2. `--config` file
3. Repo profile: `.codex/profiles/bootstrap-python-mcp-service/customization.yaml`
4. Global profile: `~/.config/gaelic-ghost/python-skills/bootstrap-python-mcp-service/customization.yaml`
5. Script defaults

## Reset and Cleanup

- `--bypassing-all-profiles`: ignore global and repo profile for this run.
- `--bypassing-repo-profile`: ignore only repo profile for this run.
- `--deleting-repo-profile`: delete repo profile before running.

## Troubleshooting

- Unknown key in YAML: script exits with an error naming the key.
- Invalid mode/flag combinations: script guardrails still apply.
- Missing explicit config file with `--config`: script exits with an error.
