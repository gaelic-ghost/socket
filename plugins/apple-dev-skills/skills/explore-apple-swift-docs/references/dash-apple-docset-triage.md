# Dash Apple Docset Triage

Use this guide when the agent needs to reason about Apple-relevant Dash coverage without pretending that every Apple framework already has a clean first-party Dash docset.

## Purpose

- help the agent recognize the Apple-relevant Dash docsets that are usually worth checking first
- keep Dash usage explicit and honest when coverage is partial
- avoid collapsing framework docs, language docs, testing docs, and sample-code docs into one vague "Apple docs" bucket

## High-Value Apple-Relevant Dash Categories

### Language and core library

Likely high-value docsets:

- `Swift`
- `Foundation`

Use these when the request is mostly about the Swift language, common library APIs, string and date handling, collections, networking primitives, and related symbol lookup.

### UI and app frameworks

Likely high-value docsets when installed:

- `UIKit`

Use these when the request is specifically UIKit-heavy and a fast local symbol search would help. Do not assume equivalent Dash coverage exists for every Apple UI framework.

### Testing and package tooling

Likely high-value docsets when installed:

- `XCTest`
- `Swift Package Manager`

Use these for older XCTest surfaces, package-manifest questions, and package-tooling lookup.

### Guides and samples

Likely high-value docsets:

- `Apple Guides and Sample Code`

Use this when the request is better answered by conceptual guides, migration documents, tutorials, or sample-code exploration than by one API symbol page.

## What Dash Is Good At Here

- quick local symbol search
- quick local full-text search when FTS is enabled
- jumping across language, package, and framework docs without leaving the local docs tool

## What Dash Should Not Be Assumed To Cover Cleanly

- every new Apple framework
- every current Apple SDK release surface
- every lifecycle or migration topic that Apple documents on the web

When coverage is unclear, say so and fall back to Xcode MCP docs or official Apple web docs instead of bluffing.

## Maintenance Note

This guide is intentionally a triage aid, not the final repo-level preferred shortlist. If maintainers later choose a fixed preferred Apple Dash shortlist, add it as a separate explicit reference instead of silently turning this triage guide into policy.

For the current Swift-package-oriented shortlist, use [dash-swift-package-shortlist.md](./dash-swift-package-shortlist.md).
