# Server-Side JVM Skills Plugin Plan

This plan records the first durable shape for a Socket-hosted server-side JVM skills plugin.

The plugin's job is to help agents build, test, package, and maintain JVM backend projects while treating Java and Scala as equal first-party language choices and leaving room for future Clojure guidance. Scala and future Clojure guidance should make functional programming visible and natural without turning Java guidance into a forced translation exercise.

## Intent

The `server-side-jvm` plugin should help agents do five things:

- choose a JVM backend project shape before scaffolding or implementation starts
- route build and dependency work through the repository's actual Gradle, Maven, or SBT setup
- write Java and Scala service code idiomatically, with functional design treated as first-class where the language and framework fit
- run and explain JVM build, test, package, runtime, diagnostics, and CI workflows
- keep JVM backend guidance separate from Android app guidance while still recognizing shared Gradle and library concerns

This is a companion guidance plugin, not a runtime plugin. The first version should not bundle an MCP server, custom build tool, private template feed, local JDK manager, framework starter, or machine-local SDK state.

## Naming Decision

Use `server-side-jvm` instead of `java-backend-skills`.

This keeps Java, Scala, and future Clojure on equal footing, matches the existing `server-side-swift` plugin shape, and describes the runtime/backend boundary instead of centering one language. The display name should be `Server-Side JVM`.

## Packaging Direction

Package the guidance as an independent child plugin under:

```text
plugins/server-side-jvm/
```

The child plugin should own its Codex-facing guidance surface:

- `.codex-plugin/plugin.json`
- `skills/` once real skills land
- plugin metadata, skill metadata, `AGENTS.md`, or maintainer notes that explain the plugin's role
- any validation scripts needed for the plugin's own authored guidance

The root Socket marketplace should list `server-side-jvm` as `NOT_AVAILABLE` while it remains a placeholder. Switch the marketplace entry to `AVAILABLE` only after the first real skill content lands and root validation passes.

## Boundary With Android Dev Skills

`android-dev-skills` owns Android app and platform work:

- Android project-shape discovery
- Android Gradle Plugin and build variants
- Kotlin-first Android implementation
- Java interoperability inside Android projects
- Java-only Android maintenance when repo defaults require it
- manifests, resources, permissions, signing, lint, tests, emulator-aware validation, and release readiness

`server-side-jvm` owns non-Android JVM backend work:

- Java, Scala, and future Clojure services
- shared non-Android JVM libraries
- Gradle, Maven, and SBT backend builds
- service runtime configuration
- persistence, API, observability, packaging, CI, and deployment-adjacent backend workflows

When a repository contains both an Android app and a JVM backend, route each change to the owning plugin. Do not make Android duplicate backend service guidance just because both surfaces use Gradle or Java.

## Language Posture

Java and Scala are first-party paths.

That means:

- do not describe Scala as secondary, niche, or merely compatible with Java
- do not silently choose Java when the user has not named a language
- ask for language preference before scaffolding when the user's request is ambiguous
- prefer Scala or future Clojure examples when a user explicitly wants functional style and the project has no stronger existing default
- preserve Java's idioms for Java repositories instead of translating Scala patterns into Java syntax
- preserve Scala's idioms for Scala repositories, including immutable data, algebraic data types where available, effect or async model choices, and explicit module boundaries
- keep future Clojure room open for data-oriented design, REPL workflows, immutable data, and functional service composition

## Documentation Sources

Use official or canonical documentation first when authoring skills:

- Java documentation from Oracle and OpenJDK
- Scala language, SBT, and Scala ecosystem documentation
- Clojure documentation when Clojure skills are added
- Gradle, Maven, and SBT documentation
- framework documentation for Spring Boot, http4s, ZIO HTTP, Akka/Pekko, Micronaut, Quarkus, or other selected server frameworks
- JUnit, ScalaTest, MUnit, Weaver, or repository-selected test framework documentation

When a skill relies on documentation, translate the relevant rule into practical workflow guidance. Do not drop citations into a skill as a substitute for explaining the effect on scaffolding, validation, project layout, runtime behavior, or user-facing diagnostics.

## Proposed Skill Inventory

### `server-side-jvm:choose-service-shape`

Help an agent decide how JVM backend work should fit into a user's project before implementation starts.

This skill should classify the requested work:

- Java service
- Scala service
- future Clojure service
- shared JVM library
- Gradle, Maven, or SBT multi-module project
- Spring Boot, Micronaut, Quarkus, http4s, ZIO HTTP, Akka/Pekko, or framework-neutral service
- package maintenance or upgrade pass
- CI, deployment, or diagnostics task

The output should recommend language choice, build tool owner, framework fit, validation commands, module boundaries, and documentation updates.

### `server-side-jvm:build-tooling-workflow`

Guide agents through Gradle, Maven, and SBT project maintenance.

This skill should cover:

- detecting the actual build tool and wrapper policy
- Java toolchains, Maven compiler configuration, Gradle toolchains, and SBT JVM settings
- dependency declaration and lock or version-catalog policy
- multi-module project boundaries
- test, package, and local run commands
- avoiding machine-local dependency paths and private unpublished artifacts

### `server-side-jvm:build-java-service`

Guide agents through idiomatic Java backend implementation.

This skill should cover:

- package and module organization
- records, sealed types, optionals, nullability conventions, and exceptions
- async and concurrency model choices
- dependency injection only where it clarifies real boundaries
- API, persistence, and service-layer tests
- human-friendly logs and diagnostics

This is a Java-specific skill, not the default JVM skill.

### `server-side-jvm:build-scala-service`

Guide agents through idiomatic Scala backend implementation.

This skill should cover:

- immutable data modeling
- algebraic data types, options, eithers, and validated values
- effect systems or future-based async models according to repo defaults
- http4s, ZIO HTTP, Akka/Pekko, Play, or framework-specific routing where relevant
- typeclass, module, and dependency boundaries without over-abstracting
- ScalaTest, MUnit, Weaver, or repo-selected testing style

This is a Scala-specific skill, not a Java compatibility layer.

### `server-side-jvm:testing-workflow`

Run, debug, filter, and explain JVM backend tests.

This skill should cover:

- Gradle, Maven, and SBT test commands
- JUnit, ScalaTest, MUnit, and repository-selected frameworks
- unit, integration, contract, and service-level tests
- testcontainers or local service dependency handoffs when the repo already uses them
- targeted reruns, flaky tests, and readable failure summaries

### `server-side-jvm:package-and-runtime-workflow`

Prepare JVM services and libraries for local run, packaging, and deployment handoffs.

This skill should cover:

- jar, fat jar, native image, container, and framework-specific package choices
- local run commands and environment configuration
- health checks and readiness probes
- secrets and config boundaries
- versioning and release notes
- handoff to repo-owned release automation when publish or deploy work is requested

### `server-side-jvm:persistence-workflow`

Guide backend persistence work without making one framework the universal default.

This skill should cover:

- JDBC, JPA/Hibernate, jOOQ, Doobie, Quill, Slick, or repo-selected persistence layers
- migrations and schema ownership
- transaction boundaries
- query tests and local database dependencies
- separating domain behavior from persistence adapters

### `server-side-jvm:observability-workflow`

Guide logging, metrics, tracing, and diagnostics for JVM services.

This skill should cover:

- SLF4J or repo-selected logging facades
- structured logging and correlation IDs
- Micrometer, OpenTelemetry, or repo-selected metrics and tracing
- privacy-safe diagnostics
- failure messages that explain what broke, where, and likely causes

### Future Skill Candidates

- `server-side-jvm:build-clojure-service`
- `server-side-jvm:spring-boot-service-workflow`
- `server-side-jvm:http4s-workflow`
- `server-side-jvm:zio-workflow`
- `server-side-jvm:akka-pekko-workflow`
- `server-side-jvm:ci-workflow`
- `server-side-jvm:upgrade-workflow`

## Completion Checklist

- [x] Create `plugins/server-side-jvm/` with `.codex-plugin/plugin.json` and `AGENTS.md`.
- [x] Wire `server-side-jvm` into the root Socket marketplace as `NOT_AVAILABLE` while it is a placeholder.
- [x] Record this first detailed skill plan.
- [x] Update root README, TODO, and ROADMAP so users understand the planned child plugin surface.
- [x] Run root metadata validation for the placeholder marketplace and manifest wiring.
- [ ] Add the first real skills for service-shape choice, build tooling, Java service work, Scala service work, and testing.
- [ ] Update plugin metadata after real skills land, including `skills`, keywords, prompts, and accurate installable descriptions.
- [ ] Switch the root marketplace entry to installable only after real skill content exists.
- [ ] Run root metadata validation again after real skill content lands.

## Exit Criteria

- [ ] The Socket marketplace exposes `server-side-jvm` as an installable child plugin after real skill content lands.
- [ ] The new skills can help an agent choose a JVM backend shape before implementation.
- [ ] Java and Scala guidance are first-class, with future Clojure support planned without renaming the plugin.
- [ ] Android app guidance stays owned by `android-dev-skills`; backend and shared non-Android JVM library guidance stays owned by `server-side-jvm`.
- [ ] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.
