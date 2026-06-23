---
name: build-java-service
description: Implement and maintain idiomatic Java backend services, including package structure, records, sealed types, nullability, optionals, exceptions, concurrency, dependency boundaries, API and persistence seams, tests, and human-friendly diagnostics.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Java server-side JVM projects and backend frameworks.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: jvm-java
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(javac:*) Bash(gradle:*) Bash(./gradlew:*) Bash(mvn:*) Bash(sbt:*)
---

# Build Java Service

## Purpose

Implement Java backend behavior without treating Java as the only JVM path.

The practical decision is how to fit the change into an existing Java service, keep domain behavior clear, choose framework boundaries deliberately, and prove the result with focused build and test commands.

## When To Use

- Use this skill when the repository is Java-first and the task changes backend behavior.
- Use this skill when `choose-service-shape` routes implementation to Java.
- Use this skill for Java service code, Java shared JVM libraries, Java API handlers, Java persistence adapters, and Java tests.
- Use Android guidance instead when the task is Android app/platform Java.

## Source Check

Use official or canonical documentation first:

- [Java documentation](https://docs.oracle.com/en/java/)
- [OpenJDK documentation](https://openjdk.org/)
- [Java Language Specification](https://docs.oracle.com/javase/specs/)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)

Use framework documentation for framework-specific behavior. Translate documentation rules into concrete code, test, or validation decisions.

## Implementation Workflow

1. Inspect the existing Java shape:
   - package names
   - framework entry points
   - controller, route, handler, service, repository, and domain boundaries
   - records, classes, interfaces, enums, sealed types, and exceptions
   - nullability annotations or conventions
   - test framework and fixture style
2. Keep domain behavior separate from transport:
   - put routing, request parsing, and response formatting at the edge
   - keep pure transformations and validation in small Java types or methods
   - keep persistence adapters behind explicit interfaces only when there are real alternate callers or tests
3. Model data intentionally:
   - use records for immutable data carriers when the project supports them
   - use sealed types when a closed hierarchy improves exhaustiveness or clarity
   - use enums for small stable sets
   - use `Optional` for return values where absence is expected, not for every field or parameter
4. Handle errors clearly:
   - distinguish validation, not-found, conflict, dependency, and unexpected failures
   - keep operator-facing messages descriptive and concrete
   - include useful context without leaking secrets or personal data
5. Add focused tests:
   - unit-test domain behavior without starting the full service when practical
   - add handler or integration tests when routing, serialization, auth, persistence, or framework behavior is the change
   - preserve existing JUnit, AssertJ, Mockito, Testcontainers, or framework-specific patterns

## Concurrency And Async

Preserve the repository's concurrency model.

- Use blocking code only where the framework and runtime expect it.
- Use `CompletableFuture`, virtual threads, reactive types, or framework async APIs only when the existing project already uses them or the task requires that model.
- Do not introduce a second async abstraction for one small change.
- Keep timeouts, cancellation, and resource cleanup explicit around external calls.

## Validation

Use `server-side-jvm:build-tooling-workflow` to choose exact commands.

Common validation shapes:

- Gradle Java module: `./gradlew :module:test`
- Maven Java module: `mvn -pl module -am test`
- SBT mixed JVM module: `sbt module/test`

Run broader validation before commit, push, PR, release, or cross-module behavior changes.

## Output Shape

Return:

1. `Changed behavior`: the Java service behavior or API changed.
2. `Code boundary`: handler, service, domain, persistence, config, or test.
3. `Data model`: records, classes, sealed types, enums, optionals, or existing convention.
4. `Error behavior`: validation, not-found, conflict, dependency, or unexpected errors.
5. `Validation`: exact build and test commands and results.

## Guardrails

- Do not convert Scala or Clojure code to Java unless the user asks.
- Do not add dependency injection, interfaces, factories, or managers unless they remove real duplication or clarify a real boundary.
- Do not hide build, test, or runtime failures behind vague error summaries.
- Do not add local jars or machine-local dependency paths.
- Do not let Android app/platform concerns leak into backend Java modules.
