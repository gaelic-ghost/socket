---
name: operate-zed-agent
description: Configure and troubleshoot Zed Agent, ACP External Agents, and Terminal Threads. Use for Zed Skills, MCP, profiles, permissions, registry installs, custom agents, and ACP logs.
metadata:
  hermes:
    category: agent-portability
    tags: [zed, acp, external-agents, agent-skills, mcp]
---

# Operate Zed Agent

Choose the Zed agent path before editing settings. Read
`references/zed-surface-map.md` when the request crosses native and external
agent configuration.

## Choose the Agent Path

- Use Zed Agent when Zed should own the model, provider, tools, profiles,
  permissions, instructions, skills, and MCP configuration.
- Use an External Agent when an ACP agent such as Codex, Claude, OpenCode, or
  Hermes should own its runtime, model, authentication, native skills, and
  persistent state while Zed owns the editor UI.
- Use a Terminal Thread when the original CLI or TUI behavior matters more than
  ACP-native diffs, approvals, or session rendering.

Do not apply Zed Agent Skills or profiles to an External Agent by assumption.
The external agent keeps its own configuration unless its ACP implementation
explicitly accepts a forwarded capability.

## Configure Zed Agent

1. Confirm the worktree is trusted before expecting project-local skills.
2. Keep skills as direct children of global `~/.agents/skills/` or project
   `.agents/skills/`; Zed does not discover nested or arbitrary search roots.
3. Keep names and descriptions concise because Zed has a catalog budget.
4. Use Zed Instructions for always-on guidance, Agent Profiles for tool
   selection, Tool Permissions for approval policy, and Zed MCP configuration
   for external tools.
5. Treat remote skill import as a one-time installation action, not a remote
   runtime registry.

## Configure an External Agent

1. Check the live canonical ACP Registry instead of trusting a product page or
   an agent's source manifest.
2. Prefer the registry only when the requested agent is actually present.
3. Otherwise add a custom `agent_servers` entry using the agent's official
   executable and arguments. Do not substitute an unreviewed third-party
   launcher merely to make a registry row appear.
4. Configure provider credentials and native agent state in the external agent
   unless its integration documents another owner.
5. Start a new thread and verify the agent identity, working directory, model,
   skills, MCP tools, and approval behavior.
6. Use `dev: open acp logs` to inspect Zed-to-agent protocol traffic.

For Hermes, use `operate-acp-agent-integration` to check the canonical registry
and validate `hermes acp --check` before adding a custom entry. The manual
command is `hermes` with `args: ["acp"]`; prefer an accepted official registry
entry if one becomes available later.

## Guards

- Do not install or update Zed, an external agent, a skill, or an MCP server
  without user intent.
- Do not claim a registry entry exists because a source repository contains an
  `agent.json`; verify the published registry feed.
- Do not expose secrets in Zed settings when the agent supports its own secure
  authentication flow.
- Do not automate visible Zed interaction without approval when a settings or
  thread check requires the app UI.

## Report

Report the selected path, Zed version when relevant, configuration owner,
authentication owner, skill and MCP sources, registry or custom launch path,
runtime evidence, and remaining editor-side checks.
