# Source Evidence

This reference records the first practical source set for the Xcode 27 coding-intelligence workflow.

## Checked 2026-06-22

### Apple Developer

- Xcode overview: https://developer.apple.com/xcode/
- What's new in Xcode: https://developer.apple.com/xcode/whats-new/
- Setting up coding intelligence: https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence
- Giving external agents access to Xcode: https://developer.apple.com/documentation/Xcode/giving-external-agents-access-to-xcode
- Writing code with intelligence in Xcode: https://developer.apple.com/documentation/Xcode/writing-code-with-intelligence-in-xcode
- Localizing your app using agents: https://developer.apple.com/documentation/Xcode/localizing-your-app-using-agents
- Device Hub: https://developer.apple.com/documentation/Xcode/device-hub

Some Apple documentation pages are JavaScript-rendered. When a page body is not available to the agent, use the Apple page URL as an existence anchor and pair behavior claims with an Apple page that exposes readable transcript text or with local Xcode tool output.

### Apple Videos

- Meet agentic coding in Xcode: https://developer.apple.com/videos/play/tech-talks/111428/
- What's new in Xcode 27: https://developer.apple.com/videos/play/wwdc2026/258/
- Xcode, agents, and you: https://developer.apple.com/videos/play/wwdc2026/259/
- Translate your app using agents in Xcode: https://developer.apple.com/videos/play/wwdc2026/213/
- Get the most out of Device Hub: https://developer.apple.com/videos/play/wwdc2026/260/

### Local Xcode Tool Output

Checked with:

```bash
xcodebuild -version
xcrun mcpbridge --help
```

Observed local Xcode version: Xcode 26.5, build 17F42.

Observed `mcpbridge` behavior:

- default mode is a STDIO bridge for Xcode MCP tools
- `run-agent <agent-name>` launches a coding agent with Xcode-provided configuration
- `--dry-run` prints the resolved command without executing
- `--no-xcode-tools` omits Xcode MCP tools from agent config
- `MCP_XCODE_PID` selects a specific Xcode process
- `MCP_XCODE_SESSION_ID` identifies an Xcode tool session

## Unverified Or Research-Only

- ACP-specific Xcode setup: no current Apple page found in this pass that made ACP the documented Xcode setup surface. Mention ACP only as unresolved or when live Xcode documentation proves it.
- Xcode plug-in package shape: keep blocked until live Xcode 27 beta inspection verifies import/package details.
- Xcode 27 beta behavior on Gale's machine: this branch was authored from a machine with Xcode 26.5 installed, so local Xcode 27 behavior was not verified here.
