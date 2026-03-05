---
name: apple-skills-router-advise-install
description: Route Apple development requests to the correct Apple skills bundle skill and advise precise installation commands when the required skill is missing. Use when users need help composing skills, selecting the right skill, or installing missing skills from this repository.
---

# Apple Skills Router Advise Install

Use this skill to route intent and provide install guidance for missing skills.

## Routing Table

- Xcode, Swift execution, MCP/CLI fallback, mutation safety, docs routing -> `$apple-xcode-workflow-execute`
- Dash docset search/install/generation -> `$apple-dash-docset-manage`
- Bootstrap new Swift package repos -> `$apple-swift-package-bootstrap`
- Sync canonical AGENTS across Swift package repos -> `$apple-swift-package-agents-sync`

## Install Advisory Workflow

1. Identify required skill from intent.
2. If available, route directly to that skill.
3. If missing, provide exact install command:
- `npx skills add gaelic-ghost/apple-dev-skills --skill <skill-name>`
4. Offer pack-level installation when it reduces friction.

## Pack Suggestions

- Xcode workflow pack:
  - `npx skills add gaelic-ghost/apple-dev-skills --skill apple-xcode-workflow-execute`
- Dash docs pack:
  - `npx skills add gaelic-ghost/apple-dev-skills --skill apple-dash-docset-manage`
- Swift package pack:
  - `npx skills add gaelic-ghost/apple-dev-skills --skill apple-swift-package-bootstrap --skill apple-swift-package-agents-sync`

## Constraints

- Do not claim implicit runtime installation APIs.
- Use documented CLI-driven install guidance.
- Keep recommendations explicit and copy-paste ready.

## References

- `references/routing-matrix.md`
- `references/install-commands.md`
- `references/customization-flow.md`

## Interactive Customization Flow

1. Load effective settings:
- `uv run python scripts/customization_config.py effective`

2. Ask targeted routing/pack preference questions with `references/customization-flow.md`.

3. Persist approved overrides:
- `uv run python scripts/customization_config.py apply --input <yaml-file>`

4. Re-check effective settings:
- `uv run python scripts/customization_config.py effective`
