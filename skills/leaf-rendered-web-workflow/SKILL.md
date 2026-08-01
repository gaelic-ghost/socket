---
name: leaf-rendered-web-workflow
description: Plan, implement, test, and diagnose Leaf-rendered Vapor sites and HTML email with typed contexts, layouts, partials, custom tags, escaping, accessibility, assets, caching, and rendering tests.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Vapor, Leaf, LeafKit, SwiftPM, server-rendered HTML, and HTML email on macOS or Linux.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-leaf
  hermes:
    category: server-side-swift
    tags: [leaf, vapor, templates, accessibility, server-rendered-html]
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Leaf-Rendered Web Workflow

## Purpose

Plan, implement, test, or diagnose a Leaf-rendered website or rich HTML email surface without turning templates into a second application layer or confusing server rendering with a client framework, design-system package, or generic Vapor route work.

The practical decision is how a request becomes a trustworthy, accessible HTML document: which Swift code owns data loading and decisions, what typed context a page receives, how layouts and components compose, where unescaped HTML is allowed, how public assets reach the runtime, and which tests prove the rendered result.

## When To Use

- Use this skill when adding or changing Leaf views, `Resources/Views`, `req.view.render`, page contexts, layouts, partial templates, server-rendered forms, HTML email templates, custom Leaf tags, Leaf configuration, source lookup, template cache behavior, public assets, or rendered HTML tests in a Vapor service.
- Use this skill when diagnosing a missing template, unexpected rendered HTML, Leaf context encoding failure, layout or component drift, incorrectly escaped output, stale template behavior, public-asset absence, form accessibility problem, or custom-tag error.
- Use this skill when deciding whether repeated server-rendered markup should be a Leaf partial, a layout slot, a typed context property, a custom tag, or ordinary Swift code.
- Do not use this skill for JSON-only Vapor APIs, generic routing, middleware, Fluent migrations, authentication policy, deployment, or Swift language style unless Leaf-rendered behavior is the reason for the work.
- Do not use this skill to introduce a CSS framework, browser build system, client-side state framework, generic design-system package, or browser automation stack. Those choices need their own concrete project scope and decision.
- Do not use this skill for a non-Vapor templating framework unless the task is an explicit comparison or migration involving Leaf.

## Source Check

Inspect the repository's templates, rendering code, tests, `Public` assets, and checked-out dependencies first. Use Dash MCP or Dash HTTP for the installed Leaf and Vapor DocC archives before public documentation. The installed Leaf archive is primarily API reference, so use the official guides when syntax, composition, or security behavior is not described locally:

- [Leaf overview](https://docs.vapor.codes/leaf/overview/)
- [Leaf custom tags](https://docs.vapor.codes/leaf/custom-tags/)
- [Vapor files](https://docs.vapor.codes/advanced/files/)
- [Vapor testing](https://docs.vapor.codes/advanced/testing/)
- [Leaf source](https://github.com/vapor/leaf)
- [LeafKit source](https://github.com/vapor/leaf-kit)

Use `vapor-server-workflow` for Vapor route, controller, middleware, configuration, and local-server behavior. Use `auth-authorization-workflow` for sessions, cookies, login, and authorization; use `persistence-workflow` for models and queries; use `docker-workflow` for image/runtime assets; and use `swift-lang` guidance for general Swift API, formatting, and source-organization decisions.

## Planning Workflow

1. Inspect the rendering surface:
   - `Package.swift` and the Leaf package product in use
   - `configure.swift` for `app.views.use(.leaf)`, `app.leaf` configuration, tags, cache, and sources
   - routes and controllers that call `req.view.render`
   - `Resources/Views`, including layouts, pages, partials, errors, and email templates
   - `Public`, CSS, JavaScript, images, fonts, generated assets, and their runtime copy path
   - page-context types, view helpers, URL builders, formatters, and authorization checks
   - request, rendering, and browser tests already present
   - Docker or deployment rules that copy runtime resources
2. Identify the rendered job:
   - public marketing or documentation page
   - authenticated page or server-rendered form
   - transactional or campaign HTML email
   - error or maintenance page
   - repeated page component
   - small custom rendering transform
3. Preserve a documented project convention when one exists. If none exists, start with one base layout, page templates, and narrowly scoped partial components instead of inventing a generic component framework.
4. Define the page context before editing the template: its stable fields, optional states, display-ready text, URLs, action availability, and error or empty states.
5. Keep fetching, authorization, business rules, state transitions, URL construction, and complex formatting in Swift. Let Leaf render already-prepared presentation data.
6. Choose the smallest reusable boundary: page context property, partial, layout slot, or custom tag.
7. Add the smallest tests that prove successful, empty, error, unauthorized, and escaping behavior relevant to the change.

## Rendering Boundary

Treat a Leaf view as the rendering edge of the service:

```text
request -> route/controller -> domain and authorization work -> typed page context -> Leaf view -> HTML response
```

The context is an explicit presentation contract. Prefer a page-specific `Encodable` struct or a small composition of `Encodable` view types over dictionaries, `Any`, database models, request objects, or a global template bag.

Prepare presentation values in Swift:

- display strings, localized or formatted dates, and stable identifiers
- route-generated URLs and form action URLs
- boolean capability flags decided after authorization
- explicit empty, validation-error, and success states
- compact component input types when a partial has a real reusable contract

Do not make templates discover permissions, query the database, derive security-sensitive links, call a service, or encode meaningful domain policy through nested conditionals. A Leaf `#if` or `#for` is appropriate for rendering a prepared state; it is not a substitute for application behavior.

When a database model happens to match a page today, still prefer a dedicated context once the page needs display formatting, authorization-derived actions, nested relations, privacy filtering, or a stable public contract. This is a local presentation boundary, not permission to add a repository, manager, or view-model framework.

## Layouts And Components

Follow the repository's existing view structure. For a new simple site, a useful minimum is:

- a base layout that owns document structure, metadata, shared assets, and global landmarks
- page templates that fill named layout content
- partials for repeated semantic markup such as a site header, footer, alert, form field, card, or navigation item
- separate email layouts when email-client constraints differ from the web layout

Use Leaf's `#extend`, `#export`, and `#import` to compose a page with its layout. Keep layout slots small and named for their user-visible purpose, such as `title`, `head`, `main`, or `footer`; do not create a large hidden global context shared across unrelated templates.

Prefer a partial when markup is repeated and its inputs can remain clear at the call site. Give a partial only the data it needs, document any required context fields with a short `#comment` when that makes a non-obvious template readable, and keep its HTML semantic on its own. A component should not silently depend on route-local variables with unrelated names.

Choose a custom `LeafTag` only when a reusable operation is difficult to express as a typed context property or partial and has a narrow, deterministic job. Register it centrally with `app.leaf.tags`, validate parameters and context data, return descriptive errors, and test it independently. Do not use custom tags to query persistence, consult authorization state, emit whole pages, or hide an application service behind template syntax.

## HTML Safety And Security

Leaf's ordinary variable output is the safe default. Keep user-controlled values, database text, query parameters, form values, and remote content on that escaped path.

`#unsafeHTML` and `UnsafeUnescapedLeafTag` are explicit trust boundaries. Use them only for content whose origin, sanitization, and intended HTML contract are documented in the Swift code that prepares it. Never use them merely because a string "already looks like HTML." Do not pass user input, Markdown output, CMS fields, or third-party text through them without a project-specific sanitization decision and tests.

Escaping text does not make every HTML context safe. Keep untrusted values out of script blocks, inline event handlers, style expressions, raw URL schemes, and arbitrary attribute-name construction. Generate links, form actions, redirects, and asset URLs in Swift from known routes or validated values rather than concatenating browser-facing strings in templates.

For authenticated browser pages, hand session, cookie, CSRF, authorization, and security-header decisions to their owner workflows. This workflow may verify that a prepared token or form state is rendered in the intended place; it does not invent a security mechanism inside Leaf.

## Accessibility And Form States

Treat Leaf markup as production user interface, not string output. The base layout should declare document language, viewport metadata, a meaningful page title path, and the landmark structure used by the site.

For page and component work:

- choose semantic elements before generic containers
- preserve a logical heading hierarchy and one clear main content landmark
- give icon-only controls accessible names
- associate every form control with a visible label
- associate validation feedback with the affected control and present a clear error summary when the form has multiple failures
- make links and controls understandable without color, position, or hover alone
- preserve a visible keyboard focus treatment in the site's CSS
- render useful empty, loading-when-server-relevant, success, and error states rather than a blank region

Do not claim VoiceOver, keyboard, contrast, responsive-layout, or browser-runtime proof from a static template inspection. Use the repository's existing browser or accessibility test lane when it exists; otherwise label these as static markup checks and leave interactive verification explicit.

## Assets, Resources, And Caching

Treat `Resources/Views` and `Public` as runtime inputs. Verify that templates, static assets, fonts, and images required by a rendered response are included by the local run and production image or deployment path. Do not place uploads, secrets, private source artifacts, or unreviewed generated files under `Public`.

Keep asset names and cache behavior intentional. Prefer a project-owned asset pipeline or existing versioning convention when one exists; do not introduce bundlers, fingerprinting, a CDN, or a CSS framework merely because a page is being edited. If a changed asset requires long-lived browser caching, establish an invalidation path before recommending that cache policy.

`app.leaf.cache` concerns Leaf's parsed-template cache, not personalized response caching. Configure renderer behavior during app setup, follow the project's development and production convention, and do not solve stale user-specific content by disabling or manipulating the template cache. Response caching, authorization variation, and HTTP cache headers require a separate explicit policy.

## HTML Email

Leaf can render rich HTML for emails as well as web pages, but email and browser HTML are separate rendering targets. Use a dedicated email layout when CSS, tracking, preheader, plain-text alternatives, unsubscribe requirements, or mail-client support diverge from the site. Do not reuse a browser layout blindly.

Keep recipient-specific content in typed email contexts, keep all untrusted content escaped, and test representative personalized and empty-state renders. Hand actual delivery, queueing, provider integration, retries, unsubscribe behavior, and compliance requirements to the service's messaging or background-job scope.

## Testing

Choose the smallest tests that prove the rendered contract:

- pure Swift tests for page-context mapping, formatting, and component input construction
- custom-tag tests for valid, missing, and malformed parameters
- Vapor route or controller tests that assert status, content type, and key rendered HTML
- rendering tests for layout inclusion, page title, empty state, validation error, authorized action availability, and server-rendered form values
- escaping tests using hostile text such as markup-like input, asserting it remains text rather than active HTML
- asset or container checks when runtime packaging is the risk

Use snapshot testing only when the repository already has an approved snapshot tool and fixtures. Do not add a snapshot dependency or browser automation framework for one Leaf change. Keep fixtures deterministic: explicit dates, locale, timezone, identifiers, and feature state avoid brittle rendered HTML.

`swift test` is the normal baseline. Use a local HTTP request only when the template path, static files, middleware, or server binding cannot be proven through the existing test surface. Treat build, test, serve, and browser interaction as separate operations.

## Handoffs

Use `vapor-server-workflow` for route registration, controllers, middleware, Vapor configuration, app commands, and local-server behavior.

Use `auth-authorization-workflow` for session cookies, login, CSRF, authenticated actions, permission checks, and browser security boundaries.

Use `persistence-workflow` for models, migrations, data loading, query performance, and database-backed page behavior.

Use `observability-tracing-workflow` for rendering errors, safe diagnostics, request correlation, and performance measurements.

Use `docker-workflow` or the deployment workflow when templates or public assets are missing from an image, release artifact, or hosted runtime.

Use a project-specific web or design workflow only when the task explicitly expands into a frontend build system, design-token library, CSS framework, or broad cross-framework component system.

## Output Shape

Return:

1. `Rendering shape`: template root, layout, page templates, partials, contexts, custom tags, public assets, and rendering entry points.
2. `Docs used`: Dash, Leaf, Vapor files, Vapor testing, source, or project-local docs consulted.
3. `Behavior`: request-to-context flow, layout composition, component inputs, states, escaping, accessibility, cache behavior, and asset behavior.
4. `Command path`: exact build, test, serve, HTTP, asset, or container commands run or recommended.
5. `Validation`: context, tag, route, rendered-HTML, escaping, asset, static accessibility, or browser evidence and its limits.
6. `Handoffs`: Vapor, auth, persistence, observability, Docker, deployment, or explicit frontend/design follow-up when the task crosses this skill's boundary.

## Guardrails

- Do not pass database models, requests, `[String: Any]`, or a generic global bag directly into Leaf views.
- Do not let templates own database queries, authorization policy, state transitions, or complex business decisions.
- Do not use `#unsafeHTML` or `UnsafeUnescapedLeafTag` with untrusted content.
- Do not treat template caching as HTTP response caching.
- Do not add a CSS framework, frontend bundler, client-side state framework, browser automation stack, or broad design-system abstraction without a separate approved scope.
- Do not claim interactive accessibility or browser proof from static HTML inspection alone.
- Do not add a repository, service, manager, coordinator, or generic component framework merely to render a Leaf page.
