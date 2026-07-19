# Setup And Agent Surfaces

Last checked against Apple developer pages and Xcode release notes on 2026-07-19.

## Source Anchors

- Apple Xcode page: https://developer.apple.com/xcode/
- What's new in Xcode: https://developer.apple.com/xcode/whats-new/
- Xcode, agents, and you: https://developer.apple.com/videos/play/wwdc2026/259/
- Meet agentic coding in Xcode: https://developer.apple.com/videos/play/tech-talks/111428/
- Setting up coding intelligence: https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence
- Giving external agents access to Xcode: https://developer.apple.com/documentation/Xcode/giving-external-agents-access-to-xcode
- Xcode 26.6 release notes: https://developer.apple.com/documentation/xcode-release-notes/xcode-26_6-release-notes

## Stable Surface To Preserve

Xcode is the owner of the coding-assistant UI, model/provider settings, project context, artifact review surfaces, and Xcode tool permissions when an agent is launched inside Xcode.

External agents are different. They run outside Xcode and connect to Xcode through the Xcode-provided Model Context Protocol bridge. Do not describe this as the agent being "inside Xcode" unless Xcode itself launched it.

ACP-hosted agents are a third explicit path. Xcode is the ACP client and owns
the conversation UI, project context, and Xcode-side permissions while the
launched agent executable owns its runtime, authentication, model, native
configuration, and supported ACP capabilities. Apple documents adding an ACP
agent in Coding Intelligence settings, and Xcode 26.6 release notes record ACP
support. Keep the agent's generic launch/handshake diagnosis in Agent
Portability Skills.

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

Local beta tool check on 2026-06-22 verified Xcode 27.0 beta build 27A5194q at the then-installed beta app path. The local check verified `xcodebuild -version`, `xcrun --find mcpbridge`, and `xcrun mcpbridge --help`; it did not verify Xcode UI settings, project-session permissions, or agent execution inside a running Xcode session.

When a claim depends on live Xcode UI, an open project, MCP connection state, agent settings, or plug-in import behavior, open the intended Xcode app and inspect the live state. For command-line checks, use the Xcode toolchain Gale selected through `xcode-select`; do not override it with `DEVELOPER_DIR`. If Gale asks to change CLI toolchains, use `xcode-select --switch`, verify the selected path and tool versions, and preserve the selection Gale requested.

## Surface Classification

Use this split before giving setup advice:

- `xcode-hosted`: Xcode starts the agent or chat provider and owns the assistant UI, artifacts, project context, and permissions.
- `acp-hosted`: Xcode launches an ACP agent and renders it in Xcode; validate the agent executable and ACP behavior separately from Xcode's permissions and tools.
- `external-mcp`: another client starts the agent and connects to Xcode through `xcrun mcpbridge`.
- `plugin-import`: Xcode Settings > Intelligence > Plug-ins imports plug-ins, skills, hooks, and MCP servers from installed agent state, a local folder, or a remote Git URL; keep authored Socket skills as the source of truth unless an import or adaptation is explicitly requested.
- `chat-provider`: Xcode uses a model provider for code chat or coding tools, but no autonomous agent permission is implied until Xcode documents that path.
- `plugin`: Xcode plug-in packaging or import behavior. The import path is verified in Xcode 27 beta, but runtime behavior for hooks, MCP commands, and non-skill components still needs targeted validation.
- `acp`: shared editor-agent protocol implementation. Xcode owns its client setup; Agent Portability Skills owns generic ACP operation and development.

## Handoff Rule

Setup and permissions stay in this skill. Execution belongs elsewhere:

- build, run, preview, file membership, and project mutation: `xcode-build-run-workflow`
- Swift Testing, XCTest, XCUITest, and `.xctestplan`: `xcode-testing-workflow`
- Apple documentation lookup: `explore-apple-swift-docs`
- existing ACP launch or handshake diagnosis: `agent-portability-skills:operate-acp-agent-integration`
- ACP server implementation: `agent-portability-skills:build-acp-agent`
