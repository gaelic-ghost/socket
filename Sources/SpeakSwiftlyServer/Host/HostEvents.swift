import Foundation

// MARK: - Host Events

struct ProfileCacheStatusSnapshot: Codable, Sendable, Equatable {
    let state: String
    let warning: String?
    let profileCount: Int
    let lastRefreshAt: String?

    enum CodingKeys: String, CodingKey {
        case state
        case warning
        case profileCount = "profile_count"
        case lastRefreshAt = "last_refresh_at"
    }
}

struct TextProfilesStatusSnapshot: Codable, Sendable, Equatable {
    let activeProfileID: String
    let storedProfileCount: Int
    let persistenceURL: String?

    enum CodingKeys: String, CodingKey {
        case activeProfileID = "active_profile_id"
        case storedProfileCount = "stored_profile_count"
        case persistenceURL = "persistence_url"
    }
}

struct JobEventUpdate: Sendable, Equatable {
    let jobID: String
    let event: ServerJobEvent
    let historyIndex: Int
    let terminal: Bool
}

enum HostEvent: Sendable {
    case transportChanged(TransportStatusSnapshot)
    case jobChanged(JobSnapshot)
    case jobEvent(JobEventUpdate)
    case playbackChanged(PlaybackStatusSnapshot)
    case profileCacheChanged(ProfileCacheStatusSnapshot)
    case textProfilesChanged(TextProfilesStatusSnapshot)
    case recentErrorRecorded(RecentErrorSnapshot)
}
