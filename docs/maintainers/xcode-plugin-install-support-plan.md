# Xcode Plug-in Install Support Plan

This plan turns the Xcode 27 beta import evidence into a practical Socket implementation path.

Date checked: 2026-07-19. The installed beta bundle is Xcode 27.0 build
27A5218g; the import/runtime observations below remain the dated 2026-06-23
probe unless a later line says otherwise.

## Goal

Make Socket products installable into Xcode 27 through Xcode's official Plug-ins UI as smoothly as possible, while keeping Socket's existing Codex marketplace model intact.

The first implementation should help maintainers and users answer three questions before any write-capable installer exists:

- Which Socket child plug-ins can Xcode recognize from the public Socket Git URL?
- Which recognized components are expected to work inside Xcode internal agents, Xcode-launched Codex, or external agents using Xcode MCP?
- Which components need path, dependency, permission, authentication, hook, or runtime validation before Socket can claim full Xcode support?

## Current Evidence

Xcode 27 beta exposes the official import path in Settings > Intelligence > Plug-ins > Add Plug-in.

The observed import choices are:

- Import from Claude Code
- Import from Codex
- Add from file
- Add from URL

The observed Xcode description is:

```text
Plug-ins extend Xcode's agentic Intelligence features with skills, subagent definitions, hooks, and MCP servers.
```

Local probe results:

- `Import from Codex` listed installed Codex plug-ins and imported `apple-dev-skills` as `6 Skills - Hooks`.
- `Add from file` imported a harmless fixture containing one `SKILL.md` and one inert `.mcp.json` server as `1 Skill - 1 MCP Server`.
- `Add from URL` rejected a local `file://` Git URL as invalid.
- `Add from URL` accepted `https://github.com/gaelic-ghost/socket.git` and enumerated Socket child plug-ins before import.
- Xcode registered imported plug-ins under `~/Library/Developer/Xcode/CodingAssistant/AgentPlugins`.
- Xcode mirrored imported payloads into its Codex and Gemini CodingAssistant homes.
- Xcode wrote MCP declarations from imported `.mcp.json` files into `~/Library/Developer/Xcode/CodingAssistant/mcp-servers.json`.

## Non-Goals

- Do not build a separate custom Xcode installer before the official UI path is exhausted.
- Do not change `xcode-select` unless the task explicitly requires the beta command-line toolchain. For bundle/build-number audits, inspect bundle metadata. For beta CLI execution, record the previous selection, switch intentionally with `xcode-select`, verify, run the normal Apple CLI, and restore the previous selection. Do not inject `DEVELOPER_DIR` overrides.
- Do not rewrite Socket as an aggregate non-Codex plugin bundle.
- Do not claim hook execution, MCP server execution, app config, or custom-agent behavior works in Xcode until runtime probes verify those surfaces.
- Do not treat Xcode-generated files as Socket source of truth.
- Do not write into Gale's user Xcode state from automation without dry-run output and explicit apply intent.

## Support Model

Support needs three separate classifications.

### Xcode Internal Plug-ins

This is the Xcode Settings > Intelligence > Plug-ins import path.

Likely support:

- skill folders with `SKILL.md`
- `.mcp.json` entries whose commands work from Xcode's CodingAssistant environment
- hooks as import-recognized metadata, pending execution validation

Likely unsupported or unknown:

- Codex apps
- `agents/openai.yaml`
- host-specific custom-agent definitions
- commands that rely on ordinary `~/.codex` state, shell rc files, local relative paths, or uninstalled dependencies

### Xcode-Launched Codex

This is Xcode's Codex runtime under `~/Library/Developer/Xcode/CodingAssistant/codex`.

Likely support:

- imported plug-in cache entries written by Xcode
- Xcode-specific Codex enablement in Xcode's `codex/config.toml`
- skills and MCP declarations that Xcode imports and mirrors

Unknown:

- whether every Socket Codex hook has the same lifecycle and trust behavior inside Xcode-launched Codex
- whether app config has an Xcode equivalent
- whether normal Codex marketplace state should be synced or merely used as source input

### External Agents Using Xcode MCP

This is an external agent configured with `xcrun mcpbridge`.

Likely support:

- Xcode project and tool access through Xcode's MCP bridge after permissions and project state are ready
- the external agent's own installed Socket skills and MCP servers

Important distinction:

- An external agent does not need a Socket Xcode plug-in merely to control Xcode.
- It still needs Socket installed in that agent's own host if the workflow depends on Socket skills.

## Implementation Slices

### Slice 1: Xcode Support Inventory — Implemented

The read-only inventory command now reads the Socket source tree and classifies
each child plug-in:

```bash
uv run scripts/audit_xcode_plugin_compatibility.py
uv run scripts/audit_xcode_plugin_compatibility.py --format json
```

Inputs:

- root marketplace entries
- child `.codex-plugin/plugin.json`
- child `.mcp.json`
- `skills/*/SKILL.md`
- hooks
- app config
- `agents/openai.yaml`

Output for each child plug-in:

- visible name and plugin id
- skill count and skill names
- MCP server names, commands, and relative path risks
- hook presence and hook files
- app config presence
- custom-agent metadata presence
- Xcode internal plug-in status: `likely`, `partial`, `blocked`, or `unknown`
- Xcode-launched Codex status: `likely`, `partial`, `blocked`, or `unknown`
- external-agent status: `likely`, `partial`, `blocked`, or `unknown`
- reason strings written in maintainer-readable language

The 2026-07-19 source audit classifies 16 skill-only child plug-ins as
structurally `likely` for all three targets. The runtime-proof queue contains
the MCP-backed plug-ins, plug-ins with Codex custom-agent metadata, the
Codex-only `agentdeck` hook, and the external Git-backed `speak-swiftly`
payload. `spotify` remains blocked because it is unavailable and has no usable
payload.

`agents/openai.yaml` files are counted separately as Codex presentation
metadata; they are not reported as Xcode subagents. Actual Socket custom agents
under `.codex/agents/` remain `partial` until Xcode documents or demonstrates a
matching import contract.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
uv run pytest
```

### Slice 2: Official Import Smoke Fixtures

Keep the import probe reproducible without requiring maintainers to improvise payloads.

Add a script or documented fixture generator that can create:

- a skill-only fixture
- a skill plus inert MCP fixture
- an optional hook-recognition fixture

The first version may write only to `/private/tmp` and print manual Xcode UI steps.

The fixture should never be committed as an installed user artifact, and it should clearly identify itself as disposable.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
```

Manual evidence to capture:

- Xcode import choice used
- detected component summary in the UI
- generated `AgentPlugins/<fixture>/plugin.json`
- changes to `mcp-servers.json`
- whether Xcode mirrors the payload into Codex and Gemini homes

### Slice 3: Public Socket URL Import Matrix

Use Xcode's `Add from URL` path against the public Socket Git URL.

Do not select and import every plug-in by default. First capture what Xcode enumerates.

Expected output:

- list of child plug-ins Xcode detects
- Xcode's component summary for each
- differences between Xcode's summary and Socket's own inventory
- plug-ins that appear importable but need runtime checks
- plug-ins that Xcode skips or misclassifies

This can start as a maintainer report before becoming a script.

### Slice 4: Runtime Validation Targets

Pick a small set of representative plug-ins and validate runtime behavior inside Xcode.

Suggested first targets:

- `apple-dev-skills`: skill and hook-recognition path
- `things-app` or `cardhop-app`: skill plus local MCP path
- `productivity-skills`: broader skill pack with MCP
- one skill-only language pack

For each selected plug-in, validate:

- Xcode internal agent can see or invoke a skill when prompted
- Xcode-launched Codex sees the imported plug-in state
- any MCP server command starts from the Xcode CodingAssistant environment
- hooks either execute with understood semantics or stay marked unverified
- uninstall or disable behavior is observable and reversible

Stop before touching service-backed or privacy-sensitive app data unless the user explicitly asks for that runtime validation.

### Slice 5: User-Facing Guidance

After the assessment and at least one runtime smoke path pass, update user-facing docs.

Candidate docs:

- root README install section
- plugin packaging strategy
- Xcode 27 agentic tooling plan
- Apple Dev Skills `xcode-coding-intelligence-workflow`

Guidance should say:

- use Xcode's official Add Plug-in UI
- use the public Socket Git URL for the Socket catalog path
- expect Xcode to show child plug-ins, not one aggregate Socket plug-in
- install only the plug-ins you trust and need
- treat MCP-backed plug-ins as requiring local dependency and permission readiness
- use external-agent MCP separately when controlling Xcode from outside Xcode

## Data Model

Prefer a small typed report model over ad hoc strings.

Suggested entities:

- `HostTarget`
  - `xcode-internal-plugin`
  - `xcode-launched-codex`
  - `external-agent-xcode-mcp`
- `ComponentKind`
  - `skill`
  - `mcp-server`
  - `hook`
  - `app-config`
  - `custom-agent`
  - `unknown`
- `SupportStatus`
  - `likely`
  - `partial`
  - `blocked`
  - `unknown`
- `SupportIssue`
  - `component`
  - `target`
  - `status`
  - `reason`
  - `evidence`
  - `next_check`

Keep paths repo-relative in generated reports when they refer to tracked files. User-home paths may appear only as observed Xcode state in maintainer evidence, not as repository links.

## AgentUtils Boundary

Socket should own:

- component inventory
- compatibility rules
- dry-run report shape
- maintainer docs
- lightweight fixture generation

AgentUtils should own later macOS-local apply behavior if the work needs:

- app-bundle discovery
- Xcode Beta versus stable app selection
- GUI state orchestration
- backup-backed writes to user-home Xcode config
- cleanup of imported disposable fixtures
- status checks across multiple agent homes

## Release Gate

Before claiming Xcode install support beyond research:

- root metadata validation passes
- relevant child tests pass
- Xcode import evidence is dated and target-versioned
- public Socket Git URL import has been checked after the target release
- every runtime claim says which Xcode surface it applies to
- unsupported or unverified components are reported plainly

## First Follow-Up Task

Run Slice 3 against the current Xcode 27 beta UI and compare Xcode's public-URL
enumeration with the deterministic source report. Do not import every plug-in or
add an apply mode. Capture component summaries first, then choose one skill-only
plugin and one MCP-backed plugin for the runtime checks in Slice 4.
