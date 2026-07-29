---
name: build-jvm-agent-service
description: Build a local-first Java or Kotlin Google ADK agent service with explicit tools, model capability checks, evaluation fixtures, and draft-before-write promotion.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Java or Kotlin server-side JVM services on macOS or other supported JVM environments.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: jvm-agent-service
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(./gradlew:*) Bash(mvn:*) Bash(sbt:*)
---

# Build JVM Agent Service

Use this skill after `choose-service-shape` identifies a JVM service and the
application needs Google Agent Development Kit (ADK), not merely one model API
call. Keep Java/Kotlin domain behavior independent from ADK orchestration at
the application edge.

## Source Check

- Google ADK: <https://adk.dev/>
- ADK Java API: <https://google.github.io/adk-docs/api-reference/java/>
- Java: <https://docs.oracle.com/en/java/>
- Kotlin: <https://kotlinlang.org/docs/home.html>

Confirm the exact ADK language/runtime and model adapter before changing code.
ADK documents local-model adapters, but an Ollama-compatible endpoint must
still pass the exact model capability gate below.

## Workflow

1. Keep the existing Java/Kotlin language decision and build tool; do not add a
   second JVM language merely for an agent library.
2. Define the non-agent baseline, typed request/result, model endpoint/exact
   model, allowed tools, and no-op behavior.
3. Use one ADK agent with narrow read-only function or MCP tools. The executor
   validates authorization, schema, timeout, and result shape independently of
   model output.
4. Prove the exact server/model combination can make valid tool calls, return
   schema-conforming structured output, decline unnecessary calls, recover from
   malformed calls, and stop at a maximum-step boundary.
5. Add sessions, memory, graph workflows, A2A, or persistence only when the
   product visibly needs resume, routing, or cross-agent behavior. Document
   retention, restart recovery, and migrations.
6. Test fake tools first, then model-adapter integration in a read-only or
   disposable environment. Report attempted and executed side effects apart.
7. Promote external writes only through `auto-with-escalation` with the exact
   target, action, evidence, and approval point named.

## Validation

Use the existing build owner: `./gradlew test`, `mvn test`, or `sbt test`.
Include unit tests for domain/tool authorization, agent workflow tests with
fake tools, and an opt-in local-model capability smoke test. Do not make a
downloaded model or live endpoint a normal unit-test prerequisite.

## Guardrails

- Do not make Gemini or Google Cloud a required dependency of a local-first
  service unless the product explicitly chooses it.
- Do not expose an agent API publicly or start a background runtime by default.
- Do not trust an agent instruction as an authorization boundary.
- Do not add A2A, MCP, graphs, or multi-agent delegation without a concrete
  caller and a testable state/recovery need.
