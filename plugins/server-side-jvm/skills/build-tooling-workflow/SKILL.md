---
name: build-tooling-workflow
description: Inspect and maintain server-side JVM build tooling across Gradle, Maven, and SBT, including wrapper policy, Java toolchains, dependencies, multi-module boundaries, local run commands, tests, package tasks, and machine-local dependency guardrails.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with server-side JVM repositories that use Gradle, Maven, or SBT.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: jvm-build
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(javac:*) Bash(gradle:*) Bash(./gradlew:*) Bash(mvn:*) Bash(sbt:*)
---

# JVM Build Tooling Workflow

## Purpose

Keep JVM build and dependency work grounded in the repository's real build tool.

The practical decision is which tool owns the project, which wrapper or pinned toolchain should be used, which module is affected, and which command proves the change without relying on machine-global state.

## When To Use

- Use this skill when a JVM backend task touches Gradle, Maven, SBT, Java versions, dependencies, modules, package tasks, or local run commands.
- Use this skill before adding dependencies or changing build files.
- Use this skill when build failures need phase-aware triage.
- Use this skill when the repository shape is unclear and `choose-service-shape` identified build tooling as the next owner.

## Source Check

Use official build tool documentation first:

- [Gradle User Manual](https://docs.gradle.org/current/userguide/userguide.html)
- [Gradle Toolchains for JVM projects](https://docs.gradle.org/current/userguide/toolchains.html)
- [Maven documentation](https://maven.apache.org/guides/)
- [Maven Compiler Plugin documentation](https://maven.apache.org/plugins/maven-compiler-plugin/)
- [SBT Reference Manual](https://www.scala-sbt.org/1.x/docs/)
- [SBT multi-project builds](https://www.scala-sbt.org/1.x/docs/Multi-Project.html)

Translate documentation rules into concrete build-file, command, or module decisions.

## Inspection Workflow

1. Identify the build owner:
   - Gradle: `settings.gradle`, `settings.gradle.kts`, `build.gradle`, `build.gradle.kts`, `gradlew`
   - Maven: `pom.xml`, `.mvn/`
   - SBT: `build.sbt`, `project/*.scala`, `project/*.sbt`
2. Prefer repository wrappers:
   - use `./gradlew` when present
   - use `./mvnw` when present
   - use `sbt` only after checking for repo-local launcher conventions
3. Inspect Java/toolchain policy:
   - Gradle Java toolchains
   - Maven compiler release/source/target
   - SBT `javacOptions`, `scalacOptions`, `ThisBuild / scalaVersion`, and JVM settings
   - `.java-version`, `.sdkmanrc`, `.tool-versions`, or CI setup
4. Inspect dependencies:
   - Gradle version catalogs, platforms, constraints, and repositories
   - Maven dependency management, parent POMs, profiles, and repositories
   - SBT library dependencies, plugins, resolvers, and cross-versioning
5. Inspect module boundaries:
   - Gradle subprojects
   - Maven modules
   - SBT projects
   - Java/Scala source sets
   - shared JVM libraries versus Android modules

## Command Selection

Choose the narrowest useful command first:

- Gradle compile: `./gradlew :module:classes`
- Gradle test: `./gradlew :module:test`
- Gradle full verification: `./gradlew test`
- Maven compile: `mvn -pl module -am test-compile`
- Maven test: `mvn -pl module -am test`
- Maven full verification: `mvn test`
- SBT compile: `sbt module/compile`
- SBT test: `sbt module/test`
- SBT full verification: `sbt test`

Use the repository's documented commands when they differ.

## Dependency Rules

- Use fetchable package repositories or source repositories only.
- Do not commit machine-local paths, local Maven repositories, local Ivy caches, unpublished local jars, or absolute paths.
- Preserve existing version catalog, dependency management, or plugin-management patterns.
- Add a new dependency only when it removes real complexity or matches an existing repo pattern.
- Keep dependency updates separate from feature work when the update has broad risk.

## Failure Triage

Classify failures by phase:

- toolchain selection
- dependency resolution
- compile
- annotation processing or code generation
- test discovery
- test execution
- package or artifact creation

Report the command, module, phase, first meaningful error, likely cause, and smallest next check.

## Output Shape

Return:

1. `Build owner`: Gradle, Maven, SBT, and wrapper command.
2. `Affected modules`: module or project names.
3. `Toolchain policy`: Java, Scala, and plugin version constraints.
4. `Dependency decision`: add, update, preserve, or remove.
5. `Validation path`: exact commands.
6. `Risk`: build, dependency, generated-source, or cross-module risks.

## Guardrails

- Do not mix Gradle, Maven, and SBT commands speculatively.
- Do not run multiple build or test commands concurrently.
- Do not add machine-local dependency paths.
- Do not change Java, Scala, Gradle, Maven, or SBT versions without explaining the compatibility impact.
- Do not make backend build decisions inside Android-owned modules unless the task is explicitly about a shared non-Android JVM library.
