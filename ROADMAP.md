# Project Roadmap

## Current Milestone
- ID: M1
- Name: Skill Roadmap Baseline
- Status: In Progress
- Target Version: v0.1.0
- Last Updated: 2026-02-27
- Summary: Establish a repository-root roadmap covering each in-repo skill and track current maintenance priorities.

## Milestones
| ID | Name | Target Version | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1 | Skill Roadmap Baseline | v0.1.0 | In Progress | 2026-03-13 | Add roadmap sections for each skill and define near-term improvements. |
| M2 | Things MCP Reminder Reliability | v0.2.0 | Planned | 2026-03-16 | Add deterministic Things reminder wrapper workflow with auth-first update path and duplicate prevention. |

## Skill Sections

### `project-roadmap-manager`
- Maintain `ROADMAP.md` as the single canonical milestone record.
- Keep `Current Milestone`, `Milestones`, `Plan History`, and `Change Log` synchronized.

### `things-week-ahead-digest`
- Refine weekly digest output for stronger prioritization and clearer next-action recommendations.
- Expand handling of checklist-like notes and project-level rollups.

### `things-mcp-reminder-wrapper`
- Enforce auth-first, update-first reminder mutations for Things MCP workflows.
- Normalize relative date language to explicit local dates before mutation.
- Prevent silent duplicate creation when update intent is clear.

### `workspace-cleanup-audit`
- Improve issue ranking and severity rationale for cleanup findings.
- Add clearer grouping by repository and artifact type for faster triage.

## Plan History
### 2026-02-27 - Accepted Plan (v0.1.0 / M1)
- Scope:
  - Create repository-root roadmap with sections for each skill in this repo.
- Acceptance Criteria:
  - `ROADMAP.md` exists at repository root.
  - The file contains a section for each skill currently in the repo.
- Risks/Dependencies:
  - Skill inventory changes over time and will require roadmap updates.

## Change Log
- 2026-02-27: Initialized repository roadmap and added per-skill sections.
- 2026-03-01: Added M2 planning and skill section for things-mcp-reminder-wrapper.
