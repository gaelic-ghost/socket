# File Provider Synchronization

File Provider is the remote-storage integration point. A provider enumerates files and folders, exposes placeholders, materializes content on demand, receives document operations, and reports remote changes to the system.

## Core Model

Use stable provider item identifiers and hierarchy identifiers. Treat versions and sync anchors as protocol state, not display metadata. Keep a clear record of local pending work, confirmed remote state, cancellation, and retry. The working set must reflect materialized and otherwise important items so the system can apply background changes and maintain availability/indexing behavior.

When remote state changes, use the documented File Provider signaling or supported push path to prompt system enumeration. If identifier stability is lost, use the documented recovery path rather than pretending stale identifiers remain valid.

## Sources

- [Synchronizing files using file provider extensions](https://developer.apple.com/documentation/fileprovider/synchronizing-files-using-file-provider-extensions)
- [Synchronizing the File Provider Extension](https://developer.apple.com/documentation/fileprovider/synchronizing-the-file-provider-extension)
- [Nonreplicated File Provider extension](https://developer.apple.com/documentation/fileprovider/nonreplicated-file-provider-extension)
