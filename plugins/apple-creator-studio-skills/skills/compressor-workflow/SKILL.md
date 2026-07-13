---
name: compressor-workflow
description: Guide safe Apple Compressor projects, presets, destinations, batches, watch-folder decisions, Final Cut Pro or Motion handoffs, job monitoring, and delivery-artifact verification. Use when a user needs to transcode or package media in Compressor without losing source media or overwriting the wrong output.
---

# Compressor Workflow

Use this skill for Compressor app operation, not low-level codec code or an assumed Compressor command-line interface.

## Source Check

Open Compressor Help or search the local Tips/Help Viewer catalog for `Compressor`. Confirm that the guide matches the installed app/version before relying on a menu path, preset behavior, or automation feature. Read `references/job-and-delivery-contract.md` for the shared preflight and verification contract.

## Workflow

1. Classify the task: one-off export, batch, preset customization, destination setup, watch-folder decision, Final Cut Pro/Motion handoff, failed job, or artifact verification.
2. Establish the artifact contract: source location, whether it must stay untouched, codec/container, dimensions, frame rate, audio layout/sample rate, captions/HDR/metadata requirements, destination, overwrite rule, and delivery target.
3. Inspect the active Compressor project before changing it: selected jobs, applied settings, destinations, job actions, output names, and any warning or missing-media state.
4. Preserve source state. Prefer a new project or duplicate when altering an existing reusable preset/job. Do not relink, remove jobs, replace source media, or overwrite a prior delivery without a visible user confirmation.
5. Choose the smallest correct setting/preset and destination. Explain any tradeoff between delivery requirements, quality, file size, compatibility, and time. Do not invent a platform specification the user has not supplied.
6. Before submitting, state the exact input, output name, destination, overwrite behavior, setting, and any batch/watch-folder effect. Get confirmation before starting a render, transcode, or operation that can overwrite an artifact.
7. Monitor the job and stop on an unexpected alert, missing-media/extension condition, failed status, or output-location mismatch. Report the concrete job, setting, destination, and error context.
8. Verify the completed artifact against the contract: existence, destination, file name, duration, dimensions, codec/container, audio, and any required captions/HDR/metadata. Record limits that require target-platform testing.

## Guards

- Do not treat the `Compressor Creator Studio` executable as a supported CLI. Use a separately verified command-line media workflow when reproducible CLI encoding is the requirement.
- Do not mistake a completed job for an acceptable delivery; inspect the artifact.
- Do not apply a preset merely because its label sounds right. Check its actual settings and target requirements.
- Do not turn on watch folders or job actions without explaining their persistent or automatic behavior and receiving confirmation.
- Hand framework code, custom readers/writers, or per-frame codec work to `apple-dev-skills` media workflows.

## Handoffs

- `logic-pro-workflow` for music/stem preparation before final delivery.
- `final-cut-pro-workflow` for editing, sharing, and source-master preparation; `motion-workflow` for composition and template authoring. Compressor owns the transcode/delivery step.
- `apple-dev-skills:video-codec-processing-workflow` or `avfoundation-media-pipeline-workflow` for code-level media processing.
- A verified `ffmpeg` workflow when a CLI artifact contract is explicitly required.
