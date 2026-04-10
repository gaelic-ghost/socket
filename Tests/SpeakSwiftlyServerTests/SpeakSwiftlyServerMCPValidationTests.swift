import Foundation
import MCP
import Testing
@testable import SpeakSwiftlyServer

// MARK: - MCP Validation Tests

extension SpeakSwiftlyServerTests {
    @available(macOS 14, *)
    @Test func embeddedMCPRejectsUnsupportedFormatArgumentsClearly() async throws {
        let runtime = MockRuntime()
        let configuration = testConfiguration()
        let state = await MainActor.run { ServerState() }
        let host = ServerHost(
            configuration: configuration,
            httpConfig: testHTTPConfig(configuration),
            mcpConfig: .init(
                enabled: true,
                path: "/mcp",
                serverName: "speak-swiftly-test-mcp",
                title: "SpeakSwiftly Test MCP"
            ),
            runtime: runtime,
            state: state
        )

        await host.start()
        await runtime.publishStatus(.residentModelReady)
        try await waitUntilReady(host)

        let mcpSurface = try #require(
            await MCPSurface.build(
                configuration: .init(
                    enabled: true,
                    path: "/mcp",
                    serverName: "speak-swiftly-test-mcp",
                    title: "SpeakSwiftly Test MCP"
                ),
                host: host
            )
        )

        try await mcpSurface.start()
        await host.markTransportListening(name: "mcp")
        let initializeMCPResponse = await mcpSurface.handle(mcpPOSTRequest(body: mcpInitializeRequestJSON()))
        let initializeSessionID = try #require(mcpSessionID(from: initializeMCPResponse))
        try await drainMCPResponse(initializeMCPResponse)

        let initializedNotificationResponse = await mcpSurface.handle(
            mcpPOSTRequest(
                body: mcpInitializedNotificationJSON(),
                sessionID: initializeSessionID
            )
        )
        #expect(mcpStatusCode(from: initializedNotificationResponse) == 202)

        let errorEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "generate_speech",
                        arguments: [
                            "text": "Bad format",
                            "profile_name": "default",
                            "text_format": "totally_invalid",
                        ]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let error = try #require(errorEnvelope["error"] as? [String: Any])
        let message = try #require(error["message"] as? String)
        #expect(message.contains("text_format"))
        #expect(message.contains("totally_invalid"))
        #expect(message.contains("plain"))

        await mcpSurface.stop()
        await host.shutdown()
    }
}
