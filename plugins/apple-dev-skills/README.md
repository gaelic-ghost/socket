# apple-dev-skills

Some skills I've been working on for Apple dev stuff, packaged as a Plugin for Codex and Claude Code.

## Active Skills

- `xcode-build-run-workflow`
  - Top-level Apple and Swift execution skill for Xcode build, run, diagnostics, previews, toolchains, file membership, and `.pbxproj`-aware mutation decisions.
- `xcode-testing-workflow`
  - Top-level Apple and Swift execution skill for Xcode-native Swift Testing, XCTest, XCUITest, `.xctestplan`, filtering, retries, and test diagnosis.
- `swift-package-build-run-workflow`
  - Top-level SwiftPM-first skill for existing package repos when the work is primarily about manifest changes, dependencies, package resources, Metal distribution, builds, runs, plugins, and Debug-versus-Release validation.
- `swift-package-testing-workflow`
  - Top-level SwiftPM-first skill for existing package repos when the work is primarily about Swift Testing, XCTest holdouts, `.xctestplan`, fixtures, async tests, and test diagnosis.
- `explore-apple-swift-docs`
  - Top-level docs skill for Apple and Swift docs exploration across Xcode MCP docs, Dash, and official web docs, with explicit Apple-framework source guidance, Dash triage guidance, and optional Dash follow-up when needed.
- `format-swift-sources`
  - Top-level skill for integrating SwiftLint and SwiftFormat across CLI, Xcode, SwiftPM, Git hooks, GitHub Actions, and SwiftFormat config export.
- `structure-swift-sources`
  - Top-level skill for splitting, moving, grouping, and documenting Swift source files after a formatting baseline is in place.
- `bootstrap-swift-package`
  - Top-level skill for new Swift package scaffolding only, with verification and `AGENTS.md` generation.
- `bootstrap-xcode-app-project`
  - Top-level skill for new native Apple app bootstrap, with a supported `XcodeGen` path and a guarded guided-Xcode path.
- `sync-xcode-project-guidance`
  - Top-level skill for bringing an existing Xcode app repo's `AGENTS.md` and workflow guidance up to baseline.
- `sync-swift-package-guidance`
  - Top-level skill for bringing an existing Swift package repo's `AGENTS.md` and workflow guidance up to baseline.

### Legacy

- `xcode-app-project-workflow`
  - Legacy compatibility entrypoint for older broad Xcode workflow references. Prefer `xcode-build-run-workflow` or `xcode-testing-workflow` for new installs, docs, and prompts.
- `swift-package-workflow`
  - Legacy compatibility entrypoint for older broad package-workflow references. Prefer `swift-package-build-run-workflow` or `swift-package-testing-workflow` for new installs, docs, and prompts.

Every active skill now follows the same documentation contract:

- one primary workflow per request type
- explicit `inputs`, `defaults`, `status`, `path_type`, and `output`
- named `fallback` and `handoff` behavior
- a clear customization stance, including explicit `policy-only` knobs or an explicit “no durable customization surface” statement

## Packaging And Discovery

This repository exports from the repository root. Top-level `skills/` is the canonical workflow-authoring and install surface today.

Shared guidance across both ecosystems:

- keep reusable workflow behavior in root `skills/`
- keep deterministic helper logic skill-scoped so both Codex and Claude can rely on it
- use POSIX symlink mirrors for local Codex and Claude project discovery on macOS and Linux:
  - `.agents/skills -> ../skills`
  - `.claude/skills -> ../skills`
- do not recreate a nested packaged plugin tree or any other second export surface under `plugins/`

Current local discovery scaffolding lives under:

- `.agents/skills`
- `.claude/skills`

For new installs, prompts, and examples, prefer the narrower execution-skill names over the legacy compatibility entrypoints.

Maintainer guidance for those adjacent surfaces lives in [AGENTS.md](./AGENTS.md).

## Standards And Docs

Maintainer-facing workflow diagrams, input and output contracts, and Agent ↔ User UX maps live in [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md). Audit procedure and source-of-truth guidance live in [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md). The current customization-system decision and follow-up plan live in [docs/maintainers/customization-consolidation-review.md](./docs/maintainers/customization-consolidation-review.md). The planned execution-skill split, guidance-preservation contract, and toolkit direction live in [docs/maintainers/execution-split-and-inference-plan.md](./docs/maintainers/execution-split-and-inference-plan.md), with the concrete guidance mapping in [docs/maintainers/workflow-guidance-preservation-matrix.md](./docs/maintainers/workflow-guidance-preservation-matrix.md).

### Maintainer References

- Agent Skills Standard: <https://agentskills.io/home>
- OpenAI Codex Skills: <https://developers.openai.com/codex/skills>
- OpenAI Codex AGENTS.md configuration: <https://developers.openai.com/codex/guides/agents-md/>
- Claude Code Plugins: <https://code.claude.com/docs/en/plugins>

### Install Surfaces

This repository exports from top-level `skills/` today. If `mcps/` or `apps/` are added later, they must also live at the repository top level. Keep repo-scoped marketplace catalogs aligned directly with root `skills/`, and do not describe or recreate a nested packaged plugin tree, repo-local installer workflow, or repo-local install-validator workflow as part of this repository's contract.

Repo-wide standards audit and coordination for this repository belongs to the maintainer workflow in `maintain-plugin-repo`.

## Maintainer Python Tooling

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

Use the executable skill entrypoints directly, for example `skills/xcode-build-run-workflow/scripts/run_workflow.py`.
For Python wrapper and customization entrypoints that declare inline `uv` dependencies such as `PyYAML`, prefer `uv run scripts/run_workflow.py ...` and `uv run scripts/customization_config.py ...` in consuming repos instead of assuming a plain `python` environment has those dependencies available.
Use targeted `uv run --group dev pytest tests/...` runs while iterating and a full `uv run --group dev pytest` pass before finalizing repo-wide maintenance.
Keep `ruff` and `mypy` available as maintainer-side `uv` tools even when a given repo pass only needs the test suite.

## Install

Install from the top-level export surface. For this repository today, that means root `skills/`.

Standalone skill installation is handled through the Vercel `skills` CLI against root `skills/`. For local project discovery on macOS and Linux, this repo also exposes `.agents/skills` and `.claude/skills` as symlink mirrors into root `skills/`.

Install one skill:

```bash
npx skills add gaelic-ghost/apple-dev-skills --skill xcode-build-run-workflow
```

Install all active skills:

```bash
npx skills add gaelic-ghost/apple-dev-skills --all
```

Common starting points:

- Xcode work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill xcode-build-run-workflow`
- Xcode testing work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill xcode-testing-workflow`
- Swift package build or run work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill swift-package-build-run-workflow`
- Swift package testing work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill swift-package-testing-workflow`
- Apple or Swift docs exploration:
  `npx skills add gaelic-ghost/apple-dev-skills --skill explore-apple-swift-docs`
- SwiftLint and SwiftFormat integration:
  `npx skills add gaelic-ghost/apple-dev-skills --skill format-swift-sources`
- Swift source organization and file-splitting cleanup:
  `npx skills add gaelic-ghost/apple-dev-skills --skill structure-swift-sources`
- New Swift package bootstrap:
  `npx skills add gaelic-ghost/apple-dev-skills --skill bootstrap-swift-package`
- New native Apple app bootstrap:
  `npx skills add gaelic-ghost/apple-dev-skills --skill bootstrap-xcode-app-project`
- Existing Xcode repo guidance sync:
  `npx skills add gaelic-ghost/apple-dev-skills --skill sync-xcode-project-guidance`
- Existing Swift package repo guidance sync:
  `npx skills add gaelic-ghost/apple-dev-skills --skill sync-swift-package-guidance`

### Migration

This repo previously experimented with a router layer and later removed it.

| Historical ID | Current State |
| --- | --- |
| `apple-skills-router-advise-install` | removed |
| `apple-skills-router` | removed |
| `apple-xcode-workflow-execute` | legacy compatibility flow through `xcode-app-project-workflow`, then `xcode-build-run-workflow` or `xcode-testing-workflow` |
| `apple-dash-docset-manage` | `explore-apple-swift-docs` |
| `apple-dash-docsets` | removed in `v4.0.0`; use `explore-apple-swift-docs` |
| `apple-swift-package-bootstrap` | removed in `v4.0.0`; use `bootstrap-swift-package` |

New install-facing names should prefer the narrower execution skills directly instead of the legacy compatibility surfaces.

The Apple plugin now ships its repo-maintenance toolkit contract directly. This repository keeps the managed toolkit source under `shared/repo-maintenance-toolkit/` so the Apple bootstrap and guidance-sync skills can install or refresh the same file set without requiring a second plugin or repo for end users. The bundled installer is profile-aware and writes `scripts/repo-maintenance/config/profile.env` so downstream repos can tell whether they are on the `swift-package` or `xcode-app` profile.

### AGENTS Guidance

Repository-consumable Swift and Apple baseline policy snippets:

- [shared/agents-snippets/apple-xcode-project-core.md](./shared/agents-snippets/apple-xcode-project-core.md)
- [shared/agents-snippets/apple-swift-package-core.md](./shared/agents-snippets/apple-swift-package-core.md)

Use these snippets for cross-project standards that belong in end-user `AGENTS.md`.

- Skills that need end-user repo-guidance snippets ship the local snippet copy that matches their workflow surface so individually installed skills can recommend it directly.
- For Apple or Swift docs exploration, prefer `explore-apple-swift-docs` over older Dash-specific guidance.
- For SwiftLint or SwiftFormat setup and config-export workflows, prefer `format-swift-sources` over scattering style-tooling snippets across unrelated skills.
- For file splitting, MARK normalization, DocC coverage, and TODO or FIXME ledger cleanup, prefer `structure-swift-sources`, usually bracketed by `format-swift-sources` before and after.
- For new Swift package repositories, `bootstrap-swift-package` copies its full `assets/AGENTS.md` template, which already incorporates the Swift-package baseline.
- For existing Xcode app repositories, prefer `sync-xcode-project-guidance` over manual snippet merging when the goal is to align repo guidance.
- For existing Swift package repositories, prefer `sync-swift-package-guidance` over manual snippet merging when the goal is to align repo guidance.
- For existing repositories, use the shared snippets for targeted updates or the skill-local copies when reading an installed skill in isolation.
- For cross-repo AGENTS drift and documentation alignment workflows, use dedicated docs-alignment skills maintained outside this repository.

## Repository Layout

```text
.
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── .claude-plugin/
│   └── marketplace.json
├── README.md
├── ROADMAP.md
├── docs/
│   └── maintainers/
│       ├── reality-audit.md
│       └── workflow-atlas.md
├── shared/
│   ├── agents-snippets/
│   │   ├── apple-swift-package-core.md
│   │   └── apple-xcode-project-core.md
│   └── repo-maintenance-toolkit/
└── skills/
    ├── bootstrap-xcode-app-project/
    ├── bootstrap-swift-package/
    ├── explore-apple-swift-docs/
    ├── format-swift-sources/
    ├── swift-package-build-run-workflow/
    ├── swift-package-testing-workflow/
    ├── sync-swift-package-guidance/
    ├── sync-xcode-project-guidance/
    ├── xcode-build-run-workflow/
    ├── xcode-testing-workflow/
    ├── swift-package-workflow/
    ├── structure-swift-sources/
    └── xcode-app-project-workflow/
```

The canonical workflow content still lives under root `skills/`. Repo-scoped Codex and Claude marketplace catalogs also point directly at that same source tree for local discovery instead of staging a second packaged plugin copy. The discovery mirrors are local POSIX symlinks for macOS and Linux development, including WSL 2 when Windows is involved.

Maintainers: authoritative skill-authoring resources live in `AGENTS.md`.

## License

See [LICENSE](./LICENSE).
