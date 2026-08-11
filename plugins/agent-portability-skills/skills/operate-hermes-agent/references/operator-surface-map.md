# Hermes Operator Surface Map

## State And Scope

| Surface | Typical ownership |
| --- | --- |
| Hermes home | Profile/runtime configuration, auth, memory, sessions, installed skills and plugins |
| Project context | Repository-specific `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and optional project plugins |
| Managed scope | Administrator-enforced configuration and secrets |
| Profile | Independent config, credentials, memory, sessions, skills, and gateway state |
| Worktree | Independent repository checkout for one coding lane |

Always resolve the active profile before interpreting a path under the Hermes home.

## Command Families

- `hermes setup`: onboarding and broad configuration.
- `hermes model`: provider login, model configuration, and between-session selection.
- `/model`: in-session switch among configured providers/models.
- `hermes tools`: toolsets and per-tool providers.
- `hermes skills`: local skills, hub skills, taps, bundles, and updates.
- `hermes status`: broad runtime state.
- `hermes update --check`: read-only update availability check; inspect carried local commits before applying an update.
- `hermes acp --check`: non-interactive ACP adapter health check.
- `hermes import-agent <claude-code|codex> --dry-run`: preview instruction,
  permission, MCP, skill, and memory migration without importing credentials.
- `hermes portal info`: Nous auth and routing only.
- `hermes dashboard`: local management UI.
- `hermes gateway`: messaging and API service process.
- `/goal draft`, `/goal show`, `/goal gate`, and `/goal wait`: persistent
  single-session objective, evidence, and wait controls.
- `/wake`: local CLI/TUI/desktop wake-word control; voice mode and desktop
  push-to-talk remain separate capture paths.

Check the [CLI command reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) before depending on a subcommand not listed here.

## Runtime Layers

Provider resolution is shared across CLI, gateway, cron, ACP, and auxiliary model calls. A provider that works for the main chat can still fail for vision, compression, title generation, MCP routing, or another auxiliary slot if that slot has separate configuration.

Prompt assembly uses stable, context, and volatile tiers. Skills and tool/model guidance live in stable material; project context is a separate context tier; memory/profile snapshots are volatile. Read [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) before changing injection behavior or diagnosing cache churn.

## Safety Controls

- command approval and dangerous-command classification;
- messaging-platform user authorization;
- local, Docker, SSH, Daytona, Modal, and Singularity terminal backends;
- MCP tool filtering and utility-tool policy;
- toolset selection per platform;
- checkpoints and `/rollback` when enabled;
- worktree isolation for parallel repository work;
- network binding and authentication for dashboard/API surfaces;
- managed scope for administrator baselines.

These controls are additive, not interchangeable.

## Common Failure Shapes

- Correct config, wrong profile.
- Provider authenticated, auxiliary model slot unresolved.
- Tool exists, platform toolset disables it.
- Skill installed, description or category makes discovery poor.
- Project plugin present, project-plugin opt-in missing.
- Dashboard/API works on localhost, remote bind lacks safe auth.
- Checkpoints expected, but opt-in was never enabled.
- Gateway running, but platform authorization or outbound delivery fails.
- Portal logged in, but a tool still routes through a direct provider.
- Agent import preview is correct, but a name collision would be skipped or
  overwritten contrary to the operator's intent.
- Goal judge has weak completion criteria or a gate is unbounded.
- Voice works in one surface while another capture path uses the wrong device.

## Authoritative Sources

- [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [CLI](https://hermes-agent.nousresearch.com/docs/user-guide/cli)
- [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Git worktrees](https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees)
- [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- [Checkpoints and rollback](https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback)
- [Tools and toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)
- [Skills system](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [Web dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard)
- [Import from other agents](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents)
- [Persistent goals](https://hermes-agent.nousresearch.com/docs/user-guide/features/goals)
- [Voice mode](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode)
- [Wake word](https://hermes-agent.nousresearch.com/docs/user-guide/features/wake-word)
