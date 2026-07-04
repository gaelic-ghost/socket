# AgentDeck Agent Configuration Sync Plan

## Working Name

`AgentDeck` is the app and helper home for Codex-connected utilities that need a stable macOS app, local helper, permission surface, or long-lived runtime identity.

The Socket `agentdeck` plugin is the Codex-facing connection point. The plugin should own the agent-facing docs, skills, MCP shims, hooks, and policy. The app should own the installed macOS runtime, durable local config manager, permission prompts, helper endpoints, and operator-facing UI.

This plan was originally drafted under the temporary name `Agent Concord`. That name described this specific feature: keep local coding agents in agreement across separate host environments without flattening their differences. The feature should now be treated as one capability inside the broader `AgentDeck` app.

Name/context notes:

- `GuideRail`: strong guidance/rules connotation, but slightly more safety-product than config-product.
- `Agent Deck`: macOS-friendly, short, and flexible, but less descriptive.
- `Concord`: cleaner than `Agent Concord`, but less searchable.
- `Config Beacon`: clear drift-detection energy, but less agent-specific.
- `Syncwright`: distinctive, but a little too cute for a utility.

## Local Findings

Normal Codex:

- User config home: `~/.codex`
- CLI version checked on 2026-06-06: `codex-cli 0.137.0`
- Global config: `~/.codex/config.toml`
- Global guidance: `~/.codex/AGENTS.md`
- Current normal config includes `model = "gpt-5.5"`, `approval_policy = "on-request"`, `approvals_reviewer = "auto_review"`, `sandbox_mode = "workspace-write"`, and workspace-write network access enabled.
- Normal Codex already has an Xcode MCP server configured as `xcode -> xcrun mcpbridge`.

Xcode Codex:

- Xcode version checked on 2026-06-06: Xcode 26.5, build 17F42
- Xcode Codex home: `~/Library/Developer/Xcode/CodingAssistant/codex`
- Xcode Codex binary: `~/Library/Developer/Xcode/CodingAssistant/Agents/codex/0.129.0-alpha.9/codex`
- Xcode Codex version checked on 2026-06-06: `codex-cli 0.129.0-alpha.9`
- Xcode-owned config currently contains only:

```toml
cli_auth_credentials_store = "keyring"

[analytics]
enabled = false
```

- No Xcode-side `AGENTS.md` was present at initial inspection after installation.
- Xcode Codex ships its own system skills and temporary plugin catalog under the Xcode Codex home.

Xcode Claude:

- Apple documents a separate Xcode-owned Claude Agent configuration folder:
  `~/Library/Developer/Xcode/CodingAssistant/ClaudeAgentConfig`
- This should be treated as a separate target profile, not as a Codex-compatible target.

## Product Thesis

AgentDeck should include a macOS utility surface for inspecting, diffing, and syncing local agent guidance/config across multiple agent hosts.

The app exists because agent hosts are no longer a single dot-directory. A developer can have normal Codex, Codex inside Xcode, Claude inside Xcode, Codex desktop app state, CLI state, plugins, skills, MCP servers, sandbox rules, and per-project guidance. These surfaces drift independently, and raw copy/symlink sync is too risky because bundled agents may lag normal CLI versions and reject newer keys.

The feature should make drift visible and make syncing boring.

## Core Principle

Canonical source, target-specific render.

Do not mirror a directory wholesale. Keep a canonical model of the desired guidance/config, then render safe target outputs based on each target's detected host, version, capabilities, and ownership rules.

## Target Model

Each target has:

- Display name, such as `Codex CLI`, `Xcode Codex`, or `Xcode Claude`.
- Home directory.
- Binary path, if applicable.
- Detected version, if applicable.
- Config format and supported config keys.
- Guidance filenames and precedence rules.
- Skills/plugins capability flags.
- MCP support flags.
- Managed/owned paths the app must not edit.
- Backup strategy.
- Validation commands.

Initial targets:

| Target | Role | Initial sync confidence |
| --- | --- | --- |
| Codex CLI / app | Primary source and normal local agent | High |
| Xcode Codex | Older bundled Codex agent with Xcode-owned home | Medium |
| Xcode Claude | Separate Xcode-owned Claude config home | Low until inspected |

## Config Compatibility Strategy

The app should maintain a compatibility table keyed by target type and detected version.

For example:

| Key | Normal Codex 0.137 | Xcode Codex 0.129 alpha | Notes |
| --- | --- | --- | --- |
| `model` | allowed | likely allowed, verify | GPT-5.5 availability is a good signal but not proof of every config key |
| `model_reasoning_effort` | allowed | verify | May have changed across releases |
| `approval_policy` | allowed | verify | User-facing behavior may differ in Xcode host |
| `approvals_reviewer` | allowed | likely omit until verified | Newer key; do not assume bundled agent supports it |
| `sandbox_mode` | allowed | verify | Xcode host may impose additional boundaries |
| `sandbox_workspace_write.network_access` | allowed | verify | Must not silently widen network access |
| `notify` | allowed | omit by default | Normal Codex app hook path is host-specific |
| `projects.*.trust_level` | allowed | omit by default | Trust entries are personal and path-heavy |
| MCP server entries | allowed | target-specific | Xcode Codex may not need the Xcode MCP bridge from inside Xcode |
| plugin cache paths | no raw sync | no raw sync | Managed cache data is not a user-authored config surface |

Unknown keys should default to `omit`, not `copy`.

## Sync Surfaces

Low-risk surfaces:

- Global guidance text
- Selected project guidance templates
- User-authored skills with clean `SKILL.md` metadata
- A small set of stable preferences after compatibility checks

Medium-risk surfaces:

- MCP server definitions
- Permission/rule profiles
- Selected plugin enablement settings
- Target-specific model defaults

High-risk surfaces:

- Auth and credential material
- Sessions and history
- Plugin cache directories
- Browser/app state
- Notification handler paths
- Temporary Xcode plugin catalogs
- Managed system skills
- Project trust lists
- Anything in `.tmp`

## MVP

The first useful version can be local-only and file-based.

MVP features:

1. Discover installed agent targets.
2. Show detected versions and config homes.
3. Parse supported config files.
4. Compare `AGENTS.md` and selected config keys.
5. Generate a dry-run sync plan.
6. Render Xcode Codex compatible config by filtering unsupported or unknown keys.
7. Create timestamped backups before writes.
8. Validate TOML after writes.
9. Never sync high-risk surfaces.

MVP output should be explicit:

- `unchanged`
- `would create`
- `would update`
- `would omit unsupported key`
- `would skip high-risk path`
- `blocked: target missing`
- `blocked: parser failed`

## macOS App Shape

Use a SwiftUI app with a small, explicit core model.

Suggested ownership:

- App-level owns the selected workspace/config profile and target discovery service.
- Scene-level owns the currently selected target, diff selection, and sync preview state.
- File operations live in dedicated service types, not in views.
- Target capability rules live in plain data structures that are easy to test.
- Views render inventory, diff, and preview state; they should not decide compatibility.

Initial screens:

- `Inventory`: detected agent targets, versions, homes, and status.
- `Guidance`: global guidance diff and target render preview.
- `Config`: key-level compatibility and target output preview.
- `Skills`: selected user-authored skill sync candidates.
- `Apply`: dry-run result, backup summary, and explicit write controls.

## Core Types

Suggested first-pass types:

- `AgentTarget`: detected install surface and host metadata.
- `AgentTargetKind`: `codexCli`, `xcodeCodex`, `xcodeClaude`, future extension cases.
- `AgentVersion`: parsed version plus raw string.
- `AgentHome`: canonical paths for config, guidance, skills, plugin cache, and temp paths.
- `CapabilityProfile`: allowed, omitted, risky, and unknown keys/surfaces.
- `CanonicalGuidance`: normalized guidance source.
- `CanonicalConfig`: parsed desired settings before target rendering.
- `RenderedConfig`: target-specific TOML plus omitted-key report.
- `SyncPlan`: ordered operations with risk labels.
- `BackupRecord`: original path, backup path, timestamp, and content hash.
- `ValidationResult`: parse checks, command checks, and warnings.

## Compatibility Probing

Prefer direct evidence over assumptions:

- Run `codex --version` for normal Codex.
- Run the Xcode Codex binary with `--version` when present.
- Parse target `config.toml` with a real TOML parser.
- Use official docs for known current Codex keys.
- Treat Xcode-managed folders as source of truth for embedded agent location.
- When a target lacks a binary or version, fall back to conservative rules.

Possible future probe:

- Start a non-interactive target Codex process with a temporary `CODEX_HOME` and minimal config to test whether specific keys are accepted. This must be opt-in and dry-run-first because it may touch auth or host-specific state.

## Safety Rules

- Default to dry-run.
- Never write without showing the exact operation list.
- Always backup before replacing files.
- Never write inside `.tmp`, session directories, browser/app state, plugin caches, or managed system skill directories.
- Never sync credentials.
- Never silently widen sandbox, network, or approval behavior.
- Never assume newer normal Codex config keys are accepted by Xcode Codex.
- Treat Xcode Claude as a separate format until inspected.

## Socket Plugin Relationship

The Socket `agentdeck` plugin should keep a copy of this plan because it owns the Codex-facing connection point.

The split should stay clear:

- `AgentDeck` owns discovery, diff rendering, backups, writes, local validation, and any macOS permission/helper behavior.
- `socket/plugins/agentdeck` owns skill guidance, MCP shims, hook wiring, plugin metadata, and agent policy.
- The plugin may expose status and request tools, but it should not directly rewrite agent homes unless that behavior is explicitly routed through the installed app or a reviewed local helper contract.

This mirrors the desktop bridge split already planned for the same app/plugin pair.

## Implementation Slices

1. Research and fixtures
   - Capture local target inventory.
   - Save sample normal Codex and Xcode Codex configs as sanitized fixtures.
   - Define target capability profiles.

2. CLI prototype
   - Build a small Swift command-line tool that discovers targets and prints JSON.
   - Add TOML parsing and render previews.
   - Add dry-run sync planning.

3. macOS shell
   - Create the SwiftUI app.
   - Add inventory and diff screens.
   - Wire dry-run previews.

4. Safe apply
   - Add backups.
   - Add writes behind explicit controls.
   - Add validation and rollback display.

5. Wider target support
   - Add Xcode Claude inspection.
   - Add user-authored skill selection.
   - Add MCP/profile diffing.

## Open Questions

- Should normal Codex `~/.codex/AGENTS.md` remain the canonical source, or should Agent Concord own a separate canonical profile and render back into normal Codex too?
- Should project guidance sync be in scope, or only global guidance and agent-home config?
- Should this be a public repo, private repo, or local-only project until the config-safety story is mature?
- Should Xcode Codex model defaults be synced at all, or left to Xcode's Intelligence UI?
- Should Xcode Claude support be read-only in the MVP?

## Near-Term Next Step

Create a small discovery prototype before building the app UI.

The prototype should print a deterministic inventory of normal Codex, Xcode Codex, and Xcode Claude surfaces, including versions, config paths, guidance presence, and obvious managed directories. That inventory becomes both the first app screen and the baseline fixture set for compatibility tests.
