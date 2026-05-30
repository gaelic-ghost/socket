---
name: swift-openapi-client-workflow
description: Build, integrate, test, and diagnose Swift OpenAPI Generator clients in Apple-platform apps and Swift packages using OpenAPIURLSession, OpenAPIRuntime, URLSessionTransport, SwiftPM plugins, Apple docs, Dash docsets, and clear handoffs to server-side Swift OpenAPI workflows when the API contract or server transport changes.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: apple-dev-skills
  category: apple-swift-openapi-client
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(find:*) Bash(sqlite3:*) Bash(curl:*)
---

# Swift OpenAPI Client Workflow

## Purpose

Add or diagnose generated Swift OpenAPI clients in Apple-platform code without confusing app-side networking with server-side transport work.

The practical decision is where the OpenAPI document lives, which app or package target runs Swift OpenAPI Generator, how the generated `Client` is configured with `OpenAPIURLSession`, how calls are isolated from UI state, and which tests prove request, response, auth, cancellation, and error behavior.

## When To Use

- Use this skill when an iOS, macOS, watchOS, tvOS, visionOS, or Swift package client should call an HTTP API from an OpenAPI description.
- Use this skill when adding or changing `swift-openapi-generator`, `swift-openapi-runtime`, or `swift-openapi-urlsession` dependencies for client generation.
- Use this skill when wiring `openapi.yaml`, `openapi.json`, or `openapi-generator-config.yaml` into an app-supporting package or target.
- Use this skill when diagnosing generated client symbols such as `Client`, `APIProtocol`, `Operations`, `Components`, response enums, content-type cases, undocumented responses, or transport errors.
- Use this skill when integrating generated calls into SwiftUI, AppKit, UIKit, Observation, async tasks, app services, or test doubles.
- Do not use this skill for generated server handlers, Vapor transport, Hummingbird transport, JSON-RPC, gRPC, or MCP-style service contracts. Hand that to `server-side-swift:openapi-rpc-workflow` when available.
- Do not use this skill for ordinary `URLSession` networking with no OpenAPI contract.

## Source Check

Start with the Apple and Swift docs gate:

- Use `explore-apple-swift-docs` for Apple framework behavior, `URLSession`, Foundation networking, Xcode package integration, Swift concurrency, Observation, SwiftUI, UIKit, AppKit, or platform lifecycle behavior.
- Use local Dash or official docs before claiming current Apple or Swift API behavior.
- Look in Dash Swift docsets for `appleswiftopenapigenerator`, `appleswiftopenapiruntime`, `appleswiftopenapiurlsession`, `swiftlangswiftpackagemanager`, and Apple Foundation or platform docs when available.
- Use [Introducing Swift OpenAPI Generator](https://www.swift.org/blog/introducing-swift-openapi-generator/) for the official client/server overview, generated `Client`, `APIProtocol`, `ClientTransport`, and `URLSessionTransport` shape.
- Use [apple/swift-openapi-generator](https://github.com/apple/swift-openapi-generator) for current generator behavior, plugin setup, examples, and supported OpenAPI features.
- Use [apple/swift-openapi-runtime](https://github.com/apple/swift-openapi-runtime) for generated runtime types, middleware concepts, and shared abstractions.
- Use [apple/swift-openapi-urlsession](https://github.com/apple/swift-openapi-urlsession) for the `OpenAPIURLSession` transport and platform support.
- Use [Swift Package Manager documentation](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/) for package plugin, target, dependency, and build behavior.

Do not claim current generator, URLSession transport, package-plugin, or Apple framework behavior from memory when current docs can be checked.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - `.xcodeproj`, `.xcworkspace`, package dependencies, and target membership when present
   - OpenAPI document path
   - `openapi-generator-config.yaml`
   - app target, shared client package target, generated-code target, and test targets
   - networking service or API client owner
   - SwiftUI, Observation, AppKit, UIKit, or other UI entry points that call the client
2. Identify the client ownership shape:
   - app target owns generated client directly
   - shared Swift package owns generated client for one or more apps
   - generated client wraps a server-side Swift service in the same workspace
   - existing hand-written client is being replaced or wrapped
3. Confirm the generator stack:
   - Swift OpenAPI Generator package plugin
   - OpenAPIRuntime runtime dependency
   - OpenAPIURLSession transport for Apple-platform URL loading
   - client generation in `openapi-generator-config.yaml`
4. Keep generated transport code away from UI views. Views should call a small app-facing service, model, environment value, or dependency shape that can be tested.
5. Keep the OpenAPI document and generator config reviewable, because they define the generated Swift symbols and response cases.
6. Validate through build, focused client tests, and app or package tests before recommending runtime manual checks.

## Client Integration

When adding Swift OpenAPI client generation:

- add fetchable package dependencies for `swift-openapi-generator`, `swift-openapi-runtime`, and `swift-openapi-urlsession`
- add the `OpenAPIGenerator` plugin to the target that owns the OpenAPI document
- add `OpenAPIRuntime` and `OpenAPIURLSession` products to the generated-client target
- configure `openapi-generator-config.yaml` to generate `types` and `client`
- instantiate generated `Client` with a documented server URL and `URLSessionTransport`
- keep base URL, auth tokens, and environment selection outside generated types
- keep secrets out of source control

For Xcode app projects, preserve project ownership. If package dependency or target membership changes require Xcode-aware mutation, hand off to `xcode-build-run-workflow` rather than editing `.pbxproj` casually.

For Swift package clients, keep `Package.swift` readable and intentional. Prefer SwiftPM commands or focused manifest edits that match the existing package style.

## App-Side Behavior

When connecting generated clients to app code:

- isolate generated response enums from UI views with a small app-facing API when the UI would otherwise switch over transport details everywhere
- handle documented response cases explicitly
- handle `.undocumented` responses with a readable error path
- preserve task cancellation; do not hide `CancellationError` behind generic networking failures
- keep authentication, retry, logging, and metrics in a transport or app-service boundary instead of scattering them across views
- map generated schemas into local app models only when the app needs persistence, editing, identity, or UI-specific state
- avoid using generated types as SwiftData, Core Data, or UI state models unless the generated schema is intentionally stable enough for that job

When an API contract change is needed, stop and surface that as server or contract work. Do not quietly patch the generated client around a mismatched server contract.

## Testing And Validation

Choose the smallest useful check:

- `swift build` to force package-plugin generation and type checking
- `swift test` for package-level client wrappers, request mapping, response handling, and fake transport behavior
- Xcode build or test workflow when the app target, scheme, simulator, or package integration is the real risk
- local HTTP checks only when integration with a real server, auth header, TLS, cookie, redirect, or streaming behavior must be proven end to end

Prefer fake `ClientTransport` or app-service seams for tests when the behavior does not require a real network. Use real `URLSessionTransport` checks only when Foundation networking behavior is the thing being verified.

When validation fails, name the exact OpenAPI operation, generated symbol, target, package plugin, transport, response case, or Apple framework surface involved. Include the likely cause, such as a missing config file, wrong target plugin placement, stale operation ID, unsupported schema shape, missing `OpenAPIURLSession` dependency, target membership drift, or an app lifecycle call running from the wrong task boundary.

## Output Shape

Return:

1. `Client shape`: OpenAPI document, generator config, target ownership, generated symbols, transport, and app-facing owner.
2. `Docs used`: Apple, Swift, Dash, GitHub, or SwiftPM docs consulted.
3. `Command path`: exact SwiftPM, Xcode, generator, validation, test, run, or HTTP commands run or recommended.
4. `Behavior`: operations, inputs, outputs, auth, cancellation, errors, UI handoff, and contract-change decisions.
5. `Validation`: build, test, app run, fake transport, real HTTP, or skipped checks.
6. `Handoffs`: server-side OpenAPI/RPC, Xcode build/run, Xcode testing, Swift package, docs exploration, persistence, or observability follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not turn an Apple app workflow into server-side transport work.
- Do not hide API contract mismatches behind app-side adapters without saying the server contract needs attention.
- Do not commit generated caches, secrets, local server URLs as production defaults, or machine-local dependency paths.
- Do not hand-edit `Package.resolved`.
- Do not edit Xcode project files casually; use Xcode-aware workflows when project membership or scheme behavior is part of the change.
- Do not let generated response enums leak into every view when a small app-facing service would keep UI code readable and testable.
