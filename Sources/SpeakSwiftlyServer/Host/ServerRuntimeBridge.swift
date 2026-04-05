import Foundation
import SpeakSwiftlyCore
import TextForSpeech

typealias SpeechNormalizationContext = TextForSpeech.Context

// MARK: - Runtime Bridge

struct RuntimeRequestHandle: Sendable {
    let id: String
    let operationName: String
    let profileName: String?
    let events: AsyncThrowingStream<SpeakSwiftly.RequestEvent, Error>

    // MARK: - Initialization

    init(
        id: String,
        operationName: String,
        profileName: String?,
        events: AsyncThrowingStream<SpeakSwiftly.RequestEvent, Error>
    ) {
        self.id = id
        self.operationName = operationName
        self.profileName = profileName
        self.events = events
    }

    init(_ handle: SpeakSwiftly.RequestHandle) {
        self.id = handle.id
        self.operationName = handle.operation
        self.profileName = handle.profileName
        self.events = handle.events
    }
}

// MARK: - Runtime Protocol

protocol ServerRuntimeProtocol: Actor {
    func start()
    func shutdown() async
    func statusEvents() -> AsyncStream<SpeakSwiftly.StatusEvent>
    func queueSpeechHandle(
        text: String,
        profileName: String,
        normalizationContext: SpeechNormalizationContext?,
        as jobType: SpeakSwiftly.Job,
        id: String
    ) async -> RuntimeRequestHandle
    func createProfileHandle(
        profileName: String,
        text: String,
        voiceDescription: String,
        outputPath: String?,
        id: String
    ) async -> RuntimeRequestHandle
    func createCloneHandle(
        profileName: String,
        referenceAudioPath: String,
        transcript: String?,
        id: String
    ) async -> RuntimeRequestHandle
    func listProfilesHandle(id: String) async -> RuntimeRequestHandle
    func removeProfileHandle(profileName: String, id: String) async -> RuntimeRequestHandle
    func listQueueHandle(_ queueType: SpeakSwiftly.Queue, id requestID: String) async -> RuntimeRequestHandle
    func playbackHandle(_ action: SpeakSwiftly.PlaybackAction, id requestID: String) async -> RuntimeRequestHandle
    func clearQueueHandle(id requestID: String) async -> RuntimeRequestHandle
    func cancelRequestHandle(with id: String, requestID: String) async -> RuntimeRequestHandle
    func activeTextProfile() -> TextForSpeech.Profile
    func baseTextProfile() -> TextForSpeech.Profile
    func textProfile(named profileID: String) -> TextForSpeech.Profile?
    func textProfiles() -> [TextForSpeech.Profile]
    func effectiveTextProfile(named profileID: String?) -> TextForSpeech.Profile
    func textProfilePersistenceURL() -> URL?
    func createTextProfile(id: String, named name: String, replacements: [TextForSpeech.Replacement]) throws -> TextForSpeech.Profile
    func storeTextProfile(_ profile: TextForSpeech.Profile) throws
    func useTextProfile(_ profile: TextForSpeech.Profile) throws
    func removeTextProfile(named profileID: String) throws
    func resetTextProfile() throws
    func addTextReplacement(_ replacement: TextForSpeech.Replacement) throws -> TextForSpeech.Profile
    func addTextReplacement(_ replacement: TextForSpeech.Replacement, toStoredTextProfileNamed profileID: String) throws -> TextForSpeech.Profile
    func replaceTextReplacement(_ replacement: TextForSpeech.Replacement) throws -> TextForSpeech.Profile
    func replaceTextReplacement(_ replacement: TextForSpeech.Replacement, inStoredTextProfileNamed profileID: String) throws -> TextForSpeech.Profile
    func removeTextReplacement(id replacementID: String) throws -> TextForSpeech.Profile
    func removeTextReplacement(id replacementID: String, fromStoredTextProfileNamed profileID: String) throws -> TextForSpeech.Profile
}

// MARK: - Runtime Adapter

extension SpeakSwiftly.Runtime: ServerRuntimeProtocol {
    func queueSpeechHandle(
        text: String,
        profileName: String,
        normalizationContext: SpeechNormalizationContext?,
        as jobType: SpeakSwiftly.Job,
        id: String
    ) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(
            await speak(
                text: text,
                with: profileName,
                as: jobType,
                textContext: normalizationContext,
                id: id
            )
        )
    }

    func createProfileHandle(
        profileName: String,
        text: String,
        voiceDescription: String,
        outputPath: String?,
        id: String
    ) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(
            await createProfile(
                named: profileName,
                from: text,
                voice: voiceDescription,
                outputPath: outputPath,
                id: id
            )
        )
    }

    func createCloneHandle(
        profileName: String,
        referenceAudioPath: String,
        transcript: String?,
        id: String
    ) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(
            await createClone(
                named: profileName,
                from: URL(fileURLWithPath: referenceAudioPath),
                transcript: transcript,
                id: id
            )
        )
    }

    func listProfilesHandle(id: String) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await profiles(id: id))
    }

    func removeProfileHandle(profileName: String, id: String) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await removeProfile(named: profileName, id: id))
    }

    func listQueueHandle(_ queueType: SpeakSwiftly.Queue, id requestID: String) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await queue(queueType, id: requestID))
    }

    func playbackHandle(_ action: SpeakSwiftly.PlaybackAction, id requestID: String) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await playback(action, id: requestID))
    }

    func clearQueueHandle(id requestID: String) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await clearQueue(id: requestID))
    }

    func cancelRequestHandle(with id: String, requestID: String) async -> RuntimeRequestHandle {
        RuntimeRequestHandle(await cancelRequest(id, requestID: requestID))
    }
}
