# Token Efficiency and Automation Audit

Date: 2026-06-22
Branch: `audit/token-efficiency-automation`

## Summary

Socket has several good existing boundaries for reducing hand-carried work:
shared Apple snippet sources, maintainer automation guidance, source-bundled
steward roles, root marketplace validation, and child validation in some
plugins. The largest remaining token-efficiency opportunities are not generic
style edits. They are moving repeated high-churn facts into narrower references,
making generated or mirrored guidance less expensive to load, and adding
automation that inventories drift before humans edit skill prose.

Top priorities:

1. Collapse repeated SwiftASB API inventory into one current-state reference and
   keep per-skill files focused on routing, ownership, and workflow-specific
   decisions.
2. Replace repeated productivity-skill subagent prose with a short local fit
   paragraph plus the existing shared maintainer guidance.
3. Treat Apple shared snippets as generated mirrors and add drift/size reporting
   so their duplication is visible before release.
4. Define Socket-owned F# `.fsx` conventions for typed hooks and compact local
   maintenance scripts, but do not migrate Python validators or the current Node
   hook until portability and startup costs are measured.
5. Use the root skill-surface audit script to keep large skills, duplicate
   snippets, stale current-version wording, missing handoff references, and
   repeated boilerplate visible before manual cleanup.

## Evidence Snapshot

- `plugins/apple-dev-skills`: 21 skill files, 3,401 `SKILL.md` lines.
- `plugins/python-skills`: 12 skill files, 1,906 `SKILL.md` lines.
- `plugins/swiftasb-skills`: 6 skill files, 1,467 `SKILL.md` lines.
- `plugins/productivity-skills`: 14 skill files, 1,580 `SKILL.md` lines.
- Root skill total: 12,703 `SKILL.md` lines across shipped child plugins.
- Root reference total: 11,439 Markdown reference lines under skill references.
- `apple-dev-skills` carries 23 skill-local snippet copies in three identical
  checksum groups.
- `productivity-skills` repeats the phrase `When the user explicitly requests
  subagents` in 10 maintainer skills, plus one `agent-portability-skills` workflow.
- `swiftasb-skills` repeats startup, diagnostics, feature-operation, generated
  wire-model, same-thread overlap, and Apple handoff facts across multiple
  skills.
- Current script inventory includes one `.mjs` file with 592 lines, 137 Python
  files with 35,750 lines, 29 shell files with 4,675 lines, and no `.fsx` or
  `.fs` files.
- The roadmap now includes an explicit Socket-owned F# `.fsx` hook and
  maintenance-script conventions item covering launch shape, repo-local
  `DOTNET_CLI_HOME`, event JSON types, validation, and graduation to compiled
  F# tools.
- `scripts/audit_skill_surfaces.py --top 5` now reports 87 skill files, 12,703
  skill lines, 264 reference files, 11,439 reference lines, 17 exact duplicate
  reference groups, 4 version-sensitive lines, and 0 missing expected handoffs
  with the current skill-specific expectation map.

## Quick Wins

### 1. Keep the root token-surface audit script report-only

`scripts/audit_skill_surfaces.py` now has a report-only default that emits:

- skill line counts by plugin and skill
- reference line counts by plugin and reference
- exact duplicate reference checksums
- repeated phrase counts from a repo-owned phrase list
- version-sensitive phrases such as `As of SwiftASB v...`
- missing expected handoff references for known cross-skill boundaries

Keep it advisory for now so maintainers can see hotspots without blocking
unrelated plugin work. If it becomes a release gate later, split strict checks
from exploratory checks first.

Evidence:

- Root validation already validates marketplace wiring in
  `scripts/validate_socket_metadata.py`.
- Apple has a manual snippet sync script at
  `plugins/apple-dev-skills/.github/scripts/sync_shared_snippets.sh`.
- Python has a child metadata validator at
  `plugins/python-skills/scripts/validate_repo_metadata.py`.

### 2. Put the Apple snippet mirror check into validation

`apple-dev-skills` already has canonical sources under
`plugins/apple-dev-skills/shared/agents-snippets/` and a script that copies them
into skill-local `references/snippets/` files. That is a good source-of-truth
shape, but the repo should also be able to detect drift without relying on a
maintainer remembering to run the sync script.

Recommended first step:

- Add a check mode to `sync_shared_snippets.sh`, or add a small Python validator
  that compares each target with its canonical source.
- Include the check in the Apple child validation path.
- Keep copies for now if current skill-loader behavior requires references to
  stay inside each skill directory.

Evidence:

- The sync script copies `apple-xcode-project-core.md` into 12 skills and
  `apple-swift-package-core.md` into 5 skills.
- The copied snippets are large enough to matter: 104 lines for Xcode project
  core and 82 lines for Swift package core.

### 3. Replace repeated productivity subagent boilerplate with compact pointers

`productivity-skills/docs/maintainers/codex-subagent-guidance.md` already defines
the shared model, good fits, poor fits, and wording pattern. Individual
maintenance skills only need:

- whether this skill can use read-heavy subagents
- the skill-specific examples of useful worker jobs
- whether apply-mode edits stay in the main thread

Avoid repeating the whole trigger model in every skill. Keep one sentence in the
skill and link the maintainer guidance for the durable policy.

Evidence:

- `maintain-project-readme` lines 47-51 carry a local subagent section.
- The shared maintainer guidance already covers trigger rules, model selection,
  sandbox behavior, good fits, poor fits, and wording pattern.

### 4. Add report-only stale-version detection for high-churn skills

SwiftASB skills contain current-version claims such as `As of SwiftASB v1.6.0`.
Those claims are valuable, but they become expensive and risky when copied
across several large skills.

Add an audit that reports:

- all `As of ... vX.Y.Z` phrases
- all repeated symbol inventories over a threshold
- all SwiftASB skills that mention a current API symbol but do not link to a
  shared reference

Do not block validation until the plugin has a chosen shared-reference shape.

### 5. Define an `.fsx` convention before migrating scripts

The current repo has no `.fsx` files. The best first move is a convention note or
small proof script, not a migration. The convention should answer the roadmap
questions directly:

- place Socket-owned F# scripts under the owning plugin's `scripts/` directory,
  not under root unless the script operates on the Socket superproject
- launch hook scripts through a tiny POSIX wrapper using
  `dotnet fsi --exec <script>.fsx`
- keep repo-local `.dotnet/`, `.nuget/`, and any chosen `DOTNET_CLI_HOME` cache
  path ignored before recommending `.fsx` hooks broadly
- model hook input and output with explicit F# records or discriminated unions
  decoded from JSON
- validate with `dotnet fsi --exec`, a smoke payload, and any repo-level
  formatter or test command the convention chooses
- graduate to a compiled F# console tool when the hook fires often, startup time
  is noticeable, the JSON-RPC client grows, or the script needs packaging and
  tests beyond a single-file proof

Good first `.fsx` candidates:

- report-only skill-surface audits with typed rows and deterministic Markdown or
  JSON output
- hook payload shape experiments where discriminated unions make event handling
  clearer than loosely typed JavaScript objects
- small maintenance scripts in `.NET` or F# repositories where the contributor
  already has the SDK and `dotnet` validation path

Poor first `.fsx` candidates:

- root marketplace validation, which is already Python and test-backed
- Python child metadata validation, which already follows the plugin's `uv`
  baseline
- release automation, where the existing shell/Python split is wired into
  release evidence, marketplace smoke tests, and current maintainer docs
- frequently fired hooks until startup cost is measured against Node and a
  compiled F# tool

Evidence:

- `plugins/codex-utilities/hooks/run-thread-title-hook.sh` currently launches
  the hook with `node`.
- `plugins/codex-utilities/scripts/session-start-hook.mjs` hand-rolls hook JSON
  parsing, environment configuration, App Server JSON-RPC over stdio, state file
  updates, and JSONL logging in one 592-line script.
- `plugins/dotnet-skills/AGENTS.md` treats F# and C# as equal first-party .NET
  choices and prefers F# examples first for neutral examples.
- `plugins/dotnet-skills/skills/build-fsharp-project/SKILL.md` already defines
  the local F# style preferences that would make typed hook event models easier
  to read: explicit modules, domain types, functional data flow, and side
  effects at the edge.

## Medium Changes

### 1. Split SwiftASB current API facts into one loaded reference

Create a reference such as
`plugins/swiftasb-skills/skills/_shared/references/current-api-inventory.md` only
if the skill loader and packaging contract can support shared references, or keep
it under one skill and link it from the others if cross-skill references are
acceptable.

If shared references are not acceptable, keep skill-local references generated
from a shared source, mirroring the Apple Dev Skills pattern.

Per-skill `SKILL.md` files should keep:

- when to use the skill
- what the skill owns
- which source files to inspect
- workflow-specific architecture and UI guidance
- validation and handoff rules
- guardrails unique to that workflow

The shared reference should own:

- current SwiftASB startup and diagnostics surfaces
- library, inventory, filesystem, config, extensions, MCP, and workspace
  companion concepts
- common thread, turn, dashboard, agenda, minimap, recent-history, and review
  surfaces
- generated wire-model boundary
- same-thread turn overlap limitation
- feature policy and feature-operation events

Evidence:

- `build-swiftui-app` and `build-appkit-app` each carry a long current API
  inventory near the top of the skill.
- The same skills repeat similar UI guidance and guardrails for startup errors,
  generated wire models, same-thread overlap, feature-operation events, Apple
  handoffs, and serialized SwiftPM/Xcode validation.
- `diagnose-integration`, `choose-integration-shape`, `build-swift-package`, and
  `explain-swiftasb` repeat related startup, feature-operation, and overlap
  facts.

### 2. Turn repeated validation-command text into plugin-local validation maps

Several language plugins repeat local validation expectations in prose. That is
appropriate when the command choice changes by project shape, but Socket can
still make it cheaper to audit by keeping plugin-local validation maps:

- `plugin`
- `skill`
- `default_validation`
- `side_effect_level`
- `current_docs_required`
- `handoff_skill`

The first implementation can be a Markdown table or JSON/TOML data file consumed
by the proposed audit script. Avoid generating skill prose until the data model
has survived a few maintenance passes.

### 3. Add a scheduled check-only Socket stewardship report

Use the existing automation suitability guidance to create a recurring
report-only automation or a `codex exec` prompt for:

- skill size deltas
- duplicated snippets
- stale version phrases
- placeholder plugin state
- marketplace metadata drift
- custom-agent inventory drift
- child validators missing from expected plugin families

This should produce a report under `docs/agents/` or as a Codex inbox summary,
not edit skills automatically.

Evidence:

- `docs/maintainers/automation-suitability.md` already recommends app
  automations for scheduled reporting and `codex exec` for bounded one-repo
  tasks.

### 4. Prototype `.fsx` only where it reduces prose and untyped branching

If Socket adopts `.fsx`, the most token-efficient use is to move repeated event
shape descriptions and maintenance checklist transformations into typed code,
then let the skill docs say "run this script" with a short contract.

Recommended proof:

1. Add a tiny `scripts/audit_skill_surfaces.fsx` or a plugin-local proof script
   that reads a bounded set of files and emits deterministic JSON.
2. Compare the same task in Python and `.fsx` for line count, startup time,
   dependency setup, error messages, and testability.
3. Only after that comparison, decide whether the first durable `.fsx` home is
   `dotnet-skills`, `codex-utilities`, or root Socket maintainer tooling.

Keep the current `.mjs` hook unless the proof shows F# materially improves the
hook's event model or maintainability. Node is already available in many Codex
plugin environments and has low-friction stdlib JSON, path, process, and stream
support. F# may win on typed event modeling, but `dotnet fsi` startup and SDK
availability are real hook-runtime risks.

## Larger Design Decisions

### 1. Decide whether Socket supports shared skill references

The main blocker to reducing duplicated references is packaging and skill-loader
behavior. If a skill can reliably link to plugin-level shared references, then
Apple snippets and future SwiftASB API inventories can live once. If not, keep
generated skill-local mirrors and validate that every copy matches its source.

Decision needed:

- Canonical shared references with cross-skill links, or
- generated skill-local mirrors with validator-enforced sync.

Risk: Do not remove skill-local files until installed-plugin behavior is proven.
Broken skill-relative links would be worse than extra tokens.

### 2. Decide whether SwiftASB gets a steward role

`docs/agents/bundled-subagent-role-candidates.md` already lists
`swiftasb-skills: swiftasb-steward` as a maybe-later role for read-heavy
integration triage, source-of-truth comparison, and failed-integration diagnosis.
This audit supports that direction, but not as a first quick win.

Good first role jobs:

- compare SwiftASB skills against current SwiftASB source files
- inventory repeated current API facts
- collect failed-integration evidence for the main thread

Do not bundle it until SwiftASB has a shared-reference or generated-mirror plan,
otherwise the role may only point at the same duplication without reducing it.

### 3. Decide whether placeholder plugins should have periodic retirement checks

`android-dev-skills` and `spotify` remain placeholder directories. They are
clearly marked as placeholders in root docs and candidate-role docs. A recurring
stewardship report should include them so they do not silently become stale
catalog clutter, but there is no evidence that they should be deleted in this
audit.

### 4. Decide whether `.fsx` belongs to `dotnet-skills` or `codex-utilities`

There are two plausible ownership models:

- `dotnet-skills` owns the authoring convention because `.fsx` is a .NET/F#
  runtime choice.
- `codex-utilities` owns hook-specific conventions because hook event payloads,
  App Server JSON-RPC, and runtime data paths are Codex utility concerns.

Recommendation: split the ownership. Put general `.fsx` style, validation, and
project-shape guidance in `dotnet-skills`; put Codex hook payload contracts and
runtime-data conventions in `codex-utilities`. Avoid a root Socket scripting
policy until at least one proof exists.

## Do Not Consolidate Yet

- Do not collapse Apple docs freshness rules into generic "check docs" language.
  Apple, Expo, OpenAI, and SwiftASB surfaces drift for different reasons and need
  local current-docs gates.
- Do not merge server-side Swift back into Apple Dev Skills. The roadmap keeps
  SwiftPM-first service work separate from Xcode/app workflows for good reason.
- Do not turn `maintain-project-repo` into a bundled worker. The existing
  candidate-role doc correctly keeps it as a main-thread orchestrator because it
  owns install, validation, release, and write-capable decisions.
- Do not remove skill-local Apple snippet copies until the installed plugin
  loader is verified against shared plugin-level reference paths.
- Do not migrate Python validators to `.fsx` just to make F# visible. Existing
  Python scripts have tests, `uv` dependency flow, and repo-local precedent.
- Do not migrate the current Node hook to `.fsx` until `dotnet fsi --exec`
  startup, SDK availability, cache behavior, and hook trust UX are measured.
- Do not automate write-heavy Swift source organization without human-approved
  slices and PR boundaries.

## Recommended Next Steps

1. Add Apple snippet sync check mode and wire it into Apple child validation.
2. Draft a SwiftASB shared-reference or generated-mirror plan, then shrink one
   SwiftASB skill as a proof of shape.
3. Add an `.fsx` convention proposal and one small report-only proof script, then
   compare it against Python and the current Node hook before recommending
   migrations.
4. Compact productivity subagent sections to skill-specific examples plus a
   shared-guidance pointer.
5. Add a check-only Socket stewardship automation around
   `scripts/audit_skill_surfaces.py`, so future token and drift issues are found
   without hand-scanning.

## Validation

This report is a docs-only proposal. Run root metadata validation after adding
the file. After adding the audit script, also run the focused script tests:

```bash
uv run pytest tests/test_audit_skill_surfaces.py
uv run scripts/audit_skill_surfaces.py --top 5
uv run scripts/validate_socket_metadata.py
```
