# Hermes Workflow Map

Use this map when a request spans multiple Hermes products or extension systems.

## User And Operator Work

- CLI, TUI, dashboard, configuration, models, tools, skills, memory, sessions, profiles, worktrees, security, checkpoints, and terminal backends belong to `operate-hermes-agent`.
- Messaging platforms, webhooks, API service exposure, long-running profiles, and remote bot operation belong to `operate-hermes-agent-gateway`.
- Portal authentication, hosted inference, managed tools, subscription proxy, Nous Chat, and Hermes Cloud belong to `use-nous-research-services`.

## Developer Work

- Portable instruction workflow: Agent Skill.
- External tool process: MCP.
- General registered behavior: Python plugin.
- Messaging channel: platform adapter.
- Inference routing: model-provider plugin or upstream core provider, depending on ownership.
- Memory or compression: memory provider or context engine.
- Media/web backend: image, video, web-search, or browser provider.
- Secret resolution: secret-source plugin.
- Native desktop UI: Desktop Plugin SDK.
- Web dashboard UI: dashboard extension SDK.
- External host: ACP, TUI gateway JSON-RPC, or Hermes API server.
- Socket-to-Hermes packaging decision: `hermes-agent-compatibility`.

## Similar Names That Are Not Equivalent

| Term | Meaning |
| --- | --- |
| Hermes messaging gateway | Long-running message/API process |
| Nous Tool Gateway | Nous-hosted tool providers |
| TUI gateway | Host-to-Hermes JSON-RPC protocol |
| Hermes Python plugin | Runtime registration through `plugin.yaml` and Python |
| Hermes desktop plugin | Native desktop UI extension |
| Hermes dashboard plugin | Web dashboard extension |
| Codex plugin | Codex distribution bundle; not a Hermes plugin |
| Claude plugin | Claude distribution bundle; not a Hermes plugin |
| Hermes Cloud | Nous-hosted Hermes deployment |
| Modal/Daytona backend | Terminal execution backend, not Hermes Cloud itself |

## Authoritative Starting Points

- [Hermes documentation](https://hermes-agent.nousresearch.com/docs/)
- [Hermes features overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview/)
- [Hermes architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [Hermes plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins)
- [Hermes programmatic integration](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration)
- [Nous Portal](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal)
