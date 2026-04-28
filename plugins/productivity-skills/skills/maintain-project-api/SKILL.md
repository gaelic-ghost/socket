---
name: maintain-project-api
description: Maintain canonical API.md files through deterministic audit and bounded apply modes. Use when a project API reference needs auditing, normalization, or bounded fixes for API surface, authentication, request and response schemas, errors, versioning, compatibility, local verification, or support guidance. This is the default baseline API.md workflow for most repos unless a narrower plugin owns that repo shape.
---

# Maintain Project API

Maintain canonical `API.md` files through one deterministic API-reference workflow.

This skill is the default baseline path for `API.md` maintenance across most repositories. Reach for a narrower plugin only when the target repo has a specialized shape that deserves its own maintainer contract, such as a skills-export or plugin-export repository.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--api-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `API.md`.
2. Load the canonical API-reference schema from `config/api-customization.template.yaml`, then merge any explicit override or project-local customization file.
3. In `check-only`, audit the required section schema, required subsection schema, required table of contents, placeholder content, and verification-command formatting.
4. In `apply`, keep edits bounded to the target `API.md` while creating a missing file from the bundled template and normalizing the document to the canonical structure.
5. Re-run the same audit to confirm post-fix status.

## Canonical Base Contract

The source of truth for the base API-reference contract lives in:

- `config/api-customization.template.yaml`
- `assets/API.template.md`

The base contract requires:

- a top-level title and short summary
- a required `## Table of Contents`
- canonical top-level sections for overview, API surface, authentication and access, requests and responses, errors, versioning and compatibility, local development and verification, and support ownership
- required subsection structure for the sections that need stable consumer-facing detail

## Writing Expectations

- `Overview > Who This API Is For` should name the real consumers: humans, services, tools, packages, apps, or maintainers.
- `Overview > Stability Status` should say whether the API is stable, experimental, internal, deprecated, or otherwise constrained.
- `API Surface` should list concrete entry points and the protocol, transport, runtime, package interface, or file format used to reach each one.
- `Authentication and Access` should describe credentials and permissions without inventing secrets, scopes, roles, or access paths.
- `Requests and Responses` should document grounded request inputs, response outputs, and data models.
- `Errors` should make failures actionable by documenting the error shape and common failure modes with likely causes or next checks.
- `Versioning and Compatibility` should make the supported compatibility window and breaking-change handling explicit.
- `Local Development and Verification > Verification` should prefer fenced commands or reproducible call examples with language info strings.
- `Support and Ownership` should name only grounded teams, maintainers, issue trackers, services, or escalation paths.

## Codex Subagent Fit

When the user explicitly asks for subagents or parallel agent work, use subagents only for read-heavy API evidence gathering before the main workflow edits or reports. Good jobs include inventorying endpoints or public symbols, checking examples against tests, reading schema definitions, or comparing compatibility claims against release notes.

Keep `apply` edits in the main thread because this skill owns one target `API.md` file and must avoid invented endpoints, schemas, credentials, or support promises. Ask workers for concise evidence and file references instead of replacement API prose.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `schema_contract`
  - `schema_violations`
  - `command_integrity_issues`
  - `content_quality_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent commands, endpoints, protocols, schemas, environment variables, credentials, permissions, version guarantees, support paths, or compatibility promises that are not grounded in the repo.
- Never edit files other than the target `API.md`.
- Keep `API.md` as the canonical API-reference filename for this skill.
- Treat this skill as a hard-enforced base template. Downstream plugins may specialize the schema, but the base skill should not do repo-profile inference.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/api-customization.md`
- `references/api-config-schema.md`
- `references/project-api-maintenance-automation-prompts.md`
