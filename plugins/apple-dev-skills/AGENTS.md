# AGENTS.md

## Repository Role

- This repository is the canonical home for Gale's Apple, Swift, and Xcode workflow skills.
- Treat `productivity-skills` as the default baseline maintainer layer for general repo docs and maintenance work; this repo is the narrower specialist layer when Apple-specific behavior should change the workflow.
- Root `skills/` is the canonical authored and exported surface.
- Keep shared reusable assets in [`shared/`](./shared/) and maintainer tests in [`tests/`](./tests/).

## Apple-specific Rules

- For Swift, Apple framework, Apple platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related guidance, require reading the relevant Apple documentation before proposing implementation changes.
- State the documented Apple behavior being relied on before design or code changes are proposed.
- If Apple docs and current code disagree, stop and surface that conflict.
- If no relevant Apple documentation can be found, say that explicitly before proceeding.
- Prefer the simplest correct Swift that is easiest to read and reason about.
- Prefer framework-provided behavior over custom boilerplate. Do not add extra wrappers, coordinators, custom codable glue, or renaming layers unless a concrete constraint requires them or they make the final code clearly easier to understand.
- Preserve source-of-truth names when the meaning has not changed, and avoid automatic case-conversion strategies unless the project explicitly wants them.
- Keep `explore-apple-swift-docs` as the canonical docs-routing surface instead of re-embedding broad docs-source selection logic into execution skills.
- For SwiftPM guidance, edit `Package.swift` intentionally and keep it readable. Agents may modify it when package structure, targets, products, or dependencies need to change, should avoid adding unnecessary dependency-provenance detail or switching to branch/revision-based requirements unless the user explicitly asks for that level of control, and should try to keep package graph updates consolidated in one change when possible.
- Treat `Package.resolved` and similar package-manager outputs as generated files. Do not tell agents to hand-edit them.

## Export Boundaries

- Keep root `skills/` as the canonical authored surface even though the repo ships plugin packaging metadata.
- Do not reintroduce nested packaged plugin trees or alternate export surfaces under `plugins/`.
