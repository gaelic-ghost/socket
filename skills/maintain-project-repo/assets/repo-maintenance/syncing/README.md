# Repo-Maintenance Syncing Steps

Add repo-specific `.sh` files here when the repository needs deterministic shared-sync steps.

The top-level `scripts/repo-maintenance/sync-shared.sh` entrypoint discovers and runs every `*.sh` file in this directory in lexical order.

Use this sync path after substantial guidance or plugin updates so checked-in repo guidance and toolkit files stay aligned.
