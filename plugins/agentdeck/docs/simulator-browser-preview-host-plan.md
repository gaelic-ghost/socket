# Simulator Browser and SwiftUI Preview Host Plan

## Decision

Investigate a local-first Simulator browser and optional Swift Package preview host as an `AgentDeck` runtime capability, with `agentdeck` owning the Codex-facing MCP and skill guidance.

The first usable path must start with the normal Xcode/CoreSimulator device that Gale selects or inspects in Device Hub. It must not create another simulator implementation, replace Xcode Canvas, or make an in-app browser the only way to see an app.

## Why This Is Worth Investigating

The existing Xcode Device Hub and Simulator app remain the best native surfaces for choosing a device, managing its state, inspecting physical devices, and doing ordinary app runs. A local browser mirror adds a different capability: an agent can observe, interact with, and capture proof from the same running Simulator without taking over the desktop foreground.

A disposable preview host could then add a narrow rapid-feedback loop for importable Swift Package views: rebuild changed preview code and swap it into a running Simulator host without relaunching that host. This is not a replacement for Xcode `#Preview`, regular Simulator runs, debugger attachment, or integration tests.

## Ownership Split

- `gaelic-ghost/AgentDeck`: signed macOS runtime, local service lifecycle, permission/status UI, Device Hub-oriented device discovery or selection handoff, local transport, frame capture, input forwarding, and cleanup.
- `socket/plugins/agentdeck`: stdio MCP adapter, `simulator-browser` and future preview-host skill guidance, confirmation policy, diagnostics, and install/troubleshooting documentation.
- `socket/plugins/apple-dev-skills`: Xcode Device Hub, project build/run, simulator, SwiftUI architecture, preview, testing, and Apple documentation guidance. It must remain the owner of Apple-development decisions.

This is a durable building-block investigation only if the local runtime can serve more than one caller: Codex visual QA, browser-visible proof, and optional agent-driven interaction. The simpler extension considered first is an Apple Dev Skills Device Hub workflow plus ordinary Simulator and Xcode Canvas use; it remains the default if browser mirroring does not add dependable agent value.

## Product Boundary

### Normal Simulator Browser

The browser path should:

- use an explicit UDID for a normal, booted CoreSimulator device;
- expose a local-only frame stream and input channel to an approved client;
- preserve the device's ordinary Simulator/Xcode ownership rather than installing instrumentation into the app under test;
- report the selected UDID, device name, runtime, active owner, local endpoint state, and teardown result;
- clean up only the bridge instance for that UDID, never use an unscoped kill operation.

Device Hub is the preferred operator-facing selection and inspection surface where its UI exposes the required device state. `AgentDeck` may use its desktop bridge to read or operate that UI after the ordinary desktop-automation permission checks. A direct `simctl` lookup is an acceptable implementation handoff for device identity and lifecycle when Device Hub is not required.

The initial transport must bind locally. LAN sharing, tunnels, remote Mac operation, camera injection, log export, and broad browser exposure are explicitly out of scope for the first version.

### Swift Package Preview Host

Only evaluate this after the browser mirror is reliable. The candidate approach is:

1. Accept an importable Swift Package manifest, target, explicit Simulator UDID, and optional preview filter.
2. Generate a disposable host Xcode project outside the package source tree.
3. Discover supported `#Preview` and `PreviewProvider` declarations and render their variants in the installed host app.
4. Watch the package source tree, rebuild an isolated preview dylib on a relevant edit, and request that the running host load a new generation.
5. Require evidence that the host PID stayed stable and that the changed frame appeared before reporting a successful hot reload.

The generated host must not edit the user's `.xcodeproj`, `.xcworkspace`, `Package.swift`, schemes, build settings, or application target. Dynamic-library loading, ABI assumptions, SwiftUI state reset behavior, symbol safety, and generated-host cleanup all need a feasibility prototype before this becomes a supported workflow.

## Proposed MCP and Skill Shape

Do not add plugin metadata until a runnable local app endpoint exists.

Possible read-first MCP tools:

- `get_simulator_bridge_status()`: installation, app reachability, permission state, selected devices, local endpoint, and cleanup state.
- `list_simulator_devices()`: normal available and booted device identities, with Device Hub handoff status when available.
- `get_simulator_frame(udid)`: frame metadata and a local preview reference for an already-authorized bridge.
- `get_preview_host_status(host_id)`: package target, selected UDID, host PID, watched paths, last build, and last reload result.

Possible later action tools:

- `start_simulator_bridge(udid)` and `stop_simulator_bridge(udid)`.
- `send_simulator_input(udid, action)`, only after read-only framing is proven and the confirmation policy covers input with external effects.
- `start_preview_host(package_path, target, udid, preview_filter)` and `stop_preview_host(host_id)`.

The `simulator-browser` skill should route agents to existing Xcode build/run and Device Hub workflows first for ordinary development. It should require explicit device selection, a read-first bridge-status check, a visible frame before success, and scoped cleanup. A future preview-host skill should declare its Swift-Package-only boundary and hand unsupported app-project previews back to Xcode Canvas.

## Implementation Slices

### Slice 1: Evidence and Device Hub Prototype

- Validate the current Device Hub UI, its accessible device identity, and its relationship to `simctl` UDIDs.
- Prototype a read-only local frame path against one explicit booted Simulator.
- Record latency, frame reliability, device-switch behavior, cancellation, stale-helper cleanup, and whether the selected device remains usable in Xcode.
- Stop if the bridge requires app instrumentation, uncontrolled system permissions, or a non-local listener.

### Slice 2: AgentDeck Local Runtime Status

- Add an `AgentDeck` status endpoint that reports Device Hub availability, CoreSimulator device identity, bridge lifecycle, permission state, and precise failure reasons.
- Add only `get_simulator_bridge_status()` to the Socket MCP adapter.
- Keep the plugin without browser or input actions until status is truthful and testable.

### Slice 3: Read-Only Browser Mirror

- Add explicit-UDID start/stop lifecycle with per-device ownership locking.
- Render the selected Simulator in an approved local browser surface.
- Add frame and teardown evidence, plus an end-to-end test that proves the ordinary Simulator remains usable.

### Slice 4: Guarded Interaction

- Add Accessibility- or protocol-backed taps, typing, gestures, rotation, and hardware-button actions only when the exact action semantics are observable.
- Apply the existing desktop-bridge action-time confirmation rules to destructive, representational, permission, upload, and sensitive-data actions.
- Keep browser interaction out of the default path when Xcode, Simulator, or a dedicated app connector is more direct.

### Slice 5: Preview-Host Feasibility

- Create a throwaway fixture Swift Package with small self-contained previews.
- Prototype generated-host build/install/launch and one modified-preview reload.
- Prove a stable host PID, new displayed view, clean repeated reload behavior, and complete cleanup.
- Document unsupported package products, dynamic-library constraints, preview dependencies, and state-reset behavior before exposing the feature.

### Slice 6: Supported Preview Host

- Add the preview-host endpoint, MCP tools, and narrow skill only if Slice 5 has reliable evidence.
- Keep it opt-in, local-only, and explicitly separate from Xcode Canvas and normal app execution.

## Success Criteria

- The browser shows and controls a selected ordinary Simulator, not a special emulator or duplicate app runtime.
- Device selection is explainable through Device Hub and/or an exact CoreSimulator UDID.
- A stopped bridge cannot disrupt another device or another Codex task.
- The first browser transport is local-only and has no hidden tunnel, LAN listener, or external telemetry requirement.
- A supported preview host leaves the user project untouched and can prove a frame change without relaunching its host process.
- Xcode Canvas, Simulator, Device Hub, debugger, and full app runs remain the recommended choices when they better match the task.
