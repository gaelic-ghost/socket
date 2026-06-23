# Setup And Agent Surfaces

Last checked against Apple developer pages and WWDC26 transcripts on 2026-06-22.

## Source Anchors

- Apple Xcode page: https://developer.apple.com/xcode/
- What's new in Xcode: https://developer.apple.com/xcode/whats-new/
- Xcode, agents, and you: https://developer.apple.com/videos/play/wwdc2026/259/
- Meet agentic coding in Xcode: https://developer.apple.com/videos/play/tech-talks/111428/
- Setting up coding intelligence: https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence
- Giving external agents access to Xcode: https://developer.apple.com/documentation/Xcode/giving-external-agents-access-to-xcode

## Stable Surface To Preserve

Xcode is the owner of the coding-assistant UI, model/provider settings, project context, artifact review surfaces, and Xcode tool permissions when an agent is launched inside Xcode.

External agents are different. They run outside Xcode and connect to Xcode through the Xcode-provided Model Context Protocol bridge. Do not describe this as the agent being "inside Xcode" unless Xcode itself launched it.

## Xcode 27 Beta Surface

As of 2026-06-22, Apple's Xcode 27 pages and WWDC26 transcripts describe:

- coding agents started from the Xcode toolbar
- conversations and tasks appearing in editor panes
- a coding-assistant sidebar for parallel conversations and tasks
- plan-mode workflows where the agent can gather context before changing files
- reviewable artifacts for source changes, generated files, previews, screenshots, and other outputs
- Xcode validation tools available to agents, including build, preview, and test workflows
- agent-assisted localization through String Catalogs
- Device Hub as the Xcode 27 surface for simulator and physical-device inspection

Treat these as beta-era Xcode 27 claims until the installed Xcode and current Apple docs confirm the behavior for the target machine.

Local beta tool check on 2026-06-22 verified Xcode 27.0 beta build 27A5194q at `/Users/galew/Applications/Betas/Xcode-beta.app`. The local check verified `xcodebuild -version`, `xcrun --find mcpbridge`, and `xcrun mcpbridge --help`; it did not verify Xcode UI settings, project-session permissions, or agent execution inside a running Xcode session.

When a claim depends on live Xcode UI, an open project, MCP connection state, agent settings, or plug-in import behavior, open the intended Xcode app and inspect the live state. For Gale's Xcode 27 beta work, use `/Users/galew/Applications/Betas/Xcode-beta.app`; for stable work, use `/Applications/Xcode.app`. Use explicit `DEVELOPER_DIR` for matching command-line checks instead of changing global `xcode-select` unless Gale asks for a global switch.

## Surface Classification

Use this split before giving setup advice:

- `xcode-hosted`: Xcode starts the agent or chat provider and owns the assistant UI, artifacts, project context, and permissions.
- `external-mcp`: another client starts the agent and connects to Xcode through `xcrun mcpbridge`.
- `skill-export`: `xcrun mcpbridge run-agent skills export` writes Xcode-visible skill bundles for inspection or setup; keep authored Socket skills as the source of truth unless an import is explicitly requested.
- `chat-provider`: Xcode uses a model provider for code chat or coding tools, but no autonomous agent permission is implied until Xcode documents that path.
- `plugin`: Xcode plug-in packaging or import behavior. Keep this research-first until live Xcode documentation and local inspection verify the package shape.
- `acp`: agent protocol setup. Do not claim Apple-documented ACP setup unless current Apple docs or local Xcode inspection show it.

## Handoff Rule

Setup and permissions stay in this skill. Execution belongs elsewhere:

- build, run, preview, file membership, and project mutation: `xcode-build-run-workflow`
- Swift Testing, XCTest, XCUITest, and `.xctestplan`: `xcode-testing-workflow`
- Apple documentation lookup: `explore-apple-swift-docs`
