# Application Support Config Plan

Status: implemented on `runtime/application-support-config`. The active LaunchAgent path now points
directly at `~/Library/Application Support/SpeakSwiftlyServer/server.yaml`, and install/refresh
paths seed that canonical file from a bundled default when it is missing.

## Context

The live `v4.3.4` LaunchAgent-backed service starts from a copied config alias at
`~/Library/SpeakSwiftlyServer/launch-agent-server.yaml` when the canonical config path contains
spaces. That alias is a patch-level durability fix: it moved the copied config out of
`~/Library/Caches`, which macOS and maintenance tools can remove independently of the installed
LaunchAgent plist.

The cleaner target is simpler: the installed service should derive its durable config root from
Foundation's standard Application Support URL, read the active config directly from
`~/Library/Application Support/SpeakSwiftlyServer/server.yaml`, and use the package bundle only for
shipped read-only defaults, templates, and resources.

## Current Failure Mode

The original alias existed because LaunchAgent installs that pointed `APP_CONFIG_FILE` directly at
`~/Library/Application Support/SpeakSwiftlyServer/server.yaml` failed while loading YAML config
through the current `swift-configuration` file-provider path. The practical symptom was that a
canonical config path containing `Application Support` was not safe enough for service startup.

The `v4.3.4` alias path avoids the immediate failure, but it still leaves two config files with
different jobs:

- the canonical operator-owned config in Application Support
- the copied LaunchAgent startup config outside Application Support

That duplication is useful only as a temporary compatibility surface. It should disappear once the
server can load the canonical path directly and reliably.

## Target Layout

Use the package bundle for shipped read-only inputs:

- default config templates
- schemas or documented example config files
- package resources such as `default.metallib`
- seed data that should be copied into user state before mutation

Use Application Support for durable per-user service state:

- `server.yaml`
- `runtime/configuration.json`
- `runtime/text-profiles.json`
- voice profile state
- any generated or user-edited runtime files that must survive restarts and cache cleanup

Use Caches only for rebuildable disposable data:

- temporary derived files
- short-lived diagnostics that can be regenerated
- noncritical indexes or scratch state

No LaunchAgent-critical config should live in Caches.

Resolve the Application Support root through Foundation URL APIs instead of hand-assembling or
escaping the path string. The space in `Application Support` is normal filesystem state, not a
special case the package should work around with alternate active config paths.

## Implementation Notes

### 1. Prove the path-with-spaces failure locally

Added a focused test that asks `ConfigStore` to read a YAML file at an `Application Support` path
with spaces. This uses the same service startup config-loading path rather than a separate parser.

Initial result before the fix:

- `ReloadingFileProvider<YAMLSnapshot>` reported the file as missing at the Application Support path
- the file had been written first, so the failure was in the provider path handling rather than the
  test fixture or YAML contents

### 2. Fix canonical config loading

`ConfigStore` now loads `APP_CONFIG_FILE` paths with spaces directly through
`URLReloadingYAMLConfigProvider`.

The provider keeps `swift-configuration` for `ConfigReader`, precedence behavior, YAML parsing, and
snapshot shape, but it owns the filesystem read and reload polling through Foundation file URLs. That
avoids the current `ReloadingFileProvider<YAMLSnapshot>` path conversion that treats the normal
`Application Support` space as an unsafe path.

There is no stringly alias fallback. If the configured path is invalid or missing, startup fails with
an explicit path-specific error.

### 3. Seed the canonical config during install and refresh

Added a package-bundled default config template and made install-style commands seed
`~/Library/Application Support/SpeakSwiftlyServer/server.yaml` when it is missing.

The install/update/refresh policy is:

- `install` seeds the default config when the canonical config file is missing
- refresh/update flows also seed the default config when the canonical config file is missing
- startup fails loudly when the resolved `APP_CONFIG_FILE` path is missing
- explicit user-provided config paths still fail loudly when missing instead of being replaced with
  bundled defaults

The default seed is a first-run convenience, not a runtime fallback. Once the LaunchAgent is pointed
at a canonical config path, the service should either load that file or report a clear missing-config
failure.

### 4. Change LaunchAgent environment shaping

Updated `ServerInstallLayout.launchAgentEnvironmentVariables(...)` so `APP_CONFIG_FILE` points to the
canonical config path, including when that path contains spaces.

After this change:

- `launchAgentConfigPath(for:)` returns the canonical standardized path unconditionally
- `launchAgentConfigAliasURL` remains only as a legacy cleanup location in the public install layout
- the active install path no longer stages a copied alias config

### 5. Clean up old alias state

Uninstall cleanup now removes both historical alias locations during the migration:

- `~/Library/Caches/SpeakSwiftlyServer/launch-agent-server.yaml`
- `~/Library/SpeakSwiftlyServer/launch-agent-server.yaml`

This cleanup should be explicit legacy removal code, not a continuing part of the active install
layout.

Once enough releases have passed, decide whether to delete the legacy cleanup or keep it as harmless
operator hygiene.

### 6. Add bundle-backed defaults only where they help

The package now bundles `default-server.yaml` as read-only shipped data that app/bootstrap code can
copy into Application Support when no canonical `server.yaml` exists.

Do not make the package bundle the active config store. Active config is user and operator state,
and it needs to remain writable outside the package artifact.

### 7. Update docs and release notes

Refresh or release-note the operator-facing docs that currently mention alias behavior:

- `README.md`
- `Sources/SpeakSwiftlyServer/SpeakSwiftlyServer.docc/Articles/LaunchAgent-Workflow.md`
- `docs/maintainers/live-service-reliability-follow-ups.md`
- release checklist or release notes for the patch that removes active alias use

The docs should say that Application Support owns durable config and runtime state, the package
bundle owns shipped read-only defaults, and Caches is not part of the LaunchAgent startup contract.

## Validation

Run the normal package and maintainer checks:

- `xcrun swift build`
- `xcrun swift test`
- `scripts/repo-maintenance/validate-all.sh`

Then run the live-service proof serially:

1. publish the patch release through `scripts/repo-maintenance/release-prepare.sh`
2. after merge, publish through `scripts/repo-maintenance/release-publish.sh --refresh-live-service`
3. verify the LaunchAgent environment shows `APP_CONFIG_FILE` pointing directly at
   `~/Library/Application Support/SpeakSwiftlyServer/server.yaml`
4. run `.release-artifacts/current/SpeakSwiftlyServerTool healthcheck --base-url http://127.0.0.1:7337`
5. confirm HTTP and MCP are both listening and MCP initialize succeeds
6. remove or temporarily rename the canonical config, rerun install or refresh, and confirm the
   bundled default is seeded back into Application Support before bootstrapping
7. remove or temporarily rename the canonical config after install, start the service without the
   install/refresh seeding path, and confirm startup fails loudly with the missing config path

## Resolved Questions

- The path-with-spaces failure is in the `ReloadingFileProvider<YAMLSnapshot>` filesystem path flow
  used by this package, not in the LaunchAgent property list or YAML contents.
- Seeding currently stays inside the command install/refresh path. A future app-facing public seeding
  API can be added when the app integration needs to call the same behavior directly.
