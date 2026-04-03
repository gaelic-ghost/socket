import Foundation
import Hummingbird
import HummingbirdTesting
import NIOCore
import SpeakSwiftlyCore
import Testing
@testable import SpeakSwiftlyServer

@available(macOS 14, *)
actor MockRuntime: ServerRuntimeProtocol {
    enum SpeakBehavior: Sendable {
        case completeImmediately
        case holdOpen
    }

    enum MutationRefreshBehavior: Sendable {
        case applyMutations
        case leaveProfilesUnchanged
    }

    var profiles: [ProfileSummary]
    var speakBehavior: SpeakBehavior
    var mutationRefreshBehavior: MutationRefreshBehavior
    private var statusContinuation: AsyncStream<WorkerStatusEvent>.Continuation?
    private var heldContinuations: [String: AsyncThrowingStream<WorkerRequestStreamEvent, Error>.Continuation] = [:]

    init(
        profiles: [ProfileSummary] = [sampleProfile()],
        speakBehavior: SpeakBehavior = .completeImmediately,
        mutationRefreshBehavior: MutationRefreshBehavior = .applyMutations
    ) {
        self.profiles = profiles
        self.speakBehavior = speakBehavior
        self.mutationRefreshBehavior = mutationRefreshBehavior
    }

    func start() {}

    func shutdown() async {
        statusContinuation?.finish()
        for continuation in heldContinuations.values {
            continuation.finish()
        }
        heldContinuations.removeAll()
    }

    func statusEvents() -> AsyncStream<WorkerStatusEvent> {
        AsyncStream { continuation in
            self.statusContinuation = continuation
        }
    }

    func submit(_ request: WorkerRequest) async -> RuntimeRequestHandle {
        switch request {
        case .listProfiles:
            return RuntimeRequestHandle(
                id: request.id,
                request: request,
                events: AsyncThrowingStream<WorkerRequestStreamEvent, Error> { continuation in
                    continuation.yield(.completed(WorkerSuccessResponse(id: request.id, profiles: profiles)))
                    continuation.finish()
                }
            )

        case .speakLiveBackground:
            var heldContinuation: AsyncThrowingStream<WorkerRequestStreamEvent, Error>.Continuation?
            let speakBehavior = self.speakBehavior
            let events = AsyncThrowingStream<WorkerRequestStreamEvent, Error> { continuation in
                continuation.yield(.acknowledged(.init(id: request.id)))
                continuation.yield(.started(.init(id: request.id, op: request.opName)))
                if speakBehavior == .completeImmediately {
                    continuation.yield(.progress(.init(id: request.id, stage: .startingPlayback)))
                    continuation.yield(.completed(.init(id: request.id)))
                    continuation.finish()
                } else {
                    heldContinuation = continuation
                }
            }
            if let heldContinuation {
                heldContinuations[request.id] = heldContinuation
            }
            return RuntimeRequestHandle(id: request.id, request: request, events: events)

        case .createProfile(_, let profileName, let text, let voiceDescription, _):
            if mutationRefreshBehavior == .applyMutations {
                profiles.append(
                    ProfileSummary(
                        profileName: profileName,
                        createdAt: Date(),
                        voiceDescription: voiceDescription,
                        sourceText: text
                    )
                )
            }
            return RuntimeRequestHandle(
                id: request.id,
                request: request,
                events: AsyncThrowingStream<WorkerRequestStreamEvent, Error> { continuation in
                    continuation.yield(.completed(WorkerSuccessResponse(id: request.id, profileName: profileName)))
                    continuation.finish()
                }
            )

        case .removeProfile(_, let profileName):
            if mutationRefreshBehavior == .applyMutations {
                profiles.removeAll { $0.profileName == profileName }
            }
            return RuntimeRequestHandle(
                id: request.id,
                request: request,
                events: AsyncThrowingStream<WorkerRequestStreamEvent, Error> { continuation in
                    continuation.yield(.completed(WorkerSuccessResponse(id: request.id, profileName: profileName)))
                    continuation.finish()
                }
            )

        case .speakLive:
            return RuntimeRequestHandle(
                id: request.id,
                request: request,
                events: AsyncThrowingStream<WorkerRequestStreamEvent, Error> { continuation in
                    continuation.finish(throwing: WorkerError(
                        code: .invalidRequest,
                        message: "MockRuntime only supports background playback in these tests."
                    ))
                }
            )
        }
    }

    func publishStatus(_ stage: WorkerStatusStage) {
        statusContinuation?.yield(.init(stage: stage))
    }

    func finishHeldSpeak(id: String) {
        guard let continuation = heldContinuations.removeValue(forKey: id) else { return }
        continuation.yield(.progress(.init(id: id, stage: .playbackFinished)))
        continuation.yield(.completed(.init(id: id)))
        continuation.finish()
    }
}

@Test func configurationLoadsDefaultsAndRejectsInvalidValues() throws {
    let defaults = try ServerConfiguration.load(environment: [:])
    #expect(defaults.host == "127.0.0.1")
    #expect(defaults.port == 7337)
    #expect(defaults.sseHeartbeatSeconds == 10)
    #expect(defaults.completedJobTTLSeconds == 900)

    do {
        _ = try ServerConfiguration.load(environment: ["APP_PORT": "zero"])
        Issue.record("Expected invalid APP_PORT to throw a configuration error.")
    } catch let error as ServerConfigurationError {
        #expect(error.message.contains("APP_PORT"))
    }
}

@available(macOS 14, *)
@Test func stateCompletesBackgroundJobsAndPrunesExpiredEntries() async throws {
    let runtime = MockRuntime()
    let state = ServerState(
        configuration: testConfiguration(completedJobTTLSeconds: 0.05, jobPruneIntervalSeconds: 0.02),
        runtime: runtime,
        makeRuntime: { runtime }
    )

    await state.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(state)

    let jobID = try await state.submitSpeak(text: "Hello from the test suite", profileName: "default", background: true)
    let snapshot = try await waitForJobSnapshot(jobID, on: state)

    #expect(snapshot.jobID == jobID)
    #expect(snapshot.status == "completed")
    #expect(snapshot.terminalEvent != nil)
    #expect(snapshot.history.count >= 3)

    try await Task.sleep(for: .milliseconds(120))
    try await waitUntilJobDisappears(jobID, on: state)

    await state.shutdown()
}

@available(macOS 14, *)
@Test func statePrunesOldestCompletedJobsWhenMaxCountIsExceeded() async throws {
    let runtime = MockRuntime()
    let state = ServerState(
        configuration: testConfiguration(completedJobTTLSeconds: 60, completedJobMaxCount: 2),
        runtime: runtime,
        makeRuntime: { runtime }
    )

    await state.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(state)

    let first = try await state.submitSpeak(text: "One", profileName: "default", background: true)
    let second = try await state.submitSpeak(text: "Two", profileName: "default", background: true)
    let third = try await state.submitSpeak(text: "Three", profileName: "default", background: true)

    _ = try await waitForJobSnapshot(first, on: state)
    _ = try await waitForJobSnapshot(second, on: state)
    _ = try await waitForJobSnapshot(third, on: state)

    try await waitUntilJobDisappears(first, on: state)
    let secondSnapshot = try await state.jobSnapshot(id: second)
    let thirdSnapshot = try await state.jobSnapshot(id: third)
    #expect(secondSnapshot.status == "completed")
    #expect(thirdSnapshot.status == "completed")

    await state.shutdown()
}

@available(macOS 14, *)
@Test func sseReplayIncludesWorkerStatusHistoryAndHeartbeat() async throws {
    let runtime = MockRuntime(speakBehavior: .holdOpen)
    let state = ServerState(
        configuration: testConfiguration(sseHeartbeatSeconds: 0.02),
        runtime: runtime,
        makeRuntime: { runtime }
    )

    await state.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(state)

    let jobID = try await state.submitSpeak(text: "Keep speaking", profileName: "default", background: true)
    _ = try await waitUntil(
        timeout: .seconds(1),
        pollInterval: .milliseconds(10)
    ) {
        let snapshot = try await state.jobSnapshot(id: jobID)
        return snapshot.history.count >= 2 ? snapshot : nil
    }

    let stream = try await state.sseStream(for: jobID)
    var iterator = stream.makeAsyncIterator()
    let first = try #require(await iterator.next())
    let second = try #require(await iterator.next())
    let third = try #require(await iterator.next())

    #expect(string(from: first).contains("event: worker_status"))
    #expect(string(from: second).contains("event: message"))
    #expect(string(from: third).contains("event: started"))

    var heartbeat: String?
    for _ in 0..<20 {
        guard let chunk = await iterator.next() else { break }
        let text = string(from: chunk)
        if text == ": keep-alive\n\n" {
            heartbeat = text
            break
        }
    }
    #expect(heartbeat == ": keep-alive\n\n")

    await runtime.finishHeldSpeak(id: jobID)
    await state.shutdown()
}

@available(macOS 14, *)
@Test func routesExposeHealthProfilesAndJobLifecycle() async throws {
    let runtime = MockRuntime()
    let configuration = testConfiguration()
    let state = ServerState(
        configuration: configuration,
        runtime: runtime,
        makeRuntime: { runtime }
    )

    await state.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(state)

    let app = makeApplication(configuration: configuration, state: state)
    try await app.test(.router) { client in
        let healthResponse = try await client.execute(uri: "/healthz", method: .get)
        let healthJSON = try jsonObject(from: healthResponse.body)
        #expect(healthResponse.status == .ok)
        #expect(healthJSON["status"] as? String == "ok")
        #expect(healthJSON["worker_ready"] as? Bool == true)

        let profilesResponse = try await client.execute(uri: "/profiles", method: .get)
        let profilesJSON = try jsonObject(from: profilesResponse.body)
        let profiles = try #require(profilesJSON["profiles"] as? [[String: Any]])
        #expect(profiles.count == 1)
        #expect(profiles.first?["profile_name"] as? String == "default")

        let speakResponse = try await client.execute(
            uri: "/speak",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Route test","profile_name":"default"}"#)
        )
        let speakJSON = try jsonObject(from: speakResponse.body)
        let jobID = try #require(speakJSON["job_id"] as? String)
        #expect(speakResponse.status == .accepted)
        #expect((speakJSON["job_url"] as? String)?.contains(jobID) == true)
        #expect((speakJSON["events_url"] as? String)?.contains(jobID) == true)
        #expect((speakJSON["job_url"] as? String)?.hasPrefix("http://") == true)

        _ = try await waitForJobSnapshot(jobID, on: state)
        let jobResponse = try await client.execute(uri: "/jobs/\(jobID)", method: .get)
        let jobJSON = try jsonObject(from: jobResponse.body)
        #expect(jobResponse.status == .ok)
        #expect(jobJSON["job_id"] as? String == jobID)
        #expect(jobJSON["status"] as? String == "completed")
    }

    await state.shutdown()
}

@available(macOS 14, *)
@Test func routesReportNotReadyAndMissingJobsClearly() async throws {
    let runtime = MockRuntime()
    let configuration = testConfiguration()
    let state = ServerState(
        configuration: configuration,
        runtime: runtime,
        makeRuntime: { runtime }
    )

    await state.start()

    let app = makeApplication(configuration: configuration, state: state)
    try await app.test(.router) { client in
        let readyResponse = try await client.execute(uri: "/readyz", method: .get)
        let readyJSON = try jsonObject(from: readyResponse.body)
        #expect(readyResponse.status == .serviceUnavailable)
        #expect(readyJSON["status"] as? String == "not_ready")

        let speakResponse = try await client.execute(
            uri: "/speak",
            method: .post,
            headers: [.contentType: "application/json"],
            body: byteBuffer(#"{"text":"Too soon","profile_name":"default"}"#)
        )
        let speakJSON = try jsonObject(from: speakResponse.body)
        #expect(speakResponse.status == .serviceUnavailable)
        let speakError = try #require(speakJSON["error"] as? [String: Any])
        #expect((speakError["message"] as? String)?.contains("cannot accept new work") == true)

        let missingJob = try await client.execute(uri: "/jobs/missing-job", method: .get)
        let missingJSON = try jsonObject(from: missingJob.body)
        #expect(missingJob.status == .notFound)
        let missingJobError = try #require(missingJSON["error"] as? [String: Any])
        #expect((missingJobError["message"] as? String)?.contains("expired from in-memory retention") == true)

        let missingEvents = try await client.execute(uri: "/jobs/missing-job/events", method: .get)
        let missingEventsJSON = try jsonObject(from: missingEvents.body)
        #expect(missingEvents.status == .notFound)
        let missingEventsError = try #require(missingEventsJSON["error"] as? [String: Any])
        #expect((missingEventsError["message"] as? String)?.contains("expired from in-memory retention") == true)
    }

    await state.shutdown()
}

@available(macOS 14, *)
@Test func profileMutationFailureMarksCacheStaleAndFailsJob() async throws {
    let runtime = MockRuntime(mutationRefreshBehavior: .leaveProfilesUnchanged)
    let state = ServerState(
        configuration: testConfiguration(),
        runtime: runtime,
        makeRuntime: { runtime }
    )

    await state.start()
    await runtime.publishStatus(.residentModelReady)
    try await waitUntilReady(state)

    let jobID = try await state.submitCreateProfile(
        profileName: "bright-guide",
        text: "Hello there",
        voiceDescription: "Warm and bright",
        outputPath: nil
    )
    let snapshot = try await waitForJobSnapshot(jobID, on: state)

    switch snapshot.terminalEvent {
    case .failed(let failure):
        #expect(failure.code == "profile_refresh_mismatch")
        #expect(failure.message.contains("could not confirm the profile list"))
    default:
        Issue.record("Expected create_profile reconciliation failure to produce a failed terminal event.")
    }

    let status = await state.statusSnapshot()
    #expect(status.profileCacheState == "stale")
    #expect(status.profileCacheWarning?.contains("could not confirm the refreshed profile list") == true)

    await state.shutdown()
}

private func testConfiguration(
    sseHeartbeatSeconds: Double = 0.05,
    completedJobTTLSeconds: Double = 30,
    completedJobMaxCount: Int = 20,
    jobPruneIntervalSeconds: Double = 0.05
) -> ServerConfiguration {
    .init(
        name: "speak-swiftly-server-tests",
        environment: "test",
        host: "127.0.0.1",
        port: 7337,
        sseHeartbeatSeconds: sseHeartbeatSeconds,
        completedJobTTLSeconds: completedJobTTLSeconds,
        completedJobMaxCount: completedJobMaxCount,
        jobPruneIntervalSeconds: jobPruneIntervalSeconds
    )
}

private func sampleProfile() -> ProfileSummary {
    .init(
        profileName: "default",
        createdAt: Date(timeIntervalSince1970: 1_700_000_000),
        voiceDescription: "Warm and clear",
        sourceText: "A reference voice sample."
    )
}

@available(macOS 14, *)
private func waitUntilReady(_ state: ServerState) async throws {
    _ = try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        let (ready, _) = await state.readinessSnapshot()
        return ready ? true : nil
    }
}

@available(macOS 14, *)
private func waitForJobSnapshot(_ jobID: String, on state: ServerState) async throws -> JobSnapshot {
    try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        do {
            let snapshot = try await state.jobSnapshot(id: jobID)
            return snapshot.terminalEvent == nil ? nil : snapshot
        } catch {
            return nil
        }
    }
}

@available(macOS 14, *)
private func waitUntilJobDisappears(_ jobID: String, on state: ServerState) async throws {
    let _: Bool = try await waitUntil(timeout: .seconds(1), pollInterval: .milliseconds(10)) {
        do {
            _ = try await state.jobSnapshot(id: jobID)
            return nil
        } catch {
            return true
        }
    }
}

private func waitUntil<T: Sendable>(
    timeout: Duration,
    pollInterval: Duration,
    condition: @escaping @Sendable () async throws -> T?
) async throws -> T {
    let deadline = ContinuousClock.now + timeout
    while ContinuousClock.now < deadline {
        if let value = try await condition() {
            return value
        }
        try await Task.sleep(for: pollInterval)
    }
    throw TimeoutError()
}

private struct TimeoutError: Error {}

private func byteBuffer(_ string: String) -> ByteBuffer {
    var buffer = ByteBufferAllocator().buffer(capacity: string.utf8.count)
    buffer.writeString(string)
    return buffer
}

private func string(from buffer: ByteBuffer) -> String {
    String(decoding: buffer.readableBytesView, as: UTF8.self)
}

private func jsonObject(from buffer: ByteBuffer) throws -> [String: Any] {
    let data = Data(buffer.readableBytesView)
    let json = try JSONSerialization.jsonObject(with: data)
    guard let dictionary = json as? [String: Any] else {
        throw JSONError.notDictionary
    }
    return dictionary
}

private enum JSONError: Error {
    case notDictionary
}
