---
name: swift-format-style-workflow
description: Align SwiftFormat, SwiftLint, formatter and linter responsibility, checked-in style config, Git hooks, and CI formatting policy for Swift repositories. Use for shared Swift style and formatting before source-organization or modernization passes.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
---

# Swift Format Style Workflow

## Purpose

Keep Swift formatting and style enforcement explicit, consistent, and aligned with the repository.

Use this skill before and after source organization or modernization cleanup. Hand off to `apple-dev-skills` when the work becomes Xcode build phases, Xcode source editor behavior, project-file mutation, or Apple app validation.

## Repository Inspection

Inspect:

- `.swiftformat`
- `.swiftlint.yml`
- `Package.swift`
- `.github/workflows/`
- Git hooks or hook installers
- Makefile, justfile, scripts, or CI helpers
- README, CONTRIBUTING, AGENTS, or package docs
- Xcode project or XcodeGen files only when the repo uses them

## Tool Responsibility

- Treat SwiftFormat as the primary owner of whitespace, wrapping, sorting, and mechanical formatting shape.
- Treat SwiftLint as a complementary signal layer for clarity, maintainability, safety, naming, documentation expectations, and project-specific hazards.
- Do not let both tools fight over the same formatting rule.
- Prefer checked-in project-root config files for shared repositories.
- Prefer repo-pinned or package-managed tooling over untracked developer-local drift when the repo already has that pattern.

## Gale Style Defaults

- Keep fluent chains compact when they read clearly.
- Do not explode readable chains into one line per tiny operation unless the chain needs diagnostic boundaries.
- Prefer shorthand closure syntax, key paths, and trailing closures when the meaning remains obvious.
- Prefer dense but readable Swift over ceremony.
- Let source organization and named intermediate values carry meaning instead of padding code with comments.

## Workflow

1. Classify the request:
   - formatter setup
   - linter setup
   - style repair
   - CI or hook alignment
   - pre-cleanup baseline
   - post-cleanup normalization
2. Inspect existing config before proposing changes.
3. Choose one enforcement path:
   - local CLI check
   - Git pre-commit hook
   - CI check
   - Xcode build phase handoff
   - SwiftPM plugin handoff
4. Run or recommend the narrowest useful command:
   - `swiftformat --lint .`
   - `swiftformat .`
   - `swiftlint lint`
5. If source files will be split or moved, hand off to `swift-source-organization-workflow`, then run formatting again.

## Output Shape

Return:

1. `Style state`: config files and enforcement surfaces observed.
2. `Tool split`: what SwiftFormat owns and what SwiftLint owns.
3. `Changes`: config, hook, CI, or source edits.
4. `Commands`: exact commands run or recommended.
5. `Validation`: pass, fail, or skipped with concrete reason.

## Guardrails

- Do not hand-format Swift when SwiftFormat is available and configured.
- Do not add SwiftLint rules as a casual cleanup without checking current repo tolerance.
- Do not introduce formatter churn unrelated to the requested work.
- Do not claim Xcode build-phase or source-editor behavior without using Apple Dev docs and handoffs.
- Do not override existing project style with a generic template.
