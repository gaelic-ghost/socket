---
name: testing-workflow
description: Run, filter, debug, and explain server-side JVM tests across Gradle, Maven, SBT, Java, Scala, JUnit, ScalaTest, MUnit, unit, integration, contract, and service-level test surfaces.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Java and Scala JVM backend test workflows.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: jvm-testing
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(gradle:*) Bash(./gradlew:*) Bash(mvn:*) Bash(sbt:*)
---

# JVM Testing Workflow

## Purpose

Run and explain JVM backend tests without assuming one language or build tool owns the platform.

The practical decision is which module to test, which build tool command is authoritative, which test framework is already in use, and whether a failure is toolchain, dependency, compile, discovery, execution, or output related.

## When To Use

- Use this skill when the user asks to run, add, debug, or explain JVM backend tests.
- Use this skill after changing Java or Scala service behavior.
- Use this skill when Gradle, Maven, or SBT test commands fail.
- Use this skill when deciding whether to run module-level or repository-level tests.

## Source Check

Use repo-local JVM files, checked-out dependency sources, Dash MCP or Dash HTTP for installed JVM docsets, and then official or canonical documentation when Dash/local coverage is missing or stale:

- [Gradle Java testing documentation](https://docs.gradle.org/current/userguide/java_testing.html)
- [Maven Surefire Plugin documentation](https://maven.apache.org/surefire/maven-surefire-plugin/)
- [SBT testing documentation](https://www.scala-sbt.org/1.x/docs/Testing.html)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [ScalaTest User Guide](https://www.scalatest.org/user_guide)
- [MUnit documentation](https://scalameta.org/munit/)

Inspect the repository before running broad checks:

```bash
rg --files -g 'settings.gradle' -g 'settings.gradle.kts' -g 'build.gradle' -g 'build.gradle.kts' -g 'pom.xml' -g 'build.sbt' -g '*.java' -g '*.scala'
```

## Test Selection

Choose the narrowest useful test command first:

- changed Gradle module: `./gradlew :module:test`
- changed Maven module: `mvn -pl module -am test`
- changed SBT module: `sbt module/test`
- changed shared library used broadly: run the affected module tests, then the broader project tests before commit
- dependency or toolchain issue: run the compile or dependency phase before behavior tests
- no test surface exists: run compile/build and report the missing test gap

Use the repository's documented commands when they differ.

## Test Framework Choice

Preserve the repository's current test framework.

For new Java test surfaces, prefer the repo's existing JUnit, AssertJ, Mockito, Spring test, Quarkus test, Micronaut test, or other framework-specific pattern.

For new Scala test surfaces, prefer the repo's existing ScalaTest, MUnit, Weaver, specs2, ZIO Test, or Cats Effect testing pattern.

Do not migrate test frameworks as part of ordinary behavior work.

## Failure Triage

Classify failures by phase:

- toolchain selection
- dependency resolution
- compile
- generated source or annotation processing
- test discovery
- test execution
- logger, report, or output generation

Report:

- exact command
- module or project
- phase
- first meaningful error
- likely cause
- smallest useful next check

## Java Test Notes

For Java tests:

- preserve JUnit version and assertion style
- avoid broad mocks when a small value-based test proves the behavior
- test domain logic without full framework startup when practical
- add service or integration tests when serialization, persistence, auth, or framework wiring changed

## Scala Test Notes

For Scala tests:

- preserve ScalaTest, MUnit, Weaver, or repo-selected style
- test pure transformations directly where practical
- keep effectful tests aligned with the repository's effect runtime
- avoid Java-shaped fixtures when small Scala values or generators would be clearer

## Output Shape

Return:

1. `Command`: exact test command.
2. `Scope`: module, project, repository, or targeted filter.
3. `Result`: pass, fail, skipped, or blocked.
4. `Failure phase`: toolchain, dependency, compile, discovery, execution, or output.
5. `Next step`: smallest useful fix or broader validation.

## Guardrails

- Do not run multiple build or test commands concurrently.
- Do not replace an existing test framework unless the user explicitly asks for that migration.
- Do not hide compile or dependency failures under a generic "tests failed" summary.
- Do not skip tests after behavior changes when a relevant test surface exists.
- Do not route Android instrumentation or emulator work through this skill.
