---
name: xcode-coding-intelligence-workflow
description: Guide Xcode coding-intelligence setup, Xcode-hosted agents, external-agent access through xcrun mcpbridge, command and tool permissions, Xcode-only agent configuration homes, and setup handoffs for Xcode 27 beta-era agentic coding workflows.
---

# Xcode Coding Intelligence Workflow

## Purpose

Guide setup and reasoning for Xcode coding intelligence without taking over normal build, run, preview, or testing execution.

This skill owns Xcode Intelligence setup, Xcode-hosted coding agents, chat providers, external-agent access through `xcrun mcpbridge`, Xcode plug-in import inspection, command and tool permissions, Xcode-only agent configuration homes, and the boundary between Xcode's assistant UI and external Codex sessions. It is the setup and permissions companion for `xcode-build-run-workflow` and `xcode-testing-workflow`.

Beta-specific note: Xcode 27 claims in this skill were checked against Apple developer pages and WWDC26 transcripts on 2026-06-22. Treat Xcode 27 behavior as beta-specific unless the target machine's installed Xcode and Apple docs confirm the same behavior.

## When To Use

- Use this skill when the task is about Xcode Intelligence settings, coding assistants, Xcode-hosted agents, chat providers, model choice, agent conversations, plan mode, artifacts, or command and tool permissions.
- Use this skill when configuring external agents to use Xcode capabilities through `xcrun mcpbridge`.
- Use this skill when inspecting Xcode's Plug-ins UI import paths for skills, hooks, and MCP servers.
- Use this skill when the user needs to distinguish Xcode-hosted agents from normal Codex sessions that connect to Xcode through MCP.
- Use this skill when the task mentions Xcode-only agent configuration homes, Xcode-launched Codex, Claude, Gemini, ChatGPT in Xcode, or other chat-provider setup.
- Use this skill when Xcode agent workflows should be checked before a build, test, preview, localization, or Device Hub handoff.
- Recommend `xcode-build-run-workflow` when the next step is workspace inspection, build, run, preview, file membership, target membership, diagnostics, or guarded project mutation.
- Recommend `xcode-testing-workflow` when the next step is Swift Testing, XCTest, XCUITest, `.xctestplan`, test filtering, retries, or test diagnosis.
- Recommend `explore-apple-swift-docs` when the user primarily needs current Apple documentation lookup rather than setup and workflow planning.
- Recommend `sync-xcode-project-guidance` when an existing Xcode app repo needs durable repo guidance updated for Xcode workflows.
- Do not use this skill as the owner for implementing custom ACP agents, custom MCP servers, Xcode plug-in packages, or broad agent-configuration sync.

## Single-Path Workflow

1. Classify the coding-intelligence request:
   - Xcode Intelligence settings
   - Xcode-hosted agent setup
   - chat provider or model-provider setup
   - external-agent access through `xcrun mcpbridge`
   - command, tool, approval, or permission policy
   - Xcode-only agent configuration home
   - plan-mode, artifacts, diff-review, preview, build, or test handoff
   - beta documentation or installed-Xcode capability check
2. Apply the Apple docs gate before making setup or behavior claims:
   - read current Apple Xcode documentation, Xcode pages, WWDC transcripts, or local Xcode tool output first
   - state the documented behavior being relied on and the date checked for beta-specific behavior
   - if Apple docs and local Xcode behavior disagree, stop and report the conflict
   - if no relevant Apple documentation can be found, say that explicitly before proceeding
3. Establish which agent surface is in play:
   - Xcode-hosted agent: started inside Xcode, uses Xcode's assistant UI, Xcode's project context, Xcode's artifact review surfaces, and Xcode-managed tool permissions
   - external agent through MCP: started outside Xcode and connected through `xcrun mcpbridge`, requiring a running Xcode instance and external-agent access
   - chat provider: model or chat setup for Xcode coding intelligence that may not imply autonomous Xcode tool use
   - exploratory agent protocol or plug-in surface: do not ship implementation guidance until Apple's current docs and local Xcode inspection verify the package and permission shape
4. Plan setup:
   - verify the target Xcode version and whether the relevant behavior is stable, beta, or local-only
   - check whether the intended Xcode app is running and open it when needed for project context, MCP bridge connection, agent settings, or UI/plugin inspection
   - use the Xcode CLI toolchain Gale selected through `xcode-select`; do not override it with `DEVELOPER_DIR`
   - open the intended beta app when the beta UI or live bridge state is required
   - change `xcode-select` only when Gale explicitly asks to switch CLI toolchains; record the previous `xcode-select -p`, verify the requested selection, and restore only when Gale asked for a temporary switch
   - verify the project is open in Xcode before expecting Xcode MCP tools to work
   - verify external-agent access is enabled before configuring an external MCP client
   - use `xcrun mcpbridge` as the Xcode-provided STDIO bridge for external MCP clients
   - use `xcrun mcpbridge run-agent <agent-name>` only when intentionally launching a coding agent with Xcode-provided configuration
   - use Xcode Settings > Intelligence > Plug-ins for official plug-in import checks
   - use `MCP_XCODE_PID` when multiple Xcode processes make auto-detection ambiguous
   - keep normal Codex config separate from Xcode-launched Codex config
5. Plan command and tool permissions:
   - identify which agent is allowed to read files, modify source, edit project settings, build, run tests, render previews, inspect devices, or search documentation
   - prefer plan-first work for architecture-sensitive or beta-sensitive changes
   - keep generated files, diffs, previews, screenshots, and other artifacts reviewable before committing
   - do not grant broad write or shell permissions just to fix setup uncertainty
6. Hand off execution:
   - build, run, preview, file membership, and project-integrity work goes to `xcode-build-run-workflow`
   - Swift Testing, XCTest, XCUITest, and `.xctestplan` work goes to `xcode-testing-workflow`
   - docs lookup goes to `explore-apple-swift-docs`
   - repo guidance sync goes to `sync-xcode-project-guidance`
7. Report:
   - Xcode version or beta target checked
   - Apple docs or local Xcode tool output relied on
   - selected agent surface
   - setup state and permission boundary
   - external-agent command shape when relevant
   - handoff skill for the next executable step

## Inputs

- `request`: optional free-text setup or workflow request.
- `xcode_version`: optional target such as `26.5`, `27 beta`, or `installed`.
- `agent_surface`: optional explicit surface such as `xcode-hosted`, `external-mcp`, `chat-provider`, `plugin`, `acp`, or `unknown`.
- `agent_name`: optional agent name when launching through Xcode, such as `codex` or `claude`.
- `permission_focus`: optional emphasis such as `read-only`, `source-edits`, `project-settings`, `build`, `test`, `preview`, `device`, or `shell`.
- Defaults:
  - docs-first guidance always applies
  - beta-specific claims require a checked date
  - setup and permissions stay here
  - execution and validation hand off to existing Xcode execution skills

## Outputs

- `status`
  - `success`: the setup or workflow recommendation is ready
  - `handoff`: the request belongs to another Apple Dev skill after coding-intelligence classification
  - `blocked`: docs, local Xcode capability checks, permissions, or missing project context prevent a safe recommendation
- `path_type`
  - `primary`: the recommendation uses documented Xcode coding-intelligence or `xcrun mcpbridge` behavior
  - `fallback`: the recommendation is limited to local Xcode inspection because Apple docs are JavaScript-gated or incomplete
- `output`
  - resolved agent surface
  - documented behavior relied on
  - beta or stable status and date checked
  - setup prerequisites
  - permission boundary
  - command shape when relevant
  - recommended handoff skill

## Guards and Stop Conditions

- Do not claim Xcode 27 beta behavior is stable Xcode behavior.
- Do not treat Xcode-generated or Xcode-copied plug-in files as Socket source of truth unless the user explicitly asks to compare or import them.
- Do not claim ACP setup, Xcode plug-in package shape, or Xcode plug-in import behavior unless current Apple docs or live Xcode inspection verify that exact surface.
- Do not collapse Xcode-hosted agents and external MCP clients into one vague "agent"; name which process owns the UI, config, context, permissions, and execution.
- Do not mutate normal Codex config, Xcode-launched agent config, shell rc files, keychains, or provider credentials without explicit user intent.
- Do not set `DEVELOPER_DIR` unless it is genuinely the only viable path and Gale has explicitly approved that exception after hearing why `xcode-select` cannot serve the task.
- Do not store provider API keys in repo files or app binaries.
- Stop with `blocked` when no relevant Apple documentation or local Xcode evidence can be found for a requested setup claim.
- If Xcode is not running and the requested setup depends on a live Xcode session, open the intended stable or beta Xcode app and continue verification. Stop with `blocked` only when Xcode cannot be opened, the required project or workspace cannot be opened or identified, external-agent access is disabled and cannot be inspected, or the user has forbidden launching the app.

## Fallbacks and Handoffs

- Recommend `explore-apple-swift-docs` when current Apple docs need to be gathered before setup can be trusted.
- Recommend `xcode-build-run-workflow` when the next step is Xcode build, run, preview, file membership, target membership, or project-integrity work.
- Recommend `xcode-testing-workflow` when the next step is Swift Testing, XCTest, XCUITest, `.xctestplan`, or test diagnosis.
- Recommend `sync-xcode-project-guidance` when the target repo needs durable Apple/Xcode guidance updated rather than one-off setup.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project guidance in a repo that will rely on Xcode coding intelligence.
- Keep custom Xcode plug-in writers and ACP-agent work research-first until the live Xcode 27 package, runtime behavior, and permission surface are verified.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep this skill focused on setup and permission decisions. If future iterations add deterministic checks for Xcode settings exports, agent config folders, or MCP bridge status, document the knobs before runtime behavior depends on them.

## References

### Workflow References

- `references/setup-and-agent-surfaces.md`
- `references/mcpbridge-and-external-agents.md`
- `references/permissions-and-artifacts.md`
- `references/source-evidence.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs current Apple docs before an Xcode coding-intelligence setup claim.
- Recommend `xcode-build-run-workflow` when the next step is build, run, preview, project membership, or project-integrity follow-through.
- Recommend `xcode-testing-workflow` when the next step is test generation, execution, `.xctestplan`, or failure diagnosis.
- Recommend `sync-xcode-project-guidance` when repo-local guidance needs to be updated for Xcode coding-intelligence workflows.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project guidance for a repo that will use Xcode coding intelligence.

### Script Inventory

- `scripts/customization_config.py`
