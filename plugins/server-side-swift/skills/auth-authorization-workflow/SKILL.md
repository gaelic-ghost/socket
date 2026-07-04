---
name: auth-authorization-workflow
description: Plan, implement, test, and diagnose server-side Swift authentication and authorization for Vapor and Hummingbird services, including Basic and Bearer auth, JWT, sessions, OAuth or OIDC handoffs, password hashing, token lifecycle, middleware placement, request context, route protection, authorization policy, security-sensitive tests, and deployment secret handoffs.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Vapor, Hummingbird, SwiftPM, JWT, sessions, OAuth/OIDC, password hashing, middleware, persistence, and server-side Swift services on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-auth
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Authentication And Authorization Workflow

## Purpose

Add, modify, test, or diagnose server-side Swift authentication and authorization without confusing identity verification, permission checks, client-side credential storage, or transport security.

The practical decision is who the request represents, how that identity was verified, what the identity is allowed to do, where that policy is enforced, how credentials and secrets are stored, and which tests prove the boundary is secure.

## When To Use

- Use this skill when adding or changing server-side authentication, authorization, sessions, JWT, bearer tokens, basic auth, login endpoints, password hashing, token refresh, OAuth or OIDC handoffs, route protection, permission checks, or auth middleware in a Vapor or Hummingbird service.
- Use this skill when diagnosing unexpected `401 Unauthorized`, `403 Forbidden`, token validation, session, cookie, password, middleware ordering, role, scope, tenant, or permission behavior.
- Use this skill when deciding whether identity belongs in a Vapor `req.auth`, a Hummingbird request context, a route-local value, or a domain service.
- Use this skill when deployment work needs auth secrets, signing keys, issuer/audience values, or cookie/session configuration.
- Do not use this skill for Apple-platform Keychain, Sign in with Apple client UI, browser storage, or mobile credential persistence. Hand client storage to the Apple-platform workflow.
- Do not use this skill for generic route, persistence, OpenAPI, Docker, Fly.io, or observability work unless auth behavior is the reason for the change.

## Source Check

Use repo-local Swift files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Swift package DocC, and then official docs or source when Dash/local coverage is missing or stale. Check one of those source-specific paths before claiming auth behavior:

- [Vapor authentication](https://docs.vapor.codes/security/authentication/)
- [Vapor JWT](https://docs.vapor.codes/security/jwt/)
- [Vapor passwords](https://docs.vapor.codes/security/passwords/)
- [Vapor sessions](https://docs.vapor.codes/advanced/sessions/)
- [Vapor Auth source](https://github.com/vapor/vapor)
- [JWTKit](https://github.com/vapor/jwt-kit)
- [Hummingbird Auth](https://github.com/hummingbird-project/hummingbird-auth)
- [Hummingbird documentation](https://docs.hummingbird.codes/)
- [Hummingbird ecosystem](https://hummingbird.codes/ecosystem/)

Use persistence, OpenAPI, observability, Docker, Fly.io, or deployment docs when auth depends on schema, API contracts, log redaction, secrets, TLS, cookies, or environment configuration.

## Planning Workflow

1. Inspect project shape:
   - `Package.swift`
   - Vapor or Hummingbird app setup
   - route groups, middleware, request context, controllers, and handlers
   - user/account/team/role/token/session models
   - password hashing, JWT signing, cookie, session, and OAuth/OIDC config
   - persistence migrations and indexes for identity data
   - tests for anonymous, authenticated, unauthorized, expired, malformed, revoked, and cross-tenant requests
   - deployment secrets and environment variables
2. Separate the boundary:
   - authentication: verifies identity
   - authorization: decides allowed action
   - session or token lifecycle: creates, stores, refreshes, revokes, and expires credentials
   - credential storage: hashes passwords and protects signing or encryption keys
3. Choose the smallest safe mechanism that fits the app:
   - bearer token for API clients
   - session cookie for browser-style apps
   - JWT when stateless signed claims are a real fit
   - OAuth/OIDC when a third-party identity provider owns login
   - internal service token only for service-to-service calls with scoped blast radius
4. Put middleware at the narrowest route group that needs it.
5. Keep authorization policy close to the domain behavior it protects.
6. Add security-sensitive tests before treating the change as complete.

## Authentication

For Vapor:

- use Vapor's documented authenticator and guard middleware model
- keep `req.auth` as authenticated identity state, not as a generic dependency container
- compose authenticators deliberately when more than one credential type may authenticate the same route
- distinguish authentication failure from missing authorization

For Hummingbird:

- verify current Hummingbird Auth docs, README, and source before naming exact package products or APIs
- keep identity in request context only when middleware and handlers need it per request
- preserve the app's existing router and middleware composition style
- avoid copying Vapor-specific `req.auth` patterns into Hummingbird code
- for `hb`-generated Lambda + API Gateway V2 projects, do not treat an openly reachable endpoint as protected just because it is deployed behind Lambda; use app or device evidence, API Gateway authorizers, signed tokens, or another explicit auth boundary before accepting sensitive requests

For any framework:

- never authenticate against hard-coded credentials outside tests or examples
- normalize and validate user identifiers intentionally
- keep password login separate from token verification when that makes tests and policy clearer
- make failure messages useful without confirming whether a specific account exists

## Authorization

Authorization answers whether an authenticated or anonymous actor may perform a specific action.

Model authorization in terms of concrete resources and operations:

- actor: user, service, admin, team member, API client, or anonymous request
- resource: account, project, document, job, token, organization, or tenant
- action: read, create, update, delete, administer, enqueue, export, or impersonate
- policy source: role, scope, ownership, membership, feature flag, entitlement, or explicit ACL

Prefer explicit policy helpers or domain methods over repeated inline conditionals in route handlers. Return `401` when authentication is required and missing or invalid; return `403` when identity is known but not allowed.

Test cross-tenant and wrong-owner access whenever a service stores user-owned or organization-owned data.

## Passwords, Tokens, Sessions, And JWT

Never store plaintext passwords. Use the framework's documented password hashing guidance or an existing repository-approved hashing package.

For tokens:

- store only hashed opaque tokens when tokens are persisted and later compared
- include creation, expiration, rotation, and revocation behavior when relevant
- avoid long-lived all-powerful tokens
- scope service tokens narrowly

For JWT:

- validate issuer, audience, expiration, not-before, algorithm, signature, and key selection when the app depends on those claims
- keep signing keys and private keys in deployment secrets
- avoid putting sensitive personal data or large authorization state in claims
- plan key rotation before relying on JWT for long-lived clients

For sessions and cookies:

- check secure, HTTP-only, SameSite, domain, path, expiration, and proxy/TLS behavior
- keep session storage compatible with multi-instance deployment
- do not assume in-memory sessions work across horizontally scaled services

## OAuth And OIDC Handoffs

Use OAuth/OIDC when a provider owns user login or federated identity.

Before implementing:

- identify the provider, flow, redirect URLs, client type, scopes, issuer, audience, and token endpoint
- store client secrets only in deployment secrets
- validate state and nonce where the flow requires them
- separate provider identity from local application authorization
- plan account linking and duplicate identity behavior

Do not build a custom OAuth/OIDC flow from memory. Use provider docs, framework packages, and security review when external identity is in scope.

## Testing

Choose tests that prove the boundary:

- anonymous request to protected route
- valid authenticated request
- malformed token or credentials
- expired, revoked, wrong-issuer, wrong-audience, or wrong-scope token
- authenticated but unauthorized actor
- cross-tenant or wrong-owner access
- password hash verification and failed password path
- session cookie settings and missing session state
- middleware ordering for grouped routes

Avoid test shortcuts that bypass the exact middleware or policy under review unless the test is intentionally unit-level and another test covers integration.

## Observability And Secrets

Logs and traces may name the auth mechanism, route, actor type, and safe stable IDs. Do not log passwords, raw tokens, authorization headers, cookies, private keys, full JWTs, OAuth codes, refresh tokens, or session contents.

Use `observability-tracing-workflow` when auth diagnostics need correlation IDs, redaction, metrics, or traces.

Use `fly-io-deployment-workflow`, `docker-workflow`, or the repository's deployment workflow when auth secrets, key files, cookie settings, or provider config must reach production.

## Handoffs

Use `vapor-server-workflow` for Vapor route grouping, middleware registration, controllers, commands, and framework config.

Use `hummingbird-server-workflow` for Hummingbird router, middleware, request context, and framework testing behavior.

Use `persistence-workflow` for user, token, role, permission, session, or audit-log schema and query design.

Use `openapi-rpc-workflow` when API contracts need auth schemes, security requirements, generated client behavior, or RPC metadata.

Use Apple-platform guidance for Keychain, Sign in with Apple client UI, local credential storage, or app-side token handling.

## Output Shape

Return:

1. `Auth shape`: framework, credential types, identity model, middleware, route groups, policies, tokens, sessions, password storage, and secrets.
2. `Docs used`: Vapor, Hummingbird, JWT, password, session, OAuth/OIDC, persistence, observability, or deployment docs consulted.
3. `Behavior`: authentication flow, authorization checks, token/session lifecycle, errors, status codes, and redaction.
4. `Command path`: exact build, test, migrate, run, secret, or HTTP commands run or recommended.
5. `Validation`: tests, migration checks, manual HTTP checks, or deployment-secret verification.
6. `Handoffs`: framework, persistence, OpenAPI/RPC, observability, Apple-platform, Docker, Fly.io, or security review follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not store plaintext passwords.
- Do not log credentials, raw tokens, authorization headers, cookies, private keys, OAuth codes, refresh tokens, or full JWTs.
- Do not treat authentication as authorization.
- Do not use in-memory session or token state for multi-instance production unless the repo explicitly accepts that limitation.
- Do not add external identity-provider behavior from memory; verify current provider and framework docs.
- Do not duplicate Apple-platform Keychain or client-side credential-storage guidance in this server-side workflow.
