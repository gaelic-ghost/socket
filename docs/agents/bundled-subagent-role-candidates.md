# Bundled Subagent Role Candidates

## Purpose

Record candidate Codex custom-agent roles that could be bundled by Socket-owned
plugins after the first Swift Steward roles. This inventory is based on
read-only plugin scans and should guide future role work without implying every
candidate should be implemented immediately.

Use this document when deciding whether a plugin has enough bounded,
read-heavy, independently useful work to justify a `.codex/agents/*.toml` role.
Keep write ownership in the main thread unless a future role explicitly earns a
separate apply contract.

## Recommendation

Add bundled roles where the job is repeatedly useful, read-heavy, and
privacy-safe enough to summarize as a review packet. Do not create a standalone
Socket plugin whose only purpose is collecting generic subagent roles yet. The
stronger near-term path is to colocate each role with the plugin that owns the
workflow knowledge.

Strong candidates:

1. `productivity-skills`: `repo-docs-auditor` (implemented)
2. `productivity-skills`: `code-slice-tracer` (implemented)
3. `agent-plugin-skills`: `skills-repo-guidance-sync` (implemented)
4. `things-app`: `things-route-auditor`
5. `cardhop-app`: `cardhop-contact-auditor`
6. `python-skills`: `python-validation-triager`
7. `rust-skills`: `rust-validation-triager`
8. `dotnet-skills`: `dotnet-validation-triager`

Keep `swift-steward` and `server-swift-steward` as the Swift-family roles
instead of adding another Apple or server-side Swift role.

## Implemented Roles

These roles are now bundled in their owning plugin roots:

- `apple-dev-skills/.codex/agents/swift-steward.toml`
- `server-side-swift/.codex/agents/server-swift-steward.toml`
- `productivity-skills/.codex/agents/repo-docs-auditor.toml`
- `productivity-skills/.codex/agents/code-slice-tracer.toml`
- `agent-plugin-skills/.codex/agents/skills-repo-guidance-sync.toml`

## Strong Candidates

### productivity-skills: repo-docs-auditor

Good fit because `maintain-project-docs` already coordinates README,
CONTRIBUTING, AGENTS, ACCESSIBILITY, and ROADMAP sweeps while checking for
cross-document drift.

Good triggers:

- "audit repo docs"
- "fix docs drift"
- "compare README and CONTRIBUTING"
- "find stale commands"

Read/write boundary: inspect docs, commands, issue references, and skill
contracts; return findings and a proposed patch set. The main thread keeps
file-specific writes so owner skills preserve each document's voice and schema.

Evidence:

- `plugins/productivity-skills/skills/maintain-project-docs/SKILL.md`
- `plugins/productivity-skills/skills/maintain-project-readme/SKILL.md`
- `plugins/productivity-skills/skills/maintain-project-contributing/SKILL.md`
- `plugins/productivity-skills/skills/maintain-project-agents/SKILL.md`
- `plugins/productivity-skills/skills/maintain-project-roadmap/SKILL.md`

### productivity-skills: code-slice-tracer

Good fit because `explain-code-slice` is a bounded read-only walkthrough skill
and already allows subagent fan-out for large traces.

Good triggers:

- "walk me through this path"
- "what calls this"
- "compare these slices"
- "follow this request through the code"

Read/write boundary: inspect code, tests, docs, and call sites; return concise
trace findings. The main thread owns the final explanation and any persistent
`SLICES.md` or architecture edits.

Evidence:

- `plugins/productivity-skills/skills/explain-code-slice/SKILL.md`
- `plugins/productivity-skills/skills/maintain-project-architecture/SKILL.md`

### agent-plugin-skills: skills-repo-guidance-sync

Good fit because the bootstrap and sync skills already audit plugin-root policy,
marketplace wording, Codex docs freshness, and guidance drift in skills-export
repositories.

Good triggers:

- "sync skills repo guidance"
- "check plugin root structure"
- "audit marketplace wording"
- "refresh Codex docs"

Read/write boundary: perform read-heavy policy and structure audit; return a
review packet. The main thread owns packaging, install-surface, marketplace, or
generated guidance edits.

Evidence:

- `plugins/agent-plugin-skills/skills/bootstrap-skills-plugin-repo/SKILL.md`
- `plugins/agent-plugin-skills/skills/sync-skills-repo-guidance/SKILL.md`

### things-app: things-route-auditor

Good fit because the plugin has a clear read-heavy lane around route coverage,
digest preparation, reminder planning, JSON-shape checks, and duplicate
analysis.

Good triggers:

- "audit my Things routes"
- "plan my week from Things"
- "check reminder duplicates"
- "review import JSON shape"
- "draft a Things digest"

Read/write boundary: read `things_read_*`, `things_find_todos`, docs, and
validation output only. Do not call `things_add_*`, `things_update_*`,
`things_import_json`, or token-writing tools from the role.

Risk: high privacy and side-effect sensitivity because the plugin can mutate a
personal task graph. Keep this role read-only, preview-first, and explicit about
not writing to Things.

Evidence:

- `plugins/things-app/mcp/README.md`
- `plugins/things-app/mcp/app/server.py`
- `plugins/things-app/mcp/app/tools.py`
- `plugins/things-app/skills/things-digest-generator/SKILL.md`
- `plugins/things-app/skills/things-reminders-manager/SKILL.md`

### cardhop-app: cardhop-contact-auditor

Good fit because the plugin has a small, bounded contact workflow surface with
schema checks, health checks, route documentation, and dry-run previews.

Good triggers:

- "check Cardhop readiness"
- "preview this contact update"
- "audit Cardhop routes"
- "verify transport choice"

Read/write boundary: inspect schema, docs, tests, and dry-run previews only. Do
not dispatch live parse, add, or update actions from the role.

Risk: high privacy and side-effect sensitivity because live dispatch touches
private contacts and macOS automation or URL-scheme paths. Keep this role
read-only unless Gale explicitly approves a separate write-capable design.

Evidence:

- `plugins/cardhop-app/mcp/README.md`
- `plugins/cardhop-app/mcp/app/server.py`
- `plugins/cardhop-app/mcp/app/tools.py`
- `plugins/cardhop-app/skills/cardhop-contact-workflow/SKILL.md`

### python-skills: python-validation-triager

Good fit because diagnosis, CI, package, tooling, upgrade, and pytest workflows
share the same read-heavy failure-analysis loop.

Good triggers:

- "uv sync failed"
- "pytest broke"
- "ruff or mypy drift"
- "package metadata issue"
- "upgrade broke CI"

Read/write boundary: inspect logs, config, manifests, tests, and docs; explain
likely cause and propose fixes. The main thread owns file edits and dependency
changes.

Evidence:

- `plugins/python-skills/skills/diagnose-python-project/SKILL.md`
- `plugins/python-skills/skills/python-ci-workflow/SKILL.md`
- `plugins/python-skills/skills/python-package-workflow/SKILL.md`
- `plugins/python-skills/skills/python-tooling-style-workflow/SKILL.md`
- `plugins/python-skills/skills/python-upgrade-workflow/SKILL.md`
- `plugins/python-skills/skills/uv-pytest-unit-testing/SKILL.md`

### rust-skills: rust-validation-triager

Good fit because Cargo shape, CI, tests, tooling, and package checks are
evidence-driven and repeatable.

Good triggers:

- "cargo test failed"
- "clippy noise"
- "package dry-run"
- "workspace shape"
- "MSRV check"

Read/write boundary: inspect manifests, logs, tests, CI, and docs; recommend a
fix path. The main thread owns edits, release decisions, and publish behavior.

Evidence:

- `plugins/rust-skills/skills/choose-project-shape/SKILL.md`
- `plugins/rust-skills/skills/ci-workflow/SKILL.md`
- `plugins/rust-skills/skills/testing-workflow/SKILL.md`
- `plugins/rust-skills/skills/tooling-style-workflow/SKILL.md`
- `plugins/rust-skills/skills/package-workflow/SKILL.md`

### dotnet-skills: dotnet-validation-triager

Good fit because restore, build, test, pack, tooling, and upgrade checks mirror
the same read-heavy validation-triage pattern as Python and Rust.

Good triggers:

- "dotnet test failed"
- "pack issue"
- ".editorconfig or analyzer drift"
- "global.json upgrade"
- "F# versus C# split"

Read/write boundary: inspect project files, logs, tests, CI, and docs; explain
the likely cause and proposed patch set. The main thread owns code and docs
changes.

Evidence:

- `plugins/dotnet-skills/skills/ci-workflow/SKILL.md`
- `plugins/dotnet-skills/skills/testing-workflow/SKILL.md`
- `plugins/dotnet-skills/skills/tooling-style-workflow/SKILL.md`
- `plugins/dotnet-skills/skills/package-workflow/SKILL.md`
- `plugins/dotnet-skills/skills/upgrade-workflow/SKILL.md`

## Maybe Later

### productivity-skills: roadmap-triage-worker

Useful for collecting TODO/FIXME comments, GitHub issue evidence, release-note
drift, and backlog candidates. Keep it separate from source-comment rewrites and
only let the main thread apply a single explicit checklist item at a time.

### productivity-skills: automation-plan-designer

Useful for plan-only analysis across Codex app automations, `codex exec`, Codex
subagents, Agents SDK services, LangGraph, evals, and escalation gates. Keep it
advisory so it does not grow into a second implementation layer.

### swiftasb-skills: swiftasb-steward

Useful for read-heavy SwiftASB integration triage, source-of-truth comparison,
and failed-integration diagnosis. Do not bundle until the plugin needs a
cross-skill auditor beyond its existing explicit decision and diagnosis skills.

### web-dev-skills: expo-native-boundary-scout

Useful as a weak candidate for Expo inline-native module boundary checks before
native edits or installs. Do not bundle yet because there is only one workflow,
the surface is freshness-sensitive, and the role would need careful handoff to
Apple Dev Skills for Swift or Xcode behavior.

## Not Yet

### android-dev-skills: android-steward

Do not add yet. The plugin is still a placeholder with no shipped skill
entrypoints. Revisit after Kotlin-first Android guidance, Gradle and Android
Gradle Plugin alignment, emulator-aware validation, and release-readiness
workflows exist.

### spotify

Do not add yet. The plugin is still a placeholder with no shipped skills, MCP
server, API inventory, or workflow docs to audit.

### maintain-project-repo as a bundled worker

Do not make `maintain-project-repo` itself a bundled subagent role yet. It is a
main-thread orchestrator with install, validation, release, and write-capable
responsibilities. Use subagents under it for read-heavy discovery, but keep the
orchestration and apply decisions in the main thread.

## Open Questions

- Should validation-triage roles share one house contract across Python, Rust,
  and .NET, or should each plugin own a separate role shape?
- Should privacy-sensitive app roles be allowed to call read-only MCP tools, or
  should they inspect docs and dry-run artifacts only until the permission model
  is clearer?
- Should future roles return the same review-packet contract as Swift Steward,
  or should non-maintenance roles use a lighter findings-only report?
