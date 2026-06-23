---
name: app-sync-workflow
description: Plan, implement, test, and diagnose app sync contracts in server-side Swift services, including incremental change feeds, cursor or token semantics, idempotent writes, conflict handling, optimistic concurrency, deleted-record/tombstone behavior, background job handoffs, API-shape coordination, and Vapor or Hummingbird integration.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Vapor, Hummingbird, SwiftPM, HTTP APIs, OpenAPI, RPC, persistence, background jobs, and client/server sync services on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-app-sync
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# App Sync Workflow

## Purpose

Design, implement, test, or diagnose server-side sync behavior without mixing the sync contract into unrelated routing, persistence, OpenAPI, RPC, auth, or background-job work.

The practical decision is how clients and the server agree on state over time: what changed, what the client has already seen, how writes avoid duplication, how conflicts are detected, how deletions are represented, and how both sides recover after retries, offline edits, or partial failure.

## When To Use

- Use this skill when adding or changing incremental sync endpoints, change feeds, cursor or token semantics, idempotent writes, conflict handling, optimistic concurrency, tombstones, deleted-record feeds, client checkpointing, sync-related background jobs, or API contracts for app state synchronization.
- Use this skill when diagnosing duplicated writes, missed changes, stale cursors, conflict loops, wrong-owner sync data, deleted records reappearing, retry bugs, out-of-order changes, pagination drift, or partial sync failures.
- Use this skill when a Vapor or Hummingbird service needs a sync contract for an Apple app, web app, CLI, or another service.
- Use this skill when deciding whether sync should be ordinary HTTP routes, OpenAPI-backed endpoints, JSON-RPC, gRPC, server-sent events, WebSockets, polling, or background jobs.
- Do not use this skill for ordinary CRUD routes, database migrations, generated OpenAPI plumbing, auth, observability, Docker, Fly.io, or local SwiftPM work unless sync semantics are the reason for the change.
- Do not absorb client-side storage or Apple-platform background task behavior. Hand client persistence and app scheduling to Apple-platform skills.

## Source Check

Use repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Swift package DocC, and then official docs or source when Dash/local coverage is missing or stale. Check one of those source-specific paths before claiming framework, protocol, or HTTP behavior:

- [HTTP Semantics RFC 9110](https://httpwg.org/specs/rfc9110.html)
- [Vapor routing](https://docs.vapor.codes/basics/routing/)
- [Vapor validation](https://docs.vapor.codes/basics/validation/)
- [Vapor Fluent migrations](https://docs.vapor.codes/fluent/migration/)
- [Vapor queues](https://docs.vapor.codes/advanced/queues/)
- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird Testing](https://docs.hummingbird.codes/2.0/documentation/hummingbird/testing/)
- [Swift Jobs](https://github.com/hummingbird-project/swift-jobs)

Use OpenAPI, RPC, persistence, auth, observability, deployment, or Apple-platform docs when the sync design depends on generated contracts, transport semantics, schema, identity, logging, background jobs, deployment guarantees, or client behavior.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - Vapor or Hummingbird route and middleware structure
   - API contract files, generated code, or RPC definitions
   - persistence models, migrations, indexes, timestamps, version fields, tombstones, and audit tables
   - auth tenant/account ownership boundaries
   - background jobs or queues
   - tests for pagination, conflicts, retries, offline edits, and deleted records
2. Identify the sync job:
   - full initial snapshot
   - incremental changes since cursor
   - push local client changes
   - reconcile conflicts
   - propagate deletes
   - enqueue expensive side effects
   - stream or poll for updates
3. Define the server-owned truth:
   - stable object identity
   - version or revision token
   - ordering key for changes
   - delete representation
   - ownership and authorization scope
   - retention window for change history
4. Define client contract:
   - cursor format and lifetime
   - page size and ordering
   - retry behavior
   - idempotency key behavior
   - conflict response shape
   - when clients must restart a full sync
5. Add tests that prove retry, conflict, pagination, deletion, and authorization behavior.

## Contract Shape

Keep sync contracts boring and explicit.

Name:

- resource types included in the sync
- route or method used to fetch changes
- route or method used to submit writes
- cursor, token, timestamp, revision, or ETag fields
- ordering rule
- page size and next-page behavior
- conflict and validation errors
- deletion/tombstone representation

Do not expose database row order as the sync order unless it is intentionally stable, indexed, and documented.

Opaque cursors are usually safer than client-parsed cursors because the server can evolve internal ordering. If cursors expire, define the exact restart behavior.

## Idempotent Writes And Retries

Assume clients, proxies, and background tasks may retry after timeouts or network loss.

For write APIs:

- use client-generated stable IDs or explicit idempotency keys when duplicate creation is a risk
- define whether repeated identical writes return the existing result or an error
- keep idempotency scope bounded by actor, resource, operation, and retention window
- make side effects such as emails, notifications, webhooks, or jobs idempotent too
- test retry after success-but-lost-response

Do not rely on clients "not retrying" as a correctness rule.

## Conflict Handling

A conflict exists when a client writes based on state the server no longer accepts.

Use a clear mechanism:

- revision field
- ETag or conditional request
- updated-at version with documented precision limits
- server-side compare-and-swap
- domain-specific merge policy

Return conflict information that lets the client decide what to do next without leaking data from resources the actor cannot access.

Use `409 Conflict` for domain conflicts and `412 Precondition Failed` for failed HTTP preconditions when the API uses conditional request semantics. Keep the repository's existing status-code style when it already documents one.

## Deletes And Tombstones

Deleted state must be syncable.

Decide:

- soft delete, tombstone table, audit log, or hard delete with change-feed record
- how long deleted records remain visible to sync
- whether deletes include actor, timestamp, reason, or version
- whether child records cascade, detach, or remain independently syncable
- what happens when a client updates a deleted record

Do not hard-delete records from sync history before all active clients can learn about the deletion unless the app has a full-resync fallback.

## Background Work And Streams

Use background jobs when sync writes trigger expensive side effects that should not block the request.

Use streaming, WebSockets, or server-sent events only when polling or ordinary incremental sync is not enough. Streaming transports still need replay or catch-up behavior after disconnects.

Hand transport-specific decisions to `openapi-rpc-workflow` when the main question is API style, generated contracts, JSON-RPC, gRPC, MCP-style tools, WebSockets, or plain HTTP.

Use `persistence-workflow` when the main risk is schema, indexes, migrations, query performance, or transaction boundaries.

## Auth, Privacy, And Observability

Every sync query and write must be scoped to the authenticated actor and tenant.

Test:

- actor only receives authorized records
- actor cannot advance a cursor into another tenant's data
- conflict responses do not leak private resource state
- deleted records remain scoped correctly

Use `auth-authorization-workflow` for identity and policy design.

Use `observability-tracing-workflow` for safe sync diagnostics, including cursor names, page counts, operation IDs, conflict counts, retry counts, and latency. Do not log raw cursors if they contain sensitive state.

## Testing

Choose tests that prove sync correctness:

- initial empty sync
- initial full sync
- incremental sync after one change
- pagination with stable ordering
- retry of a successful write
- duplicate create attempt
- stale revision conflict
- delete propagation
- update after delete
- cursor expiration or retention-window miss
- unauthorized cross-tenant read and write
- background job idempotency if side effects are queued

Prefer deterministic fixtures with explicit clocks, IDs, and revision values when the repository's test setup allows it.

## Handoffs

Use `vapor-server-workflow` or `hummingbird-server-workflow` for framework route, middleware, request context, and handler structure.

Use `openapi-rpc-workflow` when the sync API contract, generated types, or transport style is the primary work.

Use `persistence-workflow` for models, migrations, query design, transactions, indexes, and data-retention behavior.

Use `auth-authorization-workflow` for identity, tenant scoping, permissions, tokens, and session behavior.

Use `observability-tracing-workflow` for logs, metrics, traces, conflict counters, and privacy-safe diagnostics.

Use deployment skills when background workers, queue processes, or hosted runtime config must be deployed.

## Output Shape

Return:

1. `Sync shape`: resources, routes or transport, cursor, ordering, idempotency, conflict model, delete model, jobs, auth scope, and tests.
2. `Docs used`: HTTP, Vapor, Hummingbird, OpenAPI/RPC, persistence, auth, observability, jobs, deployment, or Apple-platform docs consulted.
3. `Behavior`: fetch, write, retry, conflict, delete, pagination, retention, authorization, and background work.
4. `Command path`: exact build, test, migrate, run, job, or HTTP commands run or recommended.
5. `Validation`: tests, migration checks, manual HTTP checks, job checks, or diagnostic evidence.
6. `Handoffs`: framework, OpenAPI/RPC, persistence, auth, observability, background jobs, deployment, or client follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not design sync around unstable database row order.
- Do not rely on clients avoiding retries.
- Do not leak cross-tenant or private resource state through cursors, conflicts, logs, or deleted-record feeds.
- Do not hard-delete sync history without a documented full-resync fallback or retention decision.
- Do not turn sync into a custom transport when ordinary HTTP routes or existing OpenAPI/RPC guidance fits.
- Do not duplicate Apple-platform client storage or background-execution guidance in this server-side workflow.
