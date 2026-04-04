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

enum HostEvent: Sendable {
    case transportChanged(TransportStatusSnapshot)
    case jobChanged(JobSnapshot)
    case playbackChanged(PlaybackStatusSnapshot)
    case profileCacheChanged(ProfileCacheStatusSnapshot)
    case recentErrorRecorded(RecentErrorSnapshot)
}
