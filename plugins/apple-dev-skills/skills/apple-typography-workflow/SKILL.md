---
name: apple-typography-workflow
description: Guide Apple platform typography decisions and implementation across SwiftUI Font, UIKit UIFont, AppKit NSFont, San Francisco system fonts, SF Pro, SF Compact, SF Mono, SF Pro Rounded, New York serif design, Dynamic Type, text styles, fontDesign, fontWeight, fontWidth, monospaced digits, custom font bundle integration, font licensing and redistribution boundaries, accessibility scaling, and Xcode font asset validation. Use when a task mentions Apple typography, San Francisco, SF Pro, SF Compact, SF Mono, New York, Dynamic Type, UIFontMetrics, preferredFont, NSFont.TextStyle, custom fonts, UIAppFonts, ATSApplicationFontsPath, or text style repair.
---

# Apple Typography Workflow

## Purpose

Use this skill to choose, implement, repair, and validate Apple platform typography that respects system font behavior, Dynamic Type, accessibility, platform conventions, and custom-font bundle boundaries.

It is not the generic visual-design workflow, not the SF Symbols workflow, and not the Xcode project execution workflow.

## When To Use

- Use this skill when the task mentions Apple typography, San Francisco, SF Pro, SF Compact, SF Mono, SF Pro Rounded, New York, system fonts, Dynamic Type, text styles, font designs, font weights, font widths, monospaced digits, or custom font integration.
- Use this skill when code uses SwiftUI `Font`, `fontDesign`, `fontWeight`, `fontWidth`, UIKit `UIFont`, `UIFontMetrics`, `UIFontDescriptor.SystemDesign`, AppKit `NSFont`, preferred fonts, `UIAppFonts`, or `ATSApplicationFontsPath`.
- Use this skill when text does not scale correctly, hard-coded point sizes are hurting accessibility, custom fonts are not loading, or a project is bundling fonts unnecessarily.
- Recommend `apple-ui-accessibility-workflow` when the work is broader accessibility review beyond typography scaling and readability.
- Recommend `sf-symbols-workflow` when the task is icon or symbol selection rather than text.
- Recommend `xcode-build-run-workflow` when the next step is adding font files, Info.plist keys, bundle resources, target membership, preview, build, or simulator validation.

## Single-Path Workflow

1. Classify the typography job:
   - system text style choice
   - San Francisco or system design choice
   - monospaced or monospaced-digit choice
   - New York or serif design choice
   - Dynamic Type repair
   - custom font integration
   - font licensing or redistribution boundary
   - Xcode resource or Info.plist validation
2. Apply the Apple docs gate:
   - read the relevant Apple documentation first
   - state the documented behavior being relied on before recommending implementation
   - if Apple docs and current code disagree, stop and surface the conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Choose system typography first:
   - use SwiftUI `Font` text styles and system designs for SwiftUI
   - use `UIFont.preferredFont(forTextStyle:)` and `UIFontMetrics` for UIKit
   - use `NSFont.preferredFont(forTextStyle:options:)` or system font APIs for AppKit
   - use custom font files only when the app's brand or content requirements justify them
4. Preserve accessibility scaling:
   - prefer Dynamic Type text styles over hard-coded point sizes
   - scale custom fonts through the framework-supported metrics path
   - ensure controls and layout can adapt to larger text
   - avoid using font weight, width, size, or color as the only signal for state
5. Check platform and asset boundaries:
   - do not bundle Apple system font files for normal app UI
   - avoid machine-local font paths in public docs, project files, or scripts
   - use documented Info.plist keys and Xcode resource membership for custom font files
   - state licensing and redistribution concerns once when the task asks to extract, modify, bundle, or publish Apple font assets
6. Return one recommendation path with:
   - chosen text style or font design
   - Dynamic Type behavior
   - custom font or system font decision
   - documented Apple behavior relied on
   - validation or handoff step

## Inputs

- `request`: optional free-text task description used to classify the typography question.
- `target_framework`: optional framework emphasis such as `swiftui`, `uikit`, `appkit`, or `mixed`.
- `target_platforms`: optional platform list such as `ios`, `macos`, `watchos`, `tvos`, `visionos`, or `mixed-apple`.
- `font_assets`: optional paths or names for custom font files.
- `text_role`: optional text role such as body, headline, caption, code, tabular data, brand display, or dense utility UI.
- Defaults:
  - Apple docs-first guidance always applies
  - system typography is preferred before bundled custom fonts
  - Dynamic Type and readability are part of the first recommendation, not a later polish step

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a typography recommendation is ready
  - `handoff`: another skill owns the next step after typography-aware classification
  - `blocked`: docs, asset, platform, licensing, or project context is insufficient for an honest recommendation
- `path_type`
  - `system-typography`
  - `dynamic-type-repair`
  - `custom-font-integration`
  - `licensing-boundary`
  - `project-validation`
  - `handoff`
- `output`
  - classified typography job
  - chosen system text style, design, or custom font path
  - Dynamic Type and accessibility behavior
  - licensing or redistribution boundary when relevant
  - documented Apple behavior relied on
  - validation or handoff step

## Guards and Stop Conditions

- Do not bundle Apple system font files for ordinary app UI.
- Do not hard-code machine-local font paths into public project files, scripts, or docs.
- Do not skip Dynamic Type when user-facing text is involved.
- Do not claim a custom font is loaded or available until the project resource and Info.plist path have been validated.
- Do not use typography alone to communicate important state.
- Do not repeat licensing warnings after stating the concern once for a private local task, unless the task changes into public redistribution or release.
- Stop with `blocked` when the task depends on unavailable font files, unknown license terms, or target-platform behavior that cannot be checked.

## Fallbacks and Handoffs

- Recommend `apple-ui-accessibility-workflow` for broader accessibility implementation or review.
- Recommend `sf-symbols-workflow` when the work is primarily symbol, icon, or glyph selection rather than text.
- Recommend `swiftui-app-architecture-workflow` or `appkit-app-architecture-workflow` when typography changes reveal ownership or view-structure problems.
- Recommend `xcode-build-run-workflow` for font files, bundle resources, Info.plist keys, target membership, preview, build, or simulator validation.
- Recommend `explore-apple-swift-docs` when the user primarily needs raw Apple documentation lookup.
- Recommend `references/snippets/apple-xcode-project-core.md` when repo policy or Xcode project-integrity guidance is needed before applying font resources.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on typography classification, system-font choices, Dynamic Type behavior, custom-font boundaries, and validation handoffs. If future iterations add deterministic font-bundle checks, document those helpers before relying on them.

## References

### Workflow References

- `references/system-typography-and-dynamic-type.md`
- `references/custom-fonts-and-licensing.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs direct Apple-docs lookup instead of typography workflow guidance.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project policy before integrating font assets.
- Apple documentation anchors to verify include Human Interface Guidelines Typography, SwiftUI Font, SwiftUI Applying custom fonts to text, UIKit Scaling fonts automatically, `UIFontDescriptor.SystemDesign`, `UIFontMetrics`, `UIFont.preferredFont(forTextStyle:)`, AppKit `NSFont`, `UIAppFonts`, and `ATSApplicationFontsPath`.

### Script Inventory

- `scripts/customization_config.py`
