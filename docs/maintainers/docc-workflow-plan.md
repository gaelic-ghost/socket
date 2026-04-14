# DocC Workflow Plan

Date: 2026-04-14

## Purpose

Record the chosen direction for Milestone 38 so the first DocC skill lands as a focused Apple-documentation authoring and review workflow instead of an all-in-one execution router.

## Decision

The first DocC skill should be an authoring-and-review specialist.

It should help with:

- in-source symbol documentation
- DocC article writing
- DocC extension-file writing and review
- landing-page and topic-group structure
- tutorial-aware classification and light review when the task clearly touches DocC tutorials
- content accuracy review against the current code
- DocC-specific structure and navigation review
- repo-shape checks that determine whether the project has the expected DocC surfaces

It should not become the primary owner of:

- broad Apple documentation source selection
- general Xcode or SwiftPM build orchestration
- generic Markdown or repository-doc maintenance
- the main build, export, preview, or hosting execution paths

Those execution concerns should stay with the existing execution skills, with the DocC skill handing off when the work becomes build, export, or project-integrity heavy.

## Scope Boundary

### In Scope

- Swift package and Xcode app or framework DocC authoring workflows
- deciding whether content belongs in source comments, catalog articles, extension files, or landing pages
- helping users draft or revise symbol comments, abstracts, discussions, parameter sections, return sections, and example-oriented prose
- helping users draft or revise DocC articles, overview pages, and navigation-oriented supporting content
- recognizing when a request is really about DocC tutorials and handling that as a lighter first-pass review or a deeper-docs follow-up instead of pretending tutorials are already a phase-one specialty
- reviewing DocC content for clarity, correctness, discoverability, and maintainability
- reviewing DocC structure for topic groups, nested symbol organization, and catalog layout
- identifying likely DocC-facing failure modes before the user reaches the build or export stage

### Out Of Scope

- replacing `explore-apple-swift-docs` as the canonical Apple-docs routing surface
- replacing `swift-package-build-run-workflow` or `xcode-build-run-workflow` for doc generation commands or export commands
- absorbing generic README or Markdown-maintenance work that belongs in `productivity-skills`
- promising fully validated DocC build success without handing off to an execution skill when generation is required

## Documentation Sources

The skill should teach and enforce a two-layer documentation model:

1. Use the lighter Apple and Xcode documentation surface first for the integrated product behavior:
   - [Writing documentation](https://developer.apple.com/documentation/xcode/writing-documentation)
   - [Documenting apps, frameworks, and packages](https://developer.apple.com/documentation/xcode/documenting-apps-frameworks-and-packages)
   - [Writing symbol documentation in your source files](https://developer.apple.com/documentation/xcode/writing-symbol-documentation-in-your-source-files)
   - [Adding supplemental content to a documentation catalog](https://developer.apple.com/documentation/xcode/adding-supplemental-content-to-a-documentation-catalog)
   - [Adding structure to your documentation pages](https://developer.apple.com/documentation/xcode/adding-structure-to-your-documentation-pages)
   - [Distributing documentation to other developers](https://developer.apple.com/documentation/xcode/distributing-documentation-to-other-developers)
2. Use the fuller Swift DocC material from Swift.org or an equivalent Dash docset when the user needs deeper DocC syntax, directives, and structure detail:
   - [DocC on Swift.org](https://www.swift.org/documentation/docc/)

The skill should not silently rely on memory for DocC syntax or structure rules when one of those documentation layers can answer the question directly.

Tutorial-specific directive detail should default to that deeper Swift.org or Dash-backed layer unless and until the skill grows a dedicated tutorial workflow phase.

## Repo Shapes The Skill Must Handle

### Swift Package Repos

- package with in-source documentation only
- package with an existing `.docc` catalog
- package missing a catalog but clearly ready to add one
- package where the next step becomes generation or export and should hand off to `swift-package-build-run-workflow`

### Xcode App Or Framework Repos

- app or framework target with in-source documentation only
- project with an existing documentation catalog
- project where the next step becomes `Product > Build Documentation`, `xcodebuild docbuild`, export, or project-membership follow-through and should hand off to `xcode-build-run-workflow`

## Correctness Model

The skill should distinguish three different kinds of correctness instead of flattening them together.

### Content Correctness

Does the prose describe the code's real behavior, inputs, outputs, guarantees, side effects, and important constraints?

### DocC Correctness

Does the content appear structurally valid for DocC, with plausible symbol links, topic grouping, extension-file targeting, and documentation-catalog organization?

### Project Correctness

Does the repository shape and project setup support the intended DocC generation or export path?

The first version of the skill should own the first two strongly and only diagnose or hand off the third.

For tutorials, the first version should stay at the lighter end of DocC correctness review:

- check that the request is really tutorial-shaped
- review conceptual flow and prose quality at a high level
- avoid claiming deep directive correctness without consulting the fuller DocC references

## Workflow Shape

The first version should stay single-path and narrow:

1. Classify the repo shape:
   - Swift package
   - Xcode app or framework
2. Classify the DocC task:
   - symbol-doc authoring
   - article authoring
   - extension-file or structure work
   - tutorial-aware review
   - review pass
3. Inspect the relevant source files and catalog files already on disk.
4. Produce one primary outcome:
   - revised content
   - review findings
   - structure recommendation
   - setup diagnosis with one explicit handoff
5. Hand off to an execution skill only when generation, export, preview, hosting, or Xcode or package-integrity work becomes the real next step.

## Handoff Rules

- Hand off to `explore-apple-swift-docs` when the user really needs broader Apple or Swift documentation lookup instead of DocC authoring or review help.
- Hand off to `swift-package-build-run-workflow` when a package repo needs doc generation, archive generation, export, or package-shape follow-through.
- Hand off to `xcode-build-run-workflow` when an Xcode repo needs doc generation, archive generation, export, file-membership checks, or project-integrity follow-through.
- Prefer not to route testing through the DocC skill unless the request clearly becomes execution-heavy and already belongs in the testing workflows for related repo-shape validation.

## Quality Expectations

The skill should help users improve:

- summary quality and concision
- discussion depth where a summary alone is not enough
- parameter and return coverage
- example and usage explanation quality
- conceptual separation between source comments and catalog articles
- landing-page structure and top-level topic-group clarity
- nested-symbol discoverability through extension files and topic organization
- style consistency across source comments and catalog content

The skill should avoid rewarding comment volume over clarity.

## First Implementation Slice

The first implementation slice should:

- create the new `docc-workflow` skill surface
- document the authoring-and-review-first boundary inside the skill
- add references for the Apple Xcode docs and the Swift.org DocC docs
- cover Swift package and Xcode app repo-shape detection
- teach the three-part correctness model
- make tutorials explicitly recognized but intentionally shallow in the first release
- teach explicit handoffs to the existing execution skills
- add tests for scope classification, handoff behavior, and surface completeness

## Deferred Follow-Up

These belong after the first version is stable:

- deeper tutorial-authoring and directive-specific coverage
- deeper DocC CLI coverage
- richer hosting and publishing guidance
- CI automation guidance for DocC export

## Concerns And Risks

- The biggest risk is letting the skill turn into another broad execution router. Keep authoring and review as the center of gravity.
- The second risk is duplicating `explore-apple-swift-docs`. The DocC skill should consume that pattern, not replace it.
- The third risk is overstating project correctness when no generation step has actually run. Keep that boundary explicit.
- The fourth risk is pretending tutorial support is deeper than it really is in phase one. The skill should recognize tutorial work, but it should route deeper directive and interactive-tutorial detail to the fuller DocC references until that surface is intentionally expanded.

## Recommended Roadmap Interpretation

Milestone 38 should now be read as:

- phase one: authoring and review specialist
- later follow-up: deeper generation, export, and hosting guidance once the first surface proves useful
