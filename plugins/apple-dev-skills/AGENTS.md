# AGENTS.md

This file is the Apple Dev Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, and maintainer workflow rules.

## Scope

- This repository is the canonical home for Gale's Apple, Swift, and Xcode workflow skills. It also owns reusable app-extension mechanics, MailKit, File Provider, and Finder Sync workflow guidance.
- Treat `productivity-skills` as the default baseline maintainer layer for general repo docs and maintenance work; this repo is the narrower specialist layer when Apple-specific behavior should change the workflow.
- Treat `swift-lang` as the shared Swift language layer when it is available through Socket. Keep Apple Dev focused on Apple documentation, Apple frameworks, Xcode project integrity, platform app architecture, DocC, SPI, and execution handoffs.
- Keep reusable app-extension mechanics, MailKit, and File Provider/Finder Sync boundaries here. Keep Messages/iMessage collaboration, communication-notification policy, VoIP, and Push to Talk workflows in Messaging Collaboration Skills.
- Preserve standalone-install guidance for public users who install only `apple-dev-skills`, while allowing the public README quickstart to lead with the Socket marketplace when users want Apple Dev Skills plus companion workflows from one catalog.
- Root `skills/` is the canonical authored and exported surface.
- Keep shared reusable assets in [`shared/`](./shared/) and maintainer tests in [`tests/`](./tests/).

## Apple Rules

- For Swift, Apple framework, Apple platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related guidance, require reading the relevant Apple documentation before proposing implementation changes.
- For Apple, Swift, and Xcode documentation, use Xcode MCP `DocumentationSearch` first, then the Dash.app MCP when its installed docsets cover the question. Use Dash localhost HTTP only when the Dash.app MCP is unavailable or incomplete; consult checked-out source, generated DocC, GitHub/source repositories, release notes, and readable online documentation only after those local MCP paths.
- Treat Apple Developer web pages as citation targets or last-resort readable sources, not as a generic search fallback. The no-JS web search/open surface often cannot read the actual Apple Developer documentation payload, so it is not sufficient evidence by itself.
- State the documented Apple behavior being relied on before design or code changes are proposed.
- If Apple docs and current code disagree, stop and surface that conflict.
- If no relevant Apple documentation can be found, say that explicitly before proceeding.
- Keep `explore-apple-swift-docs` as the canonical docs-routing surface instead of re-embedding broad docs-source selection logic into execution skills.
- When the task depends on a local Apple developer app or utility, verify whether the needed app is running and open it when that is the normal way to inspect or use the surface. This includes stable or beta Xcode, Icon Composer, Instruments, SF Symbols, Simulator, Accessibility Inspector, Console, Audio MIDI Setup, and related Apple developer utilities. Do not turn an unopened local app into a research blocker; launch the relevant app, then verify the window, project, document, or tool state. Ask first only when opening the app would be disruptive, destructive, require signing in, or conflict with a user-stated constraint.
- Treat Xcode's Settings > Locations > Command Line Tools dropdown as Gale's default selector for Xcode command-line tools. When a switch is needed, use the Xcode app Gale already has open; otherwise open the intended stable or beta Xcode app, navigate to Settings > Locations, choose that app in the Command Line Tools dropdown, and let macOS obtain Touch ID or administrator approval. Then verify with `xcode-select -p` and tool versions. Run `xcodebuild`, `xcrun`, `swift`, Metal tools, and related CLI commands through that selected developer directory without overriding it. Do not set `DEVELOPER_DIR`.
- Prefer framework-provided behavior over custom wrappers, coordinators, glue, or renaming layers unless a concrete constraint requires them.
- For AVFoundation, AVFAudio, Core Media, Core Audio, Audio Toolbox, and related Apple media work, strictly prefer Apple and Swift media types unless they are unsuitable for the concrete app, package, test, wire, persistence, or cross-platform boundary. Preserve framework types such as `CMTime`, `CMSampleBuffer`, `CMFormatDescription`, `AVAudioFormat`, `AudioStreamBasicDescription`, and `OSStatus` until the conversion boundary, information loss, and reason for the escape hatch are explicit.
- For Xcode app repos, tracked `.pbxproj` changes are critical project state when produced by Xcode, XcodeGen, or another project-aware workflow.
- Treat `Package.resolved` and similar package-manager outputs as generated files. Do not tell maintainers or agents to hand-edit them.

## Install Guidance

- The public README may lead with `codex plugin marketplace add gaelic-ghost/socket` and `codex plugin marketplace upgrade socket` because Socket is the preferred catalog when users want Apple Dev Skills plus companion workflows.
- Also document `codex plugin marketplace add gaelic-ghost/apple-dev-skills` and `codex plugin marketplace upgrade apple-dev-skills` for Apple-only installs.
- Keep explicit refs scoped to pinned reproducible installs and manual local clone marketplace instructions scoped to development, unpublished testing, or fallback cases.

## Validation

```bash
bash .github/scripts/validate_repo_docs.sh
uv run pytest
```

Use the docs validator when README, AGENTS, ROADMAP, active skill inventory, or maintainer docs change. Use pytest when skill behavior, scripts, validation helpers, or tested contracts change.
