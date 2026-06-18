# Plugin Install Testing

Use this guide when testing the Socket marketplace or one child plugin
marketplace without touching personal production Codex installs.

## Safety Model

Gale's personal Codex scope should stay reserved for stable production installs.
Marketplace add, remove, and upgrade tests should use an isolated temporary
`CODEX_HOME` so test marketplaces, caches, and config do not rewrite
`~/.codex/config.toml` or the production plugin cache.

The local checkout test and the Git-backed user-path test answer different
questions:

- Local checkout tests prove the current branch's marketplace metadata before
  the branch is merged or tagged.
- Git-backed tests prove the user-facing marketplace source that Codex can fetch
  from GitHub.

`codex plugin marketplace upgrade <name>` only applies to Git-backed
marketplaces. A local checkout marketplace should be added, inspected, removed,
and then discarded; trying to upgrade it should fail because it is not a Git
marketplace.

For release preparation, the repo-owned evidence command automates the Socket
local checkout add/remove path below and records the result with the current
Dependabot alert query:

```bash
scripts/release.sh release-evidence
```

It writes `.socket-release-evidence.json` in the worktree. The file is ignored
by Git, tied to the current commit, and consumed by `scripts/release.sh
release-notes X.Y.Z`. Keep the manual commands below for focused debugging,
child-specific manifest inspection, and Git-backed user-path tests.

## Socket Local Checkout Test

Run this from the `socket` checkout when validating branch-local marketplace
changes:

```bash
SOCKET_REPO="$(pwd)"
TEST_CODEX_HOME="$(mktemp -d /private/tmp/socket-codex-home.XXXXXX)"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace add "$SOCKET_REPO"

jq '.plugins[] | select(.name == "speak-swiftly")' \
  "$SOCKET_REPO/.agents/plugins/marketplace.json"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace remove socket
test ! -s "$TEST_CODEX_HOME/config.toml"
rm -rf "$TEST_CODEX_HOME"
```

Expected result for the Speak Swiftly catalog split:

- Codex reports an added marketplace named `socket` from the local checkout.
- The local marketplace entry contains `name: speak-swiftly`.
- The entry uses `source.source: url`, points at
  `https://github.com/gaelic-ghost/SpeakSwiftlyServer.git`, and sets
  `ref: main`.
- Removing `socket` leaves no configured marketplace in the temporary Codex
  home.

For ordinary child-plugin releases, inspect the changed plugin entry instead of
`speak-swiftly`. The smoke check should verify:

- Codex reports an added marketplace named `socket` from the local checkout.
- The changed child plugin entry has the expected `policy.installation` value.
- The changed child plugin entry points at the expected source path or
  Git-backed source.
- The changed child plugin root exposes `.codex-plugin/plugin.json`.
- The changed child plugin manifest exposes every expected `skills`, `hooks`,
  `mcpServers`, or `apps` component.
- Removing `socket` leaves no configured marketplace in the temporary Codex
  home.

## Socket Git-Backed Test

Run this after the Socket branch has landed in GitHub state that users can
fetch:

```bash
TEST_CODEX_HOME="$(mktemp -d /private/tmp/socket-codex-home.XXXXXX)"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace add gaelic-ghost/socket
CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace upgrade socket

jq '.plugins[] | select(.name == "speak-swiftly")' \
  "$TEST_CODEX_HOME/.tmp/marketplaces/socket/.agents/plugins/marketplace.json"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace remove socket
test ! -s "$TEST_CODEX_HOME/config.toml"
rm -rf "$TEST_CODEX_HOME"
```

Expected result:

- Codex reports `source_type = "git"` for `marketplaces.socket`.
- `upgrade socket` succeeds.
- The cached Socket marketplace contains the same `speak-swiftly` Git-backed
  root-plugin entry as the local checkout.

If the cached Socket marketplace still shows the old local
`./plugins/SpeakSwiftlyServer` entry, the test is reading an older Git revision.
Check `last_revision` in the temporary `config.toml` and wait until the intended
Socket branch has merged or install with an explicit test ref.

## Apple Dev Skills Compatibility Marketplace Test

The standalone `gaelic-ghost/apple-dev-skills` repository is a compatibility
marketplace pointer. It should not carry a local skill payload, `.codex-plugin`
root, or `.agents/skills` discovery mirror. Its marketplace entry should keep
the `apple-dev-skills` marketplace name while sourcing the plugin payload from
Socket at `./plugins/apple-dev-skills`.

Run this after the standalone compatibility pointer has landed in GitHub state
that users can fetch:

```bash
TEST_CODEX_HOME="$(mktemp -d /private/tmp/apple-dev-skills-codex-home.XXXXXX)"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace add gaelic-ghost/apple-dev-skills
CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace upgrade apple-dev-skills

jq '.plugins[] | select(.name == "apple-dev-skills")' \
  "$TEST_CODEX_HOME/.tmp/marketplaces/apple-dev-skills/.agents/plugins/marketplace.json"

test ! -e "$TEST_CODEX_HOME/.tmp/marketplaces/apple-dev-skills/skills"
test ! -e "$TEST_CODEX_HOME/.tmp/marketplaces/apple-dev-skills/.codex-plugin"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace remove apple-dev-skills
test ! -s "$TEST_CODEX_HOME/config.toml"
rm -rf "$TEST_CODEX_HOME"
```

Expected result:

- Codex reports `source_type = "git"` for `marketplaces.apple-dev-skills`.
- `upgrade apple-dev-skills` succeeds.
- The cached compatibility marketplace entry uses `source.source: git-subdir`,
  points at `https://github.com/gaelic-ghost/socket.git`, sets
  `path: ./plugins/apple-dev-skills`, and sets `ref: main`.
- The cached compatibility repository root does not expose a stale local
  `skills/` tree or `.codex-plugin/` root.
- Removing `apple-dev-skills` leaves no configured marketplace in the temporary
  Codex home.

Codex does not materialize the nested Socket `git-subdir` payload merely by
adding or upgrading the compatibility marketplace. To inspect the actual
Socket-hosted `apple-dev-skills` plugin manifest, run the Socket Git-backed test
above and inspect
`.tmp/marketplaces/socket/plugins/apple-dev-skills/.codex-plugin/plugin.json`.

## Standalone SpeakSwiftlyServer Test

The standalone repository owns the plugin payload. Run standalone install tests
from the `SpeakSwiftlyServer` checkout and keep detailed payload validation
there. Socket tests should only prove that Socket lists the same canonical
payload by Git-backed reference.

The current Codex CLI registers both local and Git-backed
`gaelic-ghost/SpeakSwiftlyServer` marketplaces as
`speak-swiftly-server-local`. Use the marketplace name Codex reports instead of
guessing from the repository name.

```bash
TEST_CODEX_HOME="$(mktemp -d /private/tmp/speak-swiftly-codex-home.XXXXXX)"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace add gaelic-ghost/SpeakSwiftlyServer
CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace upgrade speak-swiftly-server-local

jq '.plugins[] | select(.name == "speak-swiftly")' \
  "$TEST_CODEX_HOME/.tmp/marketplaces/speak-swiftly-server-local/.agents/plugins/marketplace.json"

jq '{name, version, displayName: .interface.displayName, mcpServers, hooks, skills}' \
  "$TEST_CODEX_HOME/.tmp/marketplaces/speak-swiftly-server-local/.codex-plugin/plugin.json"

CODEX_HOME="$TEST_CODEX_HOME" codex plugin marketplace remove speak-swiftly-server-local
test ! -s "$TEST_CODEX_HOME/config.toml"
rm -rf "$TEST_CODEX_HOME"
```

Expected result:

- The standalone marketplace entry contains `name: speak-swiftly` and
  `source.path: ./`.
- The cached plugin manifest declares `name: speak-swiftly`, display name
  `Speak Swiftly`, `mcpServers: ./.mcp.json`, `hooks: ./hooks/hooks.json`, and
  `skills: ./skills/`.
- Removing `speak-swiftly-server-local` leaves no configured marketplace in the
  temporary Codex home.

## Session Availability

These commands prove the marketplace and cached plugin files. They do not prove
that an already-running Codex session has refreshed its visible plugin tools and
skills. For that final check, start a fresh Codex session after the add or
upgrade and inspect the Plugin Directory or the model-visible tool list.
