---
name: openapi-rpc-workflow
description: Design, generate, implement, test, and diagnose Swift OpenAPI and RPC-style server contracts using Swift OpenAPI Generator, OpenAPIRuntime, OpenAPIHummingbird, OpenAPIVapor, SwiftPM plugins, Dash docsets, official GitHub/SPI documentation, and clear handoffs to Vapor or Hummingbird workflows.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Swift OpenAPI Generator, OpenAPIRuntime, Hummingbird, Vapor, SwiftPM, and server-side Swift services on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-openapi-rpc
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(find:*) Bash(sqlite3:*) Bash(curl:*)
---

# OpenAPI And RPC Workflow

## Purpose

Build or diagnose contract-first server-side Swift work without mixing up three different things:

- the OpenAPI description, which is the HTTP API contract
- Swift OpenAPI Generator, which generates Swift types, client calls, and server protocol stubs from that contract
- the server transport, such as OpenAPIHummingbird or OpenAPIVapor, which registers a generated `APIProtocol` implementation on a real Hummingbird or Vapor app

For RPC-style services, first identify whether the user really means OpenAPI-backed HTTP operations, JSON-RPC over HTTP, gRPC, MCP-style tool calls, or a framework-specific client/server contract. Keep plain HTTP routes as the default when the service does not need a stronger protocol contract.

## When To Use

- Use this skill when adding, editing, validating, or consuming an OpenAPI document in a Swift package.
- Use this skill when wiring Swift OpenAPI Generator into `Package.swift`, `openapi-generator-config.yaml`, generated sources, or SwiftPM plugin commands.
- Use this skill when implementing generated server stubs with `APIProtocol`, `Operations`, `Components`, `OpenAPIRuntime`, `OpenAPIHummingbird`, or `OpenAPIVapor`.
- Use this skill when choosing between Hummingbird and Vapor as the server transport for a generated API.
- Use this skill when diagnosing generated-code drift, operation ID changes, missing schemas, request/response typing, transport registration, or OpenAPI validation failures.
- Use this skill when a user says "RPC" and the next decision is whether OpenAPI, JSON-RPC, gRPC, MCP, or ordinary routes fit the service boundary.
- Do not use this skill for generic Vapor or Hummingbird route work that has no generated OpenAPI contract. Use the framework-specific workflow instead.
- Do not use this skill for Apple-platform app, simulator, preview, or Xcode project membership work.

## Source Check

Prefer repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Swift package DocC first, then official online docs when Dash/local coverage is missing or stale:

- Dash Swift docsets usually live under `~/Library/Application Support/Dash/Swift DocSets/`.
- Look for `appleswiftopenapigenerator`, `appleswiftopenapiruntime`, `hummingbirdprojectswiftopenapihummingbird`, `vaporswiftopenapivapor`, `hummingbirdprojecthummingbird`, `vaporvapor`, and `swiftlangswiftpackagemanager`.
- If querying Dash directly, inspect each docset's `Contents/Resources/docSet.dsidx` with `sqlite3` and search for symbols or guide titles before falling back to the web.
- Use [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator) for generator behavior, package plugin setup, examples, supported OpenAPI features, and links to generated-code documentation.
- Use [apple/swift-openapi-runtime](https://github.com/apple/swift-openapi-runtime) for generated runtime types and middleware concepts.
- Use [hummingbird-project/swift-openapi-hummingbird](https://github.com/hummingbird-project/swift-openapi-hummingbird) for Hummingbird server transport behavior.
- Use [vapor/swift-openapi-vapor](https://github.com/vapor/swift-openapi-vapor) for Vapor server transport behavior.
- Use [hummingbird-project/hummingbird-lambda](https://github.com/hummingbird-project/hummingbird-lambda) when diagnosing Hummingbird-generated AWS Lambda adapter behavior.
- Use [swift-server/swift-openapi-lambda](https://github.com/swift-server/swift-openapi-lambda) only when the repository intentionally chose that separate OpenAPI Lambda transport.
- Use [Swift Package Manager documentation](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/) for SwiftPM plugin, target, build, and test behavior.
- Use [OpenAPITools/openapi-generator](https://github.com/OpenAPITools/openapi-generator) only when the repository is intentionally using the Java-based OpenAPI Generator CLI instead of Apple's Swift package plugin.

Do not claim current generator, transport, or package-plugin behavior from memory when current official docs or local Dash docsets can be checked.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - OpenAPI document path, usually `openapi.yaml`, `openapi.yml`, or `openapi.json`
   - `openapi-generator-config.yaml`
   - generated source directories or build-plugin output assumptions
   - executable target, library target, and test targets
   - Hummingbird or Vapor app construction and route registration
   - generated names such as `APIProtocol`, `Operations`, `Components`, `Client`, and transport imports
2. Identify the contract owner:
   - spec-first service where the OpenAPI document drives generated server stubs
   - existing service where routes need an OpenAPI description
   - shared client/server package
   - internal RPC-like boundary where OpenAPI may or may not be the right shape
3. Confirm the generator stack:
   - Apple's Swift OpenAPI Generator package plugin for SwiftPM-first projects
   - OpenAPIHummingbird for Hummingbird server registration
   - OpenAPIVapor for Vapor server registration
   - URLSession or AsyncHTTPClient transports for generated clients when needed
   - OpenAPITools CLI only when the repo already chose that toolchain
4. Keep generated code out of source control when the project uses SwiftPM build plugins, unless the repository explicitly commits generated sources.
5. Keep the OpenAPI document and generator config reviewable, because they are the API contract and the generated Swift surface depends on them.
6. Validate in the narrowest useful order: spec validity, generation/build, server registration tests, then runtime HTTP checks if needed.

## Contract Design

For OpenAPI-backed work:

- give every operation a stable, readable `operationId`
- model request bodies, response bodies, parameters, headers, and status codes explicitly
- use shared schemas for values that cross more than one operation
- keep error responses typed enough that clients can handle them predictably
- avoid exposing internal database or framework types in the contract
- treat operation ID or schema renames as API surface changes, because generated Swift symbol names may change

For RPC-style work:

- choose OpenAPI when the boundary is HTTP operations with typed requests and responses
- choose JSON-RPC only when method-call semantics are actually part of the protocol
- choose gRPC only when the project has protobuf, streaming, or interoperability reasons that justify the extra toolchain
- choose MCP-style tools only when the caller is an agent/tool runtime rather than a normal HTTP API client
- keep ordinary Hummingbird or Vapor routes when the API is small, local, or not ready for a shared generated contract

## SwiftPM And Generator Setup

When adding Apple's Swift OpenAPI Generator to an existing package:

- add the generator package as a dependency in `Package.swift`
- add the plugin to the target that owns the OpenAPI document
- add `OpenAPIRuntime` and the selected transport product to the target dependencies
- add or update `openapi-generator-config.yaml` for generated client, server, types, or access modifier choices
- keep dependency URLs fetchable from GitHub or package registries, not local paths

Before editing `Package.swift`, inspect the current package tools version, target names, dependency style, and whether the repo pins exact versions, branches, or ranges.

## Hummingbird Transport

Use OpenAPIHummingbird when the service already uses Hummingbird or when Hummingbird is the chosen server framework.

For projects generated by current `hb init` Lambda + OpenAPI templates, keep the distinction sharp:

- `OpenAPIHummingbird` registers generated `APIProtocol` handlers on the Hummingbird `Router`.
- `hummingbird-lambda` adapts that Hummingbird router to the selected AWS Lambda event type, such as API Gateway V2.
- `swift-openapi-lambda` is a separate valid Swift OpenAPI Lambda transport, but it is not the transport generated by the Hummingbird template.
- When a project may need both long-running server and Lambda deployments, keep the generated `APIProtocol` implementation transport-neutral and put server or Lambda differences in thin executable or adapter targets.

Typical shape:

- build the `Router`
- create the handler type that conforms to generated `APIProtocol`
- call generated `registerHandlers` on the Hummingbird router or documented transport
- create and run the `Application` through the repository's existing Hummingbird lifecycle

For request-context access from generated handlers, check current OpenAPIHummingbird docs before implementing. The transport documentation has used a task-local middleware pattern so generated endpoints can reach the Hummingbird request context without turning the generated protocol implementation into a generic dependency container.

Hand off to `hummingbird-server-workflow` for route grouping, middleware order, request contexts, Hummingbird testing, service lifecycle, and deployment details that are not specific to OpenAPI generation.

## Vapor Transport

Use OpenAPIVapor when the service already uses Vapor or when Vapor is the chosen server framework.

Typical shape:

- create or reuse the Vapor `Application`
- create `VaporTransport` with the app or routes builder
- create the handler type that conforms to generated `APIProtocol`
- call generated `registerHandlers` on the transport
- run the app through the repository's existing `swift run App serve`, `app.execute()`, or documented command path

For request access from generated handlers, check current OpenAPIVapor docs before implementing. The transport documentation includes a request-injection pattern using `swift-dependencies`; only add that dependency when the service genuinely needs direct Vapor `Request` access inside generated handlers.

Hand off to `vapor-server-workflow` for controllers, middleware, Fluent migrations, environment setup, app commands, and deployment details that are not specific to OpenAPI generation.

## Testing And Validation

Prefer this order:

1. Validate the OpenAPI document with the repository's existing validator when one exists.
2. Run the smallest SwiftPM command that forces generation and type-checking, usually `swift build` or `swift test`.
3. Add pure Swift tests for domain transformations that generated handlers call.
4. Add Hummingbird or Vapor route tests for generated handler registration, request decoding, response encoding, status codes, and error bodies.
5. Use `curl` only when runtime binding, headers, streaming, middleware, or end-to-end server behavior cannot be proven through tests.

When validation fails, name the exact contract element, generated symbol, package target, or transport registration point that failed. Include the likely cause, such as a missing `operationId`, unsupported schema shape, stale generated output assumption, wrong target plugin configuration, missing transport dependency, or framework middleware order.

## Output Shape

Return:

1. `Contract shape`: OpenAPI document path, generator config, generated Swift surface, selected transport, and handler owner.
2. `Docs used`: Dash docsets, GitHub repositories, SPI docs, or official framework docs consulted.
3. `Command path`: exact SwiftPM, generator, validation, test, run, or HTTP commands run or recommended.
4. `Behavior`: operations, inputs, outputs, errors, transport registration, framework handoffs, and RPC-fit decision.
5. `Validation`: spec checks, build, tests, server run, or HTTP check results.
6. `Handoffs`: Vapor, Hummingbird, SwiftPM, gRPC, MCP, OpenAPITools CLI, client generation, deployment, or observability follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not call all RPC-shaped work OpenAPI; make the protocol choice explicit.
- Do not use OpenAPITools CLI when the Swift package is using Apple's Swift OpenAPI Generator plugin.
- Do not commit machine-local dependency paths, generated cache directories, secrets, or local service credentials.
- Do not silently rename operation IDs or shared schemas in public contracts.
- Do not add Vapor request injection, Hummingbird task-local context access, gRPC, protobuf, or MCP runtime dependencies unless the project has a concrete need for that protocol behavior.
- Do not treat generated handlers as the place for unrelated business rules; call tested domain code from the generated protocol implementation.
