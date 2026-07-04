---
name: choose-service-shape
description: Choose the right server-side JVM project shape before implementation, including Java versus Scala language choice, Gradle/Maven/SBT ownership, framework fit, validation commands, package boundaries, Android handoffs, and documentation updates.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients working with JVM backend projects, Java, Scala, Gradle, Maven, SBT, and server-side frameworks on macOS or other supported JVM development environments.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: jvm-planning
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(java:*) Bash(javac:*) Bash(gradle:*) Bash(./gradlew:*) Bash(mvn:*) Bash(sbt:*)
---

# Choose Server-Side JVM Shape

## Purpose

Pick the smallest correct JVM backend shape before code changes begin.

The practical decision is whether the work belongs in Java, Scala, future Clojure, a shared JVM library, a service framework, a build-tool maintenance pass, or a handoff to Android guidance.

## When To Use

- Use this skill when the user wants JVM backend work but has not chosen Java, Scala, framework, or build shape.
- Use this skill before scaffolding or restructuring a JVM service.
- Use this skill when a repository contains both Android and backend JVM code and ownership is ambiguous.
- Use this skill when the user asks for a functional JVM default and the repository has no stronger language convention.

## Source Check

Use repo-local JVM files, checked-out dependency sources, Dash MCP or Dash HTTP for installed JVM docsets, and then official or canonical documentation when Dash/local coverage is missing or stale. Check one of those source-specific paths before making claims about JVM, language, build, or framework behavior:

- [Java documentation](https://docs.oracle.com/en/java/)
- [OpenJDK documentation](https://openjdk.org/)
- [Scala documentation](https://docs.scala-lang.org/)
- [Gradle User Manual](https://docs.gradle.org/current/userguide/userguide.html)
- [Maven documentation](https://maven.apache.org/guides/)
- [SBT Reference Manual](https://www.scala-sbt.org/1.x/docs/)

Translate any documentation rule into the concrete repository decision it changes.

## Classification Workflow

1. Inspect the repository shape:
   - `settings.gradle`, `settings.gradle.kts`, `build.gradle`, `build.gradle.kts`
   - `pom.xml`
   - `build.sbt`, `project/`
   - `gradle.properties`
   - `.java-version`, `.sdkmanrc`, `.tool-versions`
   - `src/main/java`, `src/main/scala`, `src/test/java`, `src/test/scala`
   - `Dockerfile`, `compose.yaml`, `docker-compose.yml`
   - existing CI commands
   - Android markers such as `AndroidManifest.xml`, `com.android.application`, or `com.android.library`
2. Identify the user-visible job:
   - Java service
   - Scala service
   - future Clojure service
   - shared JVM library
   - Gradle, Maven, or SBT multi-module project
   - framework-specific service
   - testing, packaging, CI, upgrade, or diagnostics pass
3. Route Android work away from this plugin when the task is app/platform-specific:
   - Android app modules
   - Android Gradle Plugin configuration
   - manifests, resources, signing, emulator, device, or Play release work
   - Java/Kotlin interop inside Android modules
4. Choose language intentionally:
   - Ask for language preference when the user has not chosen and repo context is mixed or empty.
   - Prefer Scala when the user asks for a functional JVM default and no existing Java framework or team convention dominates.
   - Prefer Java when the repository is Java-dominant and the requested change belongs inside that existing surface.
   - Use mixed Java and Scala only when the boundary is useful and explicit.
   - Keep Clojure as a future candidate unless the repository already uses Clojure or the user explicitly asks for it.
5. Choose validation:
   - Gradle wrapper projects: `./gradlew test` or narrower tasks from the changed module.
   - Maven projects: `mvn test` or narrower module commands.
   - SBT projects: `sbt test` or scoped project/test commands.
   - Dependency or toolchain issue: run the restore/compile phase before behavior tests.

## Recommendations

### Java Service

Use Java guidance when the repository is Java-first, the framework defaults to Java, or the change belongs inside an existing Java service.

Handoff:

- `server-side-jvm:build-java-service` for implementation
- `server-side-jvm:build-tooling-workflow` for Gradle, Maven, or SBT wiring
- `server-side-jvm:testing-workflow` for tests

### Scala Service

Use Scala guidance when the repository is Scala-first, the user wants functional JVM design, or the service benefits from immutable data and explicit effect or async boundaries.

Handoff:

- `server-side-jvm:build-scala-service` for implementation
- `server-side-jvm:build-tooling-workflow` for Gradle, Maven, or SBT wiring
- `server-side-jvm:testing-workflow` for tests

### Shared JVM Library

Use a shared library when Android, backend, CLI, or multiple services need the same non-platform-specific behavior. Keep Android APIs out of a shared non-Android JVM library unless the module is explicitly Android-owned.

### Framework-Specific Service

Preserve the existing framework. If starting fresh, decide the framework from constraints first:

- Spring Boot, Micronaut, or Quarkus for broad Java ecosystem support.
- http4s, ZIO HTTP, Akka/Pekko, or Play when the repository is Scala-first and the team accepts those ecosystem choices.
- Framework-neutral modules for domain logic that should not depend on routing or persistence adapters.

## Output Shape

Return:

1. `Chosen shape`: Java service, Scala service, future Clojure service, shared JVM library, framework-specific service, or maintenance pass.
2. `Language decision`: Java, Scala, mixed, future Clojure, or user decision needed.
3. `Build owner`: Gradle, Maven, SBT, wrapper command, and relevant modules.
4. `Framework fit`: existing framework, recommended framework, or framework-neutral.
5. `Validation path`: exact build and test commands.
6. `Next skill`: the next server-side JVM or Android skill to use.

## Guardrails

- Do not silently choose Java when the user asks for functional JVM work and the repo has no stronger default.
- Do not describe Scala as secondary or niche.
- Do not make Android app/platform work server-side JVM-owned just because it uses Java or Gradle.
- Do not add a new framework, module, or mixed-language boundary without naming the concrete problem it solves.
- Do not publish or deploy by default.
