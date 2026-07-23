# tvOS Skills Plan

This plan defines the first Socket-owned tvOS guidance expansion. It is a
durable Apple Dev Skills building-block change: two narrow workflows make the
Apple TV-specific interaction and media contracts reusable without turning the
general SwiftUI, AVFoundation, or model-runtime skills into tvOS catch-alls.

## Status

Planned for the next Socket minor release.

## Decision

Add two workflows under `plugins/apple-dev-skills/skills/`:

- `tvos-app-experience-workflow`
- `tvos-media-playback-workflow`

Keep the first release guidance-only. It must not bundle a TVML runtime,
remote-control daemon, player abstraction, simulator wrapper, media service,
model asset, or Apple TV hardware test fixture.

## Why Two Workflows

The simpler extension path was to add tvOS paragraphs to
`swiftui-app-architecture-workflow`, `apple-ui-accessibility-workflow`, and
`avfoundation-media-pipeline-workflow`. That would make the common workflow
selection less clear and leave no single owner for remote focus behavior,
large-screen interaction, or media-command responsibility.

`tvos-app-experience-workflow` owns app-wide interaction design and focus
semantics. `tvos-media-playback-workflow` owns the separate playback contract:
system-player preference, media commands, Now Playing state, and the complete
custom-player responsibility boundary. The split removes duplicated ad-hoc
advice and makes the next catalog, utility, game, or video app easier to plan
without adding a new app architecture layer.

## Source Baseline

Sources were checked on 2026-07-23 through Xcode DocumentationSearch, the
installed Dash Apple API references where relevant, and readable official
Apple documentation/release-note sources.

- [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos)
- [Adding user-focusable elements to a tvOS app](https://developer.apple.com/documentation/uikit/adding-user-focusable-elements-to-a-tvos-app)
- [About focus interactions for Apple TV](https://developer.apple.com/documentation/uikit/about-focus-interactions-for-apple-tv)
- [Creating a tvOS media catalog app in SwiftUI](https://developer.apple.com/documentation/swiftui/creating-a-tvos-media-catalog-app-in-swiftui)
- [Supporting remote interactions in tvOS](https://developer.apple.com/documentation/avfoundation/supporting-remote-interactions-in-tvos)
- [TVMLKit](https://developer.apple.com/documentation/tvmlkit)
- [tvOS 26 release notes](https://developer.apple.com/documentation/tvos-release-notes/tvos-26-release-notes)
- [tvOS 27 beta release notes](https://developer.apple.com/documentation/tvos-release-notes/tvos-27-release-notes)
- [Prepare your tvOS apps for Dynamic Type](https://developer.apple.com/videos/play/wwdc2026/221/)
- [Core AI model compilation requirements](https://developer.apple.com/documentation/coreai/compiling-core-ai-models-ahead-of-time)
- [Foundation Models updates](https://developer.apple.com/documentation/updates/foundationmodels)

## Documented Platform Contract

### Interaction and UI

- Apple TV interaction is indirect: people navigate with Siri Remote gestures,
  a controller, voice, or companion devices instead of direct touchscreen
  positioning.
- Focus is a visible navigation and selection state. UIKit’s Focus Engine
  determines directional movement; apps can request reevaluation but must not
  attempt to command a directional focus move.
- SwiftUI is the primary implementation path. Use its standard tvOS lockups,
  focus sections, hover effects, and scroll behavior before reaching for UIKit
  focus customization.
- A custom layout must give focused content room to enlarge, elevate, and cast
  a shadow. Shelf clipping and rigid focus geometry are correctness problems,
  not cosmetic issues.
- Full-screen content uses gestures for content interaction, rather than using
  them to move an invisible focus target. Pointer-driven app navigation is not
  the default tvOS pattern.
- Text entry is intentionally limited. Do not make a typing-heavy flow the only
  path through a TV experience.

### Framework and Capability Boundaries

- TVMLKit has been deprecated since tvOS 18. Existing clients may need a
  migration plan, but new apps should use SwiftUI or UIKit.
- Prefer `AVPlayerViewController` and AVKit playback UI. A custom player must
  explicitly support the remote commands and media-state behaviors that the
  system player supplies by default.
- `MPRemoteCommandCenter` supplements system-player behavior and becomes an
  explicit responsibility for custom playback controls.
- Web views and widgets are not supported on tvOS. The Speech framework is not
  available in the tvOS SDK.
- RealityKit and Metal availability varies by Apple TV GPU family. Guidance must
  identify the required capability and test device rather than treating Apple
  TV hardware as one uniform target.

### tvOS 26 to tvOS 27 Beta Delta

| Surface | tvOS 26 | tvOS 27 beta planning rule |
| --- | --- | --- |
| Design | The new design treatment does not carry to Apple TV 4K (1st generation) and older devices. | Retain hardware-generation gates and test newer 4K devices separately. |
| Text accessibility | Large Text was not a system-wide tvOS contract. | Large Text/Dynamic Type is system-wide. Use text styles, flexible constraints, and content-density changes such as fewer grid columns. |
| Background Assets | Delivery had beta-era reliability limitations that require lifecycle testing. | Localized asset packs can reduce storage use; document language-variant retrieval and fallback behavior. |
| SwiftUI images | Existing app-controlled cache behavior remains intentional. | `AsyncImage` follows HTTP cache protocols; skill guidance must call out server headers, explicit cache policy, and custom session choice. |
| Buttons | Existing asset-catalog accent assumptions may exist. | Explicitly verify tint: buttons no longer automatically use the asset-catalog accent color as label tint when built with the tvOS 27 SDK. |
| TVMLKit | Already deprecated. | Still migration-only; no new TVMLKit authoring path. |
| Core AI and Foundation Models | No documented direct tvOS runtime support. | Still no direct tvOS target in the documented Core AI hardware list or the Foundation Models version matrix; do not imply on-device model support on Apple TV. |

The 27-beta statements are beta-specific and must be date- and SDK-qualified in
shipped guidance. Recheck each at the release candidate and GM before calling
them stable behavior.

## Workflow Contracts

### `tvos-app-experience-workflow`

Use when a request is about tvOS app structure, catalog or utility UI,
remote-first navigation, focus behavior, readable large-screen layout,
accessibility, platform availability, a TVMLKit migration decision, or an
Apple-TV-specific SwiftUI/UIKit boundary.

The workflow must:

1. Read current Apple documentation before making platform, framework, or beta
   claims, then state the documented behavior being relied on.
2. Classify the request as SwiftUI-first layout, focus routing, UIKit focus
   escape hatch, accessibility/Large Text, capability gating, TVMLKit
   migration, or a handoff.
3. Prefer native SwiftUI focus behavior. Escalate to `UIFocusGuide`, preferred
   focus environments, or focus-update callbacks only when geometry makes the
   standard path fail.
4. Keep focus, visual selection, VoiceOver order, Dynamic Type, RTL layout,
   remote/controller input, and focus restoration as distinct validation
   concerns.
5. Check platform restrictions before design recommendations: hardware
   generation, GPU family, remote versus controller, text-entry burden,
   simulator versus device-only feature, unavailable framework, and beta SDK.
6. Treat TVMLKit as an inventory-and-migration path. Do not suggest extending a
   deprecated architecture for a new feature.

It hands off to:

- `swiftui-app-architecture-workflow` for ordinary scene, data-flow, and
  component ownership once the tvOS constraints are resolved.
- `apple-ui-accessibility-workflow` for general accessibility-tree work that is
  not specific to tvOS focus or Large Text.
- `tvos-media-playback-workflow` for playback and media-command ownership.
- `xcode-build-run-workflow` and `xcode-testing-workflow` for execution and
  runtime verification.
- `model-lab-skills:choose-apple-model-runtime` for a genuine model-runtime
  decision; the tvOS skill must report the current direct-runtime limitation.

### `tvos-media-playback-workflow`

Use when a tvOS experience plays media, needs remote transport behavior, uses
custom playback UI, displays supporting content in AVKit, adopts HLS or
interstitials, manages Now Playing state, or must choose between the AVKit
system player and a custom player.

The workflow must:

1. Start with the `AVPlayerViewController`/AVKit system-player option and name
   the concrete product requirement that prevents using it before escalating.
2. Keep player state, command enablement, Now Playing metadata, and command
   routing in one explicitly owned media-control surface; do not scatter remote
   handlers across views.
3. Cover AVKit tabs, overlays, content proposals, HLS/interstitial behavior,
   Picture in Picture where applicable, and optional Continuity Camera as
   feature-specific paths rather than a generic media checklist.
4. Require an input matrix for Play/Pause, select, scrub, skip,
   previous/next, Menu/Back, controller, system media controls, interruption,
   and post-playback focus restoration.
5. Preserve existing `avfoundation-media-pipeline-workflow`,
   `coremedia-timing-samplebuffer-workflow`, and `avfaudio-session-workflow`
   ownership for general media pipelines, time/sample correctness, and audio
   session policy.

## First Implementation Slices

1. **Evidence and contract scaffolding**
   - Recheck the official source baseline in Xcode docs, Dash, release notes,
     and relevant WWDC transcripts.
   - Write each `SKILL.md`, its `agents/openai.yaml`, focused reference files,
     and an explicit stable/beta/version-checked evidence model.
   - Keep TVMLKit and direct-AI limitations in references and guards, not as a
     third workflow.

2. **App-experience workflow**
   - Add focused references for focus layout, SwiftUI lockups and shelves,
     UIKit escape hatches, remote/controller input, Large Text, accessibility,
     hardware/framework availability, and TVMLKit migration inventory.
   - Add tests for frontmatter, trigger selection, SwiftUI-first language,
     user-controlled-focus guard, TVMLKit deprecation language, AI handoff, and
     Xcode/testing handoffs.

3. **Media-playback workflow**
   - Add focused references for system-player preference, remote command
     handling, custom-player responsibility, Now Playing state, AVKit
     extensions, media validation, and device-only checks.
   - Add tests for system-player-first routing, `MPRemoteCommandCenter` scope,
     command-matrix coverage, and AVFoundation/Xcode handoffs.

4. **Discovery, portability, and release readiness**
   - Update the Apple Dev Skills plugin metadata, active-skill inventory,
     README prompt list, child roadmap, Hermes tap export, `mcp_servers`
     translation/index only when a Socket MCP declaration changes, and
     Claude/Cowork compatibility records.
   - Run targeted tests, `bash .github/scripts/validate_repo_docs.sh`, `uv run
     pytest`, Hermes export/validation, compatibility validation, and `uv run
     scripts/validate_socket_metadata.py` at the root.
   - Recheck beta sources and branch accounting before the minor release.

## Non-Goals

- No generic “Apple TV app” framework or a new layer above SwiftUI/UIKit.
- No new TVMLKit content authoring workflow; migration guidance only.
- No promise that Core AI, Apple’s `SystemLanguageModel`, or Foundation Models
  inference is available to tvOS apps.
- No release-specific beta claim without an exact version/date and a checked
  source.
- No simulator-only proof for hardware-dependent GPU, controller, Continuity
  Camera, or Apple TV remote behavior.

## Release Decision

This is a Socket minor release because it adds two installable, backward-
compatible Apple Dev Skills workflows. The release must follow the documented
standard Socket release mode, including repository/child validation, portability
exports, branch accounting, tag/release evidence, and marketplace upgrade only
after the release is published.
