---
name: build-dotnet-agent-service
description: Build a local-first F# or C# Semantic Kernel agent service with explicit tools, model capability checks, evaluation fixtures, and draft-before-write promotion.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with F#, C#, ASP.NET Core, and the dotnet CLI on macOS or other supported .NET environments.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: dotnet-agent-service
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(dotnet:*)
---

# Build .NET Agent Service

Use this skill when Semantic Kernel's plugin/function orchestration solves a
real .NET application need. Preserve F# and C# equality: ask for the language
when a new project has no established choice, and do not add C# only to host an
agent.

## Source Check

- Semantic Kernel: <https://learn.microsoft.com/en-us/semantic-kernel/overview/>
- .NET: <https://learn.microsoft.com/dotnet/>
- ASP.NET Core: <https://learn.microsoft.com/aspnet/core/>

## Workflow

1. Establish the deterministic baseline, typed input/output, chosen language,
   exact model endpoint/model, tool permissions, and no-op result.
2. Use Semantic Kernel only for a named plugin/function, planning, or
   orchestration requirement. Keep domain logic in F# modules or C# domain
   types rather than embedding it in prompt or endpoint code.
3. Start with narrow read-only functions. The host validates authorization,
   schemas, timeouts, and output independently of model responses.
4. Prove valid tool-call JSON, structured output, no-call behavior, malformed
   call recovery, maximum-step stopping, and grounded observations on the exact
   local/self-hosted server and model; HTTP compatibility alone is insufficient.
5. Add memory, planners, background work, or an ASP.NET endpoint only when the
   application requires it. Name retention, restart, and failure behavior.
6. Add fake-plugin tests, structured-result tests, denied-write tests, and
   opt-in local-model smoke tests. External writes remain draft-only until an
   exact `auto-with-escalation` approval gate is satisfied.

## Validation

Run the repository's narrowest `dotnet build` and `dotnet test` commands.
Separate fake-tool behavior from model-adapter smoke evidence, and report
attempted versus executed side effects.

## Guardrails

- Do not add Semantic Kernel to a library or service that only needs one direct
  model request.
- Do not store secrets, local endpoint credentials, prompts, or traces in
  source control.
- Do not start a background agent, schedule, or public endpoint by default.
- Do not use model output as permission to call a destructive plugin.
