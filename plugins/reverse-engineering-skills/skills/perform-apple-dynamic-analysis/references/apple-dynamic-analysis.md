# Apple Dynamic Analysis Reference

## Environment Manifest Additions

- Mac or device model and SoC.
- OS marketing version and build.
- Xcode, SDK, LLDB, and Instruments builds.
- Physical device, Simulator, VM, native process, or Rosetta translation.
- Developer Mode and pairing state when relevant.
- SIP or Apple Silicon security policy when relevant.
- Artifact signature, entitlements, provisioning, sandbox, hardened runtime, and `get-task-allow`.

## Method Boundaries

- Launch: debugger starts a configured executable and controls initial state.
- Attach: debugger connects to an existing process and depends on task-access policy.
- Trace/profile: Instruments or another supported collector observes selected activity.
- Logs: unified logging or app-specific logs provide timestamped runtime evidence.
- Diagnostics: crash reports or sysdiagnose packages are broader evidence with privacy and collection-cost implications.

Choose the narrowest method. Record all breakpoints, commands, probes, environment variables, injected libraries, and configuration changes because they can alter behavior.

## Address Correlation

Match image UUID and architecture first. Preserve the runtime image load address, unslid base or image-relative offset, ASLR slide, original pointer representation, and static database base. Use `correlate-apple-symbols-and-crashes` when symbol identity or frame translation is central.

## Authoritative Sources

- [LLDB tutorial](https://lldb.llvm.org/use/tutorial.html)
- [Apple crash analysis](https://developer.apple.com/documentation/xcode/analyzing-a-crash-report)
- [System Integrity Protection runtime protections](https://developer.apple.com/library/archive/documentation/Security/Conceptual/System_Integrity_Protection_Guide/RuntimeProtections/RuntimeProtections.html)
- [Apple Security Research Device](https://security.apple.com/research-device)
- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)

Use Xcode-local documentation for the installed debugger, Device Hub, Instruments, and platform build before relying on version-sensitive steps.
