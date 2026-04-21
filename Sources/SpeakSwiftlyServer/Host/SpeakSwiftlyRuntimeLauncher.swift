import Foundation
import SpeakSwiftly

/// Bridges package-owned startup environment overrides into `SpeakSwiftly.liftoff(...)`.
///
/// `SpeakSwiftly` currently resolves its profile-root override from the process environment during
/// runtime liftoff. The server keeps that process-global mutation serialized and narrowly scoped
/// here so embedded and standalone startup paths can use one explicit startup environment without
/// leaking those overrides across unrelated runtime launches.
actor SpeakSwiftlyRuntimeLauncher {
    static let shared = SpeakSwiftlyRuntimeLauncher()

    private static let bridgedEnvironmentKeys = [
        "SPEAKSWIFTLY_PROFILE_ROOT",
    ]

    static func environmentOverrides(from environment: [String: String]) -> [String: String?] {
        bridgedEnvironmentKeys.reduce(into: [String: String?]()) { result, key in
            switch key {
                case "SPEAKSWIFTLY_PROFILE_ROOT":
                    result[key] = bridgedSpeakSwiftlyProfileRoot(environment[key])
                default:
                    result[key] = environment[key]
            }
        }
    }

    static func bridgedSpeakSwiftlyProfileRoot(_ path: String?) -> String? {
        guard let path else {
            return nil
        }

        let trimmedPath = path.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmedPath.isEmpty else {
            return nil
        }

        let standardizedURL = URL(fileURLWithPath: trimmedPath, isDirectory: true)
            .standardizedFileURL

        // SpeakSwiftlyServer still models this override as the profile-store root for its own
        // runtime-configuration snapshots and CLI surface, while the pinned SpeakSwiftly runtime
        // now interprets the same env var as the broader persistence root that contains profiles/.
        guard standardizedURL.lastPathComponent == "profiles" else {
            return standardizedURL.path
        }

        return standardizedURL.deletingLastPathComponent().path
    }

    func launch<T: Sendable>(
        configuration: SpeakSwiftly.Configuration,
        environment: [String: String],
        makeRuntime: @escaping @Sendable (SpeakSwiftly.Configuration?) async -> T,
    ) async -> T {
        await withTemporaryEnvironment(overrides: Self.environmentOverrides(from: environment)) {
            await makeRuntime(configuration)
        }
    }

    private func withTemporaryEnvironment<T: Sendable>(
        overrides: [String: String?],
        body: @escaping @Sendable () async -> T,
    ) async -> T {
        let originalValues = captureEnvironmentValues(for: Array(overrides.keys))
        applyEnvironmentValues(overrides)
        let result = await body()
        applyEnvironmentValues(originalValues)
        return result
    }

    private func captureEnvironmentValues(for keys: [String]) -> [String: String?] {
        keys.reduce(into: [String: String?]()) { result, key in
            result[key] = ProcessInfo.processInfo.environment[key]
        }
    }

    private func applyEnvironmentValues(_ values: [String: String?]) {
        for (key, value) in values {
            switch value {
                case let .some(value):
                    setenv(key, value, 1)
                case .none:
                    unsetenv(key)
            }
        }
    }
}
