# tvOS App-Experience Validation

Plan manual/device evidence separately from code review. A simulator can help
with layout and basic focus exploration, but it cannot establish all hardware
interaction behavior.

| Concern | Evidence |
| --- | --- |
| Initial and restored focus | First launch, navigation return, data reload, and modal dismissal on a real Apple TV where the product depends on remote behavior. |
| Focus geometry | Navigate every cardinal direction through shelves, headers, grids, and empty/error states; verify no clipping, lost focus, or unexpected jumps. |
| Input | Siri Remote Select, Menu/Back, scrub/gesture behavior, and controller paths when claimed. |
| Large Text | Test default and large text sizes; verify readable labels, no clipping, and intentional content-density changes. |
| Accessibility | Check VoiceOver order, focused-state visibility, contrast, RTL where supported, and alternate interaction paths. |
| Platform gate | Record Apple TV model, tvOS/Xcode build, simulator/device status, and GPU/controller evidence. |
| TVMLKit migration | Verify each migrated screen's navigation, data/error state, focus, and accessibility before removing its legacy counterpart. |

Hand runtime UI execution and XCUITest mechanics to `xcode-testing-workflow`.
