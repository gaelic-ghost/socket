# Plugin Packaging Strategy

This document records the current packaging decision for the `socket` superproject.

## Working Rule

Package child repositories as independent plugins first.

If a combined plugin becomes useful later, add that as a separate `socket`-level packaging layer instead of redefining the child repositories around bundle semantics.

## Why

This keeps the near-term model simpler and lowers coupling:

- each child repository can be developed and versioned independently
- the repo-root marketplace can list plugins one by one without inventing a bundle model too early
- child repositories that carry their own repo-local marketplace can be tracked as standalone Git-backed marketplace sources without cloning `socket`
- aggregate plugins can be added later as a deliberate packaging feature
- reverting back toward fully independent repos stays easier if the superproject experiment fails

## What Is Deferred

These are intentionally not phase-one requirements:

- one plugin composed from multiple child repositories
- a single aggregate plugin manifest that becomes the source of truth for several subtree directories
- cross-repo bundle ownership rules for hooks, apps, or MCP server packaging

## Immediate Packaging Direction

The current direction is:

1. keep monorepo-owned child repos as ordinary directories under `socket/plugins/` when they no longer need an upstream subtree sync target
2. preserve explicit subtree sync only for child repos that still need to publish back out independently
3. keep the `socket` marketplace ready to list each plugin independently
4. only add marketplace entries for child repos that actually ship `.codex-plugin/plugin.json`
5. keep root `socket` docs aligned with child packaging moves and coordinated release-prep changes instead of treating the marketplace file as the only source of truth
6. keep the maintained version-bearing manifests aligned on one shared semantic version through the root release-version workflow instead of hand-editing scattered files
7. for child repositories that should remain independently cloneable, keep a repo-local `.agents/plugins/marketplace.json` whose local entry points at that child's plugin root
8. make Git-backed marketplace commands the default user install and update path for both `socket` and standalone plugin repositories

Recent monorepo-owned examples follow that rule directly: `things-app` and `cardhop-app` both package from their child-repo roots while keeping bundled MCP server code under each child repo's top-level `mcp/` directory. `apple-dev-skills` follows the same child-root packaging rule while using a root `.mcp.json` to register Xcode's built-in `xcrun mcpbridge` server instead of bundling separate server code.

Child-repo internal layout changes do not automatically imply root marketplace changes. If a child repo keeps the same packaged plugin root, keep the `socket` marketplace path stable and only update the root docs to explain the child's new internal layout. Recent example: `things-app` keeps its marketplace path at `./plugins/things-app` while its bundled MCP server lives at top-level `mcp/` inside that child repo.

## Speak Swiftly Catalog Split

`SpeakSwiftlyServer` is the exception that moved away from local child-root packaging in `socket`.

The older `socket` marketplace entry pointed at `./plugins/SpeakSwiftlyServer`, which is the full pull-only subtree mirror of the standalone Swift package. That kept the plugin install technically valid because the subtree root contains `.codex-plugin/plugin.json`, `.mcp.json`, `skills/`, and `hooks/`, but it also coupled the Socket catalog entry to the entire Swift package source tree, tests, maintainer docs, and release workflow.

The current direction is one canonical plugin payload exposed through two marketplace catalogs:

- `gaelic-ghost/SpeakSwiftlyServer` remains the canonical repository for the `speak-swiftly` plugin payload.
- `gaelic-ghost/SpeakSwiftlyServer` keeps its own repo-local marketplace so users can run `codex plugin marketplace add gaelic-ghost/SpeakSwiftlyServer`.
- `gaelic-ghost/socket` lists the same canonical plugin payload as a Git-backed root-plugin marketplace entry so users can run `codex plugin marketplace add gaelic-ghost/socket`, choose the Socket catalog, and enable `Speak Swiftly` there.
- `plugins/SpeakSwiftlyServer/` remains a pull-only subtree mirror only while it is useful for source, release, and superproject accounting. It is not the plugin payload path for Socket users.

The plugin identity should be `speak-swiftly`, and the display name should be `Speak Swiftly`. The old `speak-swiftly-server` plugin id needs explicit migration handling because existing Codex config and plugin cache entries may still be keyed to that name.

The canonical plugin payload in `SpeakSwiftlyServer` should own the Codex-facing distribution surface:

- plugin identity, install metadata, and user-facing prompts
- MCP registration for the local service endpoint
- final-reply speech hooks
- focused operator skills
- doctor or install-check scripts for plugin, hook, runtime, and voice-profile health
- migration guidance from the old `speak-swiftly-server` plugin entry

The standalone `SpeakSwiftlyServer` repository should also remain the source of truth for the Swift package, executable, LaunchAgent behavior, embedded API, HTTP/MCP implementation, API docs, release notes, and live-service validation.

The Socket catalog entry named `speak-swiftly` points at the Git-backed `gaelic-ghost/SpeakSwiftlyServer` plugin source instead of `./plugins/SpeakSwiftlyServer`. Because the plugin root is the repository root, it uses the Codex marketplace source shape for a Git-backed root plugin rather than a `git-subdir` entry. Run the marketplace audit and `uv run scripts/validate_socket_metadata.py` after changes to this entry.

Update README, ROADMAP, subtree workflow guidance, and any SpeakSwiftlyServer-facing install docs in the same pass when this catalog model changes so users see one coherent story: Codex users can install `Speak Swiftly` from either the Git-backed `socket` marketplace or the standalone `SpeakSwiftlyServer` marketplace; app embedders use `SpeakSwiftlyServer` as a Swift package.

For ordinary Speak Swiftly plugin changes, edit the standalone `SpeakSwiftlyServer` checkout. `socket` only needs a follow-up change when the marketplace entry itself, root docs, root validation behavior, or a coordinated `socket` release changes. Because the Socket entry tracks the standalone repository's `main` branch, a plugin payload edit in `SpeakSwiftlyServer` does not require copying files, subtree-pulling the source mirror, or bumping a Socket version by itself.

The doctor should be able to detect and repair duplicate installs or enablement caused by users adding both marketplaces. Its repair preference is the Socket marketplace entry: keep `speak-swiftly@socket` enabled, then disable or remove the duplicate standalone-marketplace plugin enablement after reporting the intended change. The standalone marketplace remains fully functional for users who only want Speak Swiftly, but Socket is the preferred catalog when both are configured.

`socket` itself still does not define an aggregate root plugin above the child repos. The root Codex-facing surface here is the marketplace catalog, not a packaged plugin payload or a second shared plugin bundle.

OpenAI's current [Codex plugin docs](https://developers.openai.com/codex/plugins/build) allow local repo marketplaces, personal marketplaces, and Git-backed marketplace sources through [`codex plugin marketplace add`](https://developers.openai.com/codex/plugins/build#add-a-marketplace-from-the-cli). The preferred user install and update path is therefore Git-backed:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

Use the `socket` marketplace as the all-in-one catalog when users want Gale's plugin collection or need companion skills from sibling child plugins. After adding `socket`, users still choose which plugin entries to install or enable from the Codex plugin directory; adding the marketplace exposes the catalog, it does not imply that every child plugin is installed automatically.

For child repositories such as `apple-dev-skills` and `SpeakSwiftlyServer`, the clean standalone path is a child-owned repo marketplace that points at `./` when the repository root is the plugin root:

```bash
codex plugin marketplace add gaelic-ghost/apple-dev-skills
codex plugin marketplace add gaelic-ghost/SpeakSwiftlyServer
```

`socket` can list ordinary local child plugins as `./plugins/<child>` from the superproject marketplace. For Speak Swiftly, prefer a Git-backed entry pointing at `gaelic-ghost/SpeakSwiftlyServer` so the Socket catalog and standalone catalog install the same canonical payload instead of carrying two copies. Use explicit refs such as `gaelic-ghost/socket@vX.Y.Z` only for pinned reproducible installs. Manual local marketplace roots and copied payload directories are development, unpublished-testing, and fallback tools rather than the default user-facing path.

When a user has already migrated from an older copied-plugin or personal-local-marketplace install to the Git-backed marketplace, use the repo-owned cleanup helper instead of hand-editing home-directory files:

```bash
uv run scripts/cleanup_legacy_socket_installs.py
uv run scripts/cleanup_legacy_socket_installs.py --apply
```

The helper's job is intentionally narrow. It removes known legacy `socket` entries from `~/.agents/plugins/marketplace.json` and copied personal payload directories such as `~/.codex/plugins/apple-dev-skills` after backing them up. It leaves Codex's installed cache under `~/.codex/plugins/cache/` alone, because that cache is Codex-owned install state for current marketplace entries.

## Follow-up Decision

Once several child repos have stable plugin packaging, decide whether `socket` needs:

- only an independent plugin catalog, or
- an additional aggregate plugin layer for curated bundles
