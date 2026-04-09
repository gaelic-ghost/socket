import Foundation
import MCP
import Testing
@testable import SpeakSwiftlyServer

// MARK: - MCP Route Tests

extension SpeakSwiftlyServerTests {
    @available(macOS 14, *)
    @Test func embeddedMCPRoutesListToolsAndReadSharedHostResources() async throws {
        let runtime = MockRuntime(speakBehavior: .holdOpen)
        let configuration = testConfiguration()
        let state = await MainActor.run { ServerState() }
        let runtimeProfileRootURL = URL(fileURLWithPath: NSTemporaryDirectory())
            .appendingPathComponent(UUID().uuidString, isDirectory: true)
            .appendingPathComponent("profiles", isDirectory: true)
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
            runtimeConfigurationStore: .init(
                environment: ["SPEAKSWIFTLY_PROFILE_ROOT": runtimeProfileRootURL.path],
                activeRuntimeSpeechBackend: .qwen3
            ),
            state: state
        )

        await host.start()
        await runtime.publishStatus(.residentModelReady)
        try await waitUntilReady(host)
        await host.markTransportStarting(name: "http")
        await host.markTransportStarting(name: "mcp")

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

        let listToolsEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpListToolsRequestJSON(),
                    sessionID: initializeSessionID
                )
            )
        )
        let listToolsResult = try #require(mcpResultPayload(from: listToolsEnvelope))
        let tools = try #require(listToolsResult["tools"] as? [[String: Any]])
        let toolNames = Set(tools.compactMap { $0["name"] as? String })
        #expect(toolNames == Set(MCPToolCatalog.definitions.map(\.name)))
        #expect(tools.contains { $0["name"] as? String == "queue_speech_live" })
        #expect(tools.contains { $0["name"] as? String == "create_voice_profile_from_audio" })
        #expect(tools.contains { $0["name"] as? String == "get_runtime_configuration" })
        #expect(tools.contains { $0["name"] as? String == "set_runtime_configuration" })
        #expect(tools.contains { $0["name"] as? String == "get_runtime_overview" })

        let queueSpeechToolEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "queue_speech_live",
                        arguments: [
                            "text": "Inspect MCP resources",
                            "profile_name": "default",
                            "text_profile_name": "mcp-text",
                            "cwd": "./Tests",
                            "repo_root": "../SpeakSwiftlyServer",
                            "text_format": "cli_output",
                            "nested_source_format": "rust_source",
                            "source_format": "source_code",
                        ]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let queueSpeechToolPayload = try mcpToolPayload(from: queueSpeechToolEnvelope)
        let requestID = try #require(queueSpeechToolPayload["request_id"] as? String)
        #expect(queueSpeechToolPayload["status_resource_uri"] as? String == "speak://runtime/overview")
        #expect(queueSpeechToolPayload["request_resource_uri"] as? String == "speak://requests/\(requestID)")
        let queuedSpeechInvocation = try #require(await runtime.latestQueuedSpeechInvocation())
        #expect(
            queuedSpeechInvocation.normalizationContext
                == SpeechNormalizationContext(
                    cwd: "./Tests",
                    repoRoot: "../SpeakSwiftlyServer",
                    textFormat: .cli,
                    nestedSourceFormat: .rust
                )
        )
        #expect(queuedSpeechInvocation.textProfileName == "mcp-text")
        #expect(queuedSpeechInvocation.sourceFormat == .generic)

        let createCloneToolEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "create_voice_profile_from_audio",
                        arguments: [
                            "profile_name": "clone-from-mcp",
                            "vibe": "androgenous",
                            "reference_audio_path": "./Fixtures/mcp-reference.wav",
                            "transcript": "Imported from MCP",
                            "cwd": "/tmp/mcp-clone-cwd",
                        ]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let createCloneToolPayload = try mcpToolPayload(from: createCloneToolEnvelope)
        let createCloneRequestID = try #require(createCloneToolPayload["request_id"] as? String)
        #expect(createCloneToolPayload["request_resource_uri"] as? String == "speak://requests/\(createCloneRequestID)")
        let createCloneInvocation = try #require(await runtime.latestCreateCloneInvocation())
        #expect(createCloneInvocation.profileName == "clone-from-mcp")
        #expect(createCloneInvocation.vibe == .androgenous)
        #expect(createCloneInvocation.referenceAudioPath == "./Fixtures/mcp-reference.wav")
        #expect(createCloneInvocation.transcript == "Imported from MCP")
        #expect(createCloneInvocation.cwd == "/tmp/mcp-clone-cwd")

        let listResourcesEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpListResourcesRequestJSON(),
                    sessionID: initializeSessionID
                )
            )
        )
        let listResourcesResult = try #require(mcpResultPayload(from: listResourcesEnvelope))
        let resources = try #require(listResourcesResult["resources"] as? [[String: Any]])
        let resourceURIs = Set(resources.compactMap { $0["uri"] as? String })
        #expect(resourceURIs == Set(MCPResourceCatalog.resources.map(\.uri)))
        #expect(resources.contains { $0["uri"] as? String == "speak://runtime/overview" })
        #expect(resources.contains { $0["uri"] as? String == "speak://text-profiles" })
        #expect(resources.contains { $0["uri"] as? String == "speak://voices/guide" })
        #expect(resources.contains { $0["uri"] as? String == "speak://text-profiles/guide" })
        #expect(resources.contains { $0["uri"] as? String == "speak://playback/guide" })
        #expect(resources.contains { $0["uri"] as? String == "speak://requests" })
        #expect(resources.contains { $0["uri"] as? String == "speak://runtime/configuration" })
        #expect(resources.contains { $0["uri"] as? String == "speak://runtime/status" })

        let listResourceTemplatesEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpListResourceTemplatesRequestJSON(),
                    sessionID: initializeSessionID
                )
            )
        )
        let listResourceTemplatesResult = try #require(mcpResultPayload(from: listResourceTemplatesEnvelope))
        let templates = try #require(listResourceTemplatesResult["resourceTemplates"] as? [[String: Any]])
        let templateURIs = Set(templates.compactMap { $0["uriTemplate"] as? String })
        #expect(templateURIs == Set(MCPResourceCatalog.templates.map(\.uriTemplate)))
        #expect(templates.contains { $0["uriTemplate"] as? String == "speak://voices/{profile_name}" })
        #expect(templates.contains { $0["uriTemplate"] as? String == "speak://text-profiles/stored/{profile_id}" })
        #expect(templates.contains { $0["uriTemplate"] as? String == "speak://requests/{request_id}" })

        let createTextProfileEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: #"{"jsonrpc":"2.0","id":"tool-text-profile-1","method":"tools/call","params":{"name":"create_text_profile","arguments":{"id":"mcp-text","name":"MCP Text","replacements":[{"id":"mcp-replacement","text":"CLI","replacement":"command line interface","match":"whole_token","phase":"before_built_ins","is_case_sensitive":false,"formats":["cli_output"],"priority":1}]}}}"#,
                    sessionID: initializeSessionID
                )
            )
        )
        let createTextProfilePayload = try mcpToolPayload(from: createTextProfileEnvelope)
        #expect(createTextProfilePayload["id"] as? String == "mcp-text")

        let listTextProfilesEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "get_text_profiles_state",
                        arguments: [:]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let listTextProfilesPayload = try mcpToolPayload(from: listTextProfilesEnvelope)
        let listTextStoredProfiles = try #require(listTextProfilesPayload["stored_profiles"] as? [[String: Any]])
        #expect(listTextStoredProfiles.contains { $0["id"] as? String == "mcp-text" })

        let loadTextProfilesEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "load_text_profiles",
                        arguments: [:]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let loadTextProfilesPayload = try mcpToolPayload(from: loadTextProfilesEnvelope)
        let loadedStoredProfiles = try #require(loadTextProfilesPayload["stored_profiles"] as? [[String: Any]])
        #expect(loadedStoredProfiles.contains { $0["id"] as? String == "mcp-text" })

        let saveTextProfilesEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "save_text_profiles",
                        arguments: [:]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let saveTextProfilesPayload = try mcpToolPayload(from: saveTextProfilesEnvelope)
        let savedStoredProfiles = try #require(saveTextProfilesPayload["stored_profiles"] as? [[String: Any]])
        #expect(savedStoredProfiles.contains { $0["id"] as? String == "mcp-text" })
        let persistenceActionCounts = await runtime.textProfilePersistenceActionCounts()
        #expect(persistenceActionCounts.load == 1)
        #expect(persistenceActionCounts.save == 1)

        let listPromptsEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpListPromptsRequestJSON(),
                    sessionID: initializeSessionID
                )
            )
        )
        let listPromptsResult = try #require(mcpResultPayload(from: listPromptsEnvelope))
        let prompts = try #require(listPromptsResult["prompts"] as? [[String: Any]])
        let promptNames = Set(prompts.compactMap { $0["name"] as? String })
        #expect(promptNames == Set(MCPPromptCatalog.prompts.map(\.name)))
        #expect(prompts.contains { $0["name"] as? String == "draft_profile_voice_description" })
        #expect(prompts.contains { $0["name"] as? String == "draft_text_profile" })
        #expect(prompts.contains { $0["name"] as? String == "draft_text_replacement" })
        #expect(prompts.contains { $0["name"] as? String == "draft_queue_playback_notice" })
        #expect(prompts.contains { $0["name"] as? String == "choose_surface_action" })

        let getPromptEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpGetPromptRequestJSON(
                        name: "draft_profile_voice_description",
                        arguments: [
                            "profile_goal": "gentle narration",
                            "voice_traits": "warm, steady, intimate",
                        ]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let getPromptResult = try #require(mcpResultPayload(from: getPromptEnvelope))
        let promptMessages = try #require(getPromptResult["messages"] as? [[String: Any]])
        let firstPromptMessage = try #require(promptMessages.first)
        let promptContent = try #require(firstPromptMessage["content"] as? [String: Any])
        #expect((promptContent["text"] as? String)?.contains("gentle narration") == true)

        let textProfilePromptEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpGetPromptRequestJSON(
                        name: "draft_text_profile",
                        arguments: [
                            "user_goal": "expand acronyms in technical speech",
                            "profile_scope": "swift package walkthroughs",
                            "format_focus": "swift_source",
                        ]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let textProfilePromptResult = try #require(mcpResultPayload(from: textProfilePromptEnvelope))
        let textProfilePromptMessages = try #require(textProfilePromptResult["messages"] as? [[String: Any]])
        let textProfilePromptContent = try #require(textProfilePromptMessages.first?["content"] as? [String: Any])
        #expect((textProfilePromptContent["text"] as? String)?.contains("expand acronyms in technical speech") == true)

        let statusToolEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(name: "get_runtime_overview", arguments: [:]),
                    sessionID: initializeSessionID
                )
            )
        )
        let statusToolPayload = try mcpToolPayload(from: statusToolEnvelope)
        #expect(statusToolPayload["worker_mode"] as? String == "ready")
        let statusRuntimeConfiguration = try #require(statusToolPayload["runtime_configuration"] as? [String: Any])
        #expect(statusRuntimeConfiguration["active_runtime_speech_backend"] as? String == "qwen3")
        let transports = try #require(statusToolPayload["transports"] as? [[String: Any]])
        #expect(transports.contains { $0["name"] as? String == "mcp" && $0["state"] as? String == "listening" })

        let getRuntimeConfigEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(name: "get_runtime_configuration", arguments: [:]),
                    sessionID: initializeSessionID
                )
            )
        )
        let getRuntimeConfigPayload = try mcpToolPayload(from: getRuntimeConfigEnvelope)
        #expect(getRuntimeConfigPayload["active_runtime_speech_backend"] as? String == "qwen3")
        #expect(getRuntimeConfigPayload["next_runtime_speech_backend"] as? String == "qwen3")

        let setRuntimeConfigEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpCallToolRequestJSON(
                        name: "set_runtime_configuration",
                        arguments: ["speech_backend": "marvis"]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let setRuntimeConfigPayload = try mcpToolPayload(from: setRuntimeConfigEnvelope)
        #expect(setRuntimeConfigPayload["active_runtime_speech_backend"] as? String == "qwen3")
        #expect(setRuntimeConfigPayload["next_runtime_speech_backend"] as? String == "marvis")
        #expect(setRuntimeConfigPayload["persisted_speech_backend"] as? String == "marvis")

        let runtimeResourceEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://runtime/overview"),
                    sessionID: initializeSessionID
                )
            )
        )
        let runtimeResourceResult = try #require(mcpResultPayload(from: runtimeResourceEnvelope))
        let contents = try #require(runtimeResourceResult["contents"] as? [[String: Any]])
        let firstContent = try #require(contents.first)
        let runtimeText = try #require(firstContent["text"] as? String)
        let runtimePayload = try jsonObject(from: Data(runtimeText.utf8))
        let runtimeTransports = try #require(runtimePayload["transports"] as? [[String: Any]])
        #expect(runtimeTransports.contains { $0["name"] as? String == "mcp" && $0["advertised_address"] as? String == "http://127.0.0.1:7337/mcp" })
        let runtimeRefresh = try #require(runtimePayload["runtime_refresh"] as? [String: Any])
        #expect((runtimeRefresh["sequence_id"] as? Int ?? 0) > 0)
        #expect(runtimeRefresh["source"] as? String == "runtime_overview")
        let runtimeConfiguration = try #require(runtimePayload["runtime_configuration"] as? [String: Any])
        #expect(runtimeConfiguration["next_runtime_speech_backend"] as? String == "marvis")

        let runtimeStatusResourceEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://runtime/status"),
                    sessionID: initializeSessionID
                )
            )
        )
        let runtimeStatusResourceResult = try #require(mcpResultPayload(from: runtimeStatusResourceEnvelope))
        let runtimeStatusContents = try #require(runtimeStatusResourceResult["contents"] as? [[String: Any]])
        let runtimeStatusText = try #require(runtimeStatusContents.first?["text"] as? String)
        let runtimeStatusPayload = try jsonObject(from: Data(runtimeStatusText.utf8))
        let runtimeStatus = try #require(runtimeStatusPayload["status"] as? [String: Any])
        #expect(runtimeStatus["speech_backend"] as? String == "qwen3")

        let runtimeConfigResourceEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://runtime/configuration"),
                    sessionID: initializeSessionID
                )
            )
        )
        let runtimeConfigResourceResult = try #require(mcpResultPayload(from: runtimeConfigResourceEnvelope))
        let runtimeConfigContents = try #require(runtimeConfigResourceResult["contents"] as? [[String: Any]])
        let runtimeConfigText = try #require(runtimeConfigContents.first?["text"] as? String)
        let runtimeConfigPayload = try jsonObject(from: Data(runtimeConfigText.utf8))
        #expect(runtimeConfigPayload["next_runtime_speech_backend"] as? String == "marvis")

        let jobsResourceEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://requests"),
                    sessionID: initializeSessionID
                )
            )
        )
        let jobsResourceResult = try #require(mcpResultPayload(from: jobsResourceEnvelope))
        let jobsContents = try #require(jobsResourceResult["contents"] as? [[String: Any]])
        let jobsText = try #require(jobsContents.first?["text"] as? String)
        let jobsPayload = try #require(try JSONSerialization.jsonObject(with: Data(jobsText.utf8)) as? [[String: Any]])
        #expect(jobsPayload.contains { $0["request_id"] as? String == requestID })

        let profileDetailEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://voices/default"),
                    sessionID: initializeSessionID
                )
            )
        )
        let profileDetailResult = try #require(mcpResultPayload(from: profileDetailEnvelope))
        let profileDetailContents = try #require(profileDetailResult["contents"] as? [[String: Any]])
        let profileDetailText = try #require(profileDetailContents.first?["text"] as? String)
        let profileDetailPayload = try jsonObject(from: Data(profileDetailText.utf8))
        #expect(profileDetailPayload["profile_name"] as? String == "default")

        let textProfilesResourceEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://text-profiles"),
                    sessionID: initializeSessionID
                )
            )
        )
        let textProfilesResourceResult = try #require(mcpResultPayload(from: textProfilesResourceEnvelope))
        let textProfilesContents = try #require(textProfilesResourceResult["contents"] as? [[String: Any]])
        let textProfilesText = try #require(textProfilesContents.first?["text"] as? String)
        let textProfilesPayload = try jsonObject(from: Data(textProfilesText.utf8))
        let storedProfilesPayload = try #require(textProfilesPayload["stored_profiles"] as? [[String: Any]])
        #expect(storedProfilesPayload.contains { $0["id"] as? String == "mcp-text" })

        let textProfilesGuideEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://text-profiles/guide"),
                    sessionID: initializeSessionID
                )
            )
        )
        let textProfilesGuideResult = try #require(mcpResultPayload(from: textProfilesGuideEnvelope))
        let textProfilesGuideContents = try #require(textProfilesGuideResult["contents"] as? [[String: Any]])
        let textProfilesGuideText = try #require(textProfilesGuideContents.first?["text"] as? String)
        #expect(textProfilesGuideText.contains("text_profile_name"))

        let voiceProfilesGuideEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://voices/guide"),
                    sessionID: initializeSessionID
                )
            )
        )
        let voiceProfilesGuideResult = try #require(mcpResultPayload(from: voiceProfilesGuideEnvelope))
        let voiceProfilesGuideContents = try #require(voiceProfilesGuideResult["contents"] as? [[String: Any]])
        let voiceProfilesGuideText = try #require(voiceProfilesGuideContents.first?["text"] as? String)
        #expect(voiceProfilesGuideText.contains("create_voice_profile_from_audio"))
        #expect(voiceProfilesGuideText.contains("queue_speech_live"))

        let playbackGuideEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://playback/guide"),
                    sessionID: initializeSessionID
                )
            )
        )
        let playbackGuideResult = try #require(mcpResultPayload(from: playbackGuideEnvelope))
        let playbackGuideContents = try #require(playbackGuideResult["contents"] as? [[String: Any]])
        let playbackGuideText = try #require(playbackGuideContents.first?["text"] as? String)
        #expect(playbackGuideText.contains("cancel_request"))
        #expect(playbackGuideText.contains("clear_playback_queue"))

        let chooseActionPromptEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpGetPromptRequestJSON(
                        name: "choose_surface_action",
                        arguments: [
                            "user_goal": "Help the user decide whether to clone a voice or create a synthetic profile.",
                            "current_context": "The user has not provided reference audio yet.",
                        ]
                    ),
                    sessionID: initializeSessionID
                )
            )
        )
        let chooseActionPromptResult = try #require(mcpResultPayload(from: chooseActionPromptEnvelope))
        let chooseActionPromptMessages = try #require(chooseActionPromptResult["messages"] as? [[String: Any]])
        let chooseActionPromptContent = try #require(chooseActionPromptMessages.first?["content"] as? [String: Any])
        let chooseActionPromptText = try #require(chooseActionPromptContent["text"] as? String)
        #expect(chooseActionPromptText.contains("action_type"))
        #expect(chooseActionPromptText.contains("create_voice_profile_from_description"))

        let storedTextProfileEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://text-profiles/stored/mcp-text"),
                    sessionID: initializeSessionID
                )
            )
        )
        let storedTextProfileResult = try #require(mcpResultPayload(from: storedTextProfileEnvelope))
        let storedTextProfileContents = try #require(storedTextProfileResult["contents"] as? [[String: Any]])
        let storedTextProfileText = try #require(storedTextProfileContents.first?["text"] as? String)
        let storedTextProfilePayload = try jsonObject(from: Data(storedTextProfileText.utf8))
        #expect(storedTextProfilePayload["id"] as? String == "mcp-text")

        let jobDetailEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpReadResourceRequestJSON(uri: "speak://requests/\(requestID)"),
                    sessionID: initializeSessionID
                )
            )
        )
        let jobDetailResult = try #require(mcpResultPayload(from: jobDetailEnvelope))
        let jobDetailContents = try #require(jobDetailResult["contents"] as? [[String: Any]])
        let jobDetailText = try #require(jobDetailContents.first?["text"] as? String)
        let jobDetailPayload = try jsonObject(from: Data(jobDetailText.utf8))
        #expect(jobDetailPayload["request_id"] as? String == requestID)

        let smokeSurface = try #require(
            await MCPSurface.build(
                configuration: .init(
                    enabled: true,
                    path: "/mcp",
                    serverName: "speak-swiftly-test-mcp-smoke",
                    title: "SpeakSwiftly Test MCP Smoke"
                ),
                host: host
            )
        )
        let smokeApp = assembleHBApp(
            configuration: testHTTPConfig(configuration),
            host: host,
            mcpSurface: smokeSurface
        )
        try await smokeSurface.start()
        try await smokeApp.test(.router) { client in
            let initializeResponse = try await client.execute(
                uri: "/mcp",
                method: .post,
                headers: [
                    .contentType: "application/json",
                    .accept: "application/json, text/event-stream",
                ],
                body: byteBuffer(mcpInitializeRequestJSON(id: "initialize-smoke"))
            )
            #expect(initializeResponse.status == .ok)
            #expect(mcpSessionID(from: initializeResponse)?.isEmpty == false)
        }
        await smokeSurface.stop()

        await runtime.finishHeldSpeak(id: requestID)
        await mcpSurface.stop()
        await host.shutdown()
    }

    @available(macOS 14, *)
    @Test func embeddedMCPSupportsMultipleIndependentSessions() async throws {
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

        let firstInitializeResponse = await mcpSurface.handle(
            mcpPOSTRequest(body: mcpInitializeRequestJSON(id: "initialize-first"))
        )
        let firstSessionID = try #require(mcpSessionID(from: firstInitializeResponse))
        try await drainMCPResponse(firstInitializeResponse)

        let secondInitializeResponse = await mcpSurface.handle(
            mcpPOSTRequest(body: mcpInitializeRequestJSON(id: "initialize-second"))
        )
        let secondSessionID = try #require(mcpSessionID(from: secondInitializeResponse))
        try await drainMCPResponse(secondInitializeResponse)

        #expect(firstSessionID != secondSessionID)

        let firstInitializedNotification = await mcpSurface.handle(
            mcpPOSTRequest(
                body: mcpInitializedNotificationJSON(),
                sessionID: firstSessionID
            )
        )
        #expect(mcpStatusCode(from: firstInitializedNotification) == 202)

        let secondInitializedNotification = await mcpSurface.handle(
            mcpPOSTRequest(
                body: mcpInitializedNotificationJSON(),
                sessionID: secondSessionID
            )
        )
        #expect(mcpStatusCode(from: secondInitializedNotification) == 202)

        let firstStatusEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpRuntimeOverviewToolRequestJSON(),
                    sessionID: firstSessionID
                )
            )
        )
        let firstStatusPayload = try mcpToolPayload(from: firstStatusEnvelope)
        #expect(firstStatusPayload["worker_mode"] as? String == "ready")

        let secondToolsEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpListToolsRequestJSON(),
                    sessionID: secondSessionID
                )
            )
        )
        let secondToolsResult = try #require(mcpResultPayload(from: secondToolsEnvelope))
        let secondTools = try #require(secondToolsResult["tools"] as? [[String: Any]])
        #expect(secondTools.contains { $0["name"] as? String == "get_runtime_overview" })

        let deleteFirstSessionResponse = await mcpSurface.handle(
            mcpDELETERequest(sessionID: firstSessionID)
        )
        #expect(mcpStatusCode(from: deleteFirstSessionResponse) == 200)

        let deletedSessionResponse = await mcpSurface.handle(
            mcpPOSTRequest(
                body: mcpRuntimeOverviewToolRequestJSON(),
                sessionID: firstSessionID
            )
        )
        #expect(mcpStatusCode(from: deletedSessionResponse) == 404)

        let survivingSessionEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpRuntimeOverviewToolRequestJSON(),
                    sessionID: secondSessionID
                )
            )
        )
        let survivingSessionPayload = try mcpToolPayload(from: survivingSessionEnvelope)
        #expect(survivingSessionPayload["worker_mode"] as? String == "ready")

        await mcpSurface.stop()
        await host.shutdown()
    }

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
                        name: "queue_speech_live",
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

    @available(macOS 14, *)
    @Test func embeddedMCPResourceSubscriptionsEmitUpdatedNotifications() async throws {
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
        await host.markTransportStarting(name: "http")
        await host.markTransportStarting(name: "mcp")

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

        let initializeResponse = await mcpSurface.handle(mcpPOSTRequest(body: mcpInitializeRequestJSON()))
        let sessionID = try #require(mcpSessionID(from: initializeResponse))
        try await drainMCPResponse(initializeResponse)

        let initializedNotificationResponse = await mcpSurface.handle(
            mcpPOSTRequest(
                body: mcpInitializedNotificationJSON(),
                sessionID: sessionID
            )
        )
        #expect(mcpStatusCode(from: initializedNotificationResponse) == 202)

        let streamResponse = await mcpSurface.handle(mcpGETRequest(sessionID: sessionID))
        guard case .stream(let stream, _) = streamResponse else {
            Issue.record("Expected the embedded MCP GET transport to return a standalone streaming response.")
            await mcpSurface.stop()
            await host.shutdown()
            return
        }
        var streamIterator = stream.makeAsyncIterator()
        _ = try await nextMCPStreamEnvelope(from: &streamIterator)

        let subscribeEnvelope = try await mcpEnvelope(
            from: await mcpSurface.handle(
                mcpPOSTRequest(
                    body: mcpSubscribeResourceRequestJSON(uri: "speak://runtime/overview"),
                    sessionID: sessionID
                )
            )
        )
        #expect(subscribeEnvelope["result"] != nil)

        await host.markTransportFailed(
            name: "http",
            message: "SpeakSwiftlyServer test transport failure for MCP resource subscription coverage."
        )

        let updatedNotification = try await nextMCPStreamEnvelope(from: &streamIterator)
        #expect(updatedNotification["method"] as? String == "notifications/resources/updated")
        let notificationParams = try #require(updatedNotification["params"] as? [String: Any])
        #expect(notificationParams["uri"] as? String == "speak://runtime/overview")

        await mcpSurface.stop()
        await host.shutdown()
    }
}
