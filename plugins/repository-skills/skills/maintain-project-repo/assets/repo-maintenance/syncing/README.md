# Repository Synchronization Hooks

Place only root-owned `.fsx` synchronization hooks here. `just repo-sync`
discovers them in lexical order, runs every hook, and then validates the full
repository. Keep hooks deterministic and non-interactive.
