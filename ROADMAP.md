# Project Roadmap

## Current Milestone
- ID: M11
- Name: Documentation Maintenance Cadence
- Status: Completed
- Target Version: v3.2.1
- Last Updated: 2026-03-06
- Summary: Align root docs and maintainer validation with the actual `docs/maintainers/` contract, add a durable reality-audit guide, and keep the three-skill surface unchanged.

## Milestones
| ID | Name | Target Version | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1 | Initial Apple Skill Bundle | v1.0.0 | Completed | 2026-02-27 | Initial four-skill repository baseline. |
| M2 | Portability and Customization Docs | v1.1.x | Completed | 2026-02-27 | Portability cleanup and per-skill customization docs for the original bundle. |
| M3 | Automation Prompt Support | v1.2.0 | Completed | 2026-02-27 | Automation prompt templates added to the original four skills. |
| M4 | Hybrid Apple/Xcode Workflow Suite | v1.3.0 | Completed | 2026-02-28 | Added orchestrator, MCP-first executor, CLI fallback, and safety/docs skills. |
| M5 | Discovery and README Polish | v1.4.x | Completed | 2026-02-28 | README discoverability and link/wording cleanup through `v1.4.2`. |
| M6 | Readiness and Documentation Parity | v1.5.0 | Completed | 2026-03-01 | Roadmap established, docs parity merged, and CI validation guardrails merged. |
| M7 | Claude Code Compatibility Completion | v1.7.0 | Completed | 2026-03-01 | Added grouped nested plugin manifest support. |
| M8 | Canonical Skill v2.0.0 Consolidation | v2.0.0 | Completed | 2026-03-05 | Consolidated the repository around canonical Apple skills and extracted the shared Swift/Apple snippet. |
| M9 | AGENTS Sync Skill Retirement | v3.0.0 | Completed | 2026-03-05 | Removed `apple-swift-package-agents-sync` from the active surface and replaced it with snippet-first guidance plus external docs-alignment recommendations. |
| M10 | Top-Level Skill Reset | v3.2.0 | Completed | 2026-03-05 | Removed `apple-skills-router`, restored three independent top-level skills, and kept maintainer docs separate from skill-operational docs. |
| M11 | Documentation Maintenance Cadence | v3.2.1 | Completed | 2026-03-06 | Fixed stale maintainer-doc path assumptions, added a canonical reality-audit guide, and realigned validation with `docs/maintainers/`. |
| M12 | Ongoing Audit Reporting | v3.2.x | Planned | 2026-03-13 | Refine the recurring maintainer audit/report cadence now that the canonical maintainer-doc contract is in place. |

## Plan History
### 2026-03-05 - Accepted Plan (M8 -> M9 Transition)
- Scope:
  - Keep `apple-swift-package-bootstrap` deterministic `AGENTS.md` generation.
  - Align bootstrap AGENTS template language with shared `apple-swift-core.md` baseline.
  - Remove `apple-swift-package-agents-sync` and replace routing/docs with explicit migration guidance.
  - Track removal as breaking change for `v3.0.0`.
- Acceptance Criteria:
  - Active skill surface reduced from 5 to 4.
  - README, routing references, and plugin manifest no longer publish sync skill install paths.
  - Migration section explicitly points users to `apple-swift-core.md` snippet and external docs-alignment skills.
  - Validation script passes and stale references are limited to intentional migration notes.
- Risks/Dependencies:
  - Existing users pinned to removed skill name require clear migration notes.
  - Documentation and marketplace index must stay in lockstep to avoid discovery drift.

### 2026-03-05 - Accepted Plan (M10 Documentation Cleanup)
- Scope:
  - Rewrite each active `SKILL.md` to a shared section order.
  - Standardize automation, customization, and handoff contract language.
  - Align root docs and the repository report with the active four-skill surface.
- Acceptance Criteria:
  - Every active `SKILL.md` uses the canonical section order.
  - Every customization knob is labeled `policy-only` or `runtime-enforced`.
  - Root docs no longer describe retired skills as active.
  - Repo-wide docs use one contract vocabulary for inputs, outputs, fallback, and handoff.
- Risks/Dependencies:
  - Root docs, skill docs, and metadata must land together to avoid temporary drift.
  - Public skill identifiers remain stable unless a rename is clearly justified.

### 2026-03-05 - Accepted Plan (M10 Naming-First Workflow Straightening)
- Scope:
  - Rename the public skills to a consistent `apple-<domain>-<purpose>` pattern.
  - Change crossed workflow statuses into `status` plus `path_type`.
  - Recast secondary behavior as guard, fallback, or handoff instead of peer primary workflows.
- Acceptance Criteria:
  - Old skill IDs remain only in migration notes.
  - Every active `SKILL.md` has one numbered primary workflow.
  - Every active skill documents `status` and `path_type`.
  - Router install guidance, Xcode mutation handling, and Dash stage progression are documented in straight non-crossed paths.
- Risks/Dependencies:
  - Renames require root docs, metadata, references, and runtime `SKILL_NAME` constants to land together.
  - Users pinned to old IDs need explicit migration notes.

### 2026-03-05 - Accepted Plan (M10 Router Removal and Three-Skill Reset)
- Scope:
  - Remove `apple-skills-router` entirely from the active surface.
  - Keep `apple-xcode-workflow`, `apple-dash-docsets`, and `apple-swift-package-bootstrap` as parallel top-level skills.
  - Separate maintainer docs from skill-operational docs and keep each installed skill standalone.
- Acceptance Criteria:
  - Active skill surface reduced from 4 to 3.
  - Root docs no longer imply any Apple orchestrator or default front door.
  - Each remaining skill can recommend local end-user AGENTS guidance and the other relevant top-level skills directly.
  - Validation passes with only the three remaining skills.
- Risks/Dependencies:
  - Historical migration notes must remain clear without implying the router is still active.
  - Skill-local docs must not depend on repo-root maintainer docs for operation.

### 2026-03-06 - Accepted Plan (M11 Repo Reality Audit and Documentation Alignment)
- Scope:
  - Treat the current skills, scripts, and passing tests as the source of truth for maintainer-facing docs.
  - Align root docs and maintainer-doc links to the canonical `docs/maintainers/` layout.
  - Repair the repo docs validator so it checks the canonical maintainer docs instead of a stale root-level `WORKFLOWS.md`.
  - Add a durable reality-audit guide for future documentation checks.
- Acceptance Criteria:
  - Root docs resolve to the actual maintainer-doc files on disk.
  - Repo docs validation passes without requiring a root-level `WORKFLOWS.md`.
  - Test health remains unchanged after documentation-only edits.
  - The active public skill surface remains the same three top-level skills.
- Risks/Dependencies:
  - Root docs, maintainer docs, and validation rules must change together to avoid new drift.
  - Historical roadmap notes must remain clearly historical and not imply the pre-fix drift is still current.

## Change Log
- 2026-02-28: Initialized roadmap for repository status and next-priority planning.
- 2026-02-28: Closed documentation parity follow-ups and added CI guardrail workflow.
- 2026-03-01: Completed M6 and added M7 for plugin compatibility work.
- 2026-03-05: Started M8 to deliver canonical v2.0.0 naming and consolidation.
- 2026-03-05: Expanded M8 scope to include AGENTS consolidation planning and recorded v3.0.0 sync-skill retirement milestone (M9).
- 2026-03-05: Completed M8 and M9 in the active repository surface.
- 2026-03-05: Started M10 to normalize contracts, handoffs, and policy/runtime wording across active docs.
- 2026-03-05: Expanded M10 to rename public skills for naming consistency and to straighten workflow roles across the active skill surface.
- 2026-03-05: Expanded M10 again to remove the router layer and restore three independent top-level skills.
- 2026-03-05: Completed M10 with the three-skill top-level surface and router removal.
- 2026-03-06: Completed M11 by aligning root docs and maintainer validation to the canonical `docs/maintainers/` layout and adding a reality-audit guide.
