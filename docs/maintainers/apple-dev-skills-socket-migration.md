# Apple Dev Skills Socket Migration

This note records the completed move of `apple-dev-skills` from a subtree-published standalone plugin payload into the Socket superproject while preserving update behavior for users who only installed `gaelic-ghost/apple-dev-skills`.

## Goals

- Make `socket/plugins/apple-dev-skills` the canonical authored plugin payload.
- Stop requiring routine `git subtree push --prefix=plugins/apple-dev-skills apple-dev-skills main` during Socket releases.
- Keep `codex plugin marketplace add gaelic-ghost/apple-dev-skills` useful as a compatibility path.
- Keep `codex plugin marketplace upgrade apple-dev-skills` working for existing standalone marketplace users.
- Point users toward `codex plugin marketplace add gaelic-ghost/socket` as the preferred catalog.
- Avoid duplicate payload ownership between Socket and the standalone Apple Dev Skills repository.

## Non-Goals

- Do not rename the `apple-dev-skills` plugin identity.
- Do not remove the `apple-dev-skills` entry from the Socket marketplace.
- Do not make Socket an aggregate root plugin; Socket remains a marketplace catalog.
- Do not strand existing standalone marketplace installs.

## Current State

- Socket lists `apple-dev-skills` as a local child plugin at `./plugins/apple-dev-skills`.
- The standalone `gaelic-ghost/apple-dev-skills` repository is now a compatibility marketplace and README pointer as of `v6.14.1`.
- The standalone repository preserves the `apple-dev-skills` marketplace name, but its marketplace entry sources the plugin payload from `https://github.com/gaelic-ghost/socket.git` at `./plugins/apple-dev-skills`.
- Socket releases treat substantive `plugins/apple-dev-skills` changes as ordinary monorepo-owned payload changes and do not push them back to the compatibility repository.

## Phase 1: Standalone Compatibility Release

Status: complete in `gaelic-ghost/apple-dev-skills` `v6.14.1`.

Phase 1 changes only the standalone `gaelic-ghost/apple-dev-skills` repository.

1. Replace the standalone README with a short compatibility notice:
   - Apple Dev Skills now lives in Socket.
   - Preferred install path: `codex plugin marketplace add gaelic-ghost/socket`.
   - Existing standalone users may continue to run `codex plugin marketplace upgrade apple-dev-skills`.
   - New feature work, issue tracking, and release notes live in Socket.
2. Keep a repo-local `.agents/plugins/marketplace.json`.
3. Change the standalone marketplace entry to keep the marketplace/plugin name stable while sourcing the payload from Socket:

   ```json
   {
     "name": "apple-dev-skills",
     "source": {
       "source": "git-subdir",
       "url": "https://github.com/gaelic-ghost/socket.git",
       "path": "./plugins/apple-dev-skills",
       "ref": "main"
     },
     "policy": {
       "installation": "AVAILABLE",
       "authentication": "ON_INSTALL"
     },
     "category": "Developer Tools"
   }
   ```

4. Keep or add a minimal validation check that confirms the compatibility marketplace points at Socket.
5. Publish a standalone patch release.
6. Smoke test in an isolated `CODEX_HOME`:
   - `codex plugin marketplace add gaelic-ghost/apple-dev-skills`
   - `codex plugin marketplace upgrade apple-dev-skills`
   - verify the cached marketplace uses `source_type = "git"`
   - verify the cached plugin manifest under the Socket subdirectory exposes `apple-dev-skills`
   - remove the marketplace and confirm the temporary config is empty

After Phase 1, users who installed only `apple-dev-skills` still have a working marketplace and upgrade path, but the payload comes from Socket.

## Phase 2: Socket Ownership Conversion

Status: complete.

Phase 2 changed Socket after the compatibility release became available.

1. Treat `plugins/apple-dev-skills` as monorepo-owned source, not a subtree-managed child.
2. Remove `apple-dev-skills` from Socket subtree gates.
3. Update Socket README, CONTRIBUTING, roadmap, release, subtree, and packaging docs.
4. Update plugin install testing docs with an Apple Dev Skills compatibility test.
5. Keep duplicate-install guidance: prefer `apple-dev-skills@socket` when both Socket and standalone marketplaces are configured, while preserving the standalone marketplace as a compatibility route for users who only want Apple Dev Skills.
6. Run full Socket validation and publish a Socket release.

## Duplicate Install Policy

If both Socket and standalone Apple Dev Skills marketplaces are configured, prefer the Socket marketplace entry:

- keep `apple-dev-skills@socket`
- disable or remove duplicate standalone enablement only after explaining the change
- preserve the standalone marketplace for users who intentionally want only Apple Dev Skills

This mirrors the Speak Swiftly duplicate-enable repair preference, but with Socket as the canonical payload owner.

## Release Accounting

Phase 1 is a standalone Apple Dev Skills patch release. It should not require a Socket release unless Socket docs or metadata change in the same pass.

Phase 2 is a Socket release. Once Phase 2 lands, ordinary Socket releases no longer need subtree pull or push accounting for Apple Dev Skills.
