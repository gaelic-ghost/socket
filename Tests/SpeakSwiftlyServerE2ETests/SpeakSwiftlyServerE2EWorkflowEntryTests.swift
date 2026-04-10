import Testing

// MARK: - End-to-End Workflow Entry Tests

extension SpeakSwiftlyServerE2ETests {
    @Test func httpVoiceDesignLaneRunsSequentialSilentAndAudibleCoverage() async throws {
        try await Self.runVoiceDesignLane(using: .http)
    }

    @Test func httpCloneLaneWithProvidedTranscriptRunsSequentialSilentAndAudibleCoverage() async throws {
        try await Self.runCloneLane(using: .http, transcriptMode: .provided)
    }

    @Test func httpCloneLaneWithInferredTranscriptRunsSequentialSilentAndAudibleCoverage() async throws {
        try await Self.runCloneLane(using: .http, transcriptMode: .inferred)
    }

    @Test func mcpVoiceDesignLaneRunsSequentialSilentAndAudibleCoverage() async throws {
        try await Self.runVoiceDesignLane(using: .mcp)
    }

    @Test func mcpCloneLaneWithProvidedTranscriptRunsSequentialSilentAndAudibleCoverage() async throws {
        try await Self.runCloneLane(using: .mcp, transcriptMode: .provided)
    }

    @Test func mcpCloneLaneWithInferredTranscriptRunsSequentialSilentAndAudibleCoverage() async throws {
        try await Self.runCloneLane(using: .mcp, transcriptMode: .inferred)
    }

    @Test func httpMarvisVoiceDesignProfilesRunAudibleLivePlaybackAcrossAllVibes() async throws {
        try await Self.runMarvisTripletLane(using: .http)
    }

    @Test func mcpMarvisVoiceDesignProfilesRunAudibleLivePlaybackAcrossAllVibes() async throws {
        try await Self.runMarvisTripletLane(using: .mcp)
    }

    @Test func httpMarvisQueuedLivePlaybackDrainsInOrder() async throws {
        try await Self.runQueuedMarvisTripletLane(using: .http)
    }

    @Test func mcpMarvisQueuedLivePlaybackDrainsInOrder() async throws {
        try await Self.runQueuedMarvisTripletLane(using: .mcp)
    }

    @Test func httpProfileAndCloneCreationResolveRelativePathsAgainstExplicitCallerWorkingDirectory() async throws {
        try await Self.runRelativePathProfileAndCloneLane(using: .http)
    }

    @Test func mcpProfileAndCloneCreationResolveRelativePathsAgainstExplicitCallerWorkingDirectory() async throws {
        try await Self.runRelativePathProfileAndCloneLane(using: .mcp)
    }
}
