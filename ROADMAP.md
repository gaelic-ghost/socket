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

## Skill Sections

### `project-roadmap-manager`
- Maintain `ROADMAP.md` as the single canonical milestone record.
- Keep `Current Milestone`, `Milestones`, `Plan History`, and `Change Log` synchronized.

### `talktomepy-tts`
- Status: Deprecated (legacy-only)
- Do not schedule new feature work.
- Keep existing behavior stable for backward compatibility only.
- Route new speech workflow investment to successor capabilities in `a11y-skills`.

### `things-week-ahead-digest`
- Refine weekly digest output for stronger prioritization and clearer next-action recommendations.
- Expand handling of checklist-like notes and project-level rollups.

### `workspace-cleanup-audit`
- Improve issue ranking and severity rationale for cleanup findings.
- Add clearer grouping by repository and artifact type for faster triage.

## Plan History
### 2026-02-27 - Accepted Plan (v0.1.0 / M1)
- Scope:
  - Create repository-root roadmap with sections for each skill in this repo.
  - Record near-term roadmap item for `talktomepy-tts` summarization improvements.
- Acceptance Criteria:
  - `ROADMAP.md` exists at repository root.
  - The file contains a section for each skill currently in the repo.
  - The `talktomepy-tts` section includes the requested summarization enhancement options.
- Risks/Dependencies:
  - Skill inventory changes over time and will require roadmap updates.

## Change Log
- 2026-02-27: Initialized repository roadmap and added per-skill sections, including `talktomepy-tts` summarization enhancements.
- 2026-02-27: Added TODO to investigate/fix `talktomepy-tts` script health-check timeout mismatch.
- 2026-02-28: Marked `talktomepy-tts` as deprecated and redirected new speech workflow work to successor paths.
