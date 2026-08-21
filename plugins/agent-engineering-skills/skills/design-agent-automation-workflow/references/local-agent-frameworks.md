# Local Agent Frameworks

Use this reference when planning a macOS-friendly agent application that may
run inference locally. It is a framework-selection and implementation-handoff
guide, not a claim that every framework should be installed or that a local
model is safe to give broad system access.

## Outcome

Choose the smallest framework that matches the workflow, then prove the chosen
model and tools can meet that workflow's contract. A local-first design should
retain three independent decisions:

1. workflow and orchestration framework;
2. inference server and model;
3. tool, data, state, and approval boundaries.

Do not collapse those choices into one "agent stack" decision.

## Inference Server Is Not The Agent Framework

An inference server runs a model and exposes a model API. An agent framework
plans calls, maintains state, invokes tools, and produces an application
contract. They can be replaced independently when the framework uses a
documented provider adapter or OpenAI-compatible endpoint.

| Layer | Local-first choices | Plan for |
| --- | --- | --- |
| Inference server | [Ollama](https://ollama.com/), [LM Studio](https://lmstudio.ai/), or a project-owned `llama.cpp`/MLX server | Endpoint URL, authentication if remote, model lifecycle, concurrency, and memory use. |
| Model | A tool-capable local model selected for the actual task | Tool calling, structured output, context length, vision, latency, and quality evaluation. |
| Agent framework | One of the framework lanes below | State, retries, handoffs, traces, and integration ownership. |
| Application tools | Narrow functions, MCP servers, and service clients | Explicit input schema, least privilege, destructive-action confirmation, and deterministic validation. |
| Durable state | Files, SQLite, Postgres, a framework checkpointer, or an existing application store | What survives a process restart, retention, migrations, and recovery. |

`Ollama` is the default first local server to document because the core
frameworks below publish explicit integrations. `LM Studio` is a useful local
alternative when its app-managed model workflow and OpenAI-compatible server
fit the developer better. Neither choice proves a model is adequate for an
agent loop.

Before any write-capable tool is enabled, run a capability gate with the exact
model and server: valid tool-call JSON, schema-conforming structured output,
bounded retry behavior, a refusal/no-op path, and a read-only task set that
resembles the real workflow.

## Core Framework Lanes

### OpenAI Agents SDK

Choose the OpenAI Agents SDK when the application is primarily an OpenAI agent
service: typed tools, handoffs, guardrails, approval points, traces, and a
server-owned execution loop.

- Good first lab: a read-only repository analyst that returns a typed audit
  report and never invokes a mutating tool.
- Graduate only after: a fixture-backed tool test, explicit write confirmation,
  trace capture, and a durable failure report.
- Handoff: the application owner and its Python/TypeScript stack workflow.
- Sources: <https://developers.openai.com/api/docs/guides/agents>

### LangChain and LangGraph

Use LangChain for its integration components. Choose LangGraph when the
workflow itself needs explicit graph transitions, persisted state,
pause/resume, streaming, retry handling, or a human decision at a named node.
Do not start with a graph for a single tool call or simple scheduled command.

- Good first lab: read-only intake → classify → retrieve → draft → approval →
  publish-draft, with the last node disabled until a reviewer approves it.
- Graduate only after: replay/resume tests, checkpoint migration planning, and
  test fixtures for each transition.
- Handoff: Python or TypeScript implementation guidance; retrieval work may
  instead belong in LlamaIndex.
- Sources: <https://docs.langchain.com/oss/python/langgraph/overview> and
  <https://docs.langchain.com/oss/python/integrations/chat/ollama/>

### LlamaIndex

Choose LlamaIndex when the product's hard problem is document ingestion,
indexing, retrieval, citation/provenance, or RAG evaluation. Its agents should
be consumers of a deliberately designed knowledge layer, not a reason to add
retrieval to an otherwise simple automation.

- Good first lab: index a small, permission-scoped document corpus, answer
  questions with source citations, and return a typed result.
- Graduate only after: ingestion/update policy, retrieval relevance evals,
  citation checks, and private-data retention boundaries.
- Handoff: Python implementation guidance and the application’s data owner.
- Sources: <https://docs.llamaindex.ai/en/latest/understanding/agent/structured_output/>
  and <https://docs.llamaindex.ai/en/v0.10.22/getting_started/starter_example_local/>

### n8n

Choose n8n when the value is visible, trigger-driven integration among outside
services: a schedule, webhook, form, email, spreadsheet, or CRM feeds a mostly
deterministic workflow. Keep model calls narrow and keep the surrounding
routing, transformations, retries, and delivery deterministic.

- Good first lab: a scheduled local-model classification that creates a draft
  report and requires approval before it calls an external write node.
- Graduate only after: credential storage review, idempotency keys, failed-run
  handling, and an exportable workflow fixture.
- Handoff: the owning integration/application project; do not use n8n as the
  default durable multi-agent runtime.
- Sources: <https://n8n.io/integrations/ollama/> and
  <https://docs.n8n.io/hosting/>
- Handoff: `agent-engineering-skills:design-n8n-agent-workflow` for the concrete
  n8n node, credential, idempotency, draft, and approval design.

### Google Agent Development Kit (ADK)

Choose Google Agent Development Kit (ADK) when the project needs a Google or
Gemini integration, A2A/MCP interoperability, a Google-supported agent
runtime, or a codebase spanning Python, TypeScript, Go, Java, or Kotlin. ADK
documents graph workflows and local-model adapters, including Ollama; that is
useful, but it does not make Google services a dependency of a local-first
application.

- Good first lab: a local-Ollama tool agent with one read-only MCP or function
  tool, session state, and evaluation fixtures.
- Graduate only after: adapter compatibility testing, session/memory retention
  decisions, and an action-confirmation boundary.
- Handoff: the application language owner; Java/Kotlin work belongs in the JVM
  lane through `server-side-jvm:build-jvm-agent-service`, TypeScript in the web
  lane, and Python in the Python lane.
- Sources: <https://adk.dev/>

### Pydantic AI

Choose Pydantic AI for a Python-first agent that benefits from typed
dependencies, validated tool inputs, and structured result models without
adopting a large graph runtime. It is a strong small-service candidate, not a
replacement for durable graph execution when pause/resume and explicit state
transitions are the primary problem.

- Good first lab: a typed local-Ollama research assistant whose only tool is a
  read-only document lookup.
- Graduate only after: schema-negative tests, exact dependency injection
  boundaries, and tool-call evaluation against the chosen local model.
- Handoff: Python implementation guidance.
- Sources: <https://pydantic.dev/docs/ai/overview/> and
  <https://pydantic.dev/docs/ai/models/ollama/>

## Comparison And Conditional Lanes

These frameworks deserve an explicit comparison, but should not become the
default merely because they advertise multi-agent support.

| Framework | Consider it when | Keep out of the first pass when | Official source |
| --- | --- | --- | --- |
| AutoGen | The project specifically explores conversational multi-agent patterns or already uses Microsoft’s agent ecosystem. | A deterministic pipeline or one clear agent/tool loop solves the job. | <https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/models.html> |
| CrewAI | The requested product genuinely needs role-oriented teams with clear, independently testable responsibilities. | “Researcher/writer/reviewer” is only a prompt-role costume around one linear job. | <https://docs.crewai.com/> |
| Semantic Kernel | The app is already C#/.NET-oriented or needs its plugin/function model in that ecosystem; hand implementation to `dotnet-skills:build-dotnet-agent-service`. | Adding .NET only to obtain an agent wrapper. | <https://learn.microsoft.com/en-us/semantic-kernel/overview/> |
| Hermes Agent | The user intentionally targets the Hermes runtime’s own skills, memory, automations, messaging, and provider model. | A framework-neutral app or normal Socket-maintenance workflow. | <https://hermes-agent.nousresearch.com/docs> |

Keep a watch list rather than a permanent guide for fast-moving choices such as
Mastra, smolagents, Haystack, and vendor-specific agent builders. Promote one
only after it has a clear local-server story, official docs, an owner language,
and a workflow gap not covered by the core lanes.

## Full-Layer Build Plan

Every framework-specific guide should use the same layers, so a reader can
compare real engineering decisions rather than marketing vocabulary.

### Layer 0: Problem And Non-Agent Baseline

State the user outcome, existing deterministic alternative, trigger, inputs,
outputs, and success criteria. Show why a script, scheduled job, direct API
call, or n8n workflow is insufficient before introducing planning behavior.

### Layer 1: Local Runtime And Model Contract

Specify macOS runtime assumptions, inference server, endpoint, exact model,
model download/storage ownership, CPU/GPU/unified-memory budget, and whether
the model supports the required modalities. Test tool calling and structured
output against the real server instead of assuming OpenAI-compatible HTTP
means semantic compatibility.

### Layer 2: Agent Contract And Tools

Define one agent’s instruction, typed input/output, narrow tool schemas, data
classification, read/write permissions, and no-op/refusal behavior. Start with
read-only tools. Tool documentation must say what changed, where, and how to
verify it.

### Layer 3: Workflow, State, And Recovery

Document routing, checkpoints, retries, timeout/cancellation, idempotency,
approval interruptions, session/memory retention, and recovery after restart.
Use a graph only where this state model is actually visible and valuable.

### Layer 4: Evaluation And Operations

Add fixtures, expected structured outputs, tool-call assertions, regression
sets, trace/log redaction, cost and latency measurements, operator messages,
and a durable failure report. Local does not mean unobservable or unbounded.

### Layer 5: Promotion And Deployment

Document secrets, sandboxing, least-privilege service accounts, network
exposure, database migrations, backup/retention, rollout, rollback, and the
exact approval gate for external writes. A local macOS prototype must not be
silently reclassified as a background or public service.

## Canonical Lab Matrix

Use one small, comparable lab per lane. All labs begin read-only, use an
explicit typed result, retain no secret in source control, and return a report
or draft rather than performing an irreversible action.

| Lab | Primary lane | Proves | Escalation point |
| --- | --- | --- | --- |
| Repository audit | OpenAI Agents SDK or Pydantic AI | Tool schema, typed output, trace, and local-model reliability. | Any suggested file modification becomes a separately approved proposal. |
| Approval-and-resume content workflow | LangGraph or ADK | Named state transition, checkpoint, pause/resume, and idempotent draft delivery. | Approval before the delivery node can write externally. |
| Private document research | LlamaIndex | Ingestion, retrieval, citations, and RAG evaluation. | Any corpus export, sharing, or index sync needs data-owner approval. |
| Scheduled integration draft | n8n | Trigger, deterministic routing, local model step, and failed-run recovery. | External write nodes stay disabled until the recipient/action is approved. |
| Multi-agent comparison | AutoGen or CrewAI | Whether a multi-role design beats the single-agent baseline on a fixed eval set. | Do not promote because the transcript looks persuasive; require measurable improvement. |

## First Implementation Sequence

1. Pick one real, bounded workflow and write the Layer 0 contract.
2. Serve one exact local model and pass the Layer 1 capability gate.
3. Build the read-only Layer 2 agent or workflow with fixtures.
4. Add only the Layer 3 state/recovery behavior the workflow demonstrably
   needs.
5. Run Layer 4 evaluations before adding another agent, data source, or tool.
6. Use Layer 5 only when the project is deliberately moving beyond a local
   prototype.

Use `auto-with-escalation` by default for a workflow that is safe through its
draft/report phase but would create external changes. The first escalation
should name the exact action, target, and evidence a reviewer needs; it should
not become a vague request to approve “the agent.”

## Ownership And Scope Boundaries

- Keep framework selection, local-model capability gates, safety questions,
  and the comparison matrix in `design-agent-automation-workflow`.
- Hand Python runtime code to Python-owned guidance; hand TypeScript/web work
  to its project or web-owned guidance; hand JVM work to JVM-owned guidance.
- Keep model benchmarking, conversion, and local inference experiments in
  `model-lab-skills` when that becomes the core task.
- Keep portable `SKILL.md` authoring and host adapters in
  `agent-portability-skills`; a framework guide does not make its runtime
  configuration portable.
- Do not add a shared framework wrapper, agent-manager abstraction, or
  background daemon during planning. Those are durable architectural changes
  and require a separately approved application need.
