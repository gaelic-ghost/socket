# macOS UI-Test Permission Ownership

## Purpose

Diagnose and minimize recurring macOS privacy prompts by identifying the exact operation and responsible executable before changing test code, entitlements, or Privacy & Security settings. A build script, Xcode test host, UI-test runner, helper, Debug build product, and installed Release app are separate actors; do not infer a shared permission state from their shared source repository.

## Attribution Record

Before changing permissions or rerunning a prompt-heavy scenario, record:

1. launcher: shell script, `xcodebuild`, Xcode, test plan, or another tool;
2. responsible executable: path, bundle identifier, Team ID, signing state, and build location;
3. launched or restored target: test-owned build product, installed app, helper, or external app;
4. protected operation and target resource: App Group/container data, protected folder, Accessibility, Automation, microphone, or another actual privacy class;
5. triggering API or command: `XCUIApplication.launch()`, `open`, `NSWorkspace`, helper IPC, direct file access, or another concrete operation; and
6. test configuration: test plan, environment variables, launch arguments, and whether the scenario is ordinary or opt-in prompt-heavy coverage.

Do not treat a usage description, entitlement, sandbox capability, build flag, coverage option, result-bundle option, or a generic prompt string as proof of which executable requested access.

## Default Test Path

- Keep ordinary tests inside the test-owned Debug product and its test-specific storage. Prefer temporary paths or ignored repo-local artifacts; avoid Desktop, Documents, Downloads, home-directory roots, production App Groups, and user-selected folders unless the access behavior is the subject under test.
- Launch the product under test through the test framework's normal launch path. Do not use `open`, `NSWorkspace`, or a wrapper script to restore a separately installed app as routine cleanup after a test run.
- Keep protected setup and assertions in the product or helper that owns the user-facing permission. Do not make the Xcode test host perform Accessibility, Automation, or protected-data operations merely to arrange or inspect the scenario.
- Treat installation, verification, launch, termination, and restoration as distinct operations. A test that needs an installed artifact or external app is an explicit integration scenario, not a normal build/test side effect.

## Prompt-Heavy Integration Path

Use a dedicated, versioned `.xctestplan` configuration with an explicit environment gate for a scenario that genuinely needs a real app, helper, Accessibility, Automation, protected data, or a visible prompt. Keep it disabled from ordinary local and CI runs unless the test plan intentionally enables it.

Before running it, state the exact visible action and expected prompt owner. After it, report the responsible executable, protected operation, test-plan configuration, observed prompt or denial, and whether the normal test path stayed prompt-free. If the operation belongs to a helper or installed product, test it through that product boundary rather than granting broad authority to Xcode, the terminal, or an agent host.

## Escalation Boundary

Use `macos-privacy-permissions-workflow` when the responsible executable, privacy class, signed artifact, or user-consent state is unclear. Use `diagnose-apple-entitlements` when tracked entitlements, embedded profiles, final signed code, and runtime behavior disagree.

Do not reset permissions, automate System Settings, edit TCC state, grant Full Disk Access, or add a stable testing helper merely because ordinary test scripts launch or restore the wrong app. First remove that accidental launch path and prove whether a protected operation remains.
