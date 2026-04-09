# Interactive Customization

## Checklist

1. Choose script mode:
- project script: `init_uv_python_project.sh`
- workspace script: `init_uv_python_workspace.sh`
2. Gather `name`, `path`, and `python`.
3. For project script, gather `profile`.
4. For workspace script, gather `members` and optional `profile_map`.
5. Confirm `force`, `initial_commit`, and `no_git_init`.
6. Return both YAML profile and exact command.

## Schema

Project script keys:
- `name`, `path`, `profile`, `python`, `force`, `initial_commit`, `no_git_init`

Workspace script keys:
- `name`, `path`, `members`, `profile_map`, `python`, `force`, `initial_commit`, `no_git_init`

## Source Precedence

1. CLI flags
2. `--config` file
3. Repo profile: `.codex/profiles/bootstrap-uv-python-workspace/customization.yaml`
4. Global profile: `~/.config/gaelic-ghost/python-skills/bootstrap-uv-python-workspace/customization.yaml`
5. Script defaults

## Reset and Cleanup

- `--bypassing-all-profiles`: ignore global and repo profile for this run.
- `--bypassing-repo-profile`: ignore only repo profile for this run.
- `--deleting-repo-profile`: delete repo profile before running.

## Troubleshooting

- Unknown key in YAML: script exits with an error naming the key.
- Invalid profile values: must be `package` or `service`.
- Missing explicit config file with `--config`: script exits with an error.
