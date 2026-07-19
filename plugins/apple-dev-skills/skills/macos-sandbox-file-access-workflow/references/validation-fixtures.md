# Sandbox File Access Validation Fixtures

Build a signed sandboxed fixture with open-panel selection and separate read-only/read-write modes. Persist bookmark data, terminate fully, relaunch, resolve, repair stale data, start access, perform one operation, and balance stop access.

Cover:

- file and directory selection; open/save, drag/drop, and document URLs
- selection-session access versus clean relaunch
- moved, renamed, removed, malformed, stale, revoked/inaccessible, and volume-offline resources
- read-only enforcement and attempted write
- main app, helper, XPC service, and extension consumers
- App Group match/mismatch across source, profile, and final signatures
- POSIX mode/ACL, symlink, mount, TCC-protected location, Data Vault, and SIP denials

Record app and consumer identities, exact macOS build/SDK, sandbox and signed entitlements, selection source, bookmark options, stale/start results, exact Foundation and file errors, privacy-redacted path identity, operation result, and cleanup. Automated fixtures must use generated nonsensitive paths; visible prompts or Settings changes require explicit approval and preferably a disposable guest.
