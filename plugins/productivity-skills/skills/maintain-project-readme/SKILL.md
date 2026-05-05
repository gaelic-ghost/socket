---
name: maintain-project-readme
description: Maintain README.md files against a hard-enforced canonical base schema with deterministic check-only and bounded apply modes. Use when a repository README needs a durable baseline structure that downstream plugins or repo-specific customization can extend without weakening the shared README contract.
---

# Maintain Project README

Maintain `README.md` files through one deterministic base-template workflow.

This skill is the primary layer for README maintenance. It defines the canonical shared README contract that downstream language-, framework-, stack-, or repository-specific customization can adapt through explicit extension, instead of ad hoc structure drift.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--readme-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `README.md`.
2. Load the canonical README schema from the built-in template config, then merge any explicit customization override.
3. In `check-only`, audit title and summary requirements, top-level section names and order, required subsection names, the required table of contents, and placeholder-style content.
4. In `apply`, keep edits bounded to the target `README.md` while normalizing the README into the configured canonical structure.
5. Preserve preamble material such as badges, callouts, screenshots, and extra intro prose before the first H2 while normalizing the structural contract around it.
6. When bootstrapping a missing `README.md`, ask the user for text for `Overview > Status`, `Overview > What This Project Is`, and `Overview > Motivation` before writing those subsections.
7. Use the bundled README template when bootstrapping a missing `README.md` or when a downstream workflow needs a canonical starter document; if the user has not provided text for any Overview subsection, leave that subsection body exactly `TBD`.
8. Re-run the same audit to confirm post-fix status.
9. For skills, plugin, or hybrid repositories, keep the same hard-enforced schema while grounding install, discovery, packaging, and maintainer wording in the real repo surface instead of inventing ordinary-app sections that are not actually shipped.

## Writing Expectations

- `README.md` is product-focused: write it for end users, evaluators, integrators, and their agents who need to understand what the project is, whether it fits, how to try it, and where the shipped surface lives.
- Contributor, maintainer, release, validation, branch, review, and local development procedures belong in `CONTRIBUTING.md` or a linked maintainer document. In `README.md`, keep only the shortest useful pointer to that contributor path.
- Keep the whole README near 250 lines or less by default. Treat 300 lines as a soft ceiling that should trigger consolidation unless the user explicitly wants a long-form README.
- Keep most generated or agent-edited top-level sections near 40 lines or less. Split or hoist content only when it clarifies ownership; otherwise trim repetition and link to the canonical owner.
- The user-authored `Overview` subsections may be longer when the user supplies that text. Do not shorten `Overview > Status`, `Overview > What This Project Is`, or `Overview > Motivation` unless the user explicitly asks.
- `Overview > Status`, `Overview > What This Project Is`, and `Overview > Motivation` must be written by the user in the user's own words, never by the agent.
- If one of those Overview subsections already contains text, leave that text intact and untouched unless the user explicitly provides replacement text for that exact subsection.
- If one of those Overview subsections is empty or missing, set the subsection body to exactly `TBD`; for new README files, ask the user for text to place there before falling back to `TBD`.
- `Quick Start` should stay human-focused, short, concise, and end-user friendly, or explicitly say the project is still too early for a real quick start and direct curious readers to `Development`.
- `Usage` should stay human-focused, concise, and informative. Prefer fenced code blocks with info strings when examples help.
- `Development` should stay short and reader-oriented. Prefer a direct link to `CONTRIBUTING.md` for setup, workflow, validation, review, and maintainer commands instead of duplicating those procedures in the README.
- `Repo Structure` should be a small directory tree or outline diagram, not a prose section.
- Keep README, CONTRIBUTING, TODO, ROADMAP, and AGENTS responsibilities distinct. Product summary and end-user fit belong here; contribution workflow belongs in `CONTRIBUTING.md`; backlog details belong in `TODO.md` or `ROADMAP.md`; agent-facing maintainer rules belong in `AGENTS.md`.

## Codex Subagent Fit

When the user explicitly asks for subagents or parallel agent work, use subagents only for read-heavy README discovery before the main workflow edits or reports. Good jobs include checking source docs, inventorying commands, inspecting sibling package metadata, or comparing README claims against one upstream source per worker.

Keep `apply` edits in the main thread because this skill has one target file and a hard-enforced schema. Ask subagents to return concise evidence and file references, not replacement README prose.

## Canonical Base Contract

The authoritative default shared README structure lives in:

- `config/readme-customization.template.yaml`
- `assets/README.template.md`

Treat those two files as the source of truth for the canonical base schema and the canonical bootstrap document. Downstream plugins may extend that structure through preamble and appendices, but this base skill treats the required table of contents plus the configured section block as hard-enforced.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `customization_state`
  - `schema_contract`
  - `schema_violations`
  - `content_quality_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, setup steps, or product claims that are not grounded in the repo.
- Never edit files other than the target `README.md`.
- Never move contributor or maintainer procedures into `README.md` when `CONTRIBUTING.md` or a maintainer doc is the correct owner.
- Keep the README schema hard-enforced against the configured contract instead of inferring structure from repo profile heuristics.
- Do not relax the configured schema just because the repository is a plugin, skills, or hybrid repo. Use explicit extension via preamble or appendices when the repo genuinely needs an additional structure or section.

## References

- `agents/openai.yaml`
- `config/readme-customization.template.yaml`
- `assets/README.template.md`
- `references/section-schema.md`
- `references/readme-customization.md`
- `references/readme-config-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/verification-checklist.md`
- `references/project-readme-maintenance-automation-prompts.md`
