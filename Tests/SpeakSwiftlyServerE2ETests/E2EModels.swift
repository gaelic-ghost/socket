import Foundation
import Testing
#if canImport(Darwin)
import Darwin
#endif

// MARK: - Decodable Transport Models

struct E2EReadinessSnapshot: Decodable, Sendable {
    let workerReady: Bool

    enum CodingKeys: String, CodingKey {
        case workerReady = "worker_ready"
    }
}

struct E2EJobCreatedResponse: Decodable, Sendable {
    let requestID: String

    enum CodingKeys: String, CodingKey {
        case requestID = "request_id"
    }

    var jobID: String { requestID }
}

struct E2EProfileListResponse: Decodable, Sendable {
    let profiles: [E2EProfileSnapshot]
}

struct E2EProfileSnapshot: Decodable, Sendable {
    let profileName: String
    let vibe: String?
    let voiceDescription: String?
    let sourceText: String?

    enum CodingKeys: String, CodingKey {
        case profileName = "profile_name"
        case vibe
        case voiceDescription = "voice_description"
        case sourceText = "source_text"
    }
}

struct E2ETransportStatus: Decodable, Sendable {
    let name: String
    let state: String
    let advertisedAddress: String?

    enum CodingKeys: String, CodingKey {
        case name
        case state
        case advertisedAddress = "advertised_address"
    }
}

struct E2EHealthSnapshot: Decodable, Sendable {
    let status: String
    let workerMode: String
    let workerReady: Bool

    enum CodingKeys: String, CodingKey {
        case status
        case workerMode = "worker_mode"
        case workerReady = "worker_ready"
    }
}

struct E2EStatusSnapshot: Decodable, Sendable {
    let workerMode: String
    let cachedProfiles: [E2EProfileSnapshot]
    let transports: [E2ETransportStatus]
    let generationQueue: E2EQueueStatusSnapshot
    let playbackQueue: E2EQueueStatusSnapshot
    let playback: E2EPlaybackStatusSnapshot

    enum CodingKeys: String, CodingKey {
        case workerMode = "worker_mode"
        case cachedProfiles = "cached_profiles"
        case transports
        case generationQueue = "generation_queue"
        case playbackQueue = "playback_queue"
        case playback
    }
}

struct E2EQueueStatusSnapshot: Decodable, Sendable {
    let activeRequest: E2EActiveRequestSnapshot?
    let activeRequests: [E2EActiveRequestSnapshot]
    let queuedRequests: [E2EQueuedRequestSnapshot]

    enum CodingKeys: String, CodingKey {
        case activeRequest = "active_request"
        case activeRequests = "active_requests"
        case queuedRequests = "queued_requests"
    }
}

struct E2EPlaybackStatusSnapshot: Decodable, Sendable {
    let state: String
    let activeRequest: E2EActiveRequestSnapshot?

    enum CodingKeys: String, CodingKey {
        case state
        case activeRequest = "active_request"
    }
}

struct E2EActiveRequestSnapshot: Decodable, Sendable, Equatable {
    let id: String
    let op: String
    let profileName: String?

    enum CodingKeys: String, CodingKey {
        case id
        case op
        case profileName = "profile_name"
    }
}

struct E2EQueuedRequestSnapshot: Decodable, Sendable, Equatable {
    let id: String
    let op: String
    let profileName: String?
    let queuePosition: Int

    enum CodingKeys: String, CodingKey {
        case id
        case op
        case profileName = "profile_name"
        case queuePosition = "queue_position"
    }
}

struct E2EQueueSnapshotResponse: Decodable, Sendable {
    let queueType: String
    let activeRequest: E2EActiveRequestSnapshot?
    let activeRequests: [E2EActiveRequestSnapshot]
    let queue: [E2EQueuedRequestSnapshot]

    enum CodingKeys: String, CodingKey {
        case queueType = "queue_type"
        case activeRequest = "active_request"
        case activeRequests = "active_requests"
        case queue
    }
}

struct E2EPlaybackStateResponse: Decodable, Sendable {
    let playback: E2EPlaybackStateSnapshot
}

struct E2EPlaybackStateSnapshot: Decodable, Sendable {
    let state: String
    let activeRequest: E2EActiveRequestSnapshot?

    enum CodingKeys: String, CodingKey {
        case state
        case activeRequest = "active_request"
    }
}

struct E2EQueueClearedResponse: Decodable, Sendable {
    let clearedCount: Int

    enum CodingKeys: String, CodingKey {
        case clearedCount = "cleared_count"
    }
}

struct E2EQueueCancellationResponse: Decodable, Sendable {
    let cancelledRequestID: String

    enum CodingKeys: String, CodingKey {
        case cancelledRequestID = "cancelled_request_id"
    }
}

struct E2ERequestListResponse: Decodable, Sendable {
    let requests: [E2EJobSnapshot]
}

struct E2ETextProfileListResponse: Decodable, Sendable {
    let textProfiles: E2ETextProfilesSnapshot

    enum CodingKeys: String, CodingKey {
        case textProfiles = "text_profiles"
    }
}

struct E2ETextProfileResponse: Decodable, Sendable {
    let profile: E2ETextProfileSnapshot
}

struct E2ETextProfilesSnapshot: Decodable, Sendable {
    let builtInStyle: String
    let baseProfile: E2ETextProfileSnapshot
    let activeProfile: E2ETextProfileSnapshot
    let storedProfiles: [E2ETextProfileSnapshot]
    let effectiveProfile: E2ETextProfileSnapshot

    enum CodingKeys: String, CodingKey {
        case builtInStyle = "built_in_style"
        case baseProfile = "base_profile"
        case activeProfile = "active_profile"
        case storedProfiles = "stored_profiles"
        case effectiveProfile = "effective_profile"
    }
}

struct E2ETextProfileStyleResponse: Decodable, Sendable {
    let textProfileStyle: E2ETextProfileStyleSnapshot

    enum CodingKeys: String, CodingKey {
        case textProfileStyle = "text_profile_style"
    }
}

struct E2ETextProfileSnapshot: Decodable, Sendable, Equatable {
    let id: String
    let name: String
    let replacements: [E2ETextReplacementSnapshot]
}

struct E2ETextProfileStyleSnapshot: Decodable, Sendable, Equatable {
    let builtInStyle: String

    enum CodingKeys: String, CodingKey {
        case builtInStyle = "built_in_style"
    }
}

struct E2ETextReplacementSnapshot: Decodable, Sendable, Equatable {
    let id: String
    let text: String
    let replacement: String
    let match: String
    let phase: String
    let isCaseSensitive: Bool
    let formats: [String]
    let priority: Int

    enum CodingKeys: String, CodingKey {
        case id
        case text
        case replacement
        case match
        case phase
        case isCaseSensitive = "is_case_sensitive"
        case formats
        case priority
    }
}

struct E2EJobSnapshot: Decodable, Sendable {
    let requestID: String
    let status: String
    let history: [E2EJobEvent]
    let terminalEvent: E2EJobEvent?

    enum CodingKeys: String, CodingKey {
        case requestID = "request_id"
        case status
        case history
        case terminalEvent = "terminal_event"
    }

    var jobID: String { requestID }
}

struct E2EJobEvent: Decodable, Sendable {
    let id: String?
    let event: String?
    let op: String?
    let stage: String?
    let ok: Bool?
    let reason: String?
    let profileName: String?
    let profilePath: String?
    let message: String?
    let code: String?
    let cancelledRequestID: String?

    enum CodingKeys: String, CodingKey {
        case id
        case event
        case op
        case stage
        case ok
        case reason
        case profileName = "profile_name"
        case profilePath = "profile_path"
        case message
        case code
        case cancelledRequestID = "cancelled_request_id"
    }
}
