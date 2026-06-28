# Custom Fonts and Licensing

Use this reference when the task asks to bundle font files, use brand fonts, repair font loading, or discuss Apple font assets.

## Custom Font Decision

- Use a custom font only when brand, content, or product needs justify the extra asset and validation surface.
- Confirm the font license allows app embedding before adding it to a project.
- Keep font source files in normal project resources, not machine-local paths.
- Avoid committing fonts from private or system locations unless the license and redistribution path are explicit.

## Xcode Integration Boundaries

- For iOS, watchOS, tvOS, or Mac Catalyst, Apple documents `UIAppFonts` for app-provided fonts.
- For macOS app targets, Apple documents `ATSApplicationFontsPath`.
- Xcode target membership, resource copying, Info.plist edits, previews, builds, and simulator validation belong to `xcode-build-run-workflow`.
- Do not claim a custom font is available until the resource and Info.plist path have been validated.

## Loading and Repair Checks

- Verify the font file is included in the target bundle.
- Verify the app uses the font's internal PostScript or family name expected by the framework API.
- Verify Dynamic Type scaling for user-facing text.
- Verify fallback behavior when the font fails to load.
- Use descriptive runtime messages if code must fail or fall back because a font cannot be loaded.

## Apple Font Asset Boundary

- Do not extract or bundle Apple system font files for ordinary app UI.
- Use system font APIs for San Francisco, SF Mono, rounded system designs, and New York/serif behavior.
- If the user asks to extract, modify, redistribute, package, or publish Apple font assets, state the licensing or redistribution concern once.
- Private local research may continue after that one-time note if Gale explicitly keeps the work private, but public redistribution or release needs a separate explicit decision.
