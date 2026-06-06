# Swift Steward Subagent Plan

## Purpose

Define a first Codex subagent role for Swift repository maintenance work in
Socket-hosted plugins. The role should let the main Codex session delegate
read-heavy repo maintenance, guidance-sync discovery, and draft-patch planning
while the main thread stays focused on decisions, edits, and user review.

This is a durable building-block change, not a background service. The first
version should be a bounded Codex custom-agent contract plus skill guidance.
Repo-local Python, OpenAI Agents SDK, or LangGraph implementations can come
later only when a target repository needs durable state, checkpoints, retry
behavior, or a repeatable CLI surface.

## Recommendation

Use a Codex subagent role first.

The first role should live in `apple-dev-skills` as `swift-steward`. It should
handle SwiftPM, Xcode, DocC, Apple docs, AGENTS guidance, and
`maintain-project-repo` readiness scans. It should return findings and draft
patch plans to the main agent rather than applying edits itself.

Add a sibling `server-swift-steward` role in `server-side-swift` for server-side
Swift repositories. That role should handle Vapor, Hummingbird, Swift OpenAPI,
persistence, Docker, Apple Containerization, Linux portability, and server docs
drift without moving server concerns into Apple Dev Skills.

## Not Chosen

Do not start with LangGraph for the plugin-level role. LangGraph is a better fit
when the workflow needs long-running persisted state, explicit graph
transitions, human-in-the-loop pauses, and resume behavior. The plugin-level
first slice needs in-run delegation and reviewable output, so a Codex subagent
role is smaller and easier to reason about.

Do not start with an OpenAI Agents SDK service. A service would own tools,
guardrails, state, tracing, and approval flow in application code. The current
workflow can be expressed as a Codex role contract plus existing skills.

Do not make the subagent an apply-mode editor yet. Draft patches are useful, but
the first safe version should return patch plans or proposed diffs for the main
agent and Gale to review before any file changes are applied.

## Role Boundaries

`swift-steward` owns read-heavy discovery for Apple and Swift repositories:

- classify the repository as SwiftPM, Xcode app, mixed, DocC-heavy, or unclear
- inspect `AGENTS.md`, README, CONTRIBUTING, ROADMAP, DocC catalogs, package
  manifests, Xcode markers, and repo-maintenance scripts
- compare current guidance against the relevant Apple Dev Skills workflow
- identify whether `sync-swift-package-guidance`,
  `sync-xcode-project-guidance`, `author-swift-docc-docs`, or a build/test
  workflow should own the next edit
- return draft patch plans, affected files, validation commands, and blockers

`server-swift-steward` owns read-heavy discovery for server-side Swift
repositories:

- classify the repository as Vapor, Hummingbird, OpenAPI-backed, persistence
  heavy, Dockerized, Apple-container focused, or unclear
- inspect package manifests, run commands, service entrypoints, migrations,
  Dockerfiles, Compose files, OpenAPI specs, docs, and repo-maintenance scripts
- compare current guidance against Server-Side Swift skills and official
  framework docs
- return draft patch plans, affected files, validation commands, and blockers

`productivity-skills` remains the owner for general repo-document maintenance
and `maintain-project-repo` installation or refresh behavior. The steward role
should delegate to those skills instead of duplicating their apply-mode logic.

## Trigger Policy

Codex should use these roles when Gale explicitly asks for subagents, asks to
use `swift-steward` or `server-swift-steward`, or asks for broad guidance sync
or repo maintenance and the active skill tells the main agent to ask before
delegation.

Good trigger phrases include:

- "sync guidance while we keep working"
- "do repo maintenance with a subagent"
- "use swift-steward"
- "prepare draft patches for guidance sync"
- "check this Swift repo for maintenance drift"

The main agent should keep final write ownership. A steward subagent may return
draft patches, but the main agent should review, edit, save for later, or apply
them only after the user approves that step.

## Model Policy

Set the first steward roles to `model = "gpt-5.4-mini"` because their initial
contract is bounded, read-heavy exploration and draft patch planning. This is a
role-local default, not a global Codex rule: harder synthesis, ambiguous
debugging, security-sensitive reasoning, or write-plan ownership can still use a
stronger model or omit the model field so the parent session decides.

## Output Contract

Each steward run should return:

- repo classification and confidence
- documents, manifests, scripts, and docs sources inspected
- findings grouped by owning skill or workflow
- draft patch plan or proposed diff summary
- validation commands to run after applying any patch
- blockers, ambiguity, and required user decisions

The worker should return concise evidence and file references, not raw command
logs or long exploratory transcripts.

## Safety

- Keep the first version read-heavy and report-first.
- Do not run release, tag, publish, subtree, or branch-cleanup workflows from a
  steward worker.
- Do not apply patches from the worker thread unless Gale explicitly requests
  parallel implementation and the write scope is disjoint.
- Do not invent plugin manifest support for custom agents until Codex documents
  that installed plugins expose custom-agent files directly.
- If a draft patch is useful, return it as a reviewable artifact for the main
  agent to apply with normal repository validation.

## Implementation Slices

1. Add project-scoped custom-agent draft files in the child plugin roots so the
   role contract is concrete and reviewable.
2. Teach `sync-swift-package-guidance` and `sync-xcode-project-guidance` when to
   ask for or use `swift-steward` for broad discovery.
3. Add similar server-side guidance once a server-side repo-maintenance or
   guidance-sync workflow exists there.
4. Add draft-patch report generation after the role contract is stable.
5. Consider a repo-local LangGraph sidecar only for a specific repository that
   needs persisted maintenance state, resumable handoffs, or repeated CLI
   commands.

## Sources

- OpenAI Codex Subagents: <https://developers.openai.com/codex/subagents>
- OpenAI Codex Subagent concepts:
  <https://developers.openai.com/codex/concepts/subagents>
- OpenAI GPT-5.4 mini model:
  <https://developers.openai.com/api/docs/models/gpt-5.4-mini>
- LangGraph overview: <https://docs.langchain.com/oss/python/langgraph>
- LangGraph persistence:
  <https://docs.langchain.com/oss/python/langgraph/persistence>
- LangGraph durable execution:
  <https://docs.langchain.com/oss/python/langgraph/durable-execution>
