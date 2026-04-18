# AGENTS.md

Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or project workflow surfaces in this repository.

## Repository Scope

### What This File Covers

- This repository is the canonical home for Gale's Apple, Swift, and Xcode workflow skills.
- Treat `productivity-skills` as the default baseline maintainer layer for general repo docs and maintenance work; this repo is the narrower specialist layer when Apple-specific behavior should change the workflow.
- Root `skills/` is the canonical authored and exported surface.
- Keep shared reusable assets in [`shared/`](./shared/) and maintainer tests in [`tests/`](./tests/).

### Where To Look First

- Start with [`README.md`](./README.md), [`CONTRIBUTING.md`](./CONTRIBUTING.md), [`ROADMAP.md`](./ROADMAP.md), [`docs/maintainers/workflow-atlas.md`](./docs/maintainers/workflow-atlas.md), and [`docs/maintainers/reality-audit.md`](./docs/maintainers/reality-audit.md).
- When a task touches one shipped workflow, read the corresponding directory under [`skills/`](./skills/) before inferring policy from sibling skills or older maintainer notes.
- Use [`.github/scripts/validate_repo_docs.sh`](./.github/scripts/validate_repo_docs.sh) and the pytest suite as the enforced source-of-truth checks for public-doc drift.

## Working Rules

### Change Scope

- Keep work bounded to the smallest coherent docs, skill, validator, and test surface that resolves the real drift.
- If a task starts needing a new active skill, a new export surface, or a broad repo-structure change, stop and surface that scope change before continuing.
- Collapse retired historical planning notes into `ROADMAP.md` or still-live maintainer docs instead of preserving stale standalone docs.

### Source of Truth

- For Swift, Apple framework, Apple platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related guidance, require reading the relevant Apple documentation before proposing implementation changes.
- State the documented Apple behavior being relied on before design or code changes are proposed.
- If Apple docs and current code disagree, stop and surface that conflict.
- If no relevant Apple documentation can be found, say that explicitly before proceeding.
- Prefer the simplest correct Swift that is easiest to read and reason about.
- Prefer framework-provided behavior over custom boilerplate. Do not add extra wrappers, coordinators, custom codable glue, or renaming layers unless a concrete constraint requires them or they make the final code clearly easier to understand.
- Preserve source-of-truth names when the meaning has not changed, and avoid automatic case-conversion strategies unless the project explicitly wants them.
- Keep `explore-apple-swift-docs` as the canonical docs-routing surface instead of re-embedding broad docs-source selection logic into execution skills.
- For SwiftPM guidance, edit `Package.swift` intentionally and keep it readable. Agents may modify it when package structure, targets, products, or dependencies need to change, should avoid adding unnecessary dependency-provenance detail or switching to branch/revision-based requirements unless the user explicitly asks for that level of control, and should try to keep package graph updates consolidated in one change when possible.
- Keep `Package.swift` explicit about its package-wide Swift language mode. On current Swift 6-era manifests, prefer `swiftLanguageModes: [.v6]` as the default declaration and treat `swiftLanguageVersions` as a legacy alias used only when an older manifest surface requires it.
- Treat `Package.resolved` and similar package-manager outputs as generated files. Do not tell agents to hand-edit them.

### Communication and Escalation

- Surface non-obvious tradeoffs before widening a change from one skill or one doc into repo-wide wording or policy.
- When docs, validator rules, and tests disagree, explain which surface is stale and what you are changing to bring them back into alignment.
- If a historical maintainer doc still contains live decisions, move those decisions into the active docs before deleting the old file.

## Commands

### Setup

```bash
uv sync --dev
```

### Validation

```bash
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

### Optional Project Commands

```bash
uv run python .github/scripts/validate_skill_creator_contract.py
```

Use the extra validator when a change touches the skill-creator contract or repo-doc rules that mention it.

## Review and Delivery

### Review Expectations

- Explain which shipped docs, validator rules, and tests changed and why.
- Call out deleted or consolidated maintainer docs explicitly so reviewers can see where their durable conclusions moved.
- Keep docs-only cleanup distinct from behavior-changing skill work when that split helps review.

### Definition of Done

- The changed root docs, maintainer docs, validator rules, and tests all describe the same live repository behavior.
- Grounded validation has been run or any skipped checks are called out plainly.
- Nearby docs and roadmap history have been updated when the change retires stale planning notes or changes the public workflow contract.

## Safety Boundaries

### Never Do

- Do not reintroduce nested packaged plugin trees or alternate export surfaces under `plugins/`.
- Do not weaken the Apple docs-first rule or present Apple behavior from memory when current docs are available.
- Do not tell maintainers to hand-edit generated package-manager state such as `Package.resolved`.
- Do not preserve stale historical planning docs as live guidance once their durable conclusions have already been absorbed elsewhere.

### Ask Before

- Ask before adding or removing active skills, changing the top-level export shape, or broadening the repository into a new product surface.
- Ask before deleting a maintainer doc whose decisions have not yet been folded into `ROADMAP.md` or a still-live maintainer reference.
- Ask before changing repo-wide policy that would affect downstream synced or bootstrapped guidance assets.

## Local Overrides

This repository does not currently use deeper `AGENTS.md` files under `skills/` or `docs/`. Treat this root file as the repo-wide agent contract, and use the individual skill docs plus maintainer references to refine behavior for the specific surface you are editing.
