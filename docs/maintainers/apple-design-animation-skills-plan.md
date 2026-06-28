# Apple Design, Animation, Typography, and Symbols Skills Plan

This plan captures a candidate Apple Dev Skills expansion for SwiftUI animation, Core Animation, Apple's San Francisco typography family, and SF Symbols.

## Status

Planned.

## Ownership

These skills belong in `plugins/apple-dev-skills` because they depend on Apple framework behavior, Xcode integration, local Apple developer tools, and Apple documentation. They should not move into `swift-lang`, which owns shared Swift language guidance rather than Apple UI frameworks or design-tool workflows.

The existing `swiftui-app-architecture-workflow` should stay focused on app structure, scenes, commands, focus, environment, preferences, and view composition. Animation, typography, and symbol production need separate workflow surfaces so architecture guidance does not become a generic SwiftUI grab bag.

## Proposed Skill Set

### `swiftui-animation-workflow`

Use for SwiftUI animation design and repair across animation modifiers, transactions, matched geometry, timeline-driven rendering, phase and keyframe animation APIs, symbol effects, transitions, accessibility reduce-motion behavior, previews, and performance-oriented validation.

This skill should help an agent:

- classify whether the work is interaction feedback, state transition, timeline animation, hero transition, loading/progress motion, decorative motion, or accessibility-sensitive motion
- choose SwiftUI-native animation before dropping into Core Animation or lower-level rendering
- preserve data flow clarity by keeping motion derived from explicit state instead of hidden side effects
- route structural SwiftUI questions back to `swiftui-app-architecture-workflow`
- route build, preview, simulator, and Xcode project validation to `xcode-build-run-workflow`

### `core-animation-layer-workflow`

Use for lower-level layer-backed animation and rendering with Core Animation, including `CALayer`, layer trees, implicit and explicit animations, `CAAnimation`, transactions, timing, shape layers, gradient layers, replicator layers, text layers, view/layer bridging, and performance diagnosis.

This skill should help an agent:

- decide when Core Animation is justified instead of SwiftUI animation, AppKit/UIKit animation helpers, Canvas, SpriteKit, SceneKit, Metal, or video rendering
- keep layer ownership explicit when bridging SwiftUI, AppKit, or UIKit surfaces
- reason about model layer versus presentation layer behavior before proposing fixes
- avoid custom timers or manual invalidation when framework timing primitives fit
- hand off Xcode, Instruments, simulator, or device validation to the existing execution skills

### `apple-typography-san-francisco-workflow`

Use for Apple platform typography decisions involving the San Francisco family and system typography APIs.

This skill should help an agent:

- choose system typography APIs before bundling font files
- distinguish design guidance, font family selection, variable behavior, Dynamic Type, accessibility, platform conventions, and implementation APIs
- route SwiftUI, AppKit, UIKit, and asset/font integration to the right Apple docs and project validation paths
- call out licensing and redistribution boundaries once when a task asks to bundle, extract, modify, or redistribute Apple font assets
- avoid hard-coding local font file paths, private font copies, or nonportable assumptions into public project docs

### `sf-symbols-workflow`

Use for SF Symbols library, SF Symbols app, symbol availability, symbol effects, rendering modes, variable color, palette and hierarchical color, multicolor behavior, custom symbols, animated symbols, localization or directionality concerns, asset-catalog integration, and SwiftUI/AppKit/UIKit use.

This skill should help an agent:

- inspect current Apple documentation and the local SF Symbols app before making current-version claims
- choose between built-in symbols, customized symbol variants, custom symbol templates, ordinary vector artwork, and app icons
- validate custom symbol templates and exported assets through the SF Symbols app or documented tooling when available
- keep app-icon work routed to `icon-composer-app-icon-workflow`
- keep accessibility labels, semantic meaning, color modes, and platform availability visible in implementation guidance
- hand off build, preview, and asset-catalog integration to `xcode-build-run-workflow`

## Local Tool Research Needed

Before implementing these skills, run a short local evidence pass:

- verify the SF Symbols app path and version on Gale's Mac
- check whether the app exposes useful scripting, command-line, Shortcuts, AppleScript, or Accessibility automation surfaces
- inspect current SF Symbols app menus and export/validation workflows with Computer Use only when the task needs GUI evidence
- prefer Xcode-local documentation and Dash when available, then official Apple documentation
- record current authoritative source links in the skill bodies only where they guide workflow decisions

## First Implementation Slice

Build the first slice as two skills:

1. `sf-symbols-workflow`, because it has the richest local-tool surface and the clearest boundary with existing Icon Composer guidance.
2. `swiftui-animation-workflow`, because it fills the most common app-implementation gap without forcing lower-level Core Animation guidance into the same skill.

After those land and validate, add `core-animation-layer-workflow` and `apple-typography-san-francisco-workflow` as a second slice.

## Metadata And Validation Tasks

- Add each skill under `plugins/apple-dev-skills/skills/`.
- Add `agents/openai.yaml` metadata for each skill.
- Update `plugins/apple-dev-skills/.codex-plugin/plugin.json` keywords, description, long description, and default prompts.
- Update `plugins/apple-dev-skills/AGENTS.md` only if local Apple design-tool rules need a narrower owner rule than the existing Apple Rules section.
- Add targeted tests that verify skill frontmatter, routing boundaries, docs-gate language, and important handoffs.
- Run `bash .github/scripts/validate_repo_docs.sh` from `plugins/apple-dev-skills`.
- Run `uv run pytest` from `plugins/apple-dev-skills` when tests change.
- Run `uv run scripts/validate_socket_metadata.py` from the Socket root after metadata changes.

## Open Questions

- Should `sf-symbols-workflow` include guided Computer Use walkthrough prompts for the SF Symbols app in the first release, or should the first release stay docs-and-routing only?
- Should San Francisco typography live as its own skill, or should it start as a broader `apple-typography-workflow` that treats SF as the default system font family while leaving room for New York and custom app fonts?
- Should animated SF Symbols stay inside `sf-symbols-workflow`, or should `swiftui-animation-workflow` own symbol effects once the symbol choice is already made?
