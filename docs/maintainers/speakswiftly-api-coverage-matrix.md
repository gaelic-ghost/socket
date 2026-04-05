# SpeakSwiftly API Coverage Matrix

## Purpose

This document compares the public `SpeakSwiftly` library surface in the sibling `../SpeakSwiftly` checkout against the client-facing surfaces implemented by `SpeakSwiftlyServer`.

It is meant to answer three concrete questions:

1. Which public `SpeakSwiftly` capabilities are already exposed here?
2. Which public capabilities are only partially exposed or intentionally hidden?
3. Which surface is the more appropriate client contract for each capability: HTTP, MCP, both, or neither?

Current baseline checked against sibling tag `v0.9.1`.

The sibling `SpeakSwiftly` checkout has since moved forward with a repackaged public dependency surface plus new runtime helpers for voice cloning and text-profile management. That follow-through pass is now landed here:

1. package and import alignment
   `SpeakSwiftlyServer` now depends on `TextForSpeech` directly instead of assuming the sibling package re-exports it
2. runtime-call alignment
   the server bridge now uses the current `speak(..., textContext:id:)` shape that the current sibling runtime exposes for this flow
3. transport-surface expansion
   `createClone(...)` plus the new text-profile inspection and editing helpers now have first-class HTTP and MCP coverage

## Summary

`SpeakSwiftlyServer` exposes almost the entire public runtime control plane:

- runtime lifecycle and readiness are represented through host startup plus health and status endpoints
- speech submission, profile mutation, queue inspection, playback control, queue clearing, and request cancellation are all exposed
- runtime status and request-event streams are translated into job snapshots, SSE, host snapshots, and MCP resources

What is not exposed one-to-one today:

- the library-only `accept(line:)` request-decoding entrypoint
- the raw library event and status stream types as first-class client contracts
- some library detail enums and payload types in their native shape

That means the server is best understood as a transport-oriented adapter over the public runtime, not as a byte-for-byte network mirror of the Swift library API.

## Coverage Matrix

| Public `SpeakSwiftly` symbol or capability | Server coverage | HTTP surface | MCP surface | Notes |
| --- | --- | --- | --- | --- |
| `SpeakSwiftly.live()` | Indirect | No direct route | No direct tool | Server owns runtime creation internally. Correctly host-local. |
| `SpeakSwiftly.Runtime.start()` | Indirect | No direct route | No direct tool | Starts during process boot. Correctly host-local for this server architecture. |
| `SpeakSwiftly.Runtime.shutdown()` | Indirect | No direct route | No direct tool | Runs during process shutdown. Correctly host-local. |
| `SpeakSwiftly.Runtime.statusEvents()` | Adapted | `GET /healthz`, `GET /readyz`, `GET /status`, `GET /jobs/{job_id}/events` | `status` tool, `speak://status`, `speak://runtime`, subscriptions | Exposed as derived host snapshots and worker-status events rather than raw stream subscription. |
| `SpeakSwiftly.Runtime.speak(text:with:as:context:id:)` | Full for current public job cases | `POST /speak` | `queue_speech_live` | `job` is fixed to `.live`, which matches current public enum cases. Normalization context is exposed through `cwd` and `repo_root`. |
| `SpeakSwiftly.Runtime.createProfile(named:from:voice:outputPath:id:)` | Full | `POST /profiles` | `create_profile` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.createClone(named:from:transcript:id:)` | Full | `POST /profiles/clone` | `create_clone` | Exposed as a retained voice-profile job flow just like profile creation and removal. |
| `SpeakSwiftly.Runtime.profiles(id:)` | Full | `GET /profiles` | `list_profiles`, `speak://profiles` | Exposed as cached host view rather than raw request handle. Appropriate. |
| `SpeakSwiftly.Runtime.removeProfile(named:id:)` | Full | `DELETE /profiles/{profile_name}` | `remove_profile` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.activeTextProfile()` | Full | `GET /text-profiles`, `GET /text-profiles/active` | `list_text_profiles`, `speak://text-profiles`, `speak://text-profiles/active` | Exposed as synchronous text-profile state, intentionally separate from retained voice-profile jobs. |
| `SpeakSwiftly.Runtime.baseTextProfile()` | Full | `GET /text-profiles`, `GET /text-profiles/base` | `list_text_profiles`, `speak://text-profiles`, `speak://text-profiles/base` | Full read-model exposure. |
| `SpeakSwiftly.Runtime.textProfiles()` | Full | `GET /text-profiles`, `GET /text-profiles/stored/{profile_id}` | `list_text_profiles`, `speak://text-profiles`, `speak://text-profiles/stored/{profile_id}` | Full read-model exposure for stored text profiles. |
| `SpeakSwiftly.Runtime.effectiveTextProfile(named:)` | Full | `GET /text-profiles/effective`, `GET /text-profiles/effective/{profile_id}` | `speak://text-profiles/effective`, `speak://text-profiles/effective/{profile_id}` | Exposed as the merged base-plus-selected-profile snapshot. |
| `SpeakSwiftly.Runtime.createTextProfile(id:named:replacements:)` | Full | `POST /text-profiles/stored` | `create_text_profile` | Stored text-profile creation is synchronous, not job-based. |
| `SpeakSwiftly.Runtime.storeTextProfile(_:)` | Full | `PUT /text-profiles/stored/{profile_id}` | `store_text_profile` | Full whole-profile persistence path. |
| `SpeakSwiftly.Runtime.useTextProfile(_:)` | Full | `PUT /text-profiles/active` | `use_text_profile` | Active custom text-profile selection is synchronous state mutation. |
| `SpeakSwiftly.Runtime.removeTextProfile(named:)` | Full | `DELETE /text-profiles/stored/{profile_id}` | `remove_text_profile` | Full stored-profile removal path. |
| `SpeakSwiftly.Runtime.resetTextProfile()` | Full | `POST /text-profiles/active/reset` | `reset_text_profile` | Full active-profile reset path. |
| `SpeakSwiftly.Runtime.addTextReplacement(...)` | Full | `POST /text-profiles/active/replacements`, `POST /text-profiles/stored/{profile_id}/replacements` | `add_text_replacement` | Full replacement-add path for both active and stored text profiles. |
| `SpeakSwiftly.Runtime.replaceTextReplacement(...)` | Full | `PUT /text-profiles/active/replacements/{replacement_id}`, `PUT /text-profiles/stored/{profile_id}/replacements/{replacement_id}` | `replace_text_replacement` | Full replacement-update path for both active and stored text profiles. |
| `SpeakSwiftly.Runtime.removeTextReplacement(...)` | Full | `DELETE /text-profiles/active/replacements/{replacement_id}`, `DELETE /text-profiles/stored/{profile_id}/replacements/{replacement_id}` | `remove_text_replacement` | Full replacement-removal path for both active and stored text profiles. |
| `SpeakSwiftly.Runtime.queue(_:id:)` for `.generation` | Full | `GET /queue/generation` | `list_queue_generation` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.queue(_:id:)` for `.playback` | Full | `GET /queue/playback` | `list_queue_playback` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.playback(.pause/.resume/.state,id:)` | Full | `GET /playback`, `POST /playback/pause`, `POST /playback/resume` | `playback_state`, `playback_pause`, `playback_resume` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.clearQueue(id:)` | Full | `DELETE /queue` | `clear_queue` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.cancelRequest(_:requestID:)` | Full | `DELETE /queue/{request_id}` | `cancel_request` | Full control-plane exposure. |
| `SpeakSwiftly.Runtime.accept(line:)` | Not exposed | None | None | Correctly not exposed. This is a line-oriented transport/parser bridge, not a good client contract. |
| `SpeakSwiftly.RequestHandle` | Adapted | `202` job response + `GET /jobs/{job_id}` | accepted-job tool result + `speak://jobs/{job_id}` | Exposed through host-owned job identity and retention rather than raw async streams. Appropriate. |
| `SpeakSwiftly.RequestEvent` | Adapted | `GET /jobs/{job_id}/events`, `GET /jobs/{job_id}` | job resources only indirectly | Mapped into `ServerJobEvent`. Good translation, but not native-shape parity. |
| `SpeakSwiftly.StatusEvent` | Adapted | health/readiness/status + SSE worker-status events | status/runtime resources + subscriptions | Good host-oriented translation. |
| `SpeakSwiftly.ProfileSummary` | Adapted | `GET /profiles`, status payloads | `list_profiles`, `speak://profiles`, profile detail resource | Translated into `ProfileSnapshot` with same core fields in HTTP/MCP-friendly shape. |
| `SpeakSwiftly.ActiveRequest` | Adapted | queue/playback/status payloads | queue tools/resources | Good translation. |
| `SpeakSwiftly.QueuedRequest` | Adapted | queue/status payloads | queue tools/resources | Good translation. |
| `SpeakSwiftly.PlaybackStateSnapshot` | Adapted | playback/status payloads | playback tools/resources | Good translation. |
| `SpeakSwiftly.Success` terminal payloads | Adapted | job snapshots and SSE | tool results and resources indirectly | Correctly translated into stable server response models. |
| `SpeakSwiftly.Failure` / `SpeakSwiftly.Error` / `SpeakSwiftly.ErrorCode` | Adapted | HTTP errors, job failure events | MCP errors and failed job resources indirectly | Exposed semantically, not one-to-one structurally. |
| `SpeakSwiftly.Job.live` | Full | `POST /speak` | `queue_speech_live` | Currently only public job case, fully supported. |
| `SpeakSwiftly.Queue.generation` / `.playback` | Full | queue routes | queue tools | Fully supported. |
| `SpeakSwiftly.PlaybackAction.pause` / `.resume` / `.state` | Full | playback routes | playback tools | Fully supported. |
| `SpeakSwiftly.PlaybackState.idle` / `.playing` / `.paused` | Full | playback/status/job payloads | playback/status resources | Fully supported. |
| `SpeakSwiftly.StatusStage`, `RequestEventName`, `ProgressStage`, `QueuedReason` | Adapted | surfaced in SSE/job payloads | surfaced in job/resources | Exposed by value, but through server event wrappers rather than raw library payload structs. |

## Intentional Non-Parity

These items should stay server-internal or transport-adapted unless the product goals change:

- `SpeakSwiftly.live()`, `Runtime.start()`, and `Runtime.shutdown()`
  These are host-lifecycle concerns, not client operations.

- `Runtime.accept(line:)`
  This is a line-based transport and request-decoding entrypoint. It is useful inside the library or CLI boundary, but it would be the wrong abstraction for HTTP or MCP clients.

- raw `AsyncThrowingStream` and `AsyncStream` handles
  HTTP and MCP clients are better served by retained jobs, SSE, resources, and polling endpoints than by trying to mimic Swift concurrency primitives on the wire.

## Concrete Gaps

### 1. HTTP had no retained job listing route

`ServerHost` already exposes `jobSnapshots()`, and MCP already exposes:

- `speak://jobs`
- `speak://jobs/{job_id}`

This gap is now closed by `GET /jobs`, so HTTP and MCP both have a retained-job discovery path.

### 2. MCP accepted-job results had pointed to status, not direct job detail

This gap is now closed. Accepted-job MCP results return both `status_resource_uri` and `job_resource_uri`.

### 3. MCP tool naming still follows worker-op vocabulary

Names such as `queue_speech_live`, `list_queue_generation`, and `playback_state` are perfectly valid, but they still read like protocol operation names. That makes sense historically because they line up with the worker op names, but it is slightly less ergonomic for higher-level clients than a more product-shaped vocabulary.

This is not a correctness issue. It is mainly a polish and ergonomics issue.

## Surface Appropriateness

## HTTP

HTTP is the best client surface for:

- local apps
- UI processes
- scripting clients
- anything that wants stable request and response payloads

Why it works well:

- submission uses a clean `202 Accepted` job model
- long-running work is retained and inspectable
- SSE provides a reasonable transport for live updates
- health, readiness, queue, playback, and status concepts are easy for non-Swift clients to consume

Main weaknesses:

- explicitly localhost and trust-boundary-local, not a general remote API
- no explicit API versioning yet

## MCP

MCP is the best client surface for:

- agent tooling
- operator workflows
- prompt-driven or assistant-driven control flows
- consumers that benefit from resource subscriptions and prompt catalog support

Why it works well:

- tools map naturally to command-style operations
- resources provide a read model without forcing clients to orchestrate polling manually
- subscriptions make runtime updates convenient for agent hosts
- prompts are a good fit for reusable voice-design and acknowledgement authoring

Main weaknesses:

- tool names still skew low-level and protocol-shaped
- some data is easier to discover through resource conventions than through tool-return schemas alone

## Recommended Next Moves

The highest-value library-alignment follow-through items from the previous review are now landed:

1. `POST /speak` and `queue_speech_live` both accept normalization context through `cwd` and `repo_root`.
2. HTTP now exposes `GET /jobs`.
3. Accepted-job MCP results now include `job_resource_uri`.
4. Voice clone creation now has matching HTTP and MCP job flows.
5. Text-profile inspection and replacement editing now have matching HTTP routes, MCP tools, and MCP resources.

At this point, the remaining differences are mostly intentional transport adaptations rather than missing runtime capabilities.

## Next Follow-Through Slice

The next library-alignment pass should focus on downstream contract verification and cleanup instead of new feature reach:

1. verify adjacent HTTP consumers agree with the new voice-clone and text-profile route family
2. decide whether any remaining low-level MCP tool names should be promoted to more product-shaped names
3. remove any server-local transport translation that is still redundant now that both `SpeakSwiftly` and `TextForSpeech` are wired through directly
