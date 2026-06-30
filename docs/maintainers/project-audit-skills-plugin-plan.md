# Project Audit Skills Plugin Plan

This plan records a possible Socket child plugin for exploring, mapping,
auditing, grading, and evaluating unfamiliar projects.

Working name: `project-audit-skills`.

The playful internal motivation is "evaluate this project for slop," but the
installable plugin should use professional outward-facing language such as
project audit, intake, quality map, risk grade, and remediation plan.

## Intent

The plugin should help an agent enter a new repository or project and produce a
useful map before making changes.

It should answer:

- What is this project?
- How is it structured?
- What are the real entry points, build commands, tests, docs, and release
  surfaces?
- Which parts look healthy, stale, risky, overcomplicated, underdocumented, or
  likely to waste future work?
- What should Gale do first if they want to maintain, refactor, adopt, migrate,
  rescue, or discard it?

## Scope

The first version should be a guidance plugin, not a runtime scanner.

It may use existing repo tools, language-specific skills, and validation
commands, but it should not bundle a daemon, MCP server, static-analysis engine,
or language-specific parser framework until repeated use proves that one is
worth the extra surface.

## Relationship To Existing Plugins

`productivity-skills` already owns ongoing project maintenance workflows such as
README, contributing, roadmap, accessibility, repo maintenance, GitHub settings,
automation design, and eval design.

`project-audit-skills` should own the earlier intake phase:

- unknown or newly inherited projects
- "tell me what this is" exploration
- quality and risk grading before implementation
- adoption or rescue decisions
- slop or overengineering detection before committing to a fix

Language and stack details should be delegated:

- Swift and Apple platform details to `swift-lang`, `apple-dev-skills`, or
  `server-side-swift`
- Python details to `python-skills`
- Rust details to `rust-skills`
- JVM details to `server-side-jvm`
- Android details to `android-dev-skills`
- web and Expo details to `web-dev-skills`
- binary artifact details to `reverse-engineering-skills`

## Proposed Skill Inventory

### `project-audit:explore-project`

Map a project without changing it.

Output should include repo shape, languages, package managers, entry points,
important docs, validation commands, external services, secrets boundaries, and
unknowns.

### `project-audit:map-architecture`

Describe how the project is put together.

Output should include modules, ownership boundaries, dependency direction,
runtime flows, data flows, UI or API boundaries, persistence, background work,
and places where the structure hides behavior.

### `project-audit:audit-project-quality`

Grade maintainability and implementation quality.

Output should separate evidence from judgment and cover structure, naming,
tests, docs, validation, dependency health, dead code, generated code, secrets,
accessibility, observability, and release readiness.

### `project-audit:evaluate-adoption-risk`

Support go/no-go decisions.

Output should name adoption risk, maintenance cost, likely first fixes, blocked
validation, dependency or licensing concerns, and the smallest proof needed
before investing more time.

### `project-audit:plan-remediation`

Turn an audit into an ordered cleanup plan.

Output should group work into small coherent slices, identify validation for
each slice, route stack-specific work to owning skills, and stop before making
changes unless the user asks to implement.

## Grading Model

Use explicit grades only when they help the decision.

Recommended grade axes:

- discoverability
- build and test readiness
- architecture clarity
- dependency and toolchain hygiene
- data and state-flow clarity
- risk concentration
- documentation usefulness
- release or deployment readiness
- "slop risk" as an internal shorthand for needless complexity, copy-pasted
  wrappers, unclear ownership, stale generated output, vague logs, or brittle
  automation

Grades should always include evidence and concrete next actions. Never return a
score without explaining which files, commands, or observations justify it.

## First Implementation Slice

- Create `plugins/project-audit-skills/` with `.codex-plugin/plugin.json`,
  `AGENTS.md`, and authored `skills/`.
- Add `project-audit:explore-project` and
  `project-audit:audit-project-quality` first.
- Keep the root marketplace entry `NOT_AVAILABLE` until at least those two real
  skills exist and validation passes.
- Update root README, TODO, and this plan when the plugin becomes installable.
- Run `uv run scripts/validate_socket_metadata.py` after wiring the marketplace
  entry.

## Open Questions

- Should the long-term home be a new child plugin or a focused expansion of
  `productivity-skills`?
- Should grading output be a Markdown report only, or should it also support a
  small JSON shape for future Socket Steward ingestion?
- Should "slop risk" remain internal wording, or should there be a user-facing
  "complexity risk" grade with the same practical meaning?
- Which existing Socket Steward audit outputs should seed the first examples?
