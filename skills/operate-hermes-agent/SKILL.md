---
name: operate-hermes-agent
description: Install, update, configure, run, secure, and troubleshoot Hermes Agent across its CLI, TUI, dashboard, profiles, tools, skills, memory, models, sessions, worktrees, and terminal backends.
metadata:
  hermes:
    category: agent-portability
    tags: [hermes, cli, configuration, security, troubleshooting]
---

# Operate Hermes Agent

Start from the installed runtime and the active profile, then change only the state the user placed in scope.

## Establish the Active Runtime

1. Run `hermes --version`.
2. Identify the active profile and Hermes home before reading or changing configuration.
3. Use `hermes status` for a broad runtime check and the narrower status command for the affected subsystem.
4. Distinguish the installed launcher, the managed source checkout, profile state, and project-local context.
5. Refresh the matching official docs when command names, defaults, provider catalogs, or security behavior matter.

## Choose the Operating Surface

- CLI conversation: `hermes` or `hermes chat`.
- Modern terminal UI: `hermes --tui`.
- Local management UI: `hermes dashboard`; do not expose it beyond localhost without an explicit authentication and network plan.
- Profile isolation: use Hermes profiles when config, credentials, memory, sessions, skills, or gateway state must be independent.
- Repository isolation: use Git worktrees for parallel or experimental coding sessions.
- Remote or isolated execution: choose the terminal backend deliberately; use containerized or managed backends for untrusted or unattended work.

## Configure Through Owned Commands First

- Use `hermes setup` for first-run configuration.
- Use `hermes model` for provider authentication and model setup between sessions; use `/model` for switching among configured choices inside a session.
- Use `hermes tools` for toolset and per-tool backend selection.
- Use `hermes skills` for skill discovery, install, update, and tap management.
- Use `hermes portal info` only for Nous Portal and Tool Gateway routing state.
- Edit `config.yaml` or `.env` directly only when the CLI/dashboard cannot represent the needed setting or the task is explicitly config-file work.

## Protect Operator State

- Treat auth stores, `.env`, provider keys, messaging tokens, and managed-scope configuration as secrets.
- Prefer checkpoints and worktrees for risky repository changes; confirm checkpoint state before promising `/rollback` recovery.
- Keep command approval, user authorization, terminal isolation, tool allowlists, MCP filtering, and network exposure as separate controls.
- For unattended gateways, prefer Docker, Modal, or Daytona-style isolation over direct host execution when the workflow permits it.
- Do not run install, update, login, dashboard, gateway, or browser-opening commands when the user asked only for explanation or diagnosis.

## Diagnose by Layer

1. Launcher and version.
2. Active profile and config source.
3. Provider credentials and runtime resolution.
4. Model selection and API mode.
5. Toolset and backend selection.
6. Skill or plugin discovery.
7. Session, memory, or context-file state.
8. Terminal backend, permissions, and network reachability.
9. Gateway or hosted-service state, if involved.

Report the exact layer that failed and the next read-only check before proposing a mutation.

## Verification

Verify only the affected path. Examples:

- configuration: `hermes status` plus the subsystem status command;
- provider: provider/model status and one harmless prompt;
- skill: discovery plus explicit invocation;
- terminal backend: a harmless command in the selected backend;
- worktree: repository path and branch isolation;
- security: approval, authorization, or isolation state without performing a dangerous action.

Read [references/operator-surface-map.md](references/operator-surface-map.md) for state locations, commands, failure modes, and official sources.
