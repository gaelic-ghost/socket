---
name: xcode-device-hub-workflow
description: Manage and validate simulated and physical Apple devices through Xcode Device Hub. Use when selecting or inspecting run destinations, interacting with an app, changing simulated-device environment settings, capturing screenshots or videos, pairing a device, or collecting diagnostics.
---

# Xcode Device Hub Workflow

## Purpose

Use Device Hub as Xcode's native surface for simulated and physical device work. It owns device selection, interaction, environment inspection, pairing, captures, and diagnostics; it does not replace project build/run, test, debugger, provisioning, or browser-mirror ownership.

## When To Use

- Use this workflow for a Device Hub request, a run-destination decision, simulator or physical-device inspection, screenshots, videos, environment variants, pairing, or downloaded diagnostics.
- Use it when a running Xcode app should be observed or interacted with through Device Hub rather than by opening a separate Simulator window.
- Hand project build, install, launch, and scheme selection to `xcode-build-run-workflow`.
- Hand test design and execution to `xcode-testing-workflow`; hand breakpoints and stack inspection to `xcode-debugger-mcp-workflow`.
- Hand a future local browser mirror or Swift Package preview host to the future AgentDeck runtime; do not substitute a browser bridge for Device Hub until that runtime exists and reports ready.

## Workflow

1. Read the target app, device type, runtime, and evidence goal. Distinguish a normal simulated-device check from a hardware-only, performance, camera, sensor, or pairing requirement.
2. Open the intended Xcode app and Device Hub. Open it from the run-destination menu's Manage Devices action or Xcode's Open Developer Tool menu when no app run has already opened the compact view.
3. Select the device and record its name, platform, operating-system version, and device identifier from the inspector. Keep the selected run destination and the recorded identifier aligned; do not guess a matching simulator from its name alone.
4. For a simulated device, start it and change only the requested environment setting. Treat appearance, Liquid Glass, text size, and resize-mode checks as named variants with visible before/after evidence.
5. For a physical device, inspect pairing and Developer Mode state before attempting a run. Pairing, trust prompts, Developer Mode, unpairing, and configuration changes require explicit user intent at the point of mutation.
6. Run or interact with the app through its owning build/run workflow. Device Hub interaction is proof of the same target device state, not a separate app runtime.
7. Capture a screenshot or video only after the requested state is visible. Record the device identity, app state, and destination path; Device Hub screenshots are full device resolution and may contain sensitive content.
8. Download diagnostics only when they are relevant to the reported failure, then hand the artifact to the debugger, runtime-forensics, or test workflow. State the artifact's source and avoid copying private device data into logs or commits.
9. Stop the app or device session through its owner. Do not erase, remove, unpair, or reset a device as routine cleanup.

## Outputs

- device identity and simulated-versus-physical classification
- environment or pairing state actually inspected
- capture or diagnostic artifact and what it proves
- explicit handoff for build/run, testing, debugger, provisioning, or runtime forensics

## Guards

- Do not treat Simulator results as proof of hardware rendering, battery, thermal, sensor, camera, radio, or performance behavior.
- Do not use Device Hub to infer a CoreSimulator UDID from a display name; inspect the identifier or hand discovery to the normal simulator tooling.
- Do not pair, unpair, enable Developer Mode, remove a simulator, erase data, or change a physical-device setting without the user's explicit action request.
- Do not expose a Device Hub screen or capture over a LAN, tunnel, or external browser surface. That is a separate AgentDeck runtime decision.
- Do not call a loaded Device Hub window proof that an app build, launch, or test passed; verify the requested frame, log, test result, or diagnostic instead.

## References

- `references/device-hub-scope-and-evidence.md`
- `references/device-hub-safety-and-handoffs.md`
