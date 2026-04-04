import Foundation
import Hummingbird
import HTTPTypes
import MCP
import NIOCore

// MARK: - MCP Surface

struct MCPSurface {
    private let configuration: MCPConfig
    private let host: ServerHost
    private let transport: StatefulHTTPServerTransport
    private let server: Server
    private let subscriptionBroker: MCPSubscriptionBroker

    // MARK: - Construction

    static func build(
        configuration: MCPConfig,
        host: ServerHost
    ) async -> MCPSurface? {
        guard configuration.enabled else {
            return nil
        }

        let transport = StatefulHTTPServerTransport()
        let subscriptionBroker = MCPSubscriptionBroker()
        let server = await buildServer(
            configuration: configuration,
            host: host,
            subscriptionBroker: subscriptionBroker
        )
        return .init(
            configuration: configuration,
            host: host,
            transport: transport,
            server: server,
            subscriptionBroker: subscriptionBroker
        )
    }

    // MARK: - Lifecycle

    func mount(on router: Router<BasicRequestContext>) {
        let mcpPath = RouterPath(configuration.path)

        router.get(mcpPath) { request, _ in
            let httpRequest = try await MCPHTTPBridge.makeHTTPRequest(from: request)
            let response = await transport.handleRequest(httpRequest)
            return try MCPHTTPBridge.makeResponse(from: response)
        }

        router.post(mcpPath) { request, _ in
            let httpRequest = try await MCPHTTPBridge.makeHTTPRequest(from: request)
            let response = await transport.handleRequest(httpRequest)
            return try MCPHTTPBridge.makeResponse(from: response)
        }

        router.delete(mcpPath) { request, _ in
            let httpRequest = try await MCPHTTPBridge.makeHTTPRequest(from: request)
            let response = await transport.handleRequest(httpRequest)
            return try MCPHTTPBridge.makeResponse(from: response)
        }
    }

    func start() async throws {
        try await server.start(transport: transport)
        await subscriptionBroker.start(host: host, server: server)
    }

    func stop() async {
        await subscriptionBroker.stop()
        await server.stop()
    }

    func handle(_ request: MCP.HTTPRequest) async -> MCP.HTTPResponse {
        await transport.handleRequest(request)
    }

    // MARK: - Server Assembly

    private static func buildServer(
        configuration: MCPConfig,
        host: ServerHost,
        subscriptionBroker: MCPSubscriptionBroker
    ) async -> Server {
        let server = Server(
            name: configuration.serverName,
            version: "0.1.0",
            title: configuration.title,
            instructions: """
            Shared-process SpeakSwiftly MCP surface backed by the same ServerHost used by the app-facing HTTP API. Read status and runtime resources for operator-visible state, and use the tools to queue speech, inspect queues, control playback, and manage profiles without starting a second runtime owner.
            """,
            capabilities: .init(
                resources: .init(subscribe: true, listChanged: false),
                tools: .init(listChanged: false)
            )
        )

        // MARK: - Tool Methods

        await server.withMethodHandler(ListTools.self) { _ in
            .init(tools: MCPToolCatalog.definitions)
        }

        await server.withMethodHandler(CallTool.self) { params in
            let arguments = params.arguments ?? [:]

            switch params.name {
            case "queue_speech_live":
                let jobID = try await host.submitSpeak(
                    text: requiredString("text", in: arguments),
                    profileName: requiredString("profile_name", in: arguments)
                )
                return try toolResult(
                    MCPAcceptedJobResult(
                        jobID: jobID,
                        statusResourceURI: "speak://status",
                        message: "SpeakSwiftlyServer accepted the speech request. Read speak://status or the status tool to monitor generation, playback, and transport state."
                    )
                )

            case "create_profile":
                let jobID = try await host.submitCreateProfile(
                    profileName: requiredString("profile_name", in: arguments),
                    text: requiredString("text", in: arguments),
                    voiceDescription: requiredString("voice_description", in: arguments),
                    outputPath: optionalString("output_path", in: arguments)
                )
                return try toolResult(
                    MCPAcceptedJobResult(
                        jobID: jobID,
                        statusResourceURI: "speak://status",
                        message: "SpeakSwiftlyServer accepted the profile-creation request. Read speak://status or the status tool to monitor worker state and the refreshed profile cache."
                    )
                )

            case "list_profiles":
                return try toolResult(await host.cachedProfiles())

            case "remove_profile":
                let jobID = try await host.submitRemoveProfile(
                    profileName: requiredString("profile_name", in: arguments)
                )
                return try toolResult(
                    MCPAcceptedJobResult(
                        jobID: jobID,
                        statusResourceURI: "speak://status",
                        message: "SpeakSwiftlyServer accepted the profile-removal request. Read speak://status or the status tool to monitor worker state and the refreshed profile cache."
                    )
                )

            case "list_queue_generation":
                return try toolResult(try await host.queueSnapshot(queueType: .generation))

            case "list_queue_playback":
                return try toolResult(try await host.queueSnapshot(queueType: .playback))

            case "playback_pause":
                return try toolResult(try await host.pausePlayback())

            case "playback_resume":
                return try toolResult(try await host.resumePlayback())

            case "playback_state":
                return try toolResult(try await host.playbackStateSnapshot())

            case "clear_queue":
                return try toolResult(try await host.clearQueue())

            case "cancel_request":
                return try toolResult(
                    try await host.cancelQueuedOrActiveRequest(
                        requestID: requiredString("request_id", in: arguments)
                    )
                )

            case "status":
                return try toolResult(await host.statusSnapshot())

            default:
                throw MCPError.methodNotFound(
                    "Tool '\(params.name)' is not registered on this embedded SpeakSwiftly MCP surface."
                )
            }
        }

        // MARK: - Resource Methods

        await server.withMethodHandler(ListResources.self) { _ in
            .init(resources: MCPResourceCatalog.resources)
        }

        await server.withMethodHandler(ListResourceTemplates.self) { _ in
            .init(templates: [])
        }

        await server.withMethodHandler(ResourceSubscribe.self) { params in
            try ensureKnownResourceURI(params.uri)
            await subscriptionBroker.subscribe(to: params.uri)
            return Empty()
        }

        await server.withMethodHandler(ResourceUnsubscribe.self) { params in
            try ensureKnownResourceURI(params.uri)
            await subscriptionBroker.unsubscribe(from: params.uri)
            return Empty()
        }

        await server.withMethodHandler(ReadResource.self) { params in
            switch params.uri {
            case "speak://status":
                return try resourceResult(uri: params.uri, payload: await host.statusSnapshot())

            case "speak://profiles":
                return try resourceResult(uri: params.uri, payload: await host.cachedProfiles())

            case "speak://runtime":
                return try resourceResult(uri: params.uri, payload: await host.hostStateSnapshot())

            default:
                throw MCPError.invalidRequest(
                    "Resource '\(params.uri)' is not available on this embedded SpeakSwiftly MCP surface."
                )
            }
        }

        return server
    }
}

// MARK: - Subscription Handling

private actor MCPSubscriptionBroker {
    private var subscribedResourceURIs = Set<String>()
    private var eventTask: Task<Void, Never>?

    func start(host: ServerHost, server: Server) {
        guard eventTask == nil else {
            return
        }

        let updates = Task { await host.eventUpdates() }
        eventTask = Task {
            let events = await updates.value
            for await event in events {
                if Task.isCancelled {
                    break
                }
                let updatedURIs = resourceURIsToNotify(for: event)
                guard updatedURIs.isEmpty == false else {
                    continue
                }
                for uri in updatedURIs {
                    do {
                        try await server.notify(ResourceUpdatedNotification.message(.init(uri: uri)))
                    } catch {
                        // The shared transport may be stopping or may not have a connected SSE stream yet.
                        continue
                    }
                }
            }
        }
    }

    func stop() {
        eventTask?.cancel()
        eventTask = nil
        subscribedResourceURIs.removeAll()
    }

    func subscribe(to uri: String) {
        subscribedResourceURIs.insert(uri)
    }

    func unsubscribe(from uri: String) {
        subscribedResourceURIs.remove(uri)
    }

    private func resourceURIsToNotify(for event: HostEvent) -> [String] {
        let candidateURIs: Set<String>
        switch event {
        case .transportChanged, .jobChanged, .playbackChanged, .recentErrorRecorded:
            candidateURIs = ["speak://status", "speak://runtime"]
        case .profileCacheChanged:
            candidateURIs = ["speak://status", "speak://runtime", "speak://profiles"]
        }
        return candidateURIs
            .intersection(subscribedResourceURIs)
            .sorted()
    }
}

// MARK: - Resource Validation

private func ensureKnownResourceURI(_ uri: String) throws {
    guard MCPResourceCatalog.resourceURIs.contains(uri) else {
        throw MCPError.invalidRequest(
            "Resource '\(uri)' is not available on this embedded SpeakSwiftly MCP surface."
        )
    }
}

// MARK: - HTTP Bridge

private enum MCPHTTPBridge {
    static func makeHTTPRequest(from request: Request) async throws -> MCP.HTTPRequest {
        let bodyBuffer = try await request.body.collect(upTo: 10 * 1024 * 1024)
        let bodyData = Data(bodyBuffer.readableBytesView)

        var headers = [String: String]()
        for field in request.headers {
            headers[field.name.rawName] = field.value
        }

        return MCP.HTTPRequest(
            method: request.method.rawValue,
            headers: headers,
            body: bodyData.isEmpty ? nil : bodyData,
            path: request.uri.path
        )
    }

    static func makeResponse(from response: MCP.HTTPResponse) throws -> Response {
        var headers = HTTPFields()
        for (name, value) in response.headers {
            guard let headerName = HTTPField.Name(name) else { continue }
            headers[headerName] = value
        }

        switch response {
        case .accepted:
            return Response(status: .accepted, headers: headers)

        case .ok:
            return Response(status: .ok, headers: headers)

        case .data(let data, _):
            return Response(
                status: .ok,
                headers: headers,
                body: ResponseBody(byteBuffer: byteBuffer(from: data))
            )

        case .stream(let stream, _):
            let body = ResponseBody { writer in
                for try await chunk in stream {
                    try await writer.write(byteBuffer(from: chunk))
                }
                try await writer.finish(nil)
            }
            return Response(status: .ok, headers: headers, body: body)

        case .error:
            return Response(
                status: .init(code: response.statusCode),
                headers: headers,
                body: ResponseBody(byteBuffer: byteBuffer(from: response.bodyData ?? Data()))
            )
        }
    }

    static func byteBuffer(from data: Data) -> ByteBuffer {
        var buffer = ByteBufferAllocator().buffer(capacity: data.count)
        buffer.writeBytes(data)
        return buffer
    }
}

// MARK: - Result Encoding

private func toolResult<Output: Encodable>(_ output: Output) throws -> CallTool.Result {
    let data = try JSONEncoder().encode(output)
    let json = String(decoding: data, as: UTF8.self)
    return .init(content: [.text(text: json, annotations: nil, _meta: nil)], isError: false)
}

private func resourceResult<Output: Encodable>(
    uri: String,
    payload: Output
) throws -> ReadResource.Result {
    let data = try JSONEncoder().encode(payload)
    let json = String(decoding: data, as: UTF8.self)
    return .init(contents: [.text(json, uri: uri, mimeType: "application/json")])
}

// MARK: - Argument Parsing

private func requiredString(_ key: String, in arguments: [String: Value]) throws -> String {
    guard let value = arguments[key]?.stringValue, value.isEmpty == false else {
        throw MCPError.invalidParams(
            "Tool arguments are missing the required string field '\(key)'."
        )
    }
    return value
}

private func optionalString(_ key: String, in arguments: [String: Value]) -> String? {
    guard let value = arguments[key]?.stringValue, value.isEmpty == false else {
        return nil
    }
    return value
}
