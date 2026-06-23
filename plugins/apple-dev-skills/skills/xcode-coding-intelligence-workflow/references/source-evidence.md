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
DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer xcodebuild -version
DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer xcrun --find mcpbridge
DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer xcrun mcpbridge --help
xcodebuild -version
xcrun mcpbridge --help
```

Observed beta Xcode version: Xcode 27.0, build 27A5194q.

Observed beta `mcpbridge` path:

```text
/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer/usr/bin/mcpbridge
```

Earlier default-developer-dir check observed Xcode 26.5, build 17F42.

Observed `mcpbridge` behavior:

- default mode is a STDIO bridge for Xcode MCP tools
- `run-agent <agent-name>` launches a coding agent with Xcode-provided configuration
- `--dry-run` prints the resolved command without executing
- `--no-xcode-tools` omits Xcode MCP tools from agent config
- `MCP_XCODE_PID` selects a specific Xcode process
- `MCP_XCODE_SESSION_ID` identifies an Xcode tool session

## Unverified Or Research-Only

- ACP-specific Xcode setup: no current Apple page found in this pass that made ACP the documented Xcode setup surface. Mention ACP only as unresolved or when live Xcode documentation proves it.
- Xcode 27 beta external-agent permission toggles, project-session behavior, and live agent execution were not verified here.

## Checked 2026-06-23

### Local Xcode 27 Beta Live App Probe

Checked with Xcode 27 beta running from:

```text
/Users/galew/Applications/Betas/Xcode-beta.app
```

The matching beta developer directory and Xcode process were selected explicitly:

```bash
DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer MCP_XCODE_PID=59740 xcrun mcpbridge run-agent --dry-run codex
DEVELOPER_DIR=/Users/galew/Applications/Betas/Xcode-beta.app/Contents/Developer MCP_XCODE_PID=59740 xcrun mcpbridge run-agent codex skills export --output-dir /private/tmp/socket-xcode-plugin-fixture/after-file-import-skills --replace-existing
```

Observed live beta behavior:

- `run-agent --dry-run codex` resolved Xcode's Codex executable under `~/Library/Developer/Xcode/CodingAssistant/Agents/XcodeVersions/27A5194q/codex/codex`.
- The Xcode-provided environment included `CODEX_HOME=/Users/galew/Library/Developer/Xcode/CodingAssistant/codex` and `MCP_XCODE_PID=59740`.
- The dry run reported the beta Xcode process id and a signed `codex` executable.
- The beta-scoped Codex runtime launched through `run-agent codex`, but `codex skills export` failed with `unrecognized subcommand 'export'`.

### Local Xcode 27 Beta Plug-in Import Probe

Checked through Xcode Beta Settings > Intelligence > Plug-ins.

Observed Add Plug-in choices:

- Import from Claude Code
- Import from Codex
- Add from file
- Add from URL

Observed UI description:

```text
Plug-ins extend Xcode's agentic Intelligence features with skills, subagent definitions, hooks, and MCP servers.
```

Observed import behavior:

- `Import from Codex` listed installed Codex plug-ins and imported `apple-dev-skills` as `6 Skills - Hooks`.
- `Add from file` accepted a local fixture folder containing `.codex-plugin/plugin.json`, `skills/socket-xcode-fixture-skill/SKILL.md`, and `.mcp.json`, then installed it as `1 Skill - 1 MCP Server`.
- `Add from URL` asked for the URL of a Git repository containing plug-ins, skills, or MCP servers.
- `Add from URL` rejected `file:///private/tmp/socket-xcode-plugin-fixture/socket-xcode-fixture` as invalid.
- `Add from URL` accepted `https://github.com/gaelic-ghost/socket.git` and enumerated Socket child plug-ins from the public repository before import. No additional Socket child plug-ins were imported from this URL during the probe.

Observed artifacts after import:

- Xcode registered imported plug-ins in `~/Library/Developer/Xcode/CodingAssistant/AgentPlugins/PluginsManifest.json`.
- Xcode copied plug-in payloads into `~/Library/Developer/Xcode/CodingAssistant/AgentPlugins/<plugin>/`.
- Xcode generated a normalized `plugin.json` with fields such as `id`, `importedAt`, `importSource`, `skills`, and `mcpServers`.
- Xcode copied imported plug-ins into `~/Library/Developer/Xcode/CodingAssistant/codex/plugins/cache`.
- Xcode enabled imported plug-ins in `~/Library/Developer/Xcode/CodingAssistant/codex/config.toml`.
- Xcode copied imported plug-ins into `~/Library/Developer/Xcode/CodingAssistant/gemini/.gemini/extensions`.
- Xcode wrote MCP declarations from imported `.mcp.json` files into `~/Library/Developer/Xcode/CodingAssistant/mcp-servers.json`.

Setup lesson:

- A closed or unselected Xcode app is not enough reason to block an Xcode Intelligence task. Open the intended stable or beta Xcode app, select it with `MCP_XCODE_PID` when multiple Xcode processes may exist, and then retry the bridge check.
- Keep Xcode-generated and Xcode-copied files as local evidence and comparison input. Do not copy them into authored Socket skill roots unless a separate import or adaptation task explicitly chooses that source-of-truth change.
