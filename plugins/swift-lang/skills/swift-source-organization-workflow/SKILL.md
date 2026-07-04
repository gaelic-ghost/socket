---
name: swift-source-organization-workflow
description: Organize Swift source trees and files by concern, feature, and layer; split oversized files, extract extension files, normalize MARK sections, file headers, and TODO/FIXME ledgers with stricter split defaults. Use after formatting baseline is clear.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
---

# Swift Source Organization Workflow

## Purpose

Keep Swift source trees small, navigable, and organized around real responsibility boundaries.

Use `swift-format-style-workflow` before structural edits and again afterward. Hand off to `apple-dev-skills` when file moves require Xcode target membership, project-file mutation, previews, schemes, or build/run validation.

## Workflow

1. Establish or confirm the formatting baseline.
2. Resolve repo shape:
   - Swift package
   - Xcode app project
   - mixed package plus app
   - server-side Swift service
3. Inventory source shape:
   - large files
   - mixed concerns
   - broad extensions
   - unclear access-control boundaries
   - nested types that block reuse
   - long TODO/FIXME comments
   - redundant or missing `// MARK:` sections
4. Split by concern:
   - strongly consider splitting around `250` to `300` lines when two or more concerns are present
   - treat `500` to `600` lines as a hard split signal unless the file is generated or has a documented exception
   - prefer complete passes over tiny partial splits when adjacent files are part of the same concern cleanup
5. Choose the split shape:
   - `TypeName+Models.swift`
   - `TypeName+Validation.swift`
   - `TypeName+Pipeline.swift`
   - `TypeName+Formatting.swift`
   - feature directories for independent user-facing or domain areas
   - layer directories when a package has clear API, domain, persistence, transport, or UI boundaries
6. Preserve behavior:
   - keep access control intentional
   - keep generated files untouched
   - update package manifests or Xcode project membership through the owning workflow
   - run formatting after moves

## MARK Guidance

- Add `// MARK: - <Heading>` only when it improves navigation.
- Name the responsibility boundary, not the declaration kind.
- Avoid filler headings in short files.
- Avoid comments that repeat obvious method or type names.

## File Header And Ledger Guidance

- Preserve existing license banners.
- Use file headers only when the repository already requires them or the task explicitly includes header normalization.
- Keep file-header purpose and concern text plain, specific, and non-generic.
- Move long TODO and FIXME prose into ledgers when the repo uses ledger files; keep source comments short and traceable.

## Output Shape

Return:

1. `Organization state`: repo shape and largest concern problems.
2. `Split plan`: files to split, target names, and reason for each split.
3. `Moves`: directories or manifests that need updates.
4. `Handoffs`: Apple Dev, Server-Side Swift, or package validation needs.
5. `Validation`: formatting, build, test, or project-integrity checks.

## Guardrails

- Do not split files purely by line count when the file is coherent and generated files are excluded.
- Do not invent abstraction layers just to make files shorter.
- Do not move files across Xcode-managed boundaries without project-membership follow-through.
- Do not leave duplicate helpers behind after extraction.
- Do not use `// MARK:` as decoration.
