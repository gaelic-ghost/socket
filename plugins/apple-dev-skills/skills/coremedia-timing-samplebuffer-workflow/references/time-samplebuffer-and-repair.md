# Time Sample Buffer And Repair

Use current Core Media documentation before changing timing behavior. Start from:

- `CMTime`: value, timescale, flags, epoch, validity, and indefinite states.
- `CMTimeRange`: start, duration, and end.
- `CMClock` and `CMTimebase`: host and media time relationships.
- `CMFormatDescription`: media type and format metadata.
- `CMSampleBuffer`: data readiness, timing, attachments, and media payload.
- `AVSampleBufferDisplayLayer` and `AVSampleBufferRenderSynchronizer`: display and synchronization behavior.

Type ownership:

- Keep media time as `CMTime`, `CMTimeRange`, `CMTimeMapping`, `CMClock`, and `CMTimebase` while the value participates in capture, editing, writer, display, render synchronizer, or audio/video synchronization behavior.
- Keep sample payloads as `CMSampleBuffer` and inspect `CMSampleTimingInfo`, `CMFormatDescription`, `CMBlockBuffer`, attachments, readiness, and dropped-buffer metadata before copying or projecting them into app-specific records.
- Keep media format facts in `CMFormatDescription` while appending, rendering, synchronizing, or diagnosing samples. Do not replace it with a codec string unless the framework boundary is already complete.
- Convert to `Double`, `TimeInterval`, `Date`, dictionaries, or app-specific structs only at UI, reporting, wire, persistence, or fixture boundaries, and document precision loss, invalid-time handling, and any dropped attachments.

Repair checklist:

- Print or inspect exact `CMTime` values, timescales, flags, and validity before changing math.
- Preserve the distinction between presentation timestamp, decode timestamp, and duration.
- Confirm the sample's media type and format description before appending or rendering.
- Keep `CMSampleTimingInfo` sample-specific when samples have distinct timestamps instead of flattening timing into one display time.
- Treat dropped sample buffers as metadata-bearing evidence, not normal samples.
- Use a timebase tied to the appropriate clock when synchronizing video to audio.
- Check whether the bug is produced by capture, transformation, writer, display, or synchronizer before editing timestamps.

Bad shapes:

- Converting every `CMTime` to `Double` early and hiding precision loss.
- Replacing invalid time with zero without documenting why zero is correct.
- Copying sample buffers while losing attachments or format descriptions.
