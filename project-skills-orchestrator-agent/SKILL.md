---
name: project-skills-orchestrator-agent
description: Route user requests to the best matching skill in this repository and provide install guidance when capabilities are missing. Use when users need help choosing, composing, or installing skills for roadmap management, docs maintenance, Things workflows, or workspace cleanup.
---

# Project Skills Orchestrator Agent

Use this skill as the front door for skill selection and composition.

## Workflow

1. Classify user intent by domain.
2. Select one primary skill and optional secondary skill.
3. If the capability is missing in current environment, output exact install command(s).
4. Do not auto-install skills.
5. Ask user to confirm installation before proceeding.

## Routing Output Format

Return these sections in order:

- `Selected Skill`
- `Why`
- `Install (if needed)`
- `Next Prompt`

## Install Command Template

Use this exact command format:

```bash
npx skills add gaelic-ghost/productivity-skills --skill <skill-name>
```

Never claim installation success until user confirms completion.

## Active Skills

- `project-docs-maintainer`
- `project-roadmap-maintainer`
- `project-workspace-cleaner`
- `things-reminders-manager`
- `things-digest-generator`

Use `references/skill-routing-matrix.md` for domain-to-skill mapping and composition patterns.
