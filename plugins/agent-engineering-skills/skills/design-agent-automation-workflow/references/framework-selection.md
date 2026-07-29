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
- Local-first framework planning: [local-agent-frameworks.md](./local-agent-frameworks.md)

## Selection Matrix

| Surface | Use first when | Avoid first when |
| --- | --- | --- |
| Codex app automation | The job is a recurring Codex task, inbox report, thread wake-up, reminder, or skill-backed background check. | The job needs a durable cross-run queue, custom service state, or non-Codex runtime ownership. |
| `codex exec` or Codex GitHub Action | One repository can run from a bounded prompt with explicit sandbox settings, machine-readable output, CI integration, or PR handoff. | The job needs long-running state transitions, interactive approvals inside the same run, or multi-repo scheduling logic. |
| Codex subagents | The user explicitly asks for parallel agent work and the task splits into bounded read, review, test, or independent implementation slices. | The work is a small sequential edit, one target file, background scheduling, or queue ownership. |
| OpenAI Agents SDK service | Application code should own tools, handoffs, guardrails, human review, state, tracing, and server integration. | A Codex prompt or one-shot CLI job can complete the work with simpler review boundaries. |
| LangGraph graph | The workflow is a long-running stateful graph with persistence, durable execution, human-in-the-loop pauses, streaming, and explicit resume behavior. | The task is a simple one-repo automation or prompt-level workflow that does not need graph state. |
| Hermes-specific workflow | The desired runtime is Hermes Agent itself, especially its memory, skills, messaging gateway, scheduled automation, provider, or terminal backend model. | The workflow is ordinary Codex repo maintenance or framework-neutral planning. |
| Full-auto execution | The workflow has bounded inputs, explicit write scope, deterministic or reviewable validation, durable failure reporting, bounded retries, and rollback, no-op, or draft behavior. | The workflow has unbounded external side effects, unclear success criteria, or no reliable stop condition. |
| Auto-with-escalation | Most of the workflow is safe, but one exact decision still needs user review when a named trigger fires. | The whole workflow is still underspecified, or escalation would happen on nearly every run. |
| No automation yet | The outcome, validation, owner, approval gate, or rollback path is unclear after narrowing the workflow. | The user already has a bounded repeatable task with known checks and a safe first run. |

## Framework Choice Is A Separate Decision

After choosing whether the work needs a code-owned agent service or durable
graph, choose the framework only from the requirements that remain:

| Requirement that drives the choice | Start with | Do not infer |
| --- | --- | --- |
| Typed Python tools, dependency injection, and validated outputs | Pydantic AI or the OpenAI Agents SDK | That a typed schema makes a weak local model reliable at tool selection. |
| Persisted state transitions, pause/resume, and explicit routing | LangGraph | That LangChain itself is required for a retrieval-heavy product. |
| Document ingestion, retrieval, indexes, and RAG as the product core | LlamaIndex | That a vector database or multi-agent team is required for every document task. |
| Visual, trigger-driven integration between external services | n8n | That a visual workflow needs autonomous planning or durable agent memory. |
| Google, Gemini, A2A, MCP, or a multi-language implementation boundary | Google ADK | That ADK requires a Google-hosted model; its documented model adapters include local options. |
| Conversational multi-agent research or an existing Microsoft agent surface | AutoGen or Semantic Kernel | That role-playing several agents improves a workflow with one clear deterministic path. |

Use `local-agent-frameworks.md` for the maintained framework inventory,
local-inference boundary, canonical labs, and implementation handoffs.

For read-heavy custom Codex subagent roles, prefer a role-local model choice over
a global policy. `gpt-5.4-mini` is a good soft default for bounded exploration
or audit workers; use a stronger model or omit the model override when the
worker owns hard synthesis, ambiguous debugging, or write-plan judgment.

## Required Questions

- What starts the workflow: schedule, CLI command, CI event, user request, webhook,
  message, or another service?
- What state must survive between runs?
- What can write to the repository, filesystem, external service, or user data?
- Which parts are safe for full automation, and which exact trigger escalates?
- Where does human approval happen, if anywhere, and what exactly is approved?
- What retries are allowed, and what failure record remains after a retry stops?
- What trace, log, report, or artifact proves the workflow behaved correctly?
- Which stack-owned plugin or official docs should own implementation after this
  planning pass?

## Full-Auto Fit Checks

A workflow is a good full-automation candidate when all of these are true:

- inputs are bounded or normalized before execution
- write scope is explicit and narrow
- validation is deterministic or reviewable enough to catch material failures
- failures leave a durable report
- retries are bounded
- rollback, no-op, or draft behavior prevents irreversible damage
- external side effects are absent or explicitly approved in advance

If one check fails, prefer `auto-with-escalation` and name the missing gate. Use
human-in-the-loop only for the exact decision that cannot be made safe through
scope, sandboxing, validation, rollback, or orchestration.

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
