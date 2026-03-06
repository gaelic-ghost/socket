# apple-dev-skills

Canonical Codex skills for Apple development workflows focused on Xcode execution, Dash docsets, and Swift package bootstrap.

## Active Skills

- `apple-xcode-workflow`
  - Top-level Apple and Swift skill for Xcode work, execution, diagnostics, toolchains, mutation decisions, and docs lookup.
- `apple-dash-docsets`
  - Top-level Dash skill with one entry point and internal `search -> install -> generate` workflows.
- `apple-swift-package-bootstrap`
  - Top-level skill for new Swift package scaffolding only, with verification and `AGENTS.md` generation.

Every active skill now follows the same documentation contract:

- one primary workflow per request type
- explicit `inputs`, `defaults`, `status`, `path_type`, and `output`
- named `fallback` and `handoff` behavior
- customization knobs labeled `policy-only` unless runtime enforcement exists

Maintainer-facing workflow diagrams, input/output contracts, and Agent ↔ User UX maps live in [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md). Audit procedure and source-of-truth guidance live in [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md).

## Maintainer Python Tooling

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
bash .github/scripts/sync_apple_swift_core_snippet.sh
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

Use `uv run python ...` for repo-local Python helper execution and validation.
Run the snippet sync script before validation whenever `shared/agents-snippets/apple-swift-core.md` changes.

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
- Dash work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill apple-dash-docsets`
- New Swift package bootstrap:
  `npx skills add gaelic-ghost/apple-dev-skills --skill apple-swift-package-bootstrap`

## Migration

This repo previously experimented with a router layer and later removed it.

| Historical ID | Current State |
| --- | --- |
| `apple-skills-router-advise-install` | removed |
| `apple-skills-router` | removed |
| `apple-xcode-workflow-execute` | `apple-xcode-workflow` |
| `apple-dash-docset-manage` | `apple-dash-docsets` |

The active public surface is now the three top-level skills listed above. Update install commands, references, and automation prompts accordingly.

## AGENTS Guidance

Repository-consumable Swift/Apple baseline policy snippet:

- [shared/agents-snippets/apple-swift-core.md](./shared/agents-snippets/apple-swift-core.md)

Use this snippet for cross-project standards that belong in end-user `AGENTS.md`.

- Each active skill ships its own local copy of this snippet so individually installed skills can recommend it directly.
- For new Swift package repositories, `apple-swift-package-bootstrap` copies its full `assets/AGENTS.md` template, which already incorporates this baseline.
- For existing repositories, use the shared snippet for targeted updates or the skill-local copies when reading an installed skill in isolation.
- For cross-repo AGENTS drift and documentation alignment workflows, use dedicated docs-alignment skills maintained outside this repository.

## Retired Skill Note

`apple-swift-package-agents-sync` is no longer part of the active skill surface.

- New repository scaffolds should use `apple-swift-package-bootstrap`.
- Existing repositories should use the shared snippet plus external docs-alignment skills when AGENTS maintenance is needed.

## Repository Layout

```text
.
├── README.md
├── ROADMAP.md
├── docs/
│   └── maintainers/
│       ├── reality-audit.md
│       └── workflow-atlas.md
├── shared/
│   └── agents-snippets/
│       └── apple-swift-core.md
└── skills/
    ├── apple-xcode-workflow/
    ├── apple-dash-docsets/
    └── apple-swift-package-bootstrap/
```

Maintainers: authoritative skill-authoring resources live in `AGENTS.md`.

## License

See [LICENSE](./LICENSE).
