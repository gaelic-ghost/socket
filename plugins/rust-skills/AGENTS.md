# AGENTS.md

## Repository Purpose

- This repository is the standalone plugin source for future Rust-focused Codex skills.
- Keep the repo minimal until the first real skills land.
- Prefer adding actual skill content before expanding packaging or automation.

## Current Boundaries

- `.codex-plugin/plugin.json` is the required Codex plugin root.
- Do not add extra layers or repo-local install machinery yet.
- Treat this repo as an independently versioned child repo that can also be imported into the `socket` superproject as a subtree.
