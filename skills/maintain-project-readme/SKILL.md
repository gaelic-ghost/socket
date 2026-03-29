---
name: maintain-project-readme
description: Maintain ordinary software-project README.md files through a focused audit-first workflow. Use when a project README needs clearer overview, setup, usage, development, or verification guidance. Do not use this for agent-skills, Codex plugin, Claude plugin, or similar skills or plugin repositories with specialized install and discoverability sections.
---

# Maintain Project README

Maintain ordinary software-project `README.md` files through one focused README workflow.

## Inputs

- Required: a target `README.md` path or project root
- Optional: whether the user wants audit-only findings or bounded edits
- Optional: repo context such as app type, setup flow, commands to run, and intended audience

## Workflow

1. Inspect the current README and the nearby project structure before proposing changes.
2. Identify the minimum sections needed for the project to be understandable and usable.
3. Prefer audit-first findings when the user is exploring.
4. When edits are requested, keep changes bounded to the README and preserve intentional structure that already works.
5. Keep setup, usage, development, and verification guidance concrete, readable, and consistent with the repo.
6. If the repository is a skills or plugin repo with specialized install and discoverability conventions, use `maintain-skills-readme` instead.

## Output Contract

- Return a concise audit or change plan in Markdown.
- When proposing edits, call out the missing or unclear README responsibilities in practical terms.
- If the README is already sound for its project type, say so plainly.

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, setup steps, or support claims that are not grounded in the repo.
- Do not use this skill for agent-skills, Codex plugin, Claude plugin, or similar skills/plugin repositories. Use `maintain-skills-readme` instead.

## References

- `agents/openai.yaml`
