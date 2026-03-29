# Fix Policies

## Allowed Auto-Fixes

- Command-level package manager substitutions in markdown docs when canonical manager is known.
- Deterministic command snippet corrections for language tooling (Swift/Rust/Python uv).
- Insert short `## Development Quickstart` block when absent and derivable from manifests.

## Disallowed Auto-Fixes

- Freeform narrative rewrites.
- Architecture/API behavior documentation changes.
- Broad `AGENTS.md` rewrites or unsolicited AGENTS maintenance.
- Targeted `AGENTS.md` edits without explicit user approval.
- Source code, manifests, lockfiles, CI config, or non-doc files.
- Ambiguous cases with more than one plausible canonical command set.

## Edit Constraints

- Keep edits minimal and local.
- Preserve surrounding markdown style.
- Record every attempted fix with status (`applied`, `skipped`, `error`) and reason.
