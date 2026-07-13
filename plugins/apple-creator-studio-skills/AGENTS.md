# AGENTS.md

This file is the Apple Creator Studio Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general Git, documentation, release, and validation workflow.

## Scope

- `apple-creator-studio-skills` owns human-facing and Computer Use-aware operation of Apple Creator Studio applications.
- Root `skills/` is the authored workflow surface.
- The first shipped skills own Compressor delivery jobs, Logic Pro production sessions, and MainStage concert preparation.
- This is a guidance plugin, not an unattended app-control daemon, media-processing runtime, or bundled copy of Apple Help.

## Boundaries

- Use `apple-dev-skills` for Swift, Xcode, Apple framework, AVFoundation, AVFAudio, Core Media, Core Audio, VideoToolbox, Core Image, and Image I/O implementation work.
- Use this plugin when the task operates an app project, library, session, concert, set, patch, preset, batch, destination, export, bounce, or delivery artifact.
- Use the local Tips/Help Viewer catalog and the app's Help menu to find installed-app guides when available. Confirm the opened guide matches the installed app and version; use official Apple support material when the local guide is missing or incomplete.
- Do not claim the `com.apple.tips` shell is the usable documentation surface on this Mac. The observed usable surface is `com.apple.helpviewer`, which displays the Tips/user-guide catalog.

## Safety

- Inspect the active app, selected document/project, output destination, and overwrite behavior before mutations.
- Preserve source media, sessions, concerts, patches, libraries, and projects by default.
- Require a visible user confirmation before actions that overwrite, delete, relink, replace takes, change routing or mappings, render, bounce, transcode, publish, record, or alter a live-performance configuration.
- Treat a completed UI action as insufficient proof. Verify the resulting artifact, job status, route, patch, or playback state.
- Never validate against a user’s live performance configuration. Use a disposable rehearsal fixture and observed device evidence.

## Validation

Run skill validation for every changed workflow:

```bash
uv run python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/<skill-name>
```

When manifest, marketplace, or root documentation changes, also run:

```bash
uv run scripts/validate_socket_metadata.py
```
