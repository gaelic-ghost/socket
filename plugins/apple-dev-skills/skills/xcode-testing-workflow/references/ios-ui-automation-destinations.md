# iOS UI Automation Destinations

Use the same XCUITest target and test-plan configuration on simulators and physical devices where the behavior under test is shared. The destination changes the evidence required; it is not a reason to duplicate ordinary UI-test code.

## Simulator-first coverage

Use a simulated iPhone or iPad as the default destination for fast, repeatable UI automation:

- common navigation, validation, and regression flows
- launch-argument and environment-backed fixtures
- locale, Dynamic Type, appearance, orientation, and accessibility matrices
- deterministic state-reset and broad device-size coverage

Record the simulator identifier, runtime, device model, app build, selected test-plan configuration, and resulting `.xcresult` bundle when the result will be compared or shared. Keep matrix variants in a versioned `.xctestplan` instead of relying on an operator's remembered Simulator settings.

Simulator output is not proof of hardware performance, battery or thermal behavior, physical touch ergonomics, device GPU output, radios, cameras, sensors, push delivery, or background execution. Move the affected scenario to a physical device when any of those conditions is part of the claim.

## Physical-device coverage

Run the smallest focused XCUITest flow on a paired physical device when the behavior depends on hardware or a real device environment. Before the run, confirm the device name, identifier, platform and OS version, pairing/trust state, Developer Mode state, signed app build, scheme, and test-plan configuration.

Use an explicit Xcode destination identifier for command-line execution, rather than selecting a device by display name. Keep the result bundle and failure attachments with the device identity so a simulator result cannot be mistaken for hardware proof.

For a physical-device failure, capture one bounded evidence packet:

1. the test name, app build, test-plan configuration, device identifier, and OS version
2. the failing activity and any XCUITest attachment or `.xcresult` evidence
3. one Device Hub screenshot or video only when it shows the relevant visible state
4. a targeted diagnostic only when it can explain the failure
5. the active Xcode debugger frame, variables, or focused LLDB output when source-level diagnosis is needed

Do not reset, erase, unpair, change Developer Mode, or alter a physical device's configuration as test cleanup unless the user explicitly requested that state change.

## Handoffs

- Use `xcode-device-hub-workflow` to inspect, interact with, capture from, or collect diagnostics from the selected simulator or physical device.
- Use `xcode-debugger-mcp-workflow` for a running app with a source-level failure. Its active Xcode-session route is the normal debugger path for both simulator and physical-device runs.
- Use `ios-runtime-forensics-workflow` only for its simulator-owned ETTrace and memory-graph evidence. Capture performance, thermal, battery, and hardware GPU claims on a physical device with the appropriate Xcode or Instruments workflow instead.

## Apple documentation

- [Testing in Simulator versus testing on hardware devices](https://developer.apple.com/documentation/xcode/testing-in-simulator-versus-testing-on-hardware-devices)
- [Running your app on simulated or physical devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices)
- [Testing](https://developer.apple.com/documentation/xcode/testing)
