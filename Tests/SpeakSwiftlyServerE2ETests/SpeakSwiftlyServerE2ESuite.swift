import Foundation
import Testing
#if canImport(Darwin)
import Darwin
#endif

// MARK: - End-to-End Suite

/// Keep the suite type name stable so Xcode test plans can target it directly.
@Suite(
    .serialized,
    .enabled(
        if: ProcessInfo.processInfo.environment["SPEAKSWIFTLYSERVER_E2E"] == "1",
        "Set SPEAKSWIFTLYSERVER_E2E=1 to run live end-to-end coverage."
    )
)
struct SpeakSwiftlyServerE2ETests {
    // MARK: - Test Fixtures

    static let testingProfileText = "Hello there from SpeakSwiftlyServer end-to-end coverage."
    static let testingProfileVoiceDescription = "A generic, warm, masculine, slow speaking voice."
    static let testingCloneSourceText = """
    This imported reference audio should let SpeakSwiftlyServer build a clone profile for end to end coverage with a clean transcript and steady speech.
    """
    static let testingPlaybackText = """
    Hello from the real resident SpeakSwiftlyServer playback path. This end to end test uses a longer utterance so we can observe startup buffering, queue floor recovery, drain timing, and steady streaming behavior with enough generated audio to make the diagnostics useful instead of noisy.
    """
    static let operatorControlPlaybackText = """
    Hello from the SpeakSwiftlyServer operator control lane. This coverage keeps the first request alive long enough to exercise pause and resume without falling into a trivially short utterance. After the opening section, the text shifts topics so the generated audio does not just repeat one sentence over and over while we are listening for queue mutations. We then move into a calmer wrap up that still leaves enough duration for queued cancellation and queue clearing to happen while the first playback-owned request continues draining toward completion.
    """
}
