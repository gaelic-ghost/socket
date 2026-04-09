# Xcode MCP Docs

Use Xcode MCP docs as the default Apple and Swift local-docs path when they are available and the user has not asked for another source.

- Prefer this path first for Apple framework symbols, API reference lookups, and Apple-platform behavior questions.
- When the Xcode MCP surface exposes `DocumentationSearch`, treat it as the primary symbol and topic search entrypoint for Apple-owned frameworks and lifecycle questions.
- Prefer this path especially for SwiftUI, SwiftData, Observation, UIKit, AppKit, WidgetKit, CloudKit, AVFoundation, Core Animation, Core Graphics, `URLSession`, and other Apple-owned SDK surfaces whose behavior tracks current Xcode and SDK releases.
- If Xcode MCP docs fail or are unavailable, pass the concrete failure reason into `scripts/run_workflow.py --mcp-failure-reason ...` so the workflow can shape the next docs source cleanly.
- When the user explicitly wants local multi-ecosystem docs coverage beyond Apple and Swift, Dash may still be the better fit.
