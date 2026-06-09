# Xcode 27 Agentic Tooling Skill Plan

This plan records the first Socket pass for supporting Xcode 27 beta-era coding intelligence inside the existing `apple-dev-skills` plugin.

The goal is to add practical Apple and Xcode workflows without creating a separate beta plugin yet. Keep ACP-specific exploration outside this plan except where Xcode itself exposes ACP agent setup as part of its Intelligence settings.

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

Important current Xcode 27 signals:

- Xcode integrates coding intelligence directly into the workspace, including conversations, transcript panes, artifacts panes, plan mode, source-editor coding tools, generated fixes, previews, playgrounds, and rollback through conversation history.
- Xcode Intelligence settings expose agents, chat providers, Model Context Protocol settings, Xcode plug-ins, command/tool permissions, and Xcode-only agent configuration folders.
- Xcode can add agents that support the Agent Client Protocol.
- External agents can use Xcode capabilities through Xcode's MCP server after enabling external-agent access and configuring `xcrun mcpbridge`.
- Xcode-hosted agents can use built-in Xcode guidance and skills.
- Xcode can assist with localization by adding languages, updating string catalogs, translating strings, and setting machine-translation state.
- Device Hub is now the central Xcode surface for simulated and physical device interaction, environment inspection, pairing, screenshots, videos, and diagnostics.

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
- Explain Xcode-only agent configuration homes:

  ```text
  ~/Library/Developer/Xcode/CodingAssistant/ClaudeAgentConfig
  ~/Library/Developer/Xcode/CodingAssistant/codex
  ~/Library/Developer/Xcode/CodingAssistant/gemini
  ```

- Track the difference between normal Codex config and Xcode-launched Codex config.
- Hand off broader agent configuration sync to `codex-utilities` once that plugin exposes a supported bridge/status surface.

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

### 3. `xcode-agent-localization-workflow`

Job:

- Guide Xcode agent-assisted localization work from preparation through review.

Scope:

- Add languages with Xcode-hosted agents.
- Update string catalogs by building the project where Xcode requires it.
- Use `String(localized:)` and platform-localizable APIs when strings are missed.
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

- Add `plugins/apple-dev-skills/skills/xcode-coding-intelligence-workflow/SKILL.md`.
- Add `plugins/apple-dev-skills/skills/xcode-coding-intelligence-workflow/agents/openai.yaml`.
- Add concise references for setup, MCP bridge routing, Xcode-only config homes, and permission boundaries.
- Update Apple Dev Skills metadata to advertise the new skill.
- Update existing Xcode build/test skills to route setup questions to this skill.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
uv run pytest
```

### Slice 3: Localization And Device Hub

- Add `xcode-agent-localization-workflow`.
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

- Add `xcode-agent-plugin-workflow` only after live Xcode 27 beta inspection confirms enough import/package details to make the skill useful.
- If the live import surface is too vague, keep this as a roadmap item and do not ship speculative instructions.

## Open Questions

- Does Xcode 27 beta expose enough plug-in package structure to support a real Socket-authored Xcode plug-in?
- Can one authored skill surface be packaged for both Codex and Xcode, or does Xcode require a separate distribution artifact?
- Should Xcode-launched Codex config sync remain entirely in `codex-utilities`, with Apple Dev Skills only describing the Xcode side?
- Which Apple Dev Skills workflow should own UIKit guidance if UIKit-specific beta changes keep accumulating?
- Should beta-support notes live directly in skills, in per-skill references, or in one beta compatibility reference that skills link to?

## Decision Checkpoints

- If implementation requires a custom runtime, MCP server, Xcode plug-in package, or ACP bridge, pause before widening scope.
- If supporting beta docs starts polluting stable skill guidance, consider a separate beta reference file before considering a separate plugin.
- If businesses begin depending on Socket commercially, coordinate with the licensing plan before shipping license-sensitive packaging or contribution changes.
