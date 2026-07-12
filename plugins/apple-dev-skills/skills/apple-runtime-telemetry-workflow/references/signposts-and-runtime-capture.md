# Signposts and Runtime Capture

Use `OSSignposter` for an interval or event that must be measured in Instruments. It shares the same subsystem/category model as unified logging. A signposted interval has one begin and one matching end; retain the interval state and end it on every completed path.

Good candidates are launch phases, a document load, a command execution, an image decode, or a scene transition with a concrete start and finish. Do not signpost every view body evaluation or high-frequency event without a measured reason.

Inspect signposts in an Instruments capture while performing the named scenario. For iOS simulator trace, ETTrace, symbols, and memory evidence, use `ios-runtime-forensics-workflow` so logging remains the supporting signal rather than a substitute for runtime proof.

Sources read through Xcode-local documentation:

- `doc://com.apple.documentation/documentation/os/recording-performance-data`
- `doc://com.apple.documentation/documentation/os/OSSignposter`
