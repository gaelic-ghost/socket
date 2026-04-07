# apple-dev-skills

Canonical Apple development skills with a plugin-first packaging layout for Codex and Claude Code.

## Active Skills

- `xcode-app-project-workflow`
  - Top-level Apple and Swift execution skill for Xcode work, diagnostics, toolchains, mutation decisions, and guarded fallback planning.
- `explore-apple-swift-docs`
  - Top-level docs skill for Apple and Swift docs exploration across Xcode MCP docs, Dash, and official web docs, with optional Dash follow-up when needed.
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

Every active skill now follows the same documentation contract:

- one primary workflow per request type
- explicit `inputs`, `defaults`, `status`, `path_type`, and `output`
- named `fallback` and `handoff` behavior
- a clear customization stance, including explicit `policy-only` knobs or an explicit “no durable customization surface” statement

Maintainer-facing workflow diagrams, input and output contracts, and Agent ↔ User UX maps live in [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md). Audit procedure and source-of-truth guidance live in [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md). The current customization-system decision and follow-up plan live in [docs/maintainers/customization-consolidation-review.md](./docs/maintainers/customization-consolidation-review.md).

## Packaging and Delegation

This repository now tracks a plugin-first packaging plan while keeping root `skills/` as the canonical workflow-authoring surface.

Shared guidance across both ecosystems:

- keep reusable workflow behavior in root `skills/`
- keep deterministic helper logic skill-scoped so both Codex and Claude can rely on it
- treat plugin manifests, hooks, and marketplace wiring as install-surface metadata, not as the workflow source of truth
- use POSIX symlink mirrors for local Codex and Claude project discovery on macOS and Linux:
  - `.agents/skills -> ../skills`
  - `.claude/skills -> ../skills`
  - `plugins/apple-dev-skills/skills -> ../../skills`

Current plugin scaffolding lives under:

- `plugins/apple-dev-skills/`
- `.agents/skills`
- `.claude/skills`
- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`

For local Codex plugin development, treat `plugins/apple-dev-skills/` as the installable plugin root and use the official marketplace-based plugin install flow documented by Codex.
For local Claude development, point `claude --plugin-dir /absolute/path/to/plugins/apple-dev-skills` at the tracked plugin source root.

Maintainer guidance for those adjacent surfaces now exists in [AGENTS.md](./AGENTS.md):

- Codex plugins are the installable distribution layer that can bundle skills, apps, and MCP servers.
- Codex plugin docs currently document `skills/`, `.app.json`, `.mcp.json`, and `assets/` as the packaged component surfaces.
- Claude Code plugins are a broader distribution layer that may bundle skills, commands, hooks, `bin/`, MCP or LSP config, and plugin-scoped subagents.
- Codex and Claude subagents are delegation/runtime workers, not replacements for repo guidance or top-level skills.
- Track canonical plugin source trees and shared marketplace catalogs in git.
- Keep consumer-side install copies, caches, and machine-local runtime state out of git.

The plugin package in this repo is intentionally conservative:

- Codex-compatible common denominator first
- Claude-only extras layered on top under `plugins/apple-dev-skills/hooks/` and `plugins/apple-dev-skills/bin/`
- no essential workflow behavior should depend on Claude-only extras

## Install Surfaces

Repo-local Codex packaging and personal Codex installs are different surfaces and the docs should keep them separate:

- repo-local packaged plugin root: `plugins/apple-dev-skills/`
- repo-local Codex marketplace: `.agents/plugins/marketplace.json`
- personal Codex install root: `~/.codex/plugins/apple-dev-skills`
- personal Codex marketplace: `~/.agents/plugins/marketplace.json`

The repo also tracks a repo-root Claude marketplace catalog at `.claude-plugin/marketplace.json` for Git-backed sharing, while direct local Claude development should still use `claude --plugin-dir`.

Local Codex install lifecycle work such as install, update, uninstall, verify, repair, enable, disable, and promote belongs to the maintainer workflow in `install-plugin-to-socket`, not to the bootstrap or sync skills in this repository.

After changing a repo-local marketplace entry, fully restart Codex, inspect `~/.codex/log/codex-tui.log` if the plugin does not appear, and remember that `/plugins` ordering may not be intuitive.

## Maintainer Python Tooling

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

Use the executable skill entrypoints directly, for example `skills/xcode-app-project-workflow/scripts/run_workflow.py`.
For Python wrapper and customization entrypoints that declare inline `uv` dependencies such as `PyYAML`, prefer `uv run scripts/run_workflow.py ...` and `uv run scripts/customization_config.py ...` in consuming repos instead of assuming a plain `python` environment has those dependencies available.
Use targeted `uv run --group dev pytest tests/...` runs while iterating and a full `uv run --group dev pytest` pass before finalizing repo-wide maintenance.
Keep `ruff` and `mypy` available as maintainer-side `uv` tools even when a given repo pass only needs the test suite.

## Install

Standalone skill installation is handled through the Vercel `skills` CLI against root `skills/`. Plugin packaging and local marketplace wiring target `plugins/apple-dev-skills/`. For local project discovery on macOS and Linux, this repo also exposes `.agents/skills` and `.claude/skills` as symlink mirrors into root `skills/`.

### Local Plugin Development Install

Use the packaged plugin root at `plugins/apple-dev-skills/` when smoke-testing Codex plugin wiring. The canonical local author flow is still the official Codex marketplace path:

1. Point a repo or personal marketplace entry at `./plugins/apple-dev-skills`.
2. Set `policy.installation` to `AVAILABLE`.
3. Restart Codex.
4. Open `/plugins` in Codex and install the plugin from that marketplace.

Repo-scoped marketplace shape:

```json
{
  "name": "gaelic-ghost-apple-dev-skills",
  "interface": {
    "displayName": "Gale's Apple Plugins"
  },
  "plugins": [
    {
      "name": "apple-dev-skills",
      "source": {
        "source": "local",
        "path": "./plugins/apple-dev-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Keep `source.path` relative to the marketplace root, restart Codex after marketplace changes, and verify the plugin appears in `/plugins`.

If Gale is using a local helper such as `install-plugin-to-socket`, treat that as an optional machine-local maintainer shortcut rather than part of the repository's portable install contract.

### Claude Marketplace Development

For direct local Claude work, load the tracked plugin root with `claude --plugin-dir /absolute/path/to/plugins/apple-dev-skills`.

If the repository is being shared as a Claude marketplace, use the repo-root catalog at `.claude-plugin/marketplace.json` and keep plugin paths relative to that marketplace root.

Install one skill:

```bash
npx skills add gaelic-ghost/apple-dev-skills --skill xcode-app-project-workflow
```

Install all active skills:

```bash
npx skills add gaelic-ghost/apple-dev-skills --all
```

Common starting points:

- Xcode work:
  `npx skills add gaelic-ghost/apple-dev-skills --skill xcode-app-project-workflow`
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
- Shared repo-maintenance toolkit:
  `npx skills add gaelic-ghost/productivity-skills --skill repo-maintenance-toolkit`

## Migration

This repo previously experimented with a router layer and later removed it.

| Historical ID | Current State |
| --- | --- |
| `apple-skills-router-advise-install` | removed |
| `apple-skills-router` | removed |
| `apple-xcode-workflow-execute` | `xcode-app-project-workflow` |
| `apple-dash-docset-manage` | `explore-apple-swift-docs` |
| `apple-dash-docsets` | removed in `v4.0.0`; use `explore-apple-swift-docs` |
| `apple-swift-package-bootstrap` | removed in `v4.0.0`; use `bootstrap-swift-package` |

The shared repo-maintenance toolkit now lives in `../productivity-skills`. This repository keeps a vendored toolkit snapshot under `shared/repo-maintenance-toolkit/` so the Apple bootstrap and guidance-sync skills can still install or refresh the same managed file set without depending on a second repo at runtime.

## AGENTS Guidance

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
├── plugins/
│   └── apple-dev-skills/
│       ├── .codex-plugin/
│       ├── .claude-plugin/
│       ├── assets/
│       ├── bin/
│       ├── hooks/
│       └── skills -> ../../skills
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
    ├── structure-swift-sources/
    ├── sync-swift-package-guidance/
    ├── sync-xcode-project-guidance/
    └── xcode-app-project-workflow/
```

The canonical workflow content still lives under root `skills/`. The discovery mirrors are local POSIX symlinks for macOS and Linux development, including WSL 2 when Windows is involved.

Maintainers: authoritative skill-authoring resources live in `AGENTS.md`.

## Maintainer References

- Agent Skills Standard: <https://agentskills.io/home>
- OpenAI Codex Skills: <https://developers.openai.com/codex/skills>
- OpenAI Codex AGENTS.md configuration: <https://developers.openai.com/codex/guides/agents-md/>
- Claude Code Plugins: <https://code.claude.com/docs/en/plugins>

## License

See [LICENSE](./LICENSE).
