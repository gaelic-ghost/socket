---
name: xcode-localization-workflow
description: Plan, implement, review, and validate Apple-platform localization with Xcode String Catalogs. Use for .xcstrings setup, localizable SwiftUI and Foundation text, string tables, comments, plural and device variants, XLIFF handoff, locale UI checks, or Xcode 27 agent-assisted translation.
---

# Xcode Localization Workflow

## Purpose

Make an Apple app understandable and usable in its supported languages, regions, and interface directions. This workflow owns the durable localization path: String Catalog setup, source-code extraction, translator context, translation handoff, and locale-aware UI evidence. It treats Xcode 27 agent translation as an optional beta-era acceleration, never as the reason to adopt localization or as proof that a translation is ready to ship.

Use Xcode String Catalogs (`.xcstrings`) as the default catalog format for current Xcode projects. They centralize extracted strings, translations, plural variants, and device-specific variants. They do not make arbitrary runtime strings, poor source context, date/number formatting, or clipped layouts localizable by themselves.

## When To Use

- Use this workflow when adding, repairing, migrating to, or reviewing a String Catalog.
- Use it for localizable SwiftUI, UIKit, AppKit, Foundation, attributed text, bundle/table, plural, device-variation, XLIFF, or translation-context work.
- Use it when an Xcode-hosted or external agent is asked to add languages or translate a catalog.
- Hand project inspection, source membership, build, and Xcode-managed project mutation to `xcode-build-run-workflow`.
- Hand locale-aware test design and execution to `xcode-testing-workflow`; hand visual destination selection and physical-device evidence to `xcode-device-hub-workflow`.
- Hand accessibility semantics, Dynamic Type, VoiceOver, and bidirectional-layout concerns to `apple-ui-accessibility-workflow`.
- Hand agent setup, permissions, and live Xcode 27 MCP capability discovery to `xcode-coding-intelligence-workflow`.

## Single-Path Workflow

1. Establish the localization contract before editing. Record the development language, supported language-and-region pairs, audience, tone, terminology, names that must remain unchanged, and which content is intentionally not user-facing. Put durable translator-facing guidance in `TRANSLATION.md` when the project needs more than a few code comments.
2. Inspect the app for user-visible text and its owning bundle. Do not localize identifiers, logging, protocol values, stable machine-readable data, accessibility identifiers, or text that a product requirement explicitly preserves. Do localize visible labels, actions, errors, empty states, onboarding, notifications, and format strings.
3. Add `Localizable.xcstrings` through Xcode's String Catalog file template when the target has no catalog. Keep one default catalog until a catalog has a real ownership boundary, such as Navigation or a separately shipped feature. Use a named `table` or `tableName` only when the corresponding catalog exists.
4. Make source text discoverable and contextual:
   - SwiftUI view literals such as `Text("Continue")` are localizable by default; use the API's `comment` parameter when the visual role or meaning is ambiguous.
   - Use `String(localized:table:bundle:locale:comment:)` for a resolved Foundation string, including UIKit and AppKit controls. Use `AttributedString(localized:...)` when localized Markdown or attributed content is required.
   - Use `LocalizedStringResource` when a localized resource must cross an API or process boundary before resolution. Specify the owning bundle for code in a framework or Swift package rather than silently reading the app's main bundle.
   - Prefer static literals or explicit static keys with a development-language default. Do not expect Xcode extraction to resolve a dynamically constructed key, table, or comment.
   - Never concatenate translated fragments, inject grammatical punctuation outside the localized sentence, or use English singular/plural branching in code. Put values into one localizable interpolated string so translators can reorder or inflect them.
5. Build every relevant target. Xcode discovers localizable API calls and updates the catalog on build; inspect each new or changed entry in the catalog's source view. Treat a clean build as extraction evidence, not as translation or visual-fit evidence.
6. Add the requested language and region variants in the catalog or project localization settings. Provide translator comments that explain role, audience, variable meaning, constraints, and whether a term is a product name. Enable Xcode's automatic comment generation only as a supplement to deliberately written context.
7. Model language-specific variation in the catalog:
   - For count-dependent text, start with interpolation, build, then choose **Vary by Plural**. Review the forms Xcode creates for every target language; do not assume English's one/other rules apply elsewhere.
   - Add device variants only when the wording genuinely differs by device, not to hide a layout problem.
   - Prefer localized `FormatStyle` APIs for dates, numbers, measurements, lists, and names. Do not translate preformatted English data or bake locale-specific formatting into a catalog string.
8. Translate and review. Enter known translations in Xcode or export an `.xcloc` package for a localization service, then import and review the resulting diff. Mark uncertain strings as needing review. A person fluent in the target language and region must review terminology, grammar, tone, placeholders, and cultural suitability before release.
9. Validate the product, not merely catalog completeness. Build the affected targets; run locale-specific tests where available; inspect representative long-text, Dynamic Type, right-to-left, plural, device-variant, error, onboarding, and system-dialog states. Use simulator evidence for normal visual behavior and a physical device where hardware or production-only behavior matters.
10. Use Xcode 27 agent translation only after the stable path above is in place. Confirm the installed Xcode version, the agent surface, permission boundary, and live String Catalog tool inventory through `xcode-coding-intelligence-workflow`. Preserve glossary and project guidance, review the generated catalog/XLIFF changes, and retain Xcode's machine-translation provenance. Do not present agent output as human-reviewed translation.

## Inputs

- `request`: the localization change, audit, migration, or translation task.
- `targets`: optional app, framework, package, or extension targets that own localizable text.
- `locales`: optional supported languages and regions; discover and confirm them when omitted.
- `translation_surface`: optional `catalog-editor`, `xliff`, `agent`, or `unknown`; default to the catalog editor when no external translation handoff is required.
- `validation_focus`: optional emphasis such as `plurals`, `rtl`, `dynamic-type`, `formatting`, `device-variants`, or `full`.

## Implementation Choices

### Keys, values, and generated symbols

Development-language literals are appropriate when a string's value is a stable, readable key. For product copy that must evolve independently from call sites, add a catalog key and use Xcode-generated `LocalizedStringResource` symbols. This avoids duplicating a key in code while preserving a typed parameter surface for format placeholders.

Choose one convention per catalog: readable development-language literals or semantic keys with explicit default values. Do not mix conventions casually in the same feature because translators and reviewers lose a predictable source of truth.

### Tables and bundles

Tables are an organizational boundary, not a workaround for missing context. Keep the default `Localizable` catalog for small apps. Split only when a distinct feature, framework, or ownership boundary makes translation handoff clearer. When code belongs to a framework or Swift package, pass its resource bundle explicitly and test that bundle's localization independently.

### Legacy resources

Do not bulk-convert `.strings` and `.stringsdict` resources without checking deployment targets, existing localization-service contracts, and source control diffs. String Catalogs are the recommended current Xcode path, including plural handling, but a migration should preserve every supported locale and plural form. Keep a legacy file only when a real compatibility or external-tool constraint requires it; do not create parallel duplicate catalogs as a fallback.

## Outputs

- supported language/region contract and translation guidance location
- catalog and table ownership, source APIs, and resource-bundle decision
- build-backed extraction result and reviewed catalog diff
- translation provenance and human-review status for every target locale
- locale, Dynamic Type, right-to-left, and device evidence or explicit gaps
- handoff to build/run, testing, Device Hub, accessibility, or coding-intelligence workflows

## Guards and Stop Conditions

- Do not hard-code a `DEVELOPER_DIR`, DerivedData location, product path, or simulator identifier. Use the selected Xcode toolchain and the owning build/device workflow.
- Do not infer translation quality from a 100-percent catalog indicator, an agent result, or a successful import.
- Do not translate privacy-sensitive user content, source code, logs, identifiers, secrets, or machine-readable protocol values through a catalog or an external translation service without explicit approval.
- Do not use string concatenation, runtime-generated localization keys, English plural logic, or unlocalized format values as a shortcut.
- Do not claim right-to-left support from a left-to-right simulator pass. Inspect a right-to-left locale and the affected directional UI.
- Do not perform an XLIFF import, add a language, or apply agent-generated translations without a reviewable diff and explicit scope for the changed locale set.
- Do not claim stable Xcode behavior from an Xcode 27 beta agent capability. Date beta evidence and confirm the installed Xcode surface before use.

Stop and surface the decision when the requested change needs a new catalog ownership model, changes a product's supported locales, migrates legacy translation assets, sends content to a third-party translation service, or broadens the translation scope beyond the approved target and language set.

## Fallbacks and Handoffs

- Use `xcode-build-run-workflow` when a build, target-membership, resource-bundle, or project-integrity decision is required.
- Use `xcode-testing-workflow` for deterministic localization assertions and `xcode-device-hub-workflow` for destination-specific visual evidence.
- Use `apple-ui-accessibility-workflow` when Dynamic Type, right-to-left, VoiceOver, or semantic UI behavior is the primary concern.
- Use `xcode-coding-intelligence-workflow` only for Xcode 27 agent setup, permissions, or live localization-MCP capability discovery; return here for the catalog-first implementation and review path.

## Customization

Use `references/customization-flow.md`. The initial workflow has no runtime-enforced customization knobs; it keeps the shared configuration surface available without turning locale or translation policy into hidden machine state.

Recommend `references/snippets/apple-xcode-project-core.md` when a target app repository needs durable Xcode project guidance alongside its localization contract.

## References

- `references/string-catalog-foundations.md`
- `references/source-apis-and-translator-context.md`
- `references/translation-review-and-validation.md`
- `references/agent-assisted-translation.md`
- `references/customization-flow.md`
- `references/snippets/apple-xcode-project-core.md`
