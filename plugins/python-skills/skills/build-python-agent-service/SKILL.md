---
name: build-python-agent-service
description: Build a local-first Python agent service with typed tools, exact model capability checks, evaluation fixtures, and safe promotion gates. Use for OpenAI Agents SDK, LangGraph, LlamaIndex, Pydantic AI, Google ADK Python, AutoGen, or CrewAI.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients building uv-managed Python agent services on macOS with local or remote model endpoints, typed tool contracts, and explicit validation.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-agent-service
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*) Bash(python:*)
---

# Build Python Agent Service

## Purpose

Build one bounded Python agent application without treating the model server,
agent framework, tool executor, and durable state as one inseparable stack.
Start from the smallest useful read-only agent and promote only after the exact
model, tools, evaluation fixtures, and side-effect boundary have been proved.

## When To Use

- Use for a new or existing uv-managed Python agent service.
- Use when the framework is OpenAI Agents SDK, LangGraph, LlamaIndex, Pydantic
  AI, Google ADK Python, AutoGen, or CrewAI.
- Use after `design-agent-automation-workflow` has established that a
  code-owned Python agent service is the right surface.
- Do not use for a visual integration workflow; hand off n8n work to the
  owning integration project after the planning skill selects it.
- Do not use for model benchmarking itself; hand off local model capability and
  tool-loop measurement to `model-lab-skills:evaluate-tool-calling-model`.

## Source Check

Before selecting or updating a framework, inspect the repository and use
official current documentation for the exact framework and model adapter:

- OpenAI Agents SDK: <https://developers.openai.com/api/docs/guides/agents>
- LangGraph: <https://docs.langchain.com/oss/python/langgraph/overview>
- LangChain Ollama: <https://docs.langchain.com/oss/python/integrations/chat/ollama/>
- LlamaIndex agents: <https://docs.llamaindex.ai/en/latest/understanding/agent/structured_output/>
- Pydantic AI: <https://pydantic.dev/docs/ai/overview/>
- Pydantic AI Ollama: <https://pydantic.dev/docs/ai/models/ollama/>
- Google ADK: <https://adk.dev/>
- AutoGen models: <https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/models.html>
- CrewAI: <https://docs.crewai.com/>
- uv: <https://docs.astral.sh/uv/>

State which source changed the implementation decision. Do not rely on a
framework's claimed OpenAI-compatible endpoint as proof that a local model
supports tool calls or structured output correctly.

## Implementation Sequence

1. Inspect the current project shape, its `pyproject.toml`, existing model
   client, tools, state store, tests, and deployment configuration. Prefer an
   existing service/package boundary over adding a second agent host.
2. Write the non-agent baseline: trigger, inputs, expected typed output,
   deterministic alternative, no-op behavior, and the reason planning/tool use
   is necessary.
3. Select one framework for the real workflow:
   - OpenAI Agents SDK for an application-owned agent loop with tools,
     handoffs, guardrails, and traces.
   - LangGraph when persisted transitions, pause/resume, retries, or explicit
     routing are first-class behavior.
   - LlamaIndex when ingestion, retrieval, citations, and RAG quality are the
     core product problem.
   - Pydantic AI for a compact typed Python service with validated tool and
     result models.
   - Google ADK Python when Google/Gemini, A2A/MCP, or ADK's runtime model is a
     concrete product requirement.
   - AutoGen or CrewAI only when a measured multi-agent design beats a
     single-agent baseline on the same fixed task set.
4. Declare model endpoint, exact model name and revision/tag, authentication,
   requested capabilities, context/latency limits, and model lifecycle. Keep
   local server configuration out of committed secrets and machine-local paths.
5. Run a capability gate against the exact endpoint and model before attaching
   write-capable tools: valid tool-call JSON, schema-conforming structured
   output, no-call behavior, malformed-call recovery, maximum-step stop, and a
   read-only task set resembling the intended application.
6. Implement one agent with typed input/output and narrow read-only tools.
   Tool functions must validate their own authorization, inputs, timeout, and
   result shape; model output cannot grant a capability.
7. Add durable state only when the user-visible workflow needs a restart-safe
   session, checkpoint, task queue, or approval resume point. Name the store,
   retention, migration, replay, and recovery contract.
8. Add the smallest test set: fake-tool unit cases, structured-output cases,
   model-adapter integration smoke tests, denied-write cases, and regression
   fixtures. Run live write tests only in an explicit disposable or draft mode.
9. Promote from report/draft to external writes only through
   `auto-with-escalation`: name the exact recipient, target, action, evidence,
   rollback/no-op behavior, and human approval point.

## Framework Boundaries

Do not add a framework wrapper merely to make framework names interchangeable.
Keep application domain behavior independent from the selected framework where
that boundary has a real caller: typed domain input/output, tool interfaces,
and persistence adapter. Let framework-specific orchestration stay at the
application edge.

Do not introduce LangGraph persistence, vector retrieval, multi-agent teams,
or a background queue unless the selected workflow requires its concrete
behavior. A single request/response tool loop should remain a small service or
CLI.

## Validation

At minimum, run the repository's configured quality checks. In a standard uv
project that means:

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run mypy .
```

Report separately:

1. fake-tool contract results;
2. exact local/remote model capability-gate results;
3. structured result validity;
4. attempted versus executed side effects;
5. state/resume behavior, when state exists;
6. the exact approval or no-op result for write-capable tools.

## Output Shape

Return:

1. `Framework`: selected framework and the concrete requirement it serves.
2. `Model contract`: server, exact model, capabilities proven, and limitations.
3. `Tool boundary`: tool schemas, permissions, and denied-action behavior.
4. `State`: absent or explicit persistence/recovery contract.
5. `Evaluation`: fixture, fake-tool, and live-integration evidence.
6. `Promotion gate`: exact condition for an external write.
7. `Validation`: commands run and results.

## Guardrails

- Do not install several frameworks for a comparison unless the experiment is
  explicitly requested and has one fixed evaluation set.
- Do not run an unattended local background service, scheduler, or external
  write workflow without an explicit user request and a recovery plan.
- Do not store model API keys, local endpoint credentials, or private prompt
  data in source control, fixtures, traces, or error output.
- Do not call a local model private merely because it runs on macOS; document
  every connected tool, remote endpoint, trace sink, and data store.
- Do not claim a model supports tools, structured output, or a context size
  until the exact server/model combination passes the capability gate.
