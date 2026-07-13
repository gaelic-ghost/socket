# Agent-Assisted Translation

## Boundary

Xcode 27's coding agents can help prepare a project, build targets to discover strings, populate String Catalogs, and identify localization issues. This is an optional beta-era workflow layered on a normal catalog-first project. It does not change the source API, ownership, review, or privacy requirements.

Before invoking an agent, establish the target languages and regions, glossary, audience, tone, names to retain, prohibited translations, and which catalogs/targets are in scope. Verify the active Xcode version, agent surface, permissions, and live String Catalog tools through `xcode-coding-intelligence-workflow`; tool names are not a stable contract in this workflow.

## Review contract

Ask the agent to make a reviewable, bounded locale change. Inspect the catalog and XLIFF diff, preserve machine-translation provenance, and have a fluent human reviewer check the output before shipment. Re-run locale and layout validation after changes. Do not send secrets, private user content, or text outside the approved translation scope to an agent or provider.

Apple's [Translate your app using agents in Xcode](https://developer.apple.com/videos/play/wwdc2026/213/) session documents the project preparation/build flow, language-specific Xcode guidance, machine-translation provenance in XLIFF, and the need to gather native-speaker feedback. The behavior is Xcode 27 beta-specific as checked on 2026-07-13.
