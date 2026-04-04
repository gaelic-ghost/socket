import Foundation
import MCP

// MARK: - MCP Models

struct MCPAcceptedJobResult: Codable, Sendable {
    let jobID: String
    let statusResourceURI: String
    let message: String

    enum CodingKeys: String, CodingKey {
        case jobID = "job_id"
        case statusResourceURI = "status_resource_uri"
        case message
    }
}

enum MCPToolCatalog {
    static let definitions: [Tool] = [
        Tool(
            name: "queue_speech_live",
            description: "Queue live speech playback with a stored SpeakSwiftly profile and return once the shared server host has accepted the speech job.",
            inputSchema: [
                "type": "object",
                "required": ["text", "profile_name"],
                "properties": [
                    "text": ["type": "string"],
                    "profile_name": ["type": "string"],
                ],
            ]
        ),
        Tool(
            name: "create_profile",
            description: "Create a new stored SpeakSwiftly voice profile through the shared server host.",
            inputSchema: [
                "type": "object",
                "required": ["profile_name", "text", "voice_description"],
                "properties": [
                    "profile_name": ["type": "string"],
                    "text": ["type": "string"],
                    "voice_description": ["type": "string"],
                    "output_path": ["type": "string"],
                ],
            ]
        ),
        Tool(
            name: "list_profiles",
            description: "Return the current in-memory snapshot of cached SpeakSwiftly profiles.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ],
            annotations: .init(
                readOnlyHint: true,
                destructiveHint: false,
                idempotentHint: true,
                openWorldHint: false
            )
        ),
        Tool(
            name: "remove_profile",
            description: "Remove a stored SpeakSwiftly voice profile through the shared server host.",
            inputSchema: [
                "type": "object",
                "required": ["profile_name"],
                "properties": [
                    "profile_name": ["type": "string"],
                ],
            ]
        ),
        Tool(
            name: "list_queue_generation",
            description: "Return the active SpeakSwiftly generation request plus the currently queued generation work, if any.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ],
            annotations: .init(
                readOnlyHint: true,
                destructiveHint: false,
                idempotentHint: true,
                openWorldHint: false
            )
        ),
        Tool(
            name: "list_queue_playback",
            description: "Return the active SpeakSwiftly playback request plus the currently queued playback work, if any.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ],
            annotations: .init(
                readOnlyHint: true,
                destructiveHint: false,
                idempotentHint: true,
                openWorldHint: false
            )
        ),
        Tool(
            name: "playback_pause",
            description: "Pause the current SpeakSwiftly playback stream and return the resulting playback state snapshot.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ]
        ),
        Tool(
            name: "playback_resume",
            description: "Resume the current SpeakSwiftly playback stream and return the resulting playback state snapshot.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ]
        ),
        Tool(
            name: "playback_state",
            description: "Return the current SpeakSwiftly playback state snapshot, including the active playback request when one exists.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ],
            annotations: .init(
                readOnlyHint: true,
                destructiveHint: false,
                idempotentHint: true,
                openWorldHint: false
            )
        ),
        Tool(
            name: "clear_queue",
            description: "Cancel all currently queued SpeakSwiftly requests without interrupting the active request.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ],
            annotations: .init(
                readOnlyHint: false,
                destructiveHint: true,
                idempotentHint: false,
                openWorldHint: false
            )
        ),
        Tool(
            name: "cancel_request",
            description: "Cancel one queued or active SpeakSwiftly request by request id.",
            inputSchema: [
                "type": "object",
                "required": ["request_id"],
                "properties": [
                    "request_id": ["type": "string"],
                ],
            ],
            annotations: .init(
                readOnlyHint: false,
                destructiveHint: true,
                idempotentHint: false,
                openWorldHint: false
            )
        ),
        Tool(
            name: "status",
            description: "Report worker readiness, cached profiles, queue state, playback state, and transport status from the shared server host.",
            inputSchema: [
                "type": "object",
                "properties": [:],
            ],
            annotations: .init(
                readOnlyHint: true,
                destructiveHint: false,
                idempotentHint: true,
                openWorldHint: false
            )
        ),
    ]
}

enum MCPResourceCatalog {
    static let resourceURIs = Set([
        "speak://status",
        "speak://profiles",
        "speak://runtime",
    ])

    static let resources: [Resource] = [
        Resource(
            name: "Speak Status",
            uri: "speak://status",
            description: "Operational summary from the shared SpeakSwiftly server host.",
            mimeType: "application/json"
        ),
        Resource(
            name: "Cached Profiles",
            uri: "speak://profiles",
            description: "Current cached SpeakSwiftly profile snapshot from the shared server host.",
            mimeType: "application/json"
        ),
        Resource(
            name: "Runtime Summary",
            uri: "speak://runtime",
            description: "Shared host runtime summary, including queue, playback, transport, and recent-error state.",
            mimeType: "application/json"
        ),
    ]
}
