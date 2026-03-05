# Skill Routing Matrix

## Domain Mapping

| Intent signal | Primary skill | Optional secondary skill |
| --- | --- | --- |
| Roadmap planning, milestone updates, ROADMAP.md maintenance | `project-roadmap-maintainer` | `project-docs-maintainer` |
| Docs drift, README standards, docs alignment audits | `project-docs-maintainer` | `project-roadmap-maintainer` |
| Things reminders, rescheduling, update-vs-create todo mutation | `things-reminders-manager` | `things-digest-generator` |
| Things weekly planning digest, priorities, week-ahead summary | `things-digest-generator` | `things-reminders-manager` |
| Workspace cleanup chores, stale artifacts, disk hygiene ranking | `project-workspace-cleaner` | `project-docs-maintainer` |

## Install Guidance

When a selected skill is unavailable, output:

```bash
npx skills add gaelic-ghost/productivity-skills --skill <skill-name>
```

For multi-skill composition, output one command per missing skill.

## Example Response Shape

- `Selected Skill`: `project-docs-maintainer`
- `Why`: Request asks for README/docs alignment across repositories.
- `Install (if needed)`: `npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer`
- `Next Prompt`: Use `$project-docs-maintainer` with `mode=skills_readme_alignment` and workspace path.
