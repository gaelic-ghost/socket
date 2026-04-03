import Foundation
import SpeakSwiftlyCore

// MARK: - Runtime Bridge

struct RuntimeRequestHandle: Sendable {
    let id: String
    let request: WorkerRequest
    let events: AsyncThrowingStream<WorkerRequestStreamEvent, Error>

    init(
        id: String,
        request: WorkerRequest,
        events: AsyncThrowingStream<WorkerRequestStreamEvent, Error>
    ) {
        self.id = id
        self.request = request
        self.events = events
    }

    init(_ handle: WorkerRequestHandle) {
        self.id = handle.id
        self.request = handle.request
        self.events = handle.events
    }
}

protocol ServerRuntimeProtocol: Actor {
    func start()
    func shutdown() async
    func statusEvents() -> AsyncStream<WorkerStatusEvent>
    func submit(_ request: WorkerRequest) async -> RuntimeRequestHandle
}

extension WorkerRuntime: ServerRuntimeProtocol {
    func submit(_ request: WorkerRequest) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await self.submit(request))
    }
}
