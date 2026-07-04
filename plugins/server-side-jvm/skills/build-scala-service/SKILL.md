---
name: build-scala-service
description: Implement and maintain idiomatic Scala backend services, including immutable data modeling, algebraic data types, options/eithers, effect or future-based async boundaries, framework routing, module design, tests, and functional service structure.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Scala server-side JVM projects, SBT, Gradle, Maven, and Scala backend frameworks.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: jvm-scala
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(scala:*) Bash(scalac:*) Bash(sbt:*) Bash(gradle:*) Bash(./gradlew:*) Bash(mvn:*)
---

# Build Scala Service

## Purpose

Implement Scala backend behavior with Scala as a first-class JVM path.

The practical decision is how to use immutable data, explicit effects or futures, clear module boundaries, and focused tests without translating Java service patterns into Scala syntax.

## When To Use

- Use this skill when the repository is Scala-first and the task changes backend behavior.
- Use this skill when the user asks for functional JVM backend work and repo context does not point elsewhere.
- Use this skill when `choose-service-shape` routes implementation to Scala.
- Use Java guidance instead for Java-dominant backend modules, and Android guidance for Android app/platform work.

## Source Check

Use repo-local JVM files, checked-out dependency sources, Dash MCP or Dash HTTP for installed JVM docsets, and then official or canonical documentation when Dash/local coverage is missing or stale:

- [Scala documentation](https://docs.scala-lang.org/)
- [Scala 3 Book](https://docs.scala-lang.org/scala3/book/introduction.html)
- [SBT Reference Manual](https://www.scala-sbt.org/1.x/docs/)
- [ScalaTest User Guide](https://www.scalatest.org/user_guide)
- [MUnit documentation](https://scalameta.org/munit/)

Use framework documentation for framework-specific behavior. Translate documentation rules into concrete code, test, or validation decisions.

## Implementation Workflow

1. Inspect the existing Scala shape:
   - Scala version
   - SBT, Gradle, or Maven project layout
   - package and module names
   - framework entry points
   - effect model, future model, or synchronous style
   - test framework
   - formatting and lint expectations
2. Model data functionally:
   - prefer immutable case classes for product data
   - use sealed traits or enums for closed alternatives
   - use `Option` for expected absence
   - use `Either`, validated values, or the repo's effect error channel for recoverable domain errors
   - avoid `null` unless interoperating with Java or a framework API that requires it
3. Keep behavior composable:
   - write small pure functions for domain transformations where practical
   - keep routing, request decoding, and response encoding at the edge
   - pass dependencies explicitly through the repository's existing pattern
   - avoid abstracting with typeclasses unless the abstraction has more than one real use or matches local style
4. Preserve the async/effect model:
   - use `Future` if the project is Future-based
   - use the repository's established effect system when one exists
   - do not introduce Cats Effect, ZIO, Akka/Pekko, or another runtime for one feature
   - keep resource acquisition, cancellation, retries, and timeouts explicit around external dependencies
5. Add focused tests:
   - test pure domain behavior directly
   - add route or integration tests when serialization, auth, persistence, or framework behavior changed
   - preserve ScalaTest, MUnit, Weaver, or repository-selected style

## Framework Boundaries

Preserve the existing framework unless the user asks for a framework decision.

- Keep http4s, ZIO HTTP, Akka/Pekko, Play, Spring, or framework-specific code at the service edge.
- Keep domain and validation code framework-light when it will be reused or tested independently.
- Do not make one framework's module structure the default for another framework.

## Validation

Use `server-side-jvm:build-tooling-workflow` to choose exact commands.

Common validation shapes:

- SBT module: `sbt module/test`
- SBT full check: `sbt test`
- Gradle Scala module: `./gradlew :module:test`
- Maven Scala module: `mvn -pl module -am test`

Run broader validation before commit, push, PR, release, or cross-module behavior changes.

## Output Shape

Return:

1. `Changed behavior`: the Scala service behavior or API changed.
2. `Functional boundary`: pure domain, effectful service, route edge, persistence adapter, config, or test.
3. `Data model`: case classes, sealed traits/enums, options, eithers, validated values, or existing convention.
4. `Effect model`: synchronous, `Future`, Cats Effect, ZIO, Akka/Pekko, or existing runtime.
5. `Validation`: exact build and test commands and results.

## Guardrails

- Do not treat Scala as Java with different syntax.
- Do not introduce an effect system, framework, or typeclass abstraction without a real project reason.
- Do not use `null` or exceptions for ordinary domain flow unless local conventions require it.
- Do not convert Java modules to Scala unless the user asks.
- Do not make Android app/platform concerns part of this skill.
