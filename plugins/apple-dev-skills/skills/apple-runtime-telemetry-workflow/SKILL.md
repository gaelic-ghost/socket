---
name: apple-runtime-telemetry-workflow
description: Add and verify privacy-aware Apple unified logging and signposts in macOS, iOS, and related Apple apps. Use when designing Logger categories, diagnosing intermittent runtime behavior, collecting focused evidence, or measuring an operation with OSSignposter.
---

# Apple Runtime Telemetry Workflow

## Purpose

Add the smallest useful unified-log and signpost evidence to diagnose a concrete runtime question. This workflow owns `Logger`, subsystem/category design, privacy, evidence capture, and `OSSignposter` boundaries. It does not own generic server observability, analytics, crash reporting services, or broad event collection.

## Workflow

1. State the question to answer: lifecycle, command, window/scene transition, failure classification, or duration. Do not add telemetry without a specific observation need.
2. Choose a stable subsystem and a narrow category named for the owning feature. Keep a local logger close to that feature instead of creating an application-wide logging manager.
3. Emit a small lifecycle record at the transition and a precise error or fault record at a classified failure. Include non-sensitive identifiers only when they make the event actionable.
4. Leave interpolated values private by default. Mark a value `.public` only after confirming that it has no user, account, file-path, content, credential, or other sensitive-data meaning.
5. Use `OSSignposter` only when duration or event timing is the question. Begin and end the same measured operation, retain the interval state correctly, and inspect the result in Instruments rather than treating an ordinary log line as a timing measurement.
6. Reproduce the relevant flow and inspect the evidence in Xcode's debug console, Console, or the `log` tool. Filter by the documented subsystem/category and preserve only the minimal output needed to support the diagnosis.
7. Remove temporary high-volume records after the investigation, or keep a small durable lifecycle/error set with a clear operational value.

## Guards

- Do not create a logging manager, repository, analytics pipeline, telemetry daemon, or remote collector for ordinary app diagnostics.
- Do not put secrets, personal data, file contents, raw request bodies, authorization material, or full unreviewed object descriptions in logs.
- Do not use `OSLogStore.local()` as a default app feature; Apple documents that local-store access needs an admin account and the `com.apple.logging.local-store` entitlement.
- Do not claim a signpost proves a performance improvement until an Instruments capture measures the same scenario.
- Hand ETTrace, memgraphs, leaks, and trace comparison to `ios-runtime-forensics-workflow`; hand build/run mechanics to `xcode-build-run-workflow`.

## References

- `references/logger-privacy-and-evidence.md`
- `references/signposts-and-runtime-capture.md`
