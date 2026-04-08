import Foundation
import SpeakSwiftlyCore

// MARK: - Runtime Configuration Store

struct RuntimeConfigurationStore: Sendable {
    private let environment: [String: String]
    private let configurationURL: URL
    private let profileRootURL: URL
    private let activeRuntimeSpeechBackend: SpeakSwiftly.SpeechBackend

    init(
        environment: [String: String] = ProcessInfo.processInfo.environment,
        fileManager: FileManager = .default,
        activeRuntimeSpeechBackend: SpeakSwiftly.SpeechBackend? = nil
    ) {
        let profileRootOverride = environment["SPEAKSWIFTLY_PROFILE_ROOT"]
        self.environment = environment
        self.configurationURL = SpeakSwiftly.Configuration.defaultPersistenceURL(
            fileManager: fileManager,
            profileRootOverride: profileRootOverride
        )
        if let profileRootOverride,
           profileRootOverride.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty == false
        {
            self.profileRootURL = URL(fileURLWithPath: profileRootOverride, isDirectory: true)
        } else {
            self.profileRootURL = configurationURL
                .deletingLastPathComponent()
                .appendingPathComponent("profiles", isDirectory: true)
        }
        self.activeRuntimeSpeechBackend = activeRuntimeSpeechBackend
            ?? Self.resolveNextRuntimeSpeechBackend(
                environment: environment,
                configurationURL: configurationURL
            ).speechBackend
    }

    func snapshot() -> RuntimeConfigurationSnapshot {
        let resolution = Self.resolveNextRuntimeSpeechBackend(
            environment: environment,
            configurationURL: configurationURL
        )
        let environmentOverride = SpeakSwiftly.SpeechBackend.configured(in: environment)

        return .init(
            activeRuntimeSpeechBackend: activeRuntimeSpeechBackend.rawValue,
            nextRuntimeSpeechBackend: resolution.speechBackend.rawValue,
            environmentSpeechBackendOverride: environmentOverride?.rawValue,
            persistedSpeechBackend: resolution.persistedSpeechBackend?.rawValue,
            profileRootPath: profileRootURL.path,
            persistedConfigurationPath: configurationURL.path,
            persistedConfigurationExists: resolution.configurationExists,
            persistedConfigurationState: resolution.configurationState.rawValue,
            persistedConfigurationError: resolution.configurationError,
            persistedConfigurationAppliesOnRestart: true,
            activeRuntimeMatchesNextRuntime: activeRuntimeSpeechBackend == resolution.speechBackend,
            persistedConfigurationWillAffectNextRuntimeStart: environmentOverride == nil
        )
    }

    func save(speechBackend: SpeakSwiftly.SpeechBackend) throws -> RuntimeConfigurationSnapshot {
        do {
            try SpeakSwiftly.Configuration(speechBackend: speechBackend).save(to: configurationURL)
        } catch {
            throw RuntimeConfigurationStoreError(
                "SpeakSwiftlyServer could not save the persisted runtime configuration to '\(configurationURL.path)'. Likely cause: \(error.localizedDescription)"
            )
        }
        return snapshot()
    }
}

private extension RuntimeConfigurationStore {
    enum ConfigurationState: String, Sendable {
        case missing
        case loaded
        case invalid
    }

    struct Resolution: Sendable {
        let speechBackend: SpeakSwiftly.SpeechBackend
        let persistedSpeechBackend: SpeakSwiftly.SpeechBackend?
        let configurationExists: Bool
        let configurationState: ConfigurationState
        let configurationError: String?
    }

    static func resolveNextRuntimeSpeechBackend(
        environment: [String: String],
        configurationURL: URL
    ) -> Resolution {
        let fileManager = FileManager.default
        let configurationExists = fileManager.fileExists(atPath: configurationURL.path)

        if let environmentOverride = SpeakSwiftly.SpeechBackend.configured(in: environment) {
            let persistedState = loadPersistedConfiguration(from: configurationURL, configurationExists: configurationExists)
            return .init(
                speechBackend: environmentOverride,
                persistedSpeechBackend: persistedState.persistedSpeechBackend,
                configurationExists: configurationExists,
                configurationState: persistedState.configurationState,
                configurationError: persistedState.configurationError
            )
        }

        let persistedState = loadPersistedConfiguration(from: configurationURL, configurationExists: configurationExists)
        if let persistedSpeechBackend = persistedState.persistedSpeechBackend {
            return .init(
                speechBackend: persistedSpeechBackend,
                persistedSpeechBackend: persistedSpeechBackend,
                configurationExists: configurationExists,
                configurationState: .loaded,
                configurationError: nil
            )
        }

        return .init(
            speechBackend: .qwen3,
            persistedSpeechBackend: nil,
            configurationExists: configurationExists,
            configurationState: persistedState.configurationState,
            configurationError: persistedState.configurationError
        )
    }

    static func loadPersistedConfiguration(
        from configurationURL: URL,
        configurationExists: Bool
    ) -> (
        persistedSpeechBackend: SpeakSwiftly.SpeechBackend?,
        configurationState: ConfigurationState,
        configurationError: String?
    ) {
        guard configurationExists else {
            return (nil, .missing, nil)
        }

        do {
            let configuration = try SpeakSwiftly.Configuration.load(from: configurationURL)
            return (configuration.speechBackend, .loaded, nil)
        } catch {
            return (
                nil,
                .invalid,
                "SpeakSwiftlyServer could not decode the persisted runtime configuration at '\(configurationURL.path)'. Likely cause: \(error.localizedDescription)"
            )
        }
    }
}

struct RuntimeConfigurationStoreError: LocalizedError, Sendable {
    let message: String

    init(_ message: String) {
        self.message = message
    }

    var errorDescription: String? {
        message
    }
}
