# Xcode MCP Docs

Use Xcode MCP docs as the default Apple and Swift local-docs path when they are available and the user has not asked for another source.

- Prefer this path first for Apple framework symbols, API reference lookups, and Apple-platform behavior questions.
- When the Xcode MCP surface exposes `DocumentationSearch`, treat it as the primary symbol and topic search entrypoint for Apple-owned frameworks and lifecycle questions.
- For DocC questions, treat Xcode MCP documentation results as primarily the Xcode-side product workflow for creating, building, exporting, and distributing DocC content inside Xcode, not as the fuller source of truth for DocC directive syntax or package-level DocC internals.
- Prefer this path especially for SwiftUI, SwiftData, Observation, UIKit, AppKit, WidgetKit, CloudKit, AVFoundation, Core Animation, Core Graphics, `URLSession`, and other Apple-owned SDK surfaces whose behavior tracks current Xcode and SDK releases.
- If Xcode MCP docs fail or are unavailable, record the concrete failure reason plainly, then fall back through Dash MCP, Dash localhost HTTP, and official web docs in that order.
- When the user explicitly wants local multi-ecosystem docs coverage beyond Apple and Swift, Dash may still be the better fit.
