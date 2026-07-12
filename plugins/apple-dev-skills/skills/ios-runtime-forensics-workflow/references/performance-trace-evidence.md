# Performance Trace Evidence

Define a narrow start and stop boundary before capturing. Record simulator UDID, OS, Xcode version, app build, build configuration, workload fixture, trace duration, and symbol source. Keep the capture focused on one launch or interaction.

Interpret only symbolicated evidence. A hot stack can show where samples occurred; it does not alone prove user-visible latency, memory ownership, or the correct remediation. Repeat the same flow after a change before calling the result an improvement.
