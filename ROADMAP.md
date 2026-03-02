# Project Roadmap

## Current Milestone
- ID: M7
- Name: Claude Code Compatibility Completion
- Status: Planned
- Target Version: v1.7.0
- Last Updated: 2026-03-01
- Summary: Complete end-to-end Claude Code compatibility for grouped/nested skill packaging and compatibility signaling across repository metadata and release docs.

## Milestones
| ID | Name | Target Version | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1 | Initial Apple Skill Bundle | v1.0.0 | Completed | 2026-02-27 | Initial four-skill repository baseline. |
| M2 | Portability and Customization Docs | v1.1.x | Completed | 2026-02-27 | Portability cleanup and per-skill customization docs for the original bundle. |
| M3 | Automation Prompt Support | v1.2.0 | Completed | 2026-02-27 | Automation prompt templates added to the original four skills. |
| M4 | Hybrid Apple/Xcode Workflow Suite | v1.3.0 | Completed | 2026-02-28 | Added orchestrator, MCP-first executor, CLI fallback, and safety/docs skills. |
| M5 | Discovery and README Polish | v1.4.x | Completed | 2026-02-28 | README discoverability and link/wording cleanup through `v1.4.2`. |
| M6 | Readiness and Documentation Parity | v1.5.0 | Completed | 2026-03-01 | Roadmap established, P1 docs parity merged, and P2 CI validation guardrail merged. |
| M7 | Claude Code Compatibility Completion | v1.7.0 | Planned | 2026-03-15 | Ensure full Claude Code/plugin-manifest compatibility for nested skill packs and keep release/docs compatibility signaling synchronized. |

## Plan History
### 2026-02-28 - Accepted Plan (v1.5.0 / M6)
- Scope:
  - Create root `ROADMAP.md` as the canonical milestone tracker.
  - Confirm post-`v1.3.0` documentation coverage and release-note continuity.
  - Prioritize next tasks before starting new feature work.
- Acceptance Criteria:
  - `ROADMAP.md` exists in the repo root and has synchronized `Current Milestone` and `Milestones`.
  - Top-priority follow-up work is ranked with rationale.
- Risks/Dependencies:
  - Documentation drift risk if new skills ship without matching README/customization guidance.
  - Release traceability risk if README highlights lag behind tags/releases.

### 2026-02-28 - Accepted Plan Update (v1.5.0 / M6)
- Scope:
  - Add lightweight GitHub Actions validation for roadmap presence, skill layout requirements, and README/latest-tag continuity.
- Acceptance Criteria:
  - A CI workflow runs on push/PR and fails when required docs or skill files are missing.
- Risks/Dependencies:
  - Checks may need refinement if repository structure changes.

## Change Log
- 2026-02-28: Initialized roadmap for repository status and next-priority planning.
- 2026-02-28: Closed P1 documentation parity (missing per-skill READMEs + root README v1.4.x highlights).
- 2026-02-28: Started P2 by adding CI guardrail workflow for roadmap/docs/skill-structure drift checks.
- 2026-03-01: Completed M6 after merging P2 CI guardrails and synchronizing roadmap status.
- 2026-03-01: Added M7 to track full Claude Code compatibility for nested skill-pack/plugin-manifest workflows.
