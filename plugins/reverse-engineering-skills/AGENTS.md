# AGENTS.md

This file is the Reverse Engineering Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `reverse-engineering-skills` is a monorepo-owned placeholder source for future binary inspection, decompilation, disassembly, symbol, and artifact-analysis Codex skills.
- Keep the repo intentionally minimal until the first real skill tranche lands.
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) is the required plugin root today.

## Local Rules

- Do not present this repository as already shipping reverse-engineering workflows before real skills exist.
- Keep this plugin focused on technical inspection workflows, artifact handling, reproducible notes, and evidence quality.
- Treat user, project, client, and repository scope decisions as external to the skill. The skill should not decide whether a reverse-engineering task is legitimate, authorized, or acceptable.
- Preserve original artifacts by default. Prefer copying inputs into a clearly named working area, recording hashes or identifying metadata when useful, and documenting tool versions and commands used.
- Keep platform-specific work delegated where appropriate: use `dotnet-skills` for ordinary .NET development, `apple-dev-skills` for Apple build and Xcode workflows, and this plugin only when compiled artifacts, decompiled output, symbols, or binary metadata are the center of the task.
- When this repository changes the root Socket marketplace or root docs, update those root surfaces in the same pass.
