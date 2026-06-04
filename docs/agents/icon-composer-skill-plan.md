# Icon Composer Skill Plan

This plan records a proposed Socket-hosted Apple Dev Skills workflow for using Apple's Icon Composer to design, preview, validate, and integrate full-featured app icons for macOS, iOS, iPadOS, and related Apple platforms.

The first version should be a practical Codex skill that can help Gale learn Icon Composer while also using it. The long-term direction is a packaged Mac App Store agent that uses these skills as its operating playbook for guided icon production.

## Intent

Add an `apple-dev-skills` skill that helps agents and users do seven things:

- learn the Icon Composer workflow from Apple's current documentation and the live app
- turn an app/product brief into a layered icon production plan
- prepare source artwork in a suitable Mac image editor before import
- operate Icon Composer's GUI through Computer Use when the user asks for guided hands-on work
- save and preserve `.icon` source documents as the durable design artifact
- export repeatable preview PNGs through `ictool` for review and comparison
- integrate the icon into Xcode projects without treating exported PNGs as the source of truth

This should be a workflow skill, not a fully automated icon generator. Icon quality still depends on visual judgment, source artwork, iteration, and platform preview review.

## Proposed Skill

### `apple-dev-skills:icon-composer-app-icon-workflow`

Use this when a task mentions Apple's Icon Composer, `.icon` documents, Liquid Glass app icons, Xcode app icon integration through Icon Composer, `ictool`, app icon previews, iOS app icons, iPadOS app icons, macOS app icons, Apple Watch app icons, or guided use of Icon Composer through Computer Use.

The skill should route the agent through:

1. current Apple documentation lookup
2. local tool availability checks
3. design brief and platform target collection
4. source artwork preparation
5. Icon Composer GUI workflow through Computer Use
6. preview export and visual review
7. Xcode integration and repository handoff

## Current Documentation Snapshot

Treat this section as a 2026-06-04 snapshot, not permanent truth. The implemented skill should require current Apple documentation lookup before making claims about Icon Composer behavior, Xcode integration, or platform-specific icon requirements.

As of this snapshot:

- Apple positions Icon Composer as the app for creating layered app icons across Apple platforms.
- Icon Composer documents use the `.icon` extension.
- The local Icon Composer bundle registers `.icon` documents with the `com.apple.iconcomposer.icon` content type.
- The local app bundle includes `ictool`, a command-line export tool for Icon Composer documents.
- `ictool` can export rendered PNG previews from a `.icon` document by platform, rendition, width, height, scale, light angle, tint color, and tint strength.
- Xcode should consume the Icon Composer document as the source app icon artifact when supported.

Use official Apple sources first:

- [Icon Composer](https://developer.apple.com/icon-composer/)
- [Creating your app icon using Icon Composer](https://developer.apple.com/documentation/Xcode/creating-your-app-icon-using-icon-composer)
- [Human Interface Guidelines: App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons/)
- [WWDC25: Create icons with Icon Composer](https://developer.apple.com/videos/play/wwdc2025/361/)

If Apple's docs and the live Icon Composer app disagree, stop and surface the conflict instead of inventing behavior.

## Tool Availability Contract

Before guiding a live workflow, inspect the local environment:

- locate Icon Composer, usually inside `Xcode.app/Contents/Applications/Icon Composer.app`
- verify whether the app launches on the current Mac
- locate `ictool` inside the Icon Composer app bundle
- run `ictool --help` or `ictool --version` when command-line export is part of the task
- identify the Xcode version when Xcode integration is part of the task
- identify whether the target project is an Xcode app project, Swift package, Expo app, or another project shape

Do not assume Icon Composer exists just because Xcode exists. Older Xcode installs, alternate Xcode paths, or missing developer tools can change the workflow.

## Preferred Source Artwork Apps

When image editing software is needed, prefer established Mac apps before generic web or script-only tooling:

- Pixelmator Pro
- Acorn 8
- Retrobatch

These are good default recommendations because many Mac developers and designers already have one or more installed, they are mature, high-quality Mac apps, and they fit a local Apple-platform production workflow.

Use the apps by job:

- Pixelmator Pro: detailed composition, masking, layer polish, effects, color adjustment, and high-quality source artwork edits
- Acorn 8: fast bitmap/vector-ish editing, practical layer edits, smaller icon asset adjustments, and lightweight Mac-native production work
- Retrobatch: repeatable batch processing, resizing, format conversion, metadata cleanup, and export normalization

Do not require these apps. If none are installed, fall back to the user's available editor, Figma exports, Affinity/Adobe tooling, command-line conversion, or generated assets as appropriate.

## Design Brief Contract

Collect only the details needed to start a useful icon pass:

- app name and platform targets
- app category and primary user job
- brand colors, existing logo, or visual identity constraints
- required symbol or object
- whether text is allowed; default to no text for app icons
- preferred tone, such as utility, playful, premium, developer-tool, creative-tool, or system-adjacent
- source asset paths, if any
- whether Gale wants Codex to operate the GUI or only coach them through it

For Gale's default visual taste, prefer high contrast, strong shape separation, cool-leaning bright or pastel colors when no semantic palette is stronger, and retro-future/cyberpunk/vaporwave-friendly glow or linework when it fits the app. Do not force that style onto apps where a different semantic direction is clearer.

## Source Artwork Preparation

Before opening Icon Composer, decide what the layers should be.

Prefer a small layer stack:

- background shape or field
- primary symbol/object
- secondary detail or highlight
- optional foreground accent
- optional shadow/depth element

Avoid starting with a cluttered illustration. App icons need to survive small sizes, dark and tinted appearances, and platform previews.

Preferred inputs:

- SVG for crisp symbols and simple geometry when Icon Composer accepts the shape cleanly
- PNG for rendered bitmap artwork, textures, glows, and effects
- high-resolution square exports for source images before import

Preserve editable source files from Pixelmator Pro, Acorn, Figma, or other editors separately from the `.icon` document. The `.icon` file is the app icon production source, but it is not necessarily the only design source.

## Computer Use Guidance For Icon Composer

Use Computer Use when the task requires operating Icon Composer's GUI by clicking, dragging, typing, importing layers, setting controls, or inspecting previews.

Computer Use is appropriate for:

- launching Icon Composer
- creating or opening a `.icon` document
- importing source layers
- arranging layers and groups
- toggling previews, platforms, appearances, and renditions
- adjusting visible GUI controls when the user has approved that hands-on workflow
- taking screenshots for comparison or teaching
- walking Gale through the interface while narrating what changed

Computer Use should be careful around:

- saving over an existing `.icon` document
- moving or renaming local files through the GUI
- importing files from sensitive folders
- making project changes in Xcode through the GUI

Before destructive or state-changing GUI actions, follow the Computer Use confirmation policy. Saving a new local design document in an agreed repo or working directory is normal workflow. Overwriting, deleting, moving, or renaming existing files through the GUI needs explicit confirmation at action time.

For learning sessions with Gale:

1. Start with a tiny practice icon before a real app icon when Gale has not used Icon Composer before.
2. Explain the current screen in plain language.
3. Use short action loops: perform one visible change, describe the effect, then inspect the preview.
4. Prefer screenshots or exported preview PNGs over long verbal descriptions when judging visual results.
5. Keep the user in the design loop; do not silently make taste-heavy changes.

## Command-Line Preview Export

Use `ictool` after the Icon Composer document exists.

The first skill version should support preview export guidance like:

```bash
"/Applications/Xcode.app/Contents/Applications/Icon Composer.app/Contents/Executables/ictool" \
  MyApp.icon \
  --export-image \
  --output-file previews/myapp-ios-default.png \
  --platform iOS \
  --rendition Default \
  --width 1024 \
  --height 1024 \
  --scale 2
```

The exact platform and rendition values should be discovered from current `ictool` help, Apple docs, or live errors rather than hard-coded beyond examples.

Preview export should be used for:

- comparing variants
- attaching artifacts to reviews or docs
- checking legibility at multiple sizes
- validating dark, tinted, clear, and default appearances when supported
- preserving a visual record before integrating the icon into an app project

## Xcode Integration Handoff

When integrating into an existing app project:

- inspect the repo and project shape first
- use `xcode-app-project-workflow` or `xcode-build-run-workflow` for existing Xcode project work
- preserve tracked project files and asset catalogs intentionally
- do not hand-edit generated project files or package manager outputs
- treat `.icon` as the source icon artifact when Xcode supports it
- run the narrowest useful project validation after integration

For brand-new native Apple apps, hand off to `bootstrap-xcode-app-project` first, then return to this skill for icon production once the app exists.

## Future Packaged Agent Direction

The longer-term product direction is a packaged Mac app, likely distributed through the Mac App Store, that uses these skills as the operating guidance for a local icon-production agent.

That app should be treated as a future product, not part of the first Socket skill slice.

The packaged agent could:

- ask for an app brief and target platforms
- generate or refine an icon concept
- guide the user through source artwork preparation in Mac-native editors
- open and operate Icon Composer with clear permission boundaries
- export preview sets through `ictool`
- help compare variants visually
- integrate the approved `.icon` document into an Xcode project
- preserve source artwork, preview exports, and decision notes in a project-local icon workspace

Product constraints to keep visible:

- Mac App Store distribution may constrain automation, permissions, sandboxing, file access, and control of other apps.
- GUI automation of Icon Composer may require accessibility permissions or a user-driven handoff model.
- The agent should avoid presenting itself as a fully autonomous designer; it should be a guided production assistant.
- The skill should remain useful in Codex even before any packaged app exists.
- The skill should keep local-first design and file handling as the default, with explicit consent before uploading, sharing, or transmitting artwork.

## Implementation Slices

### Slice 1: Planning Artifact

Add this plan under `docs/agents/` so the skill boundary and future product direction are visible before implementation.

Validation:

```bash
uv run scripts/validate_socket_metadata.py
```

### Slice 2: First Skill Draft

Add:

- `plugins/apple-dev-skills/skills/icon-composer-app-icon-workflow/SKILL.md`
- `plugins/apple-dev-skills/skills/icon-composer-app-icon-workflow/agents/openai.yaml`
- optional `references/` files only if the `SKILL.md` becomes too large

The first draft should include:

- frontmatter that triggers on Icon Composer, `.icon`, Liquid Glass app icons, `ictool`, app icon previews, and Xcode app icon integration
- Apple docs gate
- local tool availability checks
- source artwork app preferences
- Computer Use GUI workflow
- `ictool` preview export workflow
- Xcode handoff guidance
- future packaged-agent note

### Slice 3: Validation And Metadata

Update plugin metadata and tests only where needed for Socket discovery.

Run:

```bash
uv run scripts/validate_socket_metadata.py
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
```

Run `uv run pytest` in `plugins/apple-dev-skills` only if tests, validation helpers, or scripts change.

### Slice 4: Practice Workflow

Use Computer Use to run a tiny practice pass in Icon Composer with Gale:

- create or open a test `.icon` document
- import simple source layers
- inspect platform and appearance previews
- export one or more PNG previews with `ictool`
- record any GUI realities that should adjust the skill wording

This slice should happen before claiming the skill is mature.

### Slice 5: Future Agent Product Plan

After the skill works in Codex, create a separate product plan for the packaged Mac app.

That plan should cover:

- app architecture and sandbox constraints
- accessibility and user-consent model for GUI automation
- Icon Composer handoff model
- source artwork editor handoff model
- `ictool` export service
- project-local artifact storage
- Mac App Store review and entitlement risks

Do not mix this product plan into the first skill implementation unless Gale explicitly widens the task.

## Open Questions

- Should the first skill include a tiny bundled icon brief template, or keep the brief as plain workflow guidance?
- Should the skill include a reference file for `ictool` examples after live testing, or keep command examples in `SKILL.md`?
- Should the skill mention generated image support directly, or route generated art through the normal source artwork preparation step?
- Should the packaged Mac App Store agent live in Socket later, or in a separate app repo that consumes Socket skills?

For now, keep the first implementation inside `apple-dev-skills` as a focused workflow skill. Revisit the product/app boundary only after the live Icon Composer practice pass proves the workflow shape.
