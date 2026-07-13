# Compressor Job And Delivery Contract

Use this reference when preparing, changing, or verifying a Compressor job.

## Preflight

- Identify the source file or upstream Final Cut Pro/Motion deliverable.
- Say whether the source must remain unchanged and where the new artifact belongs.
- Record the delivery requirements: platform, container, codec, resolution, frame rate, audio, captions, HDR/color, metadata, file-size target, and deadline.
- Inspect existing jobs, selected settings, destinations, actions, output names, and warnings before editing.

## Decision Rules

| Situation | Safe default |
| --- | --- |
| Existing reusable job or preset | Duplicate or make a new project before changing it. |
| Unknown delivery platform requirements | Ask for the target or produce a clearly labeled review master; do not guess social/platform presets. |
| Existing output name in destination | Stop and ask whether to overwrite, version, or choose a new directory. |
| Batch input | List every source and destination before submission. |
| Watch folder | Explain ongoing automation, input handling, and output location before enabling or changing it. |
| Failed/stalled job | Capture job name, input, setting, destination, warning/error text, and whether output was partially written. |

## Verification

Inspect the completed output rather than relying only on the job list:

- correct directory and final file name;
- expected duration and dimensions;
- expected container and codec;
- audio presence, layout, and sample rate when relevant;
- required captions, metadata, color/HDR, or packaging behavior;
- no accidental overwrite of the source or previous delivery.

Use target-platform playback/testing when compatibility is the actual requirement.
