# Validation And Handoffs

Session code can be reviewed statically, but route, Bluetooth, AirPlay, microphone, interruption, and speaker behavior usually needs live validation.

Use `xcode-build-run-workflow` when the next step is:

- adding or checking `Info.plist` privacy strings
- checking entitlements or background modes
- running on simulator or device
- collecting Console, Xcode, or device logs
- verifying route behavior with physical accessories

Use `xcode-testing-workflow` when the next step is:

- designing regression tests around permission-state branching
- testing notification handlers with injected notification payloads
- guarding policy selection helpers

Manual validation gaps to report plainly:

- phone-call, system-alert, and route-change behavior without a device
- Bluetooth HFP, Bluetooth A2DP, AirPlay, USB audio, or wired headphones without the accessory
- microphone permission prompts after the system has already remembered the user's answer
