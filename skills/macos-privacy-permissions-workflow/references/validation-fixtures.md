# Privacy Permission Validation Fixtures

## Minimum fixture matrix

Use disposable, signed fixtures with one protected operation per mode:

- Accessibility status/request plus one harmless AX read against a named target.
- A signed Apple Events controller and target so the controller-target pair is explicit.
- Screen-capture preflight/request and one bounded capture in a disposable guest.
- `EPDeveloperTool` status/request preserving all declared authorization states.
- The same development tool reached directly, from Terminal, an IDE, an agent host, and a helper/XPC process.
- One framework-owned personal-data class with correct, missing, and malformed usage descriptions.
- A Files and Folders or Full Disk Access denial that validates the Settings-managed boundary without attempting self-grant.

## Test record

Record fixture commit/hash, bundle ID, signer/Team ID/designated requirement, macOS build, SDK/Xcode, guest/physical status, management state, prior decision/reset history, invocation path, status/preflight, visible UI, lifecycle transition, exact error, and actual operation result.

Automated checks may validate source declarations, signed identities, expected state handling, and reporting contracts. A visible prompt, System Settings edit, logout/restart, PPPC install, or live-host permission mutation requires separate explicit approval immediately before execution. Prefer a resettable SIP-enabled macOS guest; label local failure injection as lower fidelity.
