---
name: swiftdata-workflow
description: Design, implement, migrate, test, and integrate SwiftData persistence in Apple apps using current Apple documentation. Use for @Model schemas, ModelContainer and ModelContext ownership, @Query integration, relationships, uniqueness, deletion, concurrency, migrations, preview or test stores, and boundaries between persistent models, runtime domain values, records, and DTOs.
---

# SwiftData Workflow

## Purpose

Own SwiftData persistence decisions without spreading SwiftData policy across unrelated Apple skills. Start from current Apple documentation, keep persistence types distinct from runtime/domain values, and hand view composition or general source-tree work to their focused owners.

## When To Use

Use for SwiftData schemas, containers, contexts, queries, relationships, migrations, previews, tests, concurrency, and SwiftUI persistence integration.

## Single-Path Workflow

1. Read the relevant Apple SwiftData documentation through `explore-apple-swift-docs` before proposing implementation.
2. Classify the task as schema design, container/context ownership, query and mutation, relationship behavior, migration, testing/previews, or external-boundary conversion.
3. Read the matching reference:
   - `references/models-containers-and-contexts.md`
   - `references/swiftui-integration.md`
   - `references/migrations-testing-and-boundaries.md`
4. Use the project's explicit three-letter prefix. Name runtime/domain values `GEAWhatever.swift`, SwiftData `@Model` persistence types `GEAWhateverModel.swift`, and additional `Record` or `DTO` representations only when a real boundary requires them.
5. Keep SwiftData directly integrated with SwiftUI through `modelContainer`, environment `modelContext`, `@Query`, model objects, and narrow bindings. Do not insert repositories, stores, service mirrors, DTO mirrors, or view-model caches between SwiftData and SwiftUI.
6. Add a separate direct concrete service only for a non-SwiftUI concern such as networking, import/export, migration tooling, server sync, or isolated tests. That service owns its real boundary directly; it does not become a repository, persistence mirror, or wrapper between SwiftData and SwiftUI.
7. Hand view ownership and view-model composition to `swiftui-app-architecture-workflow`, filename and directory cleanup to `structure-swift-sources`, execution to `xcode-build-run-workflow`, and tests to `xcode-testing-workflow`.

## Inputs

- repository and platform context
- persistence task and existing schema state
- selected three-letter project prefix
- migration and compatibility constraints

## Outputs

Return the documented behavior, schema and ownership decision, naming decision, migration or compatibility impact, validation path, and any required handoff.

## Guards and Stop Conditions

- Reserve `Model` for persistence representations.
- Do not use `State` as a filename or type suffix for ordinary runtime/domain values.
- Do not use `+` filenames.
- Do not hide `ModelContext` concurrency or lifecycle assumptions.
- Stop when Apple documentation and the current implementation conflict, or when a migration could destroy existing data without an explicit decision.

## Fallbacks and Handoffs

- Hand Apple documentation lookup to `explore-apple-swift-docs`.
- Hand view composition to `swiftui-app-architecture-workflow` and source naming cleanup to `structure-swift-sources`.
- Hand build or test execution to the focused Xcode workflows.

## Customization

Use `references/customization-flow.md`. The first version has no runtime-enforced knobs; `scripts/customization_config.py` preserves the shared configuration contract.

## References

- `references/models-containers-and-contexts.md`
- `references/swiftui-integration.md`
- `references/migrations-testing-and-boundaries.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable repository policy rather than a one-off SwiftData decision.
