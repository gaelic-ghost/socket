# Project Roadmap

## Current Milestone
- ID: M1
- Name: Skill Roadmap Baseline
- Status: In Progress
- Target Version: v0.1.0
- Last Updated: 2026-02-27
- Summary: Establish a repository-root roadmap covering each in-repo skill and track immediate behavior improvements for `talktomepy-tts`.

## Milestones
| ID | Name | Target Version | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1 | Skill Roadmap Baseline | v0.1.0 | In Progress | 2026-03-13 | Add roadmap sections for each skill and define near-term improvements. |

## Skill Sections

### `project-roadmap-manager`
- Maintain `ROADMAP.md` as the single canonical milestone record.
- Keep `Current Milestone`, `Milestones`, `Plan History`, and `Change Log` synchronized.

### `talktomepy-tts`
- Continue improving ambiguous invocation text-selection behavior.
- TODO: Investigate and fix the `speak_with_talktomepy.sh` false health-check failure where `/health` is reachable manually but the script times out in `wait_for_service_healthy`.
- Improve summarization behavior for long source text by offering:
  - Summarize the full text.
  - Summarize section-by-section.
  - Summarize only selected sections that are suited to summarization while leaving low-value-to-summarize sections intact.

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
