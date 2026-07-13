---
name: tips-helpviewer-workflow
description: Discover local user-guide topics for installed Apple Mac apps through the Tips HelpViewer catalog, with app matching, installed-version capture, result verification, and authoritative fallback routing. Use when Codex needs task-specific help for an installed Apple app, needs to find a menu command through local Help, or must determine whether Tips/HelpViewer has a usable guide before using in-app Help, Xcode-local docs, Dash, or official vendor documentation.
---

# Tips and HelpViewer Workflow

## Purpose

Use the macOS Tips HelpViewer catalog as a read-only discovery surface for installed Apple Mac app guides. It owns local guide lookup and result verification; it does not replace the authoritative documentation owners for an app's in-app Help, Apple developer APIs, Xcode, Dash, or vendor documentation.

## When To Use

- Use when an installed Apple Mac app needs task-specific operator help, a user-guide topic, or a menu-command hint.
- Use when a local HelpViewer/Tips catalog result must be verified before relying on it.
- Recommend `explore-apple-swift-docs` for Apple framework APIs or documentation-source routing, not for ordinary app user-guide discovery.

## Single-Path Workflow

1. Identify the requested Apple app and its installed version. Do not infer an app-guide match from a product-family name or an old search result.
2. Open `com.apple.helpviewer` and search for the app plus the user task. On this Mac, its window presents as Tips and exposes a searchable catalog; do not prefer the empty `com.apple.tips` shell.
3. Inspect the guide heading, result count, and matching topic. Confirm that the guide names the intended app and that the result answers the requested Mac task.
4. Return the installed app/version, guide title, selected topic, a concise answer or navigation path, and the source classification `local-helpviewer`.
5. If the catalog has no matching guide, is incomplete, or conflicts with the active app, move forward through one owner-aware fallback: the app's in-app Help, Xcode-local documentation for Apple developer APIs, Dash when its installed docset applies, then readable official vendor documentation. State the source actually used.

## Outputs

- requested app and installed version
- `guide_match`: `matched`, `unavailable`, or `incomplete`
- guide title and selected topic when matched
- source classification: `local-helpviewer`, `in-app-help`, `xcode-local-docs`, `dash`, or `official-vendor-docs`
- one explicit handoff when the local catalog cannot answer the request

## Inputs

- requested Apple Mac app and task
- installed app identity and version
- local catalog availability and matching guide/topic, if found

## Guards and Stop Conditions

- Keep this workflow Mac-only. Do not infer iPhone or iPad guidance from a Mac catalog result.
- Treat Tips/HelpViewer as a discovery aid, not a source to scrape, bulk-export, cache, or redistribute.
- Do not claim version-specific guide coverage unless the selected guide itself exposes a matching version. Record the installed app version separately.
- Do not use a local HelpViewer result as authority for Apple framework APIs, Xcode project behavior, signing, or release policy; recommend `explore-apple-swift-docs` for API/documentation routing and the owning Xcode workflow for execution.
- Do not modify app settings, documents, libraries, projects, or system configuration while looking up help.
- Stop with `unavailable` or `incomplete` when the catalog cannot provide a trustworthy answer. Do not fill the gap from memory.

## Fallbacks and Handoffs

- Recommend the app's in-app Help when the HelpViewer catalog is unavailable or incomplete.
- Recommend `explore-apple-swift-docs` for Apple framework APIs, Xcode-local documentation, Dash, or official documentation-source routing.
- Recommend the owning app, Xcode, device, test, or Creator Studio workflow when the user needs to act on a project or system state rather than read guidance.

## Customization

Use `references/customization-flow.md`. The first version has no runtime-enforced knobs; `scripts/customization_config.py` preserves the shared Apple Dev Skills customization contract.

## References

- `references/catalog-and-fallback-contract.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when an Apple app repository needs its reusable project-policy baseline alongside a local documentation lookup.
