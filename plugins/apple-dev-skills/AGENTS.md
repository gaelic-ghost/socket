# AGENTS.md

This file is the Apple Dev Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, and maintainer workflow rules.

## Scope

- This repository is the canonical home for Gale's Apple, Swift, and Xcode workflow skills.
- Treat `productivity-skills` as the default baseline maintainer layer for general repo docs and maintenance work; this repo is the narrower specialist layer when Apple-specific behavior should change the workflow.
- Preserve standalone-install guidance for public users who install only `apple-dev-skills`, while allowing the public README quickstart to lead with the Socket marketplace when users want Apple Dev Skills plus companion workflows from one catalog.
- Root `skills/` is the canonical authored and exported surface.
- Keep shared reusable assets in [`shared/`](./shared/) and maintainer tests in [`tests/`](./tests/).

## Apple Rules

- For Swift, Apple framework, Apple platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related guidance, require reading the relevant Apple documentation before proposing implementation changes.
- State the documented Apple behavior being relied on before design or code changes are proposed.
- If Apple docs and current code disagree, stop and surface that conflict.
- If no relevant Apple documentation can be found, say that explicitly before proceeding.
- Keep `explore-apple-swift-docs` as the canonical docs-routing surface instead of re-embedding broad docs-source selection logic into execution skills.
- Prefer framework-provided behavior over custom wrappers, coordinators, glue, or renaming layers unless a concrete constraint requires them.
- For Xcode app repos, tracked `.pbxproj` changes are critical project state when produced by Xcode, XcodeGen, or another project-aware workflow.
- Treat `Package.resolved` and similar package-manager outputs as generated files. Do not tell maintainers or agents to hand-edit them.

## Install Guidance

- The public README may lead with `codex plugin marketplace add gaelic-ghost/socket` and `codex plugin marketplace upgrade socket` because Socket is the preferred catalog when users want Apple Dev Skills plus companion workflows.
- Also document `codex plugin marketplace add gaelic-ghost/apple-dev-skills` and `codex plugin marketplace upgrade apple-dev-skills` for Apple-only installs.
- Keep explicit refs scoped to pinned reproducible installs and manual local clone marketplace instructions scoped to development, unpublished testing, or fallback cases.

## Validation

```bash
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

Use the docs validator when README, AGENTS, ROADMAP, active skill inventory, or maintainer docs change. Use pytest when skill behavior, scripts, validation helpers, or tested contracts change.
