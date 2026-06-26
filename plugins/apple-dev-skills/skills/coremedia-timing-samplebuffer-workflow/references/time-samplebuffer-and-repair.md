# Time Sample Buffer And Repair

Use current Core Media documentation before changing timing behavior. Start from:

- `CMTime`: value, timescale, flags, epoch, validity, and indefinite states.
- `CMTimeRange`: start, duration, and end.
- `CMClock` and `CMTimebase`: host and media time relationships.
- `CMFormatDescription`: media type and format metadata.
- `CMSampleBuffer`: data readiness, timing, attachments, and media payload.
- `AVSampleBufferDisplayLayer` and `AVSampleBufferRenderSynchronizer`: display and synchronization behavior.

Repair checklist:

- Print or inspect exact `CMTime` values, timescales, flags, and validity before changing math.
- Preserve the distinction between presentation timestamp, decode timestamp, and duration.
- Confirm the sample's media type and format description before appending or rendering.
- Treat dropped sample buffers as metadata-bearing evidence, not normal samples.
- Use a timebase tied to the appropriate clock when synchronizing video to audio.
- Check whether the bug is produced by capture, transformation, writer, display, or synchronizer before editing timestamps.

Bad shapes:

- Converting every `CMTime` to `Double` early and hiding precision loss.
- Replacing invalid time with zero without documenting why zero is correct.
- Copying sample buffers while losing attachments or format descriptions.
