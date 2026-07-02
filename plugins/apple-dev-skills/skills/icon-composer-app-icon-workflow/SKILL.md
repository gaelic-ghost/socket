---
name: icon-composer-app-icon-workflow
description: Design, preview, validate, and integrate Apple app icons with Icon Composer. Use when a task mentions Icon Composer, .icon documents, Liquid Glass app icons, ictool preview exports, app icon design for iOS, iPadOS, macOS, or watchOS, or guided Icon Composer GUI work through Computer Use.
---

# Icon Composer App Icon Workflow

## Purpose

Use this skill to help a user learn and operate Apple's Icon Composer workflow for app icons. The skill owns the design-production path from brief to layered source artwork, Icon Composer GUI work, preview export, and Xcode handoff. It does not replace visual judgment, source artwork tools, Xcode execution skills, or product-design iteration.

## When To Use

- Use this skill when the user asks for help with Apple's Icon Composer.
- Use this skill when the task mentions `.icon` files, Liquid Glass app icons, Icon Composer documents, app icon appearance modes, or `ictool`.
- Use this skill for app icon workflows targeting iOS, iPadOS, macOS, watchOS, or Xcode app projects.
- Use this skill when the user wants Codex to guide or operate the Icon Composer GUI through Computer Use.
- Use this skill when the task is to export rendered preview PNGs from an Icon Composer document.
- Do not use this skill for generic logo design unless the logo is being prepared as an Apple app icon.
- Do not use this skill for ordinary Xcode build, run, signing, asset-catalog, or project-file work after the app icon handoff is complete.
- Recommend `bootstrap-xcode-app-project` when the app project does not exist yet.
- Recommend `xcode-build-run-workflow` when the next step is adding the `.icon` file to an existing Xcode project, choosing it in the Project Editor, building, running, or inspecting project state.
- Recommend `explore-apple-swift-docs` when the user needs a fresh Apple documentation research pass before icon-production work continues.

## Apple Documentation Gate

Before making claims about current Icon Composer behavior, Xcode integration, platform requirements, appearance modes, or exported asset expectations, check current Apple documentation.

Use official Apple sources first:

- [Icon Composer](https://developer.apple.com/icon-composer/)
- [Creating your app icon using Icon Composer](https://developer.apple.com/documentation/Xcode/creating-your-app-icon-using-icon-composer)
- [Human Interface Guidelines: App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons/)
- [Create icons with Icon Composer](https://developer.apple.com/videos/play/wwdc2025/361/)
- [Apple Design Resources](https://developer.apple.com/design/resources/)

State the documented behavior being relied on before recommending a design, export, or Xcode integration step. If Apple's docs and the live app disagree, stop and report the conflict.

Current documented anchors to verify against the live docs:

- Icon Composer creates layered app icons from one design for iPhone, iPad, Mac, and Apple Watch.
- The workflow starts in a design tool, exports layers, imports them into Icon Composer, tunes glass properties, previews platforms and appearance modes, saves a `.icon` file, and delivers that file to Xcode.
- Icon Composer can export flattened images for marketing and communication needs, but the `.icon` file is the primary app icon production artifact when Xcode supports it.
- Flat graphics should usually be exported as scalable SVG when possible. Custom gradients, raster images, and non-SVG elements should be exported as PNGs with transparent backgrounds.
- Complex or illustrative icons may still be better delivered to Xcode as individual images when the artwork does not translate well into the layered Liquid Glass model.

## Local Tool Check

Before a live workflow, inspect the Mac and report what is available:

1. Locate Icon Composer. Common stable path:
   `/Applications/Xcode.app/Contents/Applications/Icon Composer.app`
2. Check beta Xcode app paths as needed:
   `/Applications/Xcode-beta.app/Contents/Applications/Icon Composer.app`
   `/Applications/Betas/Xcode-beta.app/Contents/Applications/Icon Composer.app`
3. Verify the app is present before promising GUI guidance.
4. Open Icon Composer when the task needs live GUI inspection, document editing, platform preview, or behavior that only the app can show. Do not report that Icon Composer behavior is unverifiable merely because the app was not already open.
5. Locate `ictool`. Common stable path:
   `/Applications/Xcode.app/Contents/Applications/Icon Composer.app/Contents/Executables/ictool`
6. Check beta `ictool` paths as needed:
   `/Applications/Xcode-beta.app/Contents/Applications/Icon Composer.app/Contents/Executables/ictool`
   `/Applications/Betas/Xcode-beta.app/Contents/Applications/Icon Composer.app/Contents/Executables/ictool`
7. Run `ictool --help` or `ictool --version` when preview export is part of the task.
8. Identify the target app project shape before promising Xcode integration.

Do not assume Icon Composer exists just because Xcode exists. Older Xcode installs, alternate Xcode locations, or standalone Icon Composer installs can change the path.

## Brief Intake

Collect a short brief before editing artwork or opening Icon Composer:

- app name
- target platforms
- app category and main user job
- brand colors, existing logo, or visual identity constraints
- required symbol, object, or metaphor
- source asset paths, if any
- whether text is allowed; default to no text for app icons
- preferred tone, such as utility, playful, premium, developer-tool, creative-tool, system-adjacent, or expressive
- whether Codex should operate Icon Composer through Computer Use or coach the user step by step

For Gale's default taste, prefer high contrast, strong shape separation, cool-leaning bright or pastel colors when no semantic palette is stronger, and retro-future or cyberpunk/vaporwave-friendly glow and linework when it fits the app. Do not force that style when the app's brand or category clearly points elsewhere.

## Source Artwork Preparation

Decide the layer plan before opening Icon Composer.

Prefer a small, legible layer stack:

- background field or shape
- primary symbol or object
- secondary detail or highlight
- optional foreground accent
- optional shadow, depth, or glow element

Keep source artwork flat, opaque, and simple before import when the goal is to let Icon Composer add material, blur, shadow, specular highlights, and appearance-mode adjustments.

Preferred source formats:

- SVG for crisp symbols and flat vector geometry
- PNG with transparent background for raster images, custom gradients, rendered effects, and non-SVG artwork
- high-resolution square source exports when bitmap artwork is unavoidable

Preserve editable source documents from the design editor separately from the `.icon` document. The `.icon` file is the app icon production source, but the upstream artwork file may still be needed for deeper changes.

## Preferred Mac Artwork Apps

When image editing software is needed, prefer established Mac-native tools before generic web or script-only tooling:

- Pixelmator Pro
- Acorn 8
- Retrobatch

Use the apps by job:

- Pixelmator Pro: detailed composition, masking, layer polish, effects, color adjustment, and high-quality source artwork edits.
- Acorn 8: fast bitmap edits, practical layer work, small icon asset adjustments, and lightweight Mac-native production work.
- Retrobatch: repeatable batch processing, resizing, format conversion, metadata cleanup, and export normalization.

Do not require these apps. If none are installed, use the user's available editor, Figma exports, Sketch, Illustrator, Photoshop, command-line conversion, generated artwork, or existing assets as appropriate.

## Computer Use Workflow

Use Computer Use only when the task requires operating the Icon Composer GUI through clicks, typing, dragging, importing files, changing controls, or inspecting visual previews.

Computer Use is appropriate for:

- launching Icon Composer
- creating or opening a `.icon` document
- importing source layers
- arranging layers and groups
- selecting platform and appearance previews
- adjusting visible canvas, group, layer, and inspector controls
- checking legibility at different sizes and backgrounds
- taking screenshots for comparison or teaching
- narrating a learning session while Gale watches

Computer Use must be careful around:

- overwriting an existing `.icon` document
- deleting, moving, or renaming local files through the GUI
- importing files from sensitive folders
- making Xcode project changes through the GUI

Follow the Computer Use confirmation policy before destructive or state-changing GUI actions. Saving a new local design document in an agreed working directory is normal workflow. Overwriting, deleting, moving, or renaming existing local files through the GUI needs explicit confirmation at action time.

For learning sessions:

1. Start with a tiny practice icon when the user has not used Icon Composer before.
2. Explain the visible screen in plain language before changing it.
3. Use short loops: change one visible setting, inspect the preview, then describe the effect.
4. Prefer screenshots or exported preview PNGs over long prose when judging variants.
5. Keep the user in the design loop for taste-heavy decisions.

## Icon Composer Production Pass

Use this sequence for real icon work:

1. Refresh Apple docs and inspect local tools.
2. Confirm the brief, platform targets, and source artwork plan.
3. Prepare or export source layers from the chosen design app.
4. Open Icon Composer through Computer Use only when the user wants GUI help.
5. Import layers and preserve their visual order.
6. Organize related layers into groups when the live app supports it.
7. Tune Liquid Glass, color, composition, and appearance-mode settings in the GUI.
8. Preview the icon across target platforms, appearances, sizes, backgrounds, and grid overlays.
9. Save the `.icon` document as the durable app icon artifact.
10. Export PNG previews through Icon Composer or `ictool` for review artifacts.
11. Hand off Xcode project integration to the Xcode workflow skills.

If the icon is too complex or illustrative for the layered model, say so plainly and consider an ordinary image-based Xcode app icon path instead.

## `ictool` Preview Export

Use `ictool` after a `.icon` document exists. Treat it as a preview and review helper, not as the main design surface.

Example shape:

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

Discover exact platform and rendition values from current `ictool --help`, Apple docs, or live errors. Do not hard-code assumptions beyond examples.

Use preview exports to:

- compare variants
- attach review artifacts
- check legibility at multiple sizes
- validate default, dark, clear, tinted, mono, or other current appearances when supported
- preserve a visual record before Xcode integration

## Xcode Integration Handoff

When integrating into an existing app project:

1. Inspect the repo and project shape first.
2. Use `xcode-build-run-workflow` for project integration, build, run, and app-preview validation.
3. Preserve tracked Xcode project files and asset catalogs intentionally.
4. Do not hand-edit generated project files or package-manager outputs.
5. Treat `.icon` as the source app icon artifact when Xcode supports it.
6. Run the narrowest useful project validation after integration.

For a new native Apple app, use `bootstrap-xcode-app-project` before icon production.

## Future Packaged Agent Direction

Keep the future Mac App Store agent direction visible, but do not let it expand this skill's first implementation.

The future packaged agent could:

- collect an app brief and target platforms
- guide source artwork preparation in Mac-native editors
- operate or hand off to Icon Composer with clear user consent
- export preview sets through `ictool`
- help compare variants visually
- integrate an approved `.icon` document into an Xcode project
- preserve source artwork, preview exports, and decision notes in a project-local icon workspace

Product constraints to preserve:

- Mac App Store distribution may constrain automation, permissions, sandboxing, file access, and control of other apps.
- GUI automation of Icon Composer may require accessibility permissions or a user-driven handoff model.
- The packaged app should be a guided production assistant, not a fully autonomous designer.
- The Codex skill should remain useful before any packaged app exists.
- Keep local-first design and file handling as the default, with explicit consent before uploading, sharing, or transmitting artwork.

## Validation

For Socket implementation work involving this skill:

```bash
uv run scripts/validate_socket_metadata.py
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
```

From `plugins/apple-dev-skills`, run `uv run pytest` only when tests, validation helpers, or scripts changed.

## Handoffs

- `explore-apple-swift-docs`: fresh Apple documentation research beyond the docs gate in this skill.
- `bootstrap-xcode-app-project`: brand-new native Apple app scaffolding.
- `xcode-build-run-workflow`: existing Xcode project integration, build, run, and app validation.
- `xcode-testing-workflow`: test-specific work after icon integration affects a project.
- `swiftui-app-architecture-workflow`: app UI design or implementation work that is not the app icon itself.
