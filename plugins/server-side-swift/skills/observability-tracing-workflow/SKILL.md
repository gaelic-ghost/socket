---
name: observability-tracing-workflow
description: Plan, implement, test, and diagnose observability for server-side Swift services, including Swift Logging, Swift Metrics, Swift Distributed Tracing, OpenTelemetry handoffs, request correlation, trace propagation, structured log fields, metric naming, health signals, privacy-safe diagnostics, and Vapor or Hummingbird integration.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Swift Logging, Swift Metrics, Swift Distributed Tracing, OpenTelemetry, Vapor, Hummingbird, SwiftNIO, and server-side Swift services on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-observability
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Observability And Tracing Workflow

## Purpose

Add, refine, or diagnose observability in a server-side Swift service without confusing production signals with app behavior, deployment config, or low-level networking implementation.

The practical decision is what operators need to know from logs, metrics, traces, health checks, and diagnostics when a service is slow, failing, overloaded, misconfigured, or behaving correctly. Good instrumentation should make incidents easier to understand without leaking secrets or drowning normal operation in noise.

## When To Use

- Use this skill when adding or changing Swift Logging, Swift Metrics, Swift Distributed Tracing, OpenTelemetry wiring, request IDs, trace propagation, log metadata, metric labels, spans, sampling, exporter configuration, or diagnostic health signals.
- Use this skill when diagnosing missing logs, noisy logs, missing spans, broken trace propagation, misleading metrics, high-cardinality labels, privacy leaks, request-correlation gaps, or unclear production failure evidence.
- Use this skill when deciding what a Vapor or Hummingbird service should log, measure, trace, or expose for operations.
- Use this skill when a deployment, Docker, or Fly.io task needs better runtime signals but not when the deployment config itself is the primary change.
- Do not use this skill for ordinary route, middleware, model, migration, Dockerfile, Fly.io, or SwiftNIO pipeline work unless observability behavior is the reason for the change.
- Do not add external telemetry vendors, collectors, exporters, dashboards, or alerting services unless the user asked for that integration or the repo already depends on it.

## Source Check

Use current official docs and source before claiming observability behavior:

- [Swift Logging](https://github.com/apple/swift-log)
- [Swift Metrics](https://github.com/apple/swift-metrics)
- [Swift Distributed Tracing](https://github.com/apple/swift-distributed-tracing)
- [OpenTelemetry Swift](https://github.com/open-telemetry/opentelemetry-swift)
- [OpenTelemetry Swift documentation](https://opentelemetry.io/docs/languages/swift/)
- [Vapor logging](https://docs.vapor.codes/basics/logging/)
- [Vapor tracing](https://docs.vapor.codes/advanced/tracing/)
- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird ecosystem](https://hummingbird.codes/ecosystem/)

Use deployment, Docker, Fly.io, persistence, auth, or SwiftNIO docs when the signal depends on process lifecycle, health checks, database queries, credentials, channel pipelines, or runtime configuration.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - logging, metrics, tracing, OpenTelemetry, or exporter dependencies
   - app startup and service lifecycle
   - Vapor or Hummingbird middleware and request context
   - SwiftNIO handlers or async tasks that already emit signals
   - deployment config, log levels, health checks, and environment variables
   - tests or snapshots for observable behavior
2. Identify the operational question:
   - Which request failed?
   - Which dependency is slow or unavailable?
   - Which worker, command, or route is overloaded?
   - Which deploy, config, migration, or secret changed behavior?
   - Which user-visible action needs correlation without exposing private data?
3. Choose the smallest useful signal:
   - log for discrete events and operator-readable context
   - metric for aggregate counts, gauges, durations, and rates
   - trace span for causal request or job flow across async boundaries
   - health/readiness signal for deploy and routing decisions
4. Keep signal names and labels stable.
5. Keep high-cardinality data out of metric labels.
6. Keep secrets and sensitive personal data out of logs, traces, metrics, and health responses.
7. Add tests or manual checks that prove instrumentation is active when the repository has a reasonable way to do so.

## Logging

Use Swift Logging as the default logging API for server-side Swift packages unless the repository has already chosen another facade.

When adding logs:

- choose a level that matches operator urgency
- include concrete context such as route, command, job, dependency, record type, config key, or operation name
- include correlation IDs, request IDs, trace IDs, or user-safe account identifiers when the service already has that shape
- make error messages human-readable and specific
- avoid logging secret values, tokens, passwords, cookie contents, authorization headers, raw connection strings, private keys, or sensitive payloads

Prefer structured metadata over string concatenation when the logger supports it. Use consistent field names for the same concept across the service.

Do not add noisy per-item logs inside hot loops, request bodies, event-loop reads, or high-volume background jobs unless the log is sampled, debug-only, or explicitly needed for a short diagnostic.

## Metrics

Use Swift Metrics when the service needs aggregate numeric signals.

Prefer metrics for:

- request counts and durations by stable route or operation
- job counts, durations, failures, retries, and queue depth
- database or dependency latency
- cache hits and misses
- stream sizes, active connections, or back-pressure state
- deploy, startup, migration, and health-related counts

Keep metric labels low-cardinality. Use route templates, operation names, status classes, dependency names, queue names, and fixed outcome names. Do not use raw URLs, user IDs, emails, UUIDs, tokens, request bodies, error messages, or unbounded exception strings as labels.

## Tracing

Use Swift Distributed Tracing or the repository's existing tracing package when causal request flow matters.

Prefer traces for:

- request lifecycle across middleware, handlers, database calls, HTTP clients, jobs, and streaming boundaries
- propagation between services
- diagnosing latency distribution across nested operations
- connecting logs to a request, job, span, or trace ID

Keep span names stable and operation-oriented. Attach only metadata that is safe, bounded, and useful for diagnosis.

When using OpenTelemetry, distinguish:

- API-only instrumentation in libraries
- SDK/exporter setup in applications
- collector, backend, sampling, and dashboard work as deployment or operations scope

Do not add an exporter or vendor SDK just because spans are added. First check whether the application already owns telemetry export.

## Vapor And Hummingbird Integration

For Vapor:

- use Vapor's logging and tracing docs for framework-owned behavior
- prefer middleware for request-wide correlation, metadata, spans, and timing
- keep route-specific logs close to the route, controller, service, or command that owns the behavior
- do not leak auth headers, session cookies, request bodies, or secrets into request logs

For Hummingbird:

- inspect the app's `Application`, `Router`, middleware, and request context shape
- use middleware for request-wide correlation, timing, and propagation
- put per-request context values in request context only when middleware or handlers truly need them
- preserve the framework's existing logger and lifecycle conventions

Use `swiftnio-workflow` when instrumentation crosses into channel handlers, low-level protocol flow, event-loop latency, or back-pressure.

## Health And Readiness Signals

Health signals are operational contracts.

Use liveness for "process is alive" and readiness for "service can safely receive traffic." Readiness can include dependency checks only when the deployment target expects that behavior and the check will not overload dependencies.

Do not expose internal stack traces, secret names with values, database URLs, token details, or private infrastructure addresses in health responses.

Use deployment-specific workflows for wiring health checks into Docker, Fly.io, CI, load balancers, or process managers.

## Testing And Validation

Choose the smallest validation that proves the signal:

- unit test for log metadata, metric labels, span naming, or redaction helpers
- middleware or route test for request IDs, propagation, and response headers
- integration test for exporter or collector behavior only when the repo already has that surface
- local run plus logs or metrics scrape only when runtime behavior matters
- deployment logs or health-check output only when the task is operational

When diagnosis fails, report the exact logger, metric, label, span, propagation header, exporter, route, job, command, environment variable, or deployment surface involved.

## Handoffs

Use `vapor-server-workflow` or `hummingbird-server-workflow` for route, middleware, command, request context, or framework lifecycle changes that are not primarily instrumentation.

Use `swiftnio-workflow` for event-loop, channel, pipeline, back-pressure, or protocol-level instrumentation.

Use `auth-authorization-workflow` when the question is whether auth context is safe to log, trace, or use as an authorization signal.

Use `docker-workflow` or `fly-io-deployment-workflow` when the work is about how logs, health checks, ports, or runtime environment reach a container or hosted platform.

## Output Shape

Return:

1. `Signal shape`: loggers, metrics, spans, health routes, middleware, request context, exporters, and configuration.
2. `Docs used`: Swift Logging, Metrics, Distributed Tracing, OpenTelemetry, Vapor, Hummingbird, deployment, or SwiftNIO docs consulted.
3. `Behavior`: what is logged, counted, timed, traced, propagated, redacted, sampled, or exposed.
4. `Command path`: exact build, test, run, scrape, log, or deploy commands run or recommended.
5. `Validation`: tests, log output, metric scrape, spans, health result, or deployment evidence.
6. `Handoffs`: framework, auth, NIO, persistence, Docker, Fly.io, deployment, or operations follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not log secrets, tokens, authorization headers, cookies, connection strings, private keys, passwords, or sensitive request bodies.
- Do not use high-cardinality values as metric labels.
- Do not add telemetry exporters, vendors, collectors, dashboards, or alerting stacks without explicit scope or existing repo precedent.
- Do not claim observability package behavior from memory when current official docs or source can be checked.
- Do not treat a health endpoint as proof of route correctness unless the route itself was tested.
