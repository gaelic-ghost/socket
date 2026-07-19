# Xcode 27 Agentic Tooling Skill Plan

Current bundle check: 2026-07-19, Xcode 27.0 beta build 27A5218g. Live import
and bridge behavior in this document was last exercised on 2026-06-23 unless a
later note says otherwise.

This plan records the first Socket pass for supporting Xcode 27 beta-era coding intelligence inside the existing `apple-dev-skills` plugin.

The goal is to add practical Apple and Xcode workflows without creating a separate beta plugin yet. Keep generic ACP operation and development in Agent Portability Skills while this plan owns Xcode's documented ACP client setup, permissions, and tools.

## Current Recommendation

Add Xcode 27 support to `plugins/apple-dev-skills` as a small set of focused workflow skills plus updates to existing SwiftUI, AppKit, UIKit, Icon Composer, build, and testing guidance.

Do not create an `apple-dev-beta` plugin yet. A separate beta plugin becomes useful only if Socket needs to ship beta-only helper tools, unstable MCP servers, sample Xcode plug-ins, or other surfaces that normal Apple Dev Skills users should not install by default.

Do not make ACP itself an Apple Dev Skills owner surface. ACP is editor-agent infrastructure shared across Xcode, Zed, and other clients. Apple Dev Skills should mention ACP only where Xcode's own setup flow requires it.

## Source Evidence

Official Apple documentation checked on 2026-06-09:

- [Xcode updates](https://developer.apple.com/documentation/Updates/Xcode)
- [Setting up coding intelligence](https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence)
- [Giving external agents access to Xcode](https://developer.apple.com/documentation/Xcode/giving-external-agents-access-to-xcode)
- [Extending and customizing agents](https://developer.apple.com/documentation/Xcode/extending-and-customizing-agents)
- [Writing code with intelligence in Xcode](https://developer.apple.com/documentation/Xcode/writing-code-with-intelligence-in-xcode)
- [Using coding intelligence in the source editor](https://developer.apple.com/documentation/Xcode/using-coding-intelligence-in-the-source-editor)
- [Localizing your app using agents](https://developer.apple.com/documentation/Xcode/localizing-your-app-using-agents)
- [Device Hub](https://developer.apple.com/documentation/Xcode/device-hub)
- [Downloading and installing additional Xcode components](https://developer.apple.com/documentation/Xcode/downloading-and-installing-additional-xcode-components)
- [SwiftUI updates](https://developer.apple.com/documentation/Updates/SwiftUI)
- [UIKit updates](https://developer.apple.com/documentation/Updates/UIKit)
- [AppKit updates](https://developer.apple.com/documentation/Updates/AppKit)
- [Agent Client Protocol](https://agentclientprotocol.com/)

Refresh checked on 2026-06-22:

- [Xcode](https://developer.apple.com/xcode/)
- [What's new in Xcode](https://developer.apple.com/xcode/whats-new/)
- [What’s new in Xcode 27](https://developer.apple.com/videos/play/wwdc2026/258/)
- [Xcode, agents, and you](https://developer.apple.com/videos/play/wwdc2026/259/)
- [Meet agentic coding in Xcode](https://developer.apple.com/videos/play/tech-talks/111428/)
- [Translate your app using agents in Xcode](https://developer.apple.com/videos/play/wwdc2026/213/)
- [Get the most out of Device Hub](https://developer.apple.com/videos/play/wwdc2026/260/)
- Local `xcodebuild -version` and `xcrun mcpbridge --help` output from Xcode 26.5 build 17F42.

Live beta probe checked on 2026-06-23:

- Xcode 27 beta was opened from the then-installed beta app path.
- The matching beta `DEVELOPER_DIR` plus `MCP_XCODE_PID=59740 xcrun mcpbridge run-agent --dry-run codex` resolved Xcode's beta-scoped Codex executable and `CODEX_HOME`.
- The matching beta `DEVELOPER_DIR` plus `MCP_XCODE_PID=59740 xcrun mcpbridge run-agent codex skills export --output-dir /private/tmp/socket-xcode-plugin-fixture/after-file-import-skills --replace-existing` launched Xcode's beta-scoped Codex runtime, but that runtime reported `unrecognized subcommand 'export'`. Treat `skills export` as unusable from this Codex runtime until a later beta proves otherwise.
- Xcode Beta Settings > Intelligence > Plug-ins was inspected through the official UI. The Add Plug-in sheet exposed `Import from Claude Code`, `Import from Codex`, `Add from file`, and `Add from URL`.
- `Import from Codex` imported the installed `apple-dev-skills` plugin as `6 Skills - Hooks`.
- `Add from file` imported a harmless fixture folder containing `.codex-plugin/plugin.json`, `skills/<name>/SKILL.md`, and `.mcp.json` as `1 Skill - 1 MCP Server`.
- `Add from URL` rejected a local `file://` Git URL as invalid, but accepted `https://github.com/gaelic-ghost/socket.git` and enumerated Socket child plug-ins from the public repository before import.

Live-app setup note: do not treat "Xcode is not running" as a final blocker for Xcode Intelligence, MCP, or plug-in inspection work. Open the intended stable or beta Xcode app, select the intended process with `MCP_XCODE_PID` when needed, and retry the check before reporting a blocker.

Refresh note, 2026-07-19: Apple now documents Add an Agent for ACP-compatible
agents in Setting up coding intelligence, and Xcode 26.6 release notes state
that Xcode adds ACP support. Keep each individual agent's runtime behavior
unverified until its executable, authentication, capabilities, sessions, and
Xcode-side permissions are exercised.

Important current Xcode 27 signals:

- Xcode integrates coding intelligence directly into the workspace, including conversations, transcript panes, artifacts panes, plan mode, source-editor coding tools, generated fixes, previews, playgrounds, and rollback through conversation history.
- Xcode Intelligence settings expose agents, chat providers, Model Context Protocol settings, Xcode plug-ins, command/tool permissions, and Xcode-only agent configuration folders.
- Xcode can add agents that support the Agent Client Protocol.
- External agents can use Xcode capabilities through Xcode's MCP server after enabling external-agent access and configuring `xcrun mcpbridge`.
- Xcode-hosted agents can use built-in Xcode guidance and skills.
- Xcode can assist with localization by adding languages, updating string catalogs, translating strings, and setting machine-translation state.
- Device Hub is now the central Xcode surface for simulated and physical device interaction, environment inspection, pairing, screenshots, videos, and diagnostics.
- Xcode 27 beta can provide a beta-scoped Codex runtime through `xcrun mcpbridge run-agent` when the beta app is running and selected explicitly.
- Xcode 27 beta can import Socket-shaped plug-ins through its official Plug-ins UI from installed Codex state, a local folder, or a remote Git URL.

## Proposed Skill Surfaces

### 1. `xcode-coding-intelligence-workflow`

This should be the first new skill.

Job:

- Help an agent set up and reason about Xcode Intelligence.
- Distinguish Xcode-hosted agents from external agents using Xcode through MCP.
- Route build, run, and test execution back to existing `xcode-build-run-workflow` and `xcode-testing-workflow` instead of duplicating them.
- Explain privacy, project context, permission, and command/tool approval consequences in plain language.

Scope:

- Enable or inspect Xcode Intelligence settings.
- Configure ChatGPT in Xcode, Claude, other Chat Completions-compatible chat providers, and ACP agents at a conceptual workflow level.
- Configure external agents with `xcrun mcpbridge`, including the documented Codex command:

  ```bash
  codex mcp add xcode -- xcrun mcpbridge
  ```

- Verify external-agent access is enabled before expecting MCP tools to work.
- Require the relevant Xcode project to be open in Xcode before relying on Xcode MCP capabilities.
- Open the intended stable or beta Xcode app before declaring live Xcode Intelligence or MCP setup blocked by missing app state.
- Explain Xcode-only agent configuration homes:

  ```text
  ~/Library/Developer/Xcode/CodingAssistant/ClaudeAgentConfig
  ~/Library/Developer/Xcode/CodingAssistant/codex
  ~/Library/Developer/Xcode/CodingAssistant/gemini
  ```

- Track the difference between normal Codex config and Xcode-launched Codex config.
- Hand off broader agent configuration sync to `agentdeck` once that plugin exposes a supported bridge/status surface.

Non-goals:

- Do not implement a custom ACP agent.
- Do not implement a custom Xcode MCP server.
- Do not replace Xcode's own coding assistant UI documentation.
- Do not mutate global Codex or Xcode config without explicit user intent.

### 2. `xcode-agent-plugin-workflow`

This should be research-first and conservative.

Job:

- Help maintainers inspect and package Xcode agentic coding plug-ins only after the live Xcode 27 beta import surface is understood.
- Prevent accidental claims that Codex plugin marketplace packaging and Xcode plug-in packaging are the same thing.

Scope:

- Document how Xcode says plug-ins can contain subagents, MCP servers, and skills.
- Inspect the Xcode plug-in import UI and any exported or documented package shape before authoring a plugin.
- Decide whether a Socket child plugin can also be distributed as an Xcode plug-in, or whether Xcode needs a separate package output.
- Keep plugin installation, trust, permissions, and uninstall guidance explicit.

Non-goals:

- Do not invent an Xcode plug-in manifest format.
- Do not add a second packaging layer to Socket until a concrete Xcode import shape is verified.
- Do not make a beta-only distribution promise before local install testing works.

### 3. `xcode-localization-workflow`

Job:

- Guide durable Xcode String Catalog localization from preparation through review, with agent-assisted translation as an optional Xcode 27 beta-era path.

Scope:

- Add and organize catalogs, languages, and regions through Xcode's stable localization surfaces.
- Update string catalogs by building the project where Xcode requires it.
- Use `Text`, `String(localized:)`, `AttributedString(localized:)`, `LocalizedStringResource`, and owning resource bundles when strings are missed or cross module boundaries.
- Cover source comments, glossary terms, non-translatable strings, tone, region, audience, plurals, device variants, generated symbols, and locale-aware formatting before translation.
- Preserve or create project translation guidance such as `TRANSLATION.md`.
- Track glossary terms, non-translatable strings, tone, region, and audience.
- Explain that Xcode marks generated translations as machine translated in string catalogs and XLIFF exports.
- Require review by people fluent in the target languages and regions before shipping.
- Route visual fit, Dynamic Type, right-to-left layout, previews, simulator, and physical-device checks through existing UI, build, and test workflows.

Non-goals:

- Do not claim machine translation is release-ready without human review.
- Do not flatten translation guidance into generic AGENTS content when a dedicated project translation file is clearer.

### 4. `xcode-device-hub-workflow`

Job:

- Help agents and maintainers use Device Hub for simulator and physical-device workflow decisions.

Scope:

- Choose simulated versus physical devices based on feature needs.
- Configure simulator environments.
- Pair and inspect physical devices.
- Interact with app screens in Device Hub.
- Capture screenshots and videos.
- Download diagnostics and route findings into debugging or test workflows.
- Coordinate with Xcode components and runtime installation when a required platform is missing.

Non-goals:

- Do not replace existing simulator build/run/test workflows.
- Do not automate physical-device actions without explicit user permission and a visible device state.

### 5. `apple-beta-docs-triage-workflow`

Job:

- Provide a repeatable beta-docs pass for new Apple beta drops.

Scope:

- Identify the beta target: Xcode version, OS version, SDK, framework, and date checked.
- Prefer Xcode-local docs, Dash, and official Apple documentation before community sources.
- Separate shipped stable guidance from beta-only notes.
- Record availability gates, SDK requirements, migration risks, and doc uncertainty.
- Decide whether the finding belongs in an existing skill, a new skill, a roadmap note, or no action.
- Require local Xcode or SDK verification before claiming a tool exists on Gale's machine.

Non-goals:

- Do not turn every beta API into a new skill.
- Do not claim future GM behavior from beta documentation.
- Do not treat rumors or screenshots as enough evidence for repo guidance.

## Existing Skills To Update

### `xcode-build-run-workflow` and `xcode-testing-workflow`

Current state:

- These skills already reference Xcode-owned MCP tools exposed through `xcrun mcpbridge`.

Updates:

- Link to `xcode-coding-intelligence-workflow` for setup and permission work.
- Keep tool execution guidance focused on build, run, test, logs, destinations, and diagnostics.
- Refresh MCP tool matrices against the live Xcode 27 beta bridge once installed locally.

### `swiftui-ui-patterns`

Add Xcode 27 SwiftUI guidance for:

- `@State` macro behavior when built with Xcode 27 or later.
- `ContentBuilder` as the unified replacement for type-specific builders where applicable.
- Reorderable containers.
- Custom swipe actions in non-list containers.
- Toolbar visibility priorities, overflow menus, pinned trailing placement, and minimize behavior.
- URL-backed document read/write APIs.
- `AsyncImage` request and URL session support.
- Gesture input kinds.
- Optional item and error alert or confirmation-dialog overloads.

### `swiftui-liquid-glass`

Keep the skill focused on Liquid Glass, but add Xcode 27 notes where they affect:

- Icon Composer preview behavior.
- Toolbar behavior that changes Liquid Glass composition.
- Migration decisions between 2025 Liquid Glass APIs and newer Xcode 27 UI APIs.

### AppKit Guidance

Update AppKit architecture and interop guidance for:

- `NSControl.Events`.
- Drag initiation from gesture recognizers.
- Sidecar touch gesture-recognizer support.
- `NSRefreshController` and touch scrolling in scroll views.
- Observation tracking in AppKit views.
- Gesture recognizer Info.plist keys.
- SwiftUI `GestureInputKinds` in mixed AppKit/SwiftUI apps.

### UIKit Guidance

Add or update UIKit-oriented Apple Dev Skills guidance for:

- iOS 27 scene-based lifecycle requirement for apps built with the latest SDK.
- Sensor data alignment with UI orientation.
- Observation-tracked compositional layouts.
- Mac Catalyst support updates for `UIRefreshControl` and `UIStepper`.
- Drag initiation timing in gesture-rich views.
- Text view viewport and attachment reuse improvements.

If there is no current UIKit owner skill, capture this as a future Apple Dev Skills skill candidate instead of burying it in SwiftUI guidance.

### `icon-composer-app-icon-workflow`

Update with Xcode 27 Icon Composer notes for:

- Refraction strength.
- Highlight alignment.
- Previewing icons in previous OS releases.

## Implementation Slices

### Slice 1: Planning And Metadata

- Add this plan to Socket maintainer docs.
- Add roadmap/TODO entries for the first implementation pass.
- Do not change installable plugin metadata yet.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
```

### Slice 2: First Skill

- [x] Add `plugins/apple-dev-skills/skills/xcode-coding-intelligence-workflow/SKILL.md`.
- [x] Add `plugins/apple-dev-skills/skills/xcode-coding-intelligence-workflow/agents/openai.yaml`.
- [x] Add concise references for setup, MCP bridge routing, Xcode-only config homes, and permission boundaries.
- [x] Update Apple Dev Skills metadata to advertise the new skill.
- [x] Update existing Xcode build/test skills to route setup questions to this skill.

Completed on 2026-06-22 with the first practical setup and permission workflow. Xcode 27 claims are dated beta-era claims, and local `mcpbridge` behavior is recorded separately from Xcode 27 behavior because this authoring machine had Xcode 26.5 installed.

Updated on 2026-06-23 after a live Xcode 27 beta probe. The beta app produced confirmed `run-agent --dry-run codex` evidence through the then-used beta toolchain selection plus `MCP_XCODE_PID`. A direct `codex skills export` attempt through Xcode's beta-scoped Codex runtime failed, so Xcode plug-in support should use the official Plug-ins UI import paths instead of bridge-based skill export. This is historical evidence, not current command guidance; current workflows select Apple command-line toolchains through `xcode-select` rather than injecting `DEVELOPER_DIR`.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
uv run pytest
```

### Slice 3: Localization And Device Hub

- Add `xcode-localization-workflow` as a stable catalog-first workflow with optional agent-assisted translation.
- Add `xcode-device-hub-workflow`.
- Update plugin metadata and Apple Dev Skills roadmap.
- Add handoff notes from build/test/UI skills.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
uv run pytest
```

### Slice 4: Beta Docs Triage And Framework Updates

- Add `apple-beta-docs-triage-workflow`.
- Refresh SwiftUI, AppKit, UIKit, and Icon Composer guidance with Xcode 27 beta-specific notes.
- Keep every beta claim dated and source-linked.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
uv run pytest
```

### Slice 5: Xcode Plug-In Research

- [x] Use a harmless fixture before trying to package Socket itself. The fixture contained one skill and one inert MCP server declaration.
- [x] Record whether Xcode accepts a Git URL, local file, archive, or manifest URL, and whether it writes Codex, Gemini, or Xcode-native configuration.
- Add `xcode-agent-plugin-workflow` after this evidence is shaped into a maintainer workflow and install support assessment.
- Keep writer behavior behind a dry-run assessment before generating or applying any user-home config.
- Do not treat local Xcode binary strings as a public schema. They are useful probe hints only.

Observed import behavior:

- Xcode accepts a local folder through `Add from file`.
- Xcode rejects a local `file://` Git URL through `Add from URL`.
- Xcode accepts the public Socket GitHub URL through `Add from URL` and enumerates child plug-ins before import.
- Xcode writes imported plug-ins to `~/Library/Developer/Xcode/CodingAssistant/AgentPlugins`.
- Xcode mirrors imported payloads into `~/Library/Developer/Xcode/CodingAssistant/codex/plugins/cache` and `~/Library/Developer/Xcode/CodingAssistant/gemini/.gemini/extensions`.
- Xcode writes MCP server declarations from imported `.mcp.json` files into `~/Library/Developer/Xcode/CodingAssistant/mcp-servers.json`.

### Slice 6: Xcode-Visible Skill Comparison

- Compare the exported Xcode-visible skills against existing Socket Apple Dev Skills.
- Decide whether any Xcode 27 beta guidance should be copied into Socket-authored references, summarized with Apple source links, or left as Xcode-owned built-in expertise.
- Keep Socket's authored skills independent from the local export directory unless a later task explicitly approves an import path.
- Keep this slice blocked until an actual Xcode-visible skill export path works. The 2026-06-23 beta-scoped Codex runtime did not support `codex skills export`.

### Slice 7: Socket-To-Xcode Install Assessment

- Inventory Socket child plugins by component type: skills, MCP servers, hooks, apps, and `agents/openai.yaml`.
- For each plugin, classify support for:
  - Xcode-launched Codex through `~/Library/Developer/Xcode/CodingAssistant/codex`
  - Xcode internal agents through the Xcode Plug-ins UI
  - external agents using `xcrun mcpbridge`
- Treat skill-only plugins as likely first candidates for Xcode internal-agent support.
- Treat local MCP plugins as requiring path, dependency, authentication, and permission handling before they can be full-fidelity Xcode plug-ins.
- Treat hooks as recognized by import but execution-unverified until a follow-up probe confirms behavior.
- Treat Codex apps and OpenAI custom-agent metadata as non-portable until Xcode exposes matching component contracts.
- The read-only source assessment is now implemented by `uv run scripts/audit_xcode_plugin_compatibility.py`; use its `likely`, `partial`, `blocked`, and `unknown` queue before choosing live import targets.

## Open Questions

- Which Socket child plug-ins can be imported from the public Git URL with full runtime behavior, not just recognized metadata?
- Can one authored skill surface be packaged for both Codex and Xcode, or does Xcode require a separate distribution artifact?
- Should Xcode-launched Codex config sync remain entirely in `agentdeck`, with Apple Dev Skills only describing the Xcode side?
- Should Socket ship a dedicated Xcode plug-in artifact per child plugin, a generated aggregate Xcode manifest, or only a dry-run/apply adapter for Xcode-launched Codex until Apple's plug-in schema is public?
- Which Apple Dev Skills workflow should own UIKit guidance if UIKit-specific beta changes keep accumulating?
- Should beta-support notes live directly in skills, in per-skill references, or in one beta compatibility reference that skills link to?

## Decision Checkpoints

- If implementation requires a custom runtime, MCP server, Xcode plug-in package, or ACP bridge, pause before widening scope.
- If supporting beta docs starts polluting stable skill guidance, consider a separate beta reference file before considering a separate plugin.
- If businesses begin depending on Socket commercially, coordinate with the licensing plan before shipping license-sensitive packaging or contribution changes.
