# System Typography and Dynamic Type

Use this reference when choosing Apple system typography, text styles, or scaling behavior.

## System Font Choices

- Prefer system typography APIs for normal app UI.
- Use SwiftUI `Font` text styles for SwiftUI.
- Use `Font.system(_:design:weight:)` when a design such as default, rounded, monospaced, or serif is a real semantic or visual choice.
- Use UIKit `UIFont.preferredFont(forTextStyle:)` for dynamic system text styles.
- Use `UIFontDescriptor.SystemDesign` for UIKit system designs such as default, rounded, monospaced, and serif.
- Use AppKit `NSFont.preferredFont(forTextStyle:options:)` or system font APIs for macOS text.
- Use monospaced digits for aligned numeric data when full monospace text is not wanted.

## San Francisco and New York

- Treat San Francisco as the system default family surfaced through framework system font APIs, not as a font file to bundle.
- Expect platform-specific system defaults, such as SF Pro on iOS and SF Compact on watchOS where Apple documents that behavior.
- Use rounded, monospaced, or serif system designs through framework APIs when available.
- Treat New York as the system serif design exposed through Apple typography APIs, not as a bundled file for ordinary app UI.

## Dynamic Type Rules

- Prefer semantic text styles over fixed point sizes.
- In UIKit, pair preferred fonts with `adjustsFontForContentSizeCategory` where supported.
- For custom fonts in UIKit, use `UIFontMetrics` to scale from the chosen text style.
- In SwiftUI, prefer `Font` text styles and custom font APIs that participate in Dynamic Type.
- Validate larger text sizes when layout risk is real.

## Readability Rules

- Do not rely on small text to make dense UI fit.
- Use weight, width, and design changes to support hierarchy, not to replace clear labels.
- Avoid using type treatment alone to communicate important state.
- Consider accessibility and localization before tightening tracking, line height, or text containers.
