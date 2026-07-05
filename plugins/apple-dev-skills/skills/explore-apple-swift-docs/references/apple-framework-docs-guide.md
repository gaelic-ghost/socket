# Apple Framework Docs Guide

Use this guide when the user asks about a concrete Apple API, framework, lifecycle rule, or platform behavior and the agent needs to choose the right docs source instead of treating every request like a generic search.

## Default Rule

- Prefer Xcode MCP docs first for Apple-first frameworks and symbols when the docs tool is available.
- Prefer Dash next when the needed Apple-adjacent docset is already installed and the request benefits from fast local search across symbols or snippets.
- Prefer open source Swift repositories, generated DocC, or release notes when the relevant Swift package or tool is open source and available there.
- Prefer official Apple web docs when Xcode MCP docs are unavailable, when Dash coverage is missing or thin, or when the answer needs an authoritative public link, but only if the content is actually readable through the available source.
- Do not treat generic no-JS web search or no-JS page extraction as a readable source for Apple Developer documentation. Apple Developer pages often require JavaScript-rendered payloads, so a URL or search snippet alone is not enough evidence.

## Common Apple Framework Families

### Xcode MCP docs first

Use Xcode MCP docs as the primary path for these Apple framework and platform families:

- SwiftUI
- Observation
- SwiftData
- AppKit
- UIKit
- WidgetKit
- CloudKit
- AVFoundation
- Core Animation
- Core Graphics
- URL Loading System and `URLSession`
- Foundation-on-Apple when the question is Apple-platform behavior rather than pure language syntax
- app lifecycle, scene lifecycle, previews, and Xcode-managed workflow behavior

Why:

- These surfaces are Apple-owned and shift with SDK and Xcode releases.
- The docs are usually symbol-centric and lifecycle-sensitive, which fits the Xcode MCP docs path well.

### Dash often helps when installed

Dash is often a strong local companion for these surfaces when the relevant docsets are installed:

- Swift language reference
- Foundation
- UIKit
- XCTest
- Swift Package Manager
- Apple Guides and Sample Code

Why:

- These are strong candidates for quick local symbol search, full-text search, and side-by-side reading with non-Apple docs.

### Source repositories and official web docs when local coverage is weak

Prefer source repositories, generated DocC, release notes, or readable official Apple web docs directly when:

- the relevant Swift package, tool, or standard-library-adjacent surface is open source and the repository or generated docs answer the question
- the framework is new enough that local Dash coverage is unclear
- the question depends on the latest release notes or migration guidance
- the agent needs a citable public URL
- the local Xcode MCP docs path is unavailable

## Common Request Types

### Framework behavior questions

Examples:

- SwiftUI state invalidation
- SwiftData query behavior
- Observation lifecycle rules
- UIKit view-controller containment
- AppKit responder-chain behavior

Preferred path:

- Xcode MCP docs, then Dash if useful, then readable official Apple web docs if needed

### Language and standard-library questions

Examples:

- Swift concurrency syntax
- protocol or generic rules
- standard library behavior

Preferred path:

- Xcode MCP docs or Dash `Swift`, then official Swift project docs, source, or generated docs if needed

### Test-framework questions

Examples:

- Swift Testing
- XCTest
- XCUITest
- `.xctestplan`

Preferred path:

- Xcode MCP docs first, with Dash `XCTest` as a local supplement when installed

### Samples, guides, and migration help

Examples:

- sample code
- migration guidance
- tutorial-style walkthroughs

Preferred path:

- Apple Guides and Sample Code in Dash when installed, otherwise source repositories or readable official Apple web docs

## Tooling Notes

- If the active Xcode MCP surface exposes `DocumentationSearch`, use it as the first symbol and topic search path before falling back.
- If Dash is installed but full-text search is disabled for a relevant docset, consider enabling FTS before doing broad text search.
- Do not assume Dash has first-party coverage for every Apple framework just because Apple docs exist on the web.
- Do not claim Apple Developer documentation was checked from a generic web-search result when the actual page body was not readable.
