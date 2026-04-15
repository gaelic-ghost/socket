# Dash Call Library

Use this reference when the skill needs direct Dash calls instead of wrapper-led exploration. The intended order is:

1. Dash MCP tools when they are available.
2. Dash localhost HTTP when MCP is unavailable or incomplete.
3. Dash URL scheme or macOS Service only when the task is specifically app-level or the direct machine-readable surfaces are unavailable.

## Dash MCP Examples

### List installed docsets

Use `list_installed_docsets` first to resolve the current machine-local identifiers before targeted search:

```json
{}
```

### Search one or more installed docsets

Use `search_documentation` after resolving identifiers:

```json
{
  "query": "Observation",
  "docset_identifiers": "swift,foundation",
  "search_snippets": true,
  "max_results": 10
}
```

### Enable full-text search for a docset

Use `enable_docset_fts` only when the docset reports `full_text_search: disabled`:

```json
{
  "identifier": "swift"
}
```

### Load a page from a previous search result

Use `load_documentation_page` with the returned `load_url`:

```json
{
  "load_url": "http://127.0.0.1:50364/docsets/swift/documentation/..."
}
```

## Dash Local HTTP Examples

### Health check

Read the Dash API port from `~/Library/Application Support/Dash/.dash_api_server/status.json`, then verify the service before other calls:

```bash
curl "http://127.0.0.1:${PORT}/health"
```

### Schema check

Use this when MCP is unavailable and the agent needs to confirm the direct HTTP structure:

```bash
curl "http://127.0.0.1:${PORT}/schema"
```

### List installed docsets

```bash
curl "http://127.0.0.1:${PORT}/docsets/list"
```

### Search installed docsets

```bash
curl --get "http://127.0.0.1:${PORT}/search" \
  --data-urlencode "query=Observation" \
  --data-urlencode "docset_identifiers=swift,foundation" \
  --data-urlencode "search_snippets=true" \
  --data-urlencode "max_results=10"
```

### Enable full-text search

```bash
curl --get "http://127.0.0.1:${PORT}/docsets/enable_fts" \
  --data-urlencode "identifier=swift"
```

## High-Value Docset Targets

Use these as common starting points, then resolve the current installed identifier at runtime:

- `Swift`
- `Foundation`
- `UIKit`
- `XCTest`
- `Apple Guides and Sample Code`
- `swiftlang/swift-docc main`
- `swiftlang/swift-testing main`
- `apple/swift-log main`
- `apple/swift-collections main`
- `apple/swift-nio main`
- `nicklockwood/SwiftFormat main`
- `realm/SwiftLint main`

Use [dash-apple-docset-triage.md](./dash-apple-docset-triage.md) for Apple-relevant triage and [dash-swift-package-shortlist.md](./dash-swift-package-shortlist.md) for the fuller Swift package shortlist.
