# Security-Scoped Bookmark Lifecycle

## Creation

1. Receive a URL from a supported user-selection or document interaction.
2. Choose application-scoped or document-scoped behavior and read-only scope deliberately; verify the current platform API and entitlement requirements.
3. Create bookmark data with the appropriate security-scope options.
4. Store the bookmark bytes as sensitive authorization state. Associate them with a stable app record, not merely a path string.

## Resolution and use

1. Load bookmark data and resolve it with matching security-scope options.
2. Capture the stale result. If stale, recreate and persist bookmark data from the resolved URL before treating repair as complete.
3. Call `startAccessingSecurityScopedResource()` immediately around the narrow operation.
4. Balance a successful start with `stopAccessingSecurityScopedResource()` using structured cleanup such as `defer`. Do not stop when start returned false, and do not hold access for the app lifetime by default.
5. Preserve Foundation error domain/code/message and the later file-operation error separately.

```swift
var stale = false
let url = try URL(
    resolvingBookmarkData: data,
    options: [.withSecurityScope],
    relativeTo: nil,
    bookmarkDataIsStale: &stale
)

if stale {
    let repaired = try url.bookmarkData(
        options: [.withSecurityScope],
        includingResourceValuesForKeys: nil,
        relativeTo: nil
    )
    try persist(repaired)
}

let started = url.startAccessingSecurityScopedResource()
defer {
    if started { url.stopAccessingSecurityScopedResource() }
}
try performNarrowOperation(at: url)
```

Adapt options and storage to the current documented API, sandbox shape, and read-only requirement. Validate selection-session access separately from post-relaunch bookmark access.

## Failure matrix

Test valid, stale, corrupt, missing, moved, renamed, removed, inaccessible, revoked, read-only, wrong-scope, wrong-process, and volume-offline cases. A resolved URL does not prove the file operation is authorized; another layer can still deny it.
