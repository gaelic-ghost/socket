# Framework Selection

Use this reference when the user needs the reasoning behind the chosen agent or
automation surface.

## Official Sources

- Codex app automations: <https://developers.openai.com/codex/app/automations>
- Codex non-interactive mode: <https://developers.openai.com/codex/noninteractive>
- Codex GitHub Action: <https://developers.openai.com/codex/github-action>
- Codex subagents: <https://developers.openai.com/codex/subagents>
- OpenAI Agents SDK: <https://developers.openai.com/api/docs/guides/agents>
- LangGraph: <https://docs.langchain.com/oss/python/langgraph/overview>
- Hermes Agent: <https://hermes-agent.nousresearch.com/docs>
- Hermes Agent Hugging Face integration: <https://huggingface.co/docs/inference-providers/main/en/integrations/hermes-agent>

## Selection Matrix

| Surface | Use first when | Avoid first when |
| --- | --- | --- |
| Codex app automation | The job is a recurring Codex task, inbox report, thread wake-up, reminder, or skill-backed background check. | The job needs a durable cross-run queue, custom service state, or non-Codex runtime ownership. |
| `codex exec` or Codex GitHub Action | One repository can run from a bounded prompt with explicit sandbox settings, machine-readable output, CI integration, or PR handoff. | The job needs long-running state transitions, interactive approvals inside the same run, or multi-repo scheduling logic. |
| Codex subagents | The user explicitly asks for parallel agent work and the task splits into bounded read, review, test, or independent implementation slices. | The work is a small sequential edit, one target file, background scheduling, or queue ownership. |
| OpenAI Agents SDK service | Application code should own tools, handoffs, guardrails, human review, state, tracing, and server integration. | A Codex prompt or one-shot CLI job can complete the work with simpler review boundaries. |
| LangGraph graph | The workflow is a long-running stateful graph with persistence, durable execution, human-in-the-loop pauses, streaming, and explicit resume behavior. | The task is a simple one-repo automation or prompt-level workflow that does not need graph state. |
| Hermes-specific workflow | The desired runtime is Hermes Agent itself, especially its memory, skills, messaging gateway, scheduled automation, provider, or terminal backend model. | The workflow is ordinary Codex repo maintenance or framework-neutral planning. |
| No automation yet | The outcome, validation, owner, approval gate, or rollback path is unclear. | The user already has a bounded repeatable task with known checks and a safe first run. |

## Required Questions

- What starts the workflow: schedule, CLI command, CI event, user request, webhook,
  message, or another service?
- What state must survive between runs?
- What can write to the repository, filesystem, external service, or user data?
- Where does human approval happen, and what exactly is approved?
- What retries are allowed, and what failure record remains after a retry stops?
- What trace, log, report, or artifact proves the workflow behaved correctly?
- Which stack-owned plugin or official docs should own implementation after this
  planning pass?

## Handoff Rules

- Hand Python service implementation to `python-skills`.
- Hand TypeScript, web service, or frontend implementation to the Build Web Apps
  plugin or the repo's owning JavaScript/TypeScript workflow.
- Hand Swift, SwiftPM, Xcode, or Apple-platform work to the Apple/Swift-owned
  skills.
- Hand repo-document maintenance back to the specific `maintain-project-*`
  productivity skill that owns the target document.
- Hand Hermes runtime work to official Hermes docs unless a dedicated
  Hermes-owned skill exists.
