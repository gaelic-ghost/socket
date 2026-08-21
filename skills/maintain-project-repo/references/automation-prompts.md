# Repository Maintenance Prompts

- Install or refresh the fixed FSX repository-maintenance assets, then run the
  complete documentation transaction.
- Report the managed-file and four-document result without mutation.
- Run `just repo-validate` for local or CI validation.
- Run `just repo-sync` for all deterministic shared-asset synchronization.
- Use the three `just repo-release-*` recipes for an explicit protected-main
  release and never poll a remote gate.
- Require branch reachability and accounting evidence before cleanup.

Never request direct script execution, Python, shell, per-file documentation
commands, or project-local schemas.
