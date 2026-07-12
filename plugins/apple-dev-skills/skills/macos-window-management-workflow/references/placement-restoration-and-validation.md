# Placement, Restoration, and Validation

Use `windowIdealPlacement` to describe an appropriate zoom size or position for the current display and content, not to impose a permanent screen geometry. Let the person resize and move normal windows.

State restoration is a user-controlled system preference on macOS. The default is to respect it. `restorationBehavior(.disabled)` is appropriate only when restoring a window would be transient, misleading, unsafe, or disproportionately expensive.

Validate more than appearance:

- open and close each scene shape;
- move, resize, zoom, minimize, and enter full screen where applicable;
- switch focus between two windows and inspect Window-menu entries;
- relaunch with restoration enabled and disabled;
- confirm the accessible title and keyboard focus remain usable after custom chrome;
- exercise the oldest supported macOS availability path.
