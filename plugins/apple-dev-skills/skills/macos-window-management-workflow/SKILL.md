---
name: macos-window-management-workflow
description: Design, implement, and validate SwiftUI and AppKit macOS window behavior. Use when choosing window scenes, toolbar or title-bar treatment, drag regions, placement, resizing, restoration, document or utility windows, and focused window ownership.
---

# macOS Window Management Workflow

## Purpose

Own concrete macOS window behavior that sits below broad app architecture: scene selection, chrome, drag affordances, sizing, placement, restoration, utility windows, and validation. Keep application-wide ownership and AppKit controller architecture with `swiftui-app-architecture-workflow` and `appkit-app-architecture-workflow`.

## Workflow

1. Identify the window's job: main content, document, settings, inspector, utility, transient activity, or external display. Start from `WindowGroup`, `Window`, `Settings`, or `DocumentGroup`; do not start by hiding the title bar.
2. Define the window's ownership and identity. Give independently openable windows stable scene values and user-facing titles so Window-menu, restoration, and focus behavior remain understandable.
3. Choose the least-custom chrome. Prefer normal title bars and standard toolbars; use `windowToolbarStyle`, `toolbarBackgroundVisibility`, `toolbarVisibility`, or `windowStyle` only to support the window's job.
4. If custom chrome removes a normal drag surface, add `WindowDragGesture` only in a region that does not steal content controls. Use `allowsWindowActivationEvents(true)` only when the window must activate and drag from the same gesture.
5. Treat placement, resizing, and zoom as behavioral contracts. Use scene-level placement APIs only when the content has a real ideal size or position; do not force a fixed geometry that fights user resizing or display changes.
6. Respect state restoration by default. Disable restoration only for a truly transient, expensive, or unsafe-to-reconstruct window, and explain what opens instead on relaunch.
7. Escalate to AppKit only for an actual AppKit-owned requirement such as `NSWindow` behavior, panels, responder-chain menus, or a controller lifecycle that SwiftUI cannot represent cleanly.
8. Validate on the oldest supported macOS plus the current target: launch, open another window, focus switching, resize/zoom, full screen, close/reopen, restoration, VoiceOver title, and Window-menu state.

## Guards

- Do not use borderless or hidden-title-bar styling as a generic design upgrade.
- Do not make an app non-draggable when removing its toolbar background or toolbar.
- Do not replace user restoration preferences with app policy without a concrete transient-window reason.
- Do not push AppKit window-controller ownership into a SwiftUI view just to reach a window property.
- Do not claim Simulator, preview, or screenshot proof covers keyboard focus, restoration, or multiwindow behavior without exercising it.

## References

- `references/window-scene-and-chrome-rules.md`
- `references/placement-restoration-and-validation.md`
