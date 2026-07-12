# Device Hub Scope and Evidence

Apple's Xcode documentation checked through Xcode DocumentationSearch on 2026-07-12 describes Device Hub as the surface that manages simulated and physical devices used as Xcode run destinations. Its compact view opens when an app runs on a simulator; the expanded view separates a sidebar, device canvas, and inspector.

- The inspector exposes device details such as name, operating-system version, and device identifier, and can download diagnostics.
- Device Hub can change simulated-device environment settings including Appearance, Liquid Glass, and Text Size, and supports simulated-iPhone resize mode.
- Device Hub interaction controls can drive an app on a selected simulated or physical device. A physical device remains its own hardware target; the Device Hub view is not a simulator substitute.
- Device Hub screenshots are saved at the target device's full resolution. Treat captures as potentially sensitive artifacts.

Sources read through Xcode-local documentation:

- `doc://com.apple.documentation/documentation/Xcode/device-hub`
- `doc://com.apple.documentation/documentation/Xcode/interacting-with-your-app-in-device-hub`
- `doc://com.apple.documentation/documentation/Xcode/configuring-the-environment-of-a-simulated-device`
- `doc://com.apple.documentation/documentation/Xcode/capturing-screenshots-and-videos-from-devices`
