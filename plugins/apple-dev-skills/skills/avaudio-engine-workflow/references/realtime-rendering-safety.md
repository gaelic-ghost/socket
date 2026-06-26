# Realtime Rendering Safety

Audio render callbacks and source or sink node blocks are time-sensitive. Keep them boring.

Avoid inside render paths:

- allocation
- locks
- file I/O
- network I/O
- logging
- `await`
- main-actor hops
- SwiftUI or AppKit updates
- broad notification posting
- work that can block on another thread

Repair pattern:

- Preallocate buffers and state outside the render path.
- Use lock-free or bounded handoff only when the design truly needs cross-thread communication.
- Move UI and persistence updates to a non-real-time queue after capturing minimal state.
- Make callback ownership explicit so object lifetimes outlive the audio unit, source node, sink node, or tap.
- If the code cannot satisfy real-time constraints, move the work to offline rendering or a non-real-time processing stage.
