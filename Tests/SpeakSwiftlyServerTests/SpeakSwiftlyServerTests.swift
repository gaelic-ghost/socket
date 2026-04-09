import Foundation
import Hummingbird
import HummingbirdTesting
import HTTPTypes
import SpeakSwiftlyCore
import Testing
import TextForSpeech
@testable import SpeakSwiftlyServer

// MARK: - Route Tests

/// Keep these lifecycle-heavy route and MCP tests serialized so Swift Testing
/// does not interleave independent hosts, MCP surfaces, and held-open requests.
@Suite(.serialized)
struct SpeakSwiftlyServerTests {

@available(macOS 14, *)
@Test func routesExposeHealthProfilesAndQueuedSpeechJobLifecycle() async throws {
    let runtime = MockRuntime()
    let configuration = testConfiguration()
    let state = await MainActor.run { ServerState() }
    let runtimeProfileRootURL = URL(fileURLWithPath: NSTemporaryDirectory())
        .appendingPathComponent(UUID().uuidString, isDirectory: true)
        .appendingPathComponent("profiles", isDirectory: true)
    let host = ServerHost(
        configuration: configuration,
        runtime: runtime,
        runtimeConfigurationStore: .init(
            environment: ["SPEAKSWIFTLY_PROFILE_ROOT": runtimeProfileRootURL.path],
            activeRuntimeSpeechBackend: .qwen3
        ),
        state: state
    )

    await host.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(host)

    let app = assembleHBApp(configuration: testHTTPConfig(configuration), host: host)
    try await app.test(.router) { client in
        let healthResponse = try await client.execute(uri: "/healthz", method: .get)
        let healthJSON = try jsonObject(from: healthResponse.body)
        #expect(healthResponse.status == .ok)
        #expect(healthJSON["status"] as? String == "ok")
        #expect(healthJSON["worker_ready"] as? Bool == true)

        let runtimeHostResponse = try await client.execute(uri: "/runtime/host", method: .get)
        let runtimeHostJSON = try jsonObject(from: runtimeHostResponse.body)
        let runtimeRefresh = try #require(runtimeHostJSON["runtime_refresh"] as? [String: Any])
        #expect((runtimeRefresh["sequence_id"] as? Int ?? 0) > 0)
        #expect(runtimeRefresh["source"] as? String == "runtime_overview")
        #expect((runtimeRefresh["started_at"] as? String)?.isEmpty == false)
        #expect((runtimeRefresh["generation_queue_refreshed_at"] as? String)?.isEmpty == false)
        #expect((runtimeRefresh["playback_queue_refreshed_at"] as? String)?.isEmpty == false)
        #expect((runtimeRefresh["playback_state_refreshed_at"] as? String)?.isEmpty == false)
        #expect((runtimeRefresh["completed_at"] as? String)?.isEmpty == false)

        let runtimeConfigResponse = try await client.execute(uri: "/runtime/configuration", method: .get)
        let runtimeConfigJSON = try jsonObject(from: runtimeConfigResponse.body)
        #expect(runtimeConfigResponse.status == .ok)
        #expect(runtimeConfigJSON["active_runtime_speech_backend"] as? String == "qwen3")
        #expect(runtimeConfigJSON["next_runtime_speech_backend"] as? String == "qwen3")
        #expect(runtimeConfigJSON["persisted_configuration_state"] as? String == "missing")

        let updateRuntimeConfigResponse = try await client.execute(
            uri: "/runtime/configuration",
            method: .put,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"speech_backend":"marvis"}"#)
        )
        let updateRuntimeConfigJSON = try jsonObject(from: updateRuntimeConfigResponse.body)
        #expect(updateRuntimeConfigResponse.status == .ok)
        #expect(updateRuntimeConfigJSON["active_runtime_speech_backend"] as? String == "qwen3")
        #expect(updateRuntimeConfigJSON["next_runtime_speech_backend"] as? String == "marvis")
        #expect(updateRuntimeConfigJSON["persisted_speech_backend"] as? String == "marvis")
        #expect(updateRuntimeConfigJSON["persisted_configuration_state"] as? String == "loaded")

        let profilesResponse = try await client.execute(uri: "/voices", method: .get)
        let profilesJSON = try jsonObject(from: profilesResponse.body)
        let profiles = try #require(profilesJSON["profiles"] as? [[String: Any]])
        #expect(profiles.count == 1)
        #expect(profiles.first?["profile_name"] as? String == "default")

        let createTextProfileResponse = try await client.execute(
            uri: "/text-profiles/stored",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(
                #"{"id":"swift-docs","name":"Swift Docs","replacements":[{"id":"replace-1","text":"SPM","replacement":"Swift Package Manager","match":"whole_token","phase":"before_built_ins","is_case_sensitive":false,"formats":["swift_source"],"priority":3}]}"#
            )
        )
        let createTextProfileJSON = try jsonObject(from: createTextProfileResponse.body)
        let createdTextProfile = try #require(createTextProfileJSON["profile"] as? [String: Any])
        #expect(createTextProfileResponse.status == .ok)
        #expect(createdTextProfile["id"] as? String == "swift-docs")

        let textProfilesResponse = try await client.execute(uri: "/text-profiles", method: .get)
        let textProfilesJSON = try jsonObject(from: textProfilesResponse.body)
        let textProfiles = try #require(textProfilesJSON["text_profiles"] as? [String: Any])
        let storedTextProfiles = try #require(textProfiles["stored_profiles"] as? [[String: Any]])
        #expect(storedTextProfiles.contains { $0["id"] as? String == "swift-docs" })

        let loadTextProfilesResponse = try await client.execute(uri: "/text-profiles/load", method: .post)
        let loadTextProfilesJSON = try jsonObject(from: loadTextProfilesResponse.body)
        let loadedTextProfiles = try #require(loadTextProfilesJSON["text_profiles"] as? [String: Any])
        let loadedStoredProfiles = try #require(loadedTextProfiles["stored_profiles"] as? [[String: Any]])
        #expect(loadedStoredProfiles.contains { $0["id"] as? String == "swift-docs" })

        let saveTextProfilesResponse = try await client.execute(uri: "/text-profiles/save", method: .post)
        let saveTextProfilesJSON = try jsonObject(from: saveTextProfilesResponse.body)
        let savedTextProfiles = try #require(saveTextProfilesJSON["text_profiles"] as? [String: Any])
        let savedStoredProfiles = try #require(savedTextProfiles["stored_profiles"] as? [[String: Any]])
        #expect(savedStoredProfiles.contains { $0["id"] as? String == "swift-docs" })

        let useTextProfileResponse = try await client.execute(
            uri: "/text-profiles/active",
            method: .put,
            headers: [.contentType: "application/json"],
            body: byteBuffer(
                #"{"profile":{"id":"operator","name":"Operator","replacements":[{"id":"replace-2","text":"MCP","replacement":"Model Context Protocol","match":"exact_phrase","phase":"after_built_ins","is_case_sensitive":false,"formats":[],"priority":2}]}}"#
            )
        )
        let useTextProfileJSON = try jsonObject(from: useTextProfileResponse.body)
        let activeTextProfile = try #require(useTextProfileJSON["profile"] as? [String: Any])
        #expect(activeTextProfile["id"] as? String == "operator")

        let effectiveTextProfileResponse = try await client.execute(uri: "/text-profiles/effective/swift-docs", method: .get)
        let effectiveTextProfileJSON = try jsonObject(from: effectiveTextProfileResponse.body)
        let effectiveTextProfile = try #require(effectiveTextProfileJSON["profile"] as? [String: Any])
        let effectiveReplacements = try #require(effectiveTextProfile["replacements"] as? [[String: Any]])
        #expect(effectiveReplacements.contains { $0["id"] as? String == "replace-1" })

        let removeTextReplacementResponse = try await client.execute(
            uri: "/text-profiles/stored/swift-docs/replacements/replace-1",
            method: .delete
        )
        let removeTextReplacementJSON = try jsonObject(from: removeTextReplacementResponse.body)
        let trimmedTextProfile = try #require(removeTextReplacementJSON["profile"] as? [String: Any])
        let trimmedReplacements = try #require(trimmedTextProfile["replacements"] as? [[String: Any]])
        #expect(trimmedReplacements.isEmpty)
        let persistenceActionCounts = await runtime.textProfilePersistenceActionCounts()
        #expect(persistenceActionCounts.load == 1)
        #expect(persistenceActionCounts.save == 1)

        let cloneResponse = try await client.execute(
            uri: "/voices/from-audio",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(
                #"{"profile_name":"clone-default","vibe":"femme","reference_audio_path":"./Fixtures/reference.wav","transcript":"Cloned route test transcript.","cwd":"/tmp/http-clone-cwd"}"#
            )
        )
        let cloneJSON = try jsonObject(from: cloneResponse.body)
        let cloneJobID = try #require(cloneJSON["request_id"] as? String)
        #expect(cloneResponse.status == .accepted)
        _ = try await waitForJobSnapshot(cloneJobID, on: host)

        let cloneInvocation = try #require(await runtime.latestCreateCloneInvocation())
        #expect(cloneInvocation.profileName == "clone-default")
        #expect(cloneInvocation.referenceAudioPath == "./Fixtures/reference.wav")
        #expect(cloneInvocation.transcript == "Cloned route test transcript.")
        #expect(cloneInvocation.cwd == "/tmp/http-clone-cwd")

        let speakResponse = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Route test","profile_name":"default","text_profile_name":"swift-docs","cwd":"./Sources","repo_root":"../SpeakSwiftlyServer","text_format":"markdown","nested_source_format":"swift_source","source_format":"python_source"}"#)
        )
        let speakJSON = try jsonObject(from: speakResponse.body)
        let speakJobID = try #require(speakJSON["request_id"] as? String)
        #expect(speakResponse.status == .accepted)
        #expect((speakJSON["request_url"] as? String)?.contains(speakJobID) == true)
        #expect((speakJSON["events_url"] as? String)?.contains(speakJobID) == true)
        #expect((speakJSON["request_url"] as? String)?.hasPrefix("http://") == true)
        let queuedSpeechInvocation = try #require(await runtime.latestQueuedSpeechInvocation())
        #expect(
            queuedSpeechInvocation.normalizationContext
                == SpeechNormalizationContext(
                    cwd: "./Sources",
                    repoRoot: "../SpeakSwiftlyServer",
                    textFormat: .markdown,
                    nestedSourceFormat: .swift
                )
        )
        #expect(queuedSpeechInvocation.textProfileName == "swift-docs")
        #expect(queuedSpeechInvocation.sourceFormat == .python)

        _ = try await waitForJobSnapshot(speakJobID, on: host)

        let jobsResponse = try await client.execute(uri: "/requests", method: .get)
        let jobsJSON = try jsonObject(from: jobsResponse.body)
        let jobs = try #require(jobsJSON["requests"] as? [[String: Any]])
        #expect(jobsResponse.status == .ok)
        #expect(jobs.contains { $0["request_id"] as? String == speakJobID })

        let foregroundJobResponse = try await client.execute(uri: "/requests/\(speakJobID)", method: .get)
        let foregroundJobJSON = try jsonObject(from: foregroundJobResponse.body)
        #expect(foregroundJobResponse.status == .ok)
        #expect(foregroundJobJSON["request_id"] as? String == speakJobID)
        #expect(foregroundJobJSON["status"] as? String == "completed")
        let foregroundHistory = try #require(foregroundJobJSON["history"] as? [[String: Any]])
        #expect(foregroundHistory.contains { $0["event"] as? String == "started" })
        #expect(foregroundHistory.filter { $0["ok"] as? Bool == true }.count == 2)
    }

    await host.shutdown()
}

@available(macOS 14, *)
@Test func speakRouteRejectsUnsupportedFormatArgumentsClearly() async throws {
    let runtime = MockRuntime()
    let configuration = testConfiguration()
    let state = await MainActor.run { ServerState() }
    let host = ServerHost(
        configuration: configuration,
        runtime: runtime,
        state: state
    )

    await host.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(host)

    let app = assembleHBApp(configuration: testHTTPConfig(configuration), host: host)
    try await app.test(.router) { client in
        let response = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(
                #"{"text":"Bad format","profile_name":"default","text_format":"totally_invalid","source_format":"not_a_real_source"}"#
            )
        )
        let responseJSON = try jsonObject(from: response.body)
        let error = try #require(responseJSON["error"] as? [String: Any])
        let message = try #require(error["message"] as? String)

        #expect(response.status == .badRequest)
        #expect(message.contains("text_format"))
        #expect(message.contains("totally_invalid"))
        #expect(message.contains("plain"))
    }

    await host.shutdown()
}

@available(macOS 14, *)
@Test func routesExposeQueueInspectionAndControlOperations() async throws {
    let runtime = MockRuntime(speakBehavior: .holdOpen)
    let configuration = testConfiguration()
    let state = await MainActor.run { ServerState() }
    let host = ServerHost(
        configuration: configuration,
        runtime: runtime,
        state: state
    )

    await host.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(host)

    let app = assembleHBApp(configuration: testHTTPConfig(configuration), host: host)
    try await app.test(.router) { client in
        let activeResponse = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Hold the line","profile_name":"default"}"#)
        )
        let activeJobID = try #require(try jsonObject(from: activeResponse.body)["request_id"] as? String)

        let queuedResponse = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Queue this request","profile_name":"default"}"#)
        )
        let queuedJobID = try #require(try jsonObject(from: queuedResponse.body)["request_id"] as? String)

        let queueResponse = try await client.execute(uri: "/generation/queue", method: .get)
        let queueJSON = try jsonObject(from: queueResponse.body)
        #expect(queueResponse.status == .ok)
        #expect(queueJSON["queue_type"] as? String == "generation")
        let activeRequest = try #require(queueJSON["active_request"] as? [String: Any])
        #expect(activeRequest["id"] as? String == activeJobID)
        let activeRequests = try #require(queueJSON["active_requests"] as? [[String: Any]])
        #expect(activeRequests.count == 1)
        #expect(activeRequests.first?["id"] as? String == activeJobID)
        let queuedRequests = try #require(queueJSON["queue"] as? [[String: Any]])
        #expect(queuedRequests.count == 1)
        #expect(queuedRequests.first?["id"] as? String == queuedJobID)
        #expect(queuedRequests.first?["queue_position"] as? Int == 1)

        let playbackStateResponse = try await client.execute(uri: "/playback/state", method: .get)
        let playbackStateJSON = try jsonObject(from: playbackStateResponse.body)
        #expect(playbackStateResponse.status == .ok)
        let playback = try #require(playbackStateJSON["playback"] as? [String: Any])
        #expect(playback["state"] as? String == "playing")
        let playbackActiveRequest = try #require(playback["active_request"] as? [String: Any])
        #expect(playbackActiveRequest["id"] as? String == activeJobID)

        let pauseResponse = try await client.execute(uri: "/playback/pause", method: .post)
        let pauseJSON = try jsonObject(from: pauseResponse.body)
        #expect(pauseResponse.status == .ok)
        #expect((pauseJSON["playback"] as? [String: Any])?["state"] as? String == "paused")

        let resumeResponse = try await client.execute(uri: "/playback/resume", method: .post)
        let resumeJSON = try jsonObject(from: resumeResponse.body)
        #expect(resumeResponse.status == .ok)
        #expect((resumeJSON["playback"] as? [String: Any])?["state"] as? String == "playing")

        let playbackQueueResponse = try await client.execute(uri: "/playback/queue", method: .get)
        let playbackQueueJSON = try jsonObject(from: playbackQueueResponse.body)
        #expect(playbackQueueResponse.status == .ok)
        #expect(playbackQueueJSON["queue_type"] as? String == "playback")
        #expect((playbackQueueJSON["active_request"] as? [String: Any])?["id"] as? String == activeJobID)
        #expect((playbackQueueJSON["active_requests"] as? [[String: Any]])?.first?["id"] as? String == activeJobID)
        #expect((playbackQueueJSON["queue"] as? [[String: Any]])?.isEmpty == true)

        let cancelResponse = try await client.execute(uri: "/playback/requests/\(queuedJobID)", method: .delete)
        let cancelJSON = try jsonObject(from: cancelResponse.body)
        #expect(cancelResponse.status == .ok)
        #expect(cancelJSON["cancelled_request_id"] as? String == queuedJobID)

        let cancelledSnapshot = try await waitForJobSnapshot(queuedJobID, on: host)
        switch cancelledSnapshot.terminalEvent {
        case .failed(let failure):
            #expect(failure.code == SpeakSwiftly.ErrorCode.requestCancelled.rawValue)
        default:
            Issue.record("Expected the cancelled queued request to terminate with a request_cancelled failure.")
        }

        let anotherQueuedResponse = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Queue another request","profile_name":"default"}"#)
        )
        let anotherQueuedJobID = try #require(try jsonObject(from: anotherQueuedResponse.body)["request_id"] as? String)

        let clearResponse = try await client.execute(uri: "/playback/queue", method: .delete)
        let clearJSON = try jsonObject(from: clearResponse.body)
        #expect(clearResponse.status == .ok)
        #expect(clearJSON["cleared_count"] as? Int == 1)

        let clearedSnapshot = try await waitForJobSnapshot(anotherQueuedJobID, on: host)
        switch clearedSnapshot.terminalEvent {
        case .failed(let failure):
            #expect(failure.code == SpeakSwiftly.ErrorCode.requestCancelled.rawValue)
        default:
            Issue.record("Expected the cleared queued request to terminate with a request_cancelled failure.")
        }

        let emptyQueueResponse = try await client.execute(uri: "/generation/queue", method: .get)
        let emptyQueueJSON = try jsonObject(from: emptyQueueResponse.body)
        let remainingQueue = try #require(emptyQueueJSON["queue"] as? [[String: Any]])
        #expect(remainingQueue.isEmpty)
        #expect((emptyQueueJSON["active_request"] as? [String: Any])?["id"] as? String == activeJobID)
        #expect((emptyQueueJSON["active_requests"] as? [[String: Any]])?.first?["id"] as? String == activeJobID)
    }

    await runtime.finishHeldSpeak(id: try await waitForActiveRequestID(on: host))
    await host.shutdown()
}

@available(macOS 14, *)
@Test func routesReportNotReadyAndMissingJobsClearly() async throws {
    let runtime = MockRuntime()
    let configuration = testConfiguration()
    let state = await MainActor.run { ServerState() }
    let host = ServerHost(
        configuration: configuration,
        runtime: runtime,
        state: state
    )

    await host.start()

    let app = assembleHBApp(configuration: testHTTPConfig(configuration), host: host)
    try await app.test(.router) { client in
        let readyResponse = try await client.execute(uri: "/readyz", method: .get)
        let readyJSON = try jsonObject(from: readyResponse.body)
        #expect(readyResponse.status == .serviceUnavailable)
        #expect(readyJSON["status"] as? String == "not_ready")

        let speakResponse = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Too soon","profile_name":"default"}"#)
        )
        let speakJSON = try jsonObject(from: speakResponse.body)
        #expect(speakResponse.status == .serviceUnavailable)
        let speakError = try #require(speakJSON["error"] as? [String: Any])
        #expect((speakError["message"] as? String)?.contains("cannot accept new work") == true)

        let missingJob = try await client.execute(uri: "/requests/missing-job", method: .get)
        let missingJSON = try jsonObject(from: missingJob.body)
        #expect(missingJob.status == .notFound)
        let missingJobError = try #require(missingJSON["error"] as? [String: Any])
        #expect((missingJobError["message"] as? String)?.contains("expired from in-memory retention") == true)

        let missingEvents = try await client.execute(uri: "/requests/missing-job/events", method: .get)
        let missingEventsJSON = try jsonObject(from: missingEvents.body)
        #expect(missingEvents.status == .notFound)
        let missingEventsError = try #require(missingEventsJSON["error"] as? [String: Any])
        #expect((missingEventsError["message"] as? String)?.contains("expired from in-memory retention") == true)
    }

    await host.shutdown()
}

@available(macOS 14, *)
@Test func routesReportWorkerStartupFailureClearly() async throws {
    let runtime = MockRuntime()
    let configuration = testConfiguration()
    let state = await MainActor.run { ServerState() }
    let host = ServerHost(
        configuration: configuration,
        runtime: runtime,
        state: state
    )

    await host.start()
    await runtime.publishStatus(.residentModelFailed)

    let app = assembleHBApp(configuration: testHTTPConfig(configuration), host: host)
    try await app.test(.router) { client in
        let readyResponse = try await client.execute(uri: "/readyz", method: .get)
        let readyJSON = try jsonObject(from: readyResponse.body)
        #expect(readyResponse.status == .serviceUnavailable)
        #expect(readyJSON["status"] as? String == "not_ready")
        #expect(readyJSON["worker_mode"] as? String == "failed")
        #expect((readyJSON["startup_error"] as? String)?.contains("startup failure") == true)

        let statusResponse = try await client.execute(uri: "/runtime/host", method: .get)
        let statusJSON = try jsonObject(from: statusResponse.body)
        #expect(statusResponse.status == .ok)
        #expect(statusJSON["worker_mode"] as? String == "failed")
        #expect(statusJSON["worker_stage"] as? String == "resident_model_failed")
        #expect((statusJSON["worker_failure_summary"] as? String)?.contains("startup failure") == true)

        let speakResponse = try await client.execute(
            uri: "/speech/live",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Still broken","profile_name":"default"}"#)
        )
        let speakJSON = try jsonObject(from: speakResponse.body)
        #expect(speakResponse.status == .serviceUnavailable)
        let speakError = try #require(speakJSON["error"] as? [String: Any])
        #expect((speakError["message"] as? String)?.contains("startup failure") == true)
    }

    await host.shutdown()
}

@available(macOS 14, *)
@Test func runtimeDegradationWhileSpeechJobsAreInFlightMarksJobsDegradedAndRejectsNewWork() async throws {
    let runtime = MockRuntime(speakBehavior: .holdOpen)
    let state = await MainActor.run { ServerState() }
    let host = ServerHost(
        configuration: testConfiguration(),
        runtime: runtime,
        state: state
    )

    await host.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(host)

    let activeJobID = try await host.submitSpeak(text: "Keep talking", profileName: "default")
    let queuedJobID = try await host.submitSpeak(text: "Wait your turn", profileName: "default")

    _ = try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        let snapshot = try await host.jobSnapshot(id: queuedJobID)
        return snapshot.history.contains {
            guard case .queued = $0 else { return false }
            return true
        } ? snapshot : nil
    }

    await runtime.publishStatus(.residentModelFailed)

    let degradedReadiness = try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        let snapshot = await host.readinessSnapshot()
        return snapshot.1.workerMode == "failed" ? snapshot : nil
    }
    #expect(degradedReadiness.0 == false)
    #expect(degradedReadiness.1.workerMode == "failed")
    #expect(degradedReadiness.1.workerStage == "resident_model_failed")
    #expect(degradedReadiness.1.startupError?.contains("startup failure") == true)

    let degradedHostState = await host.hostStateSnapshot()
    #expect(degradedHostState.playback.state == "idle")
    #expect(degradedHostState.playbackQueue.activeRequest == nil)
    #expect(degradedHostState.runtimeRefresh?.source == "cached_worker_not_ready")

    let activeSnapshot = try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        let snapshot = try await host.jobSnapshot(id: activeJobID)
        return snapshot.history.contains {
            guard case .workerStatus(let event) = $0 else { return false }
            return event.workerMode == "failed" && event.stage == "resident_model_failed"
        } ? snapshot : nil
    }
    #expect(activeSnapshot.terminalEvent == nil)

    let queuedSnapshot = try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        let snapshot = try await host.jobSnapshot(id: queuedJobID)
        return snapshot.history.contains {
            guard case .workerStatus(let event) = $0 else { return false }
            return event.workerMode == "failed" && event.stage == "resident_model_failed"
        } ? snapshot : nil
    }
    #expect(queuedSnapshot.terminalEvent == nil)

    do {
        _ = try await host.submitSpeak(text: "Do not accept this", profileName: "default")
        Issue.record("Expected the degraded worker state to reject new speech work.")
    } catch {
        let message = String(describing: error)
        #expect(message.contains("startup failure"))
    }

    await runtime.finishHeldSpeak(id: activeJobID)
    await host.shutdown()
}

@available(macOS 14, *)
@Test func profileMutationFailureMarksCacheStaleAndFailsJob() async throws {
    let runtime = MockRuntime(mutationRefreshBehavior: .leaveProfilesUnchanged)
    let state = await MainActor.run { ServerState() }
    let host = ServerHost(
        configuration: testConfiguration(),
        runtime: runtime,
        state: state
    )

    await host.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(host)

    let jobID = try await host.submitCreateProfile(
        profileName: "bright-guide",
        vibe: .femme,
        text: "Hello there",
        voiceDescription: "Warm and bright",
        outputPath: nil,
        cwd: nil
    )
    let snapshot = try await waitForJobSnapshot(jobID, on: host)

    switch snapshot.terminalEvent {
    case .failed(let failure):
        #expect(failure.code == "profile_refresh_mismatch")
        #expect(failure.message.contains("could not confirm the profile list"))
    default:
        Issue.record("Expected create_voice_profile_from_description reconciliation failure to produce a failed terminal event.")
    }

    let status = await host.statusSnapshot()
    #expect(status.profileCacheState == "stale")
    #expect(status.profileCacheWarning?.contains("could not confirm the refreshed profile list") == true)

    await host.shutdown()
}

}
