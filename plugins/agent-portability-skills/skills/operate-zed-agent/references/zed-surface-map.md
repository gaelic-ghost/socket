# Zed Agent Surface Map

| Surface | Owner | Skills and configuration |
| --- | --- | --- |
| Zed Agent | Zed | Zed providers, profiles, permissions, instructions, `.agents/skills`, and Zed MCP |
| External Agent | ACP agent process | Agent-native auth, models, config, skills, and state; Zed owns editor UI and may forward MCP |
| Terminal Thread | CLI or TUI process | Native terminal behavior and agent configuration |

## Zed Skill Constraints

- Global root: `~/.agents/skills/`
- Project root: `<worktree>/.agents/skills/`
- Direct-child skill directories only
- Project skills require a trusted worktree
- Global and project-local skills with the same name resolve to project-local
- Total catalog name and description budget: 50 KB
- No runtime remote skill registry or arbitrary search paths
- Zed Skills apply to Zed Agent, not automatically to External Agents

## External Agent Checks

1. Query the canonical ACP Registry.
2. If present, install through Zed's registry UI.
3. If absent, verify the official executable and use a custom `agent_servers`
   entry only when the agent supports ACP locally.
4. Verify agent-native authentication before starting meaningful work.
5. Inspect `dev: open acp logs` for handshake, session, and tool failures.
6. Check forwarded Zed MCP and native agent MCP independently.

Official references:

- https://zed.dev/docs/ai/agents
- https://zed.dev/docs/ai/zed-agent
- https://zed.dev/docs/ai/external-agents
- https://zed.dev/docs/ai/skills
- https://zed.dev/docs/ai/instructions
- https://zed.dev/docs/ai/mcp
