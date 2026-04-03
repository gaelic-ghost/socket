# apple-dev-skills

Canonical Apple development skills with an in-progress plugin-first packaging layout for Codex and Claude Code.

## Active Skills

- `apple-xcode-workflow`
  - Top-level Apple and Swift execution skill for Xcode work, diagnostics, toolchains, mutation decisions, and guarded fallback planning. Planned rename: `xcode-app-project-workflow`.
- `explore-apple-swift-docs`
  - Top-level docs skill for Apple and Swift docs exploration across Xcode MCP docs, Dash, and official web docs, with optional Dash follow-up when needed.
- `bootstrap-swift-package`
  - Top-level skill for new Swift package scaffolding only, with verification and `AGENTS.md` generation.
- `bootstrap-xcode-app-project`
  - Top-level skill for new native Apple app bootstrap, with a supported `XcodeGen` path and a guarded guided-Xcode path.
- `sync-xcode-project-guidance`
  - Top-level skill for bringing an existing Xcode app repo's `AGENTS.md` and workflow guidance up to baseline.
- `sync-swift-package-guidance`
  - Top-level skill for bringing an existing Swift package repo's `AGENTS.md` and workflow guidance up to baseline.

Every active skill now follows the same documentation contract:

- one primary workflow per request type
- explicit `inputs`, `defaults`, `status`, `path_type`, and `output`
- named `fallback` and `handoff` behavior
- customization knobs labeled `policy-only` unless runtime enforcement exists

Maintainer-facing workflow diagrams, input and output contracts, and Agent ↔ User UX maps live in [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md). Audit procedure and source-of-truth guidance live in [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md).

## Packaging and Delegation

This repository now tracks a plugin-first packaging plan while keeping root `skills/` as the canonical workflow-authoring surface.

Shared guidance across both ecosystems:

- keep reusable workflow behavior in root `skills/`
- keep deterministic helper logic skill-scoped so both Codex and Claude can rely on it
- do not treat plugin-root `assets/` as a shared runtime resource layer; in current Codex docs they are install-surface presentation assets
- treat plugin manifests and marketplace wiring as install-surface metadata, not as the workflow source of truth

Current plugin scaffolding lives under:

- `plugins/apple-dev-skills/`
- `.agents/plugins/marketplace.json`

Maintainer guidance for those adjacent surfaces now exists in [AGENTS.md](./AGENTS.md):

- Codex plugins are the installable distribution layer that can bundle skills, apps, and MCP servers.
- Codex plugin docs currently document `skills/`, `.app.json`, `.mcp.json`, and `assets/` as the packaged component surfaces.
- Claude Code plugins are a broader distribution layer that may bundle skills, commands, hooks, `bin/`, MCP or LSP config, and plugin-scoped subagents.
- Codex and Claude subagents are delegation/runtime workers, not replacements for repo guidance or top-level skills.

The plugin scaffold in this repo is intentionally conservative:

- Codex-compatible common denominator first
- Claude-only extras layered on top under `plugins/apple-dev-skills/hooks/` and `plugins/apple-dev-skills/bin/`
- no essential workflow behavior should depend on Claude-only extras

## Maintainer Python Tooling

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
bash .github/scripts/sync_shared_snippets.sh
uv run python .github/scripts/validate_skill_creator_contract.py
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

Use the executable skill entrypoints directly, for example `skills/apple-xcode-workflow/scripts/run_workflow.py`.
Use `uv run pytest` for the repo's test suite and other repo-root validation commands.
Run the snippet sync script before validation whenever files under `shared/agents-snippets/` change.

## Install

Install one skill:

```bash
npx skills add gaelic-ghost/apple-dev-skills --skill apple-xcode-workflow
```

Install all active skills:

```bash
npx skills add gaelic-ghost/apple-dev-skills --all
```

Common starting points:

- Xcode work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill apple-xcode-workflow`
- Apple or Swift docs exploration:
  `npx skills add gaelic-ghost/apple-dev-skills --skill explore-apple-swift-docs`
- New Swift package bootstrap:
  `npx skills add gaelic-ghost/apple-dev-skills --skill bootstrap-swift-package`
- New native Apple app bootstrap:
  `npx skills add gaelic-ghost/apple-dev-skills --skill bootstrap-xcode-app-project`
- Existing Xcode repo guidance sync:
  `npx skills add gaelic-ghost/apple-dev-skills --skill sync-xcode-project-guidance`
- Existing Swift package repo guidance sync:
  `npx skills add gaelic-ghost/apple-dev-skills --skill sync-swift-package-guidance`

## Migration

This repo previously experimented with a router layer and later removed it.

| Historical ID | Current State |
| --- | --- |
| `apple-skills-router-advise-install` | removed |
| `apple-skills-router` | removed |
| `apple-xcode-workflow-execute` | `apple-xcode-workflow` |
| `apple-dash-docset-manage` | `explore-apple-swift-docs` |
| `apple-dash-docsets` | deprecated compatibility shim that redirects to `explore-apple-swift-docs` |
| `apple-swift-package-bootstrap` | deprecated compatibility shim that redirects to `bootstrap-swift-package` |

The current active skill surface now includes both guidance-sync skills alongside the app and package bootstrap surfaces.

Future rename cleanup for the remaining `apple-*` skills is tracked in [ROADMAP.md](./ROADMAP.md).

## AGENTS Guidance

Repository-consumable Swift and Apple baseline policy snippets:

- [shared/agents-snippets/apple-xcode-project-core.md](./shared/agents-snippets/apple-xcode-project-core.md)
- [shared/agents-snippets/apple-swift-package-core.md](./shared/agents-snippets/apple-swift-package-core.md)

Use these snippets for cross-project standards that belong in end-user `AGENTS.md`.

- Each active skill ships the local snippet copy that matches its workflow surface so individually installed skills can recommend it directly.
- For Apple or Swift docs exploration, prefer `explore-apple-swift-docs` over older Dash-specific guidance.
- For new Swift package repositories, `bootstrap-swift-package` copies its full `assets/AGENTS.md` template, which already incorporates the Swift-package baseline.
- For existing Xcode app repositories, prefer `sync-xcode-project-guidance` over manual snippet merging when the goal is to align repo guidance.
- For existing Swift package repositories, prefer `sync-swift-package-guidance` over manual snippet merging when the goal is to align repo guidance.
- For existing repositories, use the shared snippets for targeted updates or the skill-local copies when reading an installed skill in isolation.
- For cross-repo AGENTS drift and documentation alignment workflows, use dedicated docs-alignment skills maintained outside this repository.

## Deprecated Skill Note

`apple-dash-docsets` is no longer part of the active skill surface.

- Use `explore-apple-swift-docs` for Apple or Swift docs exploration.
- The new docs skill still includes Dash compatibility and optional Dash install follow-up.
- The old skill remains on disk only as a compatibility redirect for older references.

`apple-swift-package-agents-sync` is no longer part of the active skill surface.

- New repository scaffolds should use `bootstrap-swift-package`.
- Existing Swift package repositories should use `sync-swift-package-guidance` when AGENTS maintenance is needed.

## Repository Layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── README.md
├── ROADMAP.md
├── docs/
│   └── maintainers/
│       ├── reality-audit.md
│       └── workflow-atlas.md
├── plugins/
│   └── apple-dev-skills/
│       ├── .codex-plugin/
│       ├── .claude-plugin/
│       ├── assets/
│       ├── bin/
│       ├── hooks/
│       └── skills/
├── shared/
│   └── agents-snippets/
│       ├── apple-swift-package-core.md
│       └── apple-xcode-project-core.md
└── skills/
    ├── bootstrap-xcode-app-project/
    ├── apple-dash-docsets/
    ├── apple-swift-package-bootstrap/
    ├── apple-xcode-workflow/
    ├── bootstrap-swift-package/
    ├── explore-apple-swift-docs/
    ├── sync-swift-package-guidance/
    └── sync-xcode-project-guidance/
```

The plugin directories are packaging scaffolds. The canonical workflow content still lives under root `skills/` until packaging sync is fully implemented.

Maintainers: authoritative skill-authoring resources live in `AGENTS.md`.

## License

See [LICENSE](./LICENSE).
