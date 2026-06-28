# Engine Graph And Repair

Use current AVFAudio documentation before proposing graph changes. Start from:

- `AVAudioEngine`: graph ownership, runtime mutation limits, manual rendering, and node lifecycle.
- `AVAudioNode`: attachment, busses, and exact format matching except where mixers and output nodes convert.
- `AVAudioInputNode` and `AVAudioOutputNode`: hardware availability and enabled-state checks.
- `AVAudioPlayerNode`: scheduling and completion callbacks.
- `AVAudioSourceNode` and `AVAudioSinkNode`: render-block boundaries.
- `AVAudioUnit`: async instantiation and underlying Core Audio unit access.

Type ownership:

- Keep graph topology in `AVAudioEngine`, `AVAudioNode`, `AVAudioInputNode`, `AVAudioOutputNode`, `AVAudioMixerNode`, `AVAudioPlayerNode`, `AVAudioSourceNode`, `AVAudioSinkNode`, and `AVAudioUnit` terms until the graph is inspected.
- Keep audio formats and buffers as `AVAudioFormat`, `AVAudioPCMBuffer`, `AVAudioFile`, `AVAudioConverter`, or `AudioStreamBasicDescription` where those values still configure Apple APIs.
- Use `AVAudioUnit` as the first modern hosting boundary for Audio Units; drop to Core Audio `AudioUnit` only when the required unit behavior is not exposed through AVFAudio.
- Introduce custom graph or format descriptors only as app-domain summaries, test fixtures, or persistence shapes, and keep the conversion back to AVFAudio explicit.

Repair checklist:

- Draw the graph in text: owner, nodes, attachment order, connection order, formats, start, schedule, stop, and teardown.
- Confirm every useful node is attached before connection or use.
- Check bus formats at each edge before adding converters or mixers.
- Use mixers deliberately when channel-count or format conversion needs a stable boundary.
- Keep completion handlers and callback thread context explicit.
- Treat manual rendering as a separate mode where the app drives rendering and the engine disconnects from devices.

Bad shapes:

- One global engine whose nodes are mutated by unrelated UI, file playback, capture, and effects code.
- Hidden format conversion helpers that make failures harder to inspect.
- Rebuilding the graph on every UI state change instead of separating graph lifecycle from control parameters.
