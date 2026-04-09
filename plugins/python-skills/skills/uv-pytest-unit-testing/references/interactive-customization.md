# Interactive Customization

## Checklist

1. Choose script mode:
- bootstrap script: `bootstrap_pytest_uv.sh`
- run script: `run_pytest_uv.sh`
2. Gather `workspace_root` and optional `package`.
3. For bootstrap mode, confirm `with_cov` and `dry_run`.
4. For run mode, gather optional `path` and optional pytest passthrough args.
5. Return both YAML profile and exact command.

## Schema

Bootstrap script keys:
- `workspace_root` (string, default current directory)
- `package` (string, optional)
- `with_cov` (bool, default `false`)
- `dry_run` (bool, default `false`)

Run script keys:
- `workspace_root` (string, default current directory)
- `package` (string, optional)
- `path` (string, optional)

## Source Precedence

1. CLI flags
2. `--config` file
3. Repo profile: `.codex/profiles/uv-pytest-unit-testing/customization.yaml`
4. Global profile: `~/.config/gaelic-ghost/python-skills/uv-pytest-unit-testing/customization.yaml`
5. Script defaults

## Reset and Cleanup

- `--bypassing-all-profiles`: ignore global and repo profile for this run.
- `--bypassing-repo-profile`: ignore only repo profile for this run.
- `--deleting-repo-profile`: delete repo profile before running.

## Troubleshooting

- Unknown key in YAML: script exits with an error naming the key.
- Missing explicit config file with `--config`: script exits with an error.
- Ensure `--` is used for pytest passthrough args in run mode.
