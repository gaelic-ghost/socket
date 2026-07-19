---
name: build-acp-agent
description: Design, implement, test, and package an ACP agent/server. Use for protocol negotiation, sessions, streaming updates, tool rendering, permissions, authentication, SDK choice, and registry submission.
metadata:
  hermes:
    category: agent-portability
    tags: [acp, json-rpc, sdk, registry, agent-development]
---

# Build ACP Agent

Build the agent process that an ACP client launches. Do not build an editor
plug-in or MCP server when the requirement is an editor-native coding agent.
Read `references/acp-implementation-map.md` before selecting an SDK or registry
distribution.

## Implementation Workflow

1. Define concrete client targets and the user-visible behavior they require.
2. Use the current stable ACP protocol and an official SDK when its language and
   runtime fit. Use raw JSON-RPC only when an SDK cannot support a required
   platform or feature.
3. Implement initialization first:
   - negotiate `protocolVersion`
   - advertise only implemented agent capabilities
   - inspect client filesystem and terminal capabilities before using them
   - advertise real authentication methods and implementation information
4. Implement the required session baseline: new, prompt, cancel, and update.
5. Add optional load, resume, fork, list, close, delete, modes, configuration,
   plans, slash commands, rich prompt content, or MCP transports only with
   matching capability declarations and tests.
6. Render tool calls, diffs, terminals, plans, and streamed content in the ACP
   structures the target clients understand.
7. Route dangerous operations through permission requests and fail closed when
   approval transport fails or times out.
8. Keep stdout exclusively for ACP JSON-RPC. Send logs and diagnostics to
   stderr without leaking credentials or prompt content unnecessarily.
9. Bind every session to its client-provided cwd and any negotiated additional
   roots. Isolate cancellation, model choice, history, and mutable state by
   session.
10. Test initialization, authentication, session lifecycle, streaming,
    cancellation, permissions, invalid messages, process shutdown, and each
    advertised optional capability against representative clients.

## Distribution And Registry

- Treat source support, package publication, and canonical registry publication
  as three separate states.
- Publish a fetchable binary, `npx`, or `uvx` distribution that launches the
  ACP process directly and reproducibly.
- Keep the source-owned registry manifest version aligned with the published
  package.
- Submit the manifest to the canonical ACP Registry and do not claim registry
  availability until the live registry feed contains the entry.
- Require a genuine agent-owned or terminal authentication method when the
  registry requires authentication discovery.
- Do not replace an official package with an unrelated third-party launcher
  merely to satisfy a distribution shape.

## Host Validation

- Validate Zed with a custom agent during development, inspect ACP logs, then
  verify the canonical registry path after publication.
- Validate Xcode through its documented Add an Agent flow and Xcode-owned
  permissions. Keep Xcode tool behavior separate from protocol conformance.
- Validate Hermes-specific changes against `hermes acp --check` plus the
  Hermes adapter's session, approval, cwd, and provider behavior.

## Guards

- Do not infer wire compatibility from SDK, schema-artifact, or package version
  numbers; use negotiated ACP protocol version and capabilities.
- Do not advertise methods that are stubs or only work in one client.
- Do not make ACP a general agent-to-agent orchestration layer.
- Do not embed provider secrets in registry manifests, launch arguments, logs,
  or test fixtures.

## Report

Report client targets, SDK and protocol version, required and optional methods,
capability matrix, auth flow, session/state model, permission behavior,
distribution source, registry state, tests, and client-specific limitations.
