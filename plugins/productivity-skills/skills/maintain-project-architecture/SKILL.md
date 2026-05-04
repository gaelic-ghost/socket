---
name: maintain-project-architecture
description: Maintain docs/architecture/ARCHITECTURE.md, SLICES.md, and architecture.json for a repository's product/module architecture and provable code slices. Use when a repo needs architecture docs that explain Swift products, Codex plugins, skills, MCP configs, modules, construction, ownership, evidence, stale claims, and slice inventory without generic diagrams or ungrounded architecture claims.
---

# Maintain Project Architecture

Maintain the repo-local architecture documentation under `docs/architecture/`.

This skill is related to `explain-code-slice`, but it owns the durable architecture files. `explain-code-slice` explains or records one end-to-end path. This skill keeps the repo-wide product/module map and the slice index coherent.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--architecture-dir <path>`

## Workflow

1. Resolve the project root and architecture directory.
2. Detect Swift package products and targets when `Package.swift` exists:
   - prefer `swift package dump-package` when it succeeds
   - fall back to conservative `Package.swift` text scanning
3. Detect Codex plugin repository surfaces when plugin metadata exists:
   - treat `.codex-plugin/plugin.json` manifests as plugin products
   - treat `.agents/plugins/marketplace.json` catalogs as marketplace products that expose plugin entries
   - treat `skills/*/SKILL.md` files and declared `.mcp.json` files as module targets
   - record only manifest-backed or marketplace-backed relationships
4. Build or refresh `docs/architecture/architecture.json` with product, target, relationship, evidence, and slice placeholders.
5. In `check-only`, audit required files, required sections, and stale product or target facts in `architecture.json`.
6. In `apply`, create missing architecture files and refresh generated model facts without inventing symbols, data flows, or ownership claims.
7. Leave `SLICES.md` present even when no provable slices have been recorded yet.
8. Re-run the same audit and report remaining findings.

## Required Files

- `docs/architecture/ARCHITECTURE.md`
- `docs/architecture/SLICES.md`
- `docs/architecture/architecture.json`

## Writing Expectations

- `ARCHITECTURE.md` is descriptive. Put preferences, constraints, and "do not" rules in `AGENTS.md`, not here.
- Use fixed section names so Gale can ask for a specific section without ambiguity.
- Treat Swift Package Manager products and targets as first-class architecture facts when available.
- Treat Codex plugin manifests, plugin marketplaces, skills, and declared MCP configs as first-class architecture facts when available.
- Explain products/modules in terms of what they do, who creates or consumes them, what they own, and what code evidence proves that claim.
- Do not use Mermaid, generic graph diagrams, unlabeled arrows, curved-line diagrams, centered text, or diagram labels that interrupt connector lines.
- Keep visual claims in structured `architecture.json` until a purpose-built viewer can render them with Gale-readable layout.
- Every generated claim should have evidence: a file path, manifest entry, symbol, command output, or explicit "unverified" marker.

## Visual Grammar

Use `references/visual-grammar.md` when shaping any generated visual model or future viewer output.

Core rules:

- vertical flow dominates
- left/top start position, never center-first reading
- no center-aligned text
- no unlabeled or ambiguous connectors
- connectors must represent one explicit relationship kind such as `creates`, `passes`, `stores`, `calls`, `returns`, `owns`, or `depends-on`
- data models appear before slice steps
- code nodes must include symbol names and file anchors when known

## Slices

`SLICES.md` is always created. It may remain mostly empty until provable flows are discovered.

When the user asks for a new slice explanation, use `explain-code-slice` for the walkthrough and update `docs/architecture/SLICES.md` with the slice if the path is provable from code.

## Codex Subagent Fit

When the user explicitly asks for subagents or parallel agent work, use subagents only for read-heavy discovery. Good jobs include scanning package manifests, listing products and targets, finding entrypoints, or tracing one candidate slice. Keep writes to `ARCHITECTURE.md`, `SLICES.md`, and `architecture.json` in the main thread so the architecture story stays coherent.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `detected_model`
  - `schema_violations`
  - `stale_claims`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent products, modules, slices, symbols, data models, or code relationships.
- Never edit files outside the architecture directory.
- Never use generic architecture diagrams as filler.
- Treat stale product or target facts as audit failures.

## References

- `assets/ARCHITECTURE.template.md`
- `assets/SLICES.template.md`
- `references/visual-grammar.md`
- `references/architecture-json.md`
- `scripts/maintain_project_architecture.py`
