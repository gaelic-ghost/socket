import Foundation
import Hummingbird
import SpeakSwiftlyCore
import TextForSpeech

// MARK: - Profile Models

public struct ProfileSnapshot: Codable, Sendable, Equatable {
    public let profileName: String
    public let vibe: String
    public let createdAt: String
    public let voiceDescription: String
    public let sourceText: String

    enum CodingKeys: String, CodingKey {
        case profileName = "profile_name"
        case vibe
        case createdAt = "created_at"
        case voiceDescription = "voice_description"
        case sourceText = "source_text"
    }

    init(profile: SpeakSwiftly.ProfileSummary) {
        self.profileName = profile.profileName
        self.vibe = profile.vibe.rawValue
        self.createdAt = TimestampFormatter.string(from: profile.createdAt)
        self.voiceDescription = profile.voiceDescription
        self.sourceText = profile.sourceText
    }
}

struct ProfileListResponse: ResponseEncodable, Sendable {
    let profiles: [ProfileSnapshot]
}

// MARK: - Text Profile Models

public struct TextReplacementSnapshot: Codable, Sendable, Equatable {
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

    init(replacement: TextForSpeech.Replacement) {
        self.id = replacement.id
        self.text = replacement.text
        self.replacement = replacement.replacement
        self.match = replacement.match.rawValue
        self.phase = replacement.phase.rawValue
        self.isCaseSensitive = replacement.isCaseSensitive
        self.formats = (
            replacement.textFormats.map(\.rawValue)
            + replacement.sourceFormats.map(\.rawValue)
        ).sorted()
        self.priority = replacement.priority
    }

    func model() throws -> TextForSpeech.Replacement {
        guard let match = TextForSpeech.Replacement.Match(rawValue: match) else {
            throw HTTPError(
                .badRequest,
                message: "Text replacement '\(id)' used unsupported match '\(match)'. Expected one of: exact_phrase, whole_token."
            )
        }
        guard let phase = TextForSpeech.Replacement.Phase(rawValue: phase) else {
            throw HTTPError(
                .badRequest,
                message: "Text replacement '\(id)' used unsupported phase '\(phase)'. Expected one of: before_built_ins, after_built_ins."
            )
        }

        let resolvedFormats = try formats.map(resolveNormalizationFormat(_:))
        let textFormats: Set<TextForSpeech.TextFormat> = Set(resolvedFormats.compactMap { format in
            guard case .text(let textFormat) = format else {
                return nil
            }
            return textFormat
        })
        let sourceFormats: Set<TextForSpeech.SourceFormat> = Set(resolvedFormats.compactMap { format in
            guard case .source(let sourceFormat) = format else {
                return nil
            }
            return sourceFormat
        })
        return TextForSpeech.Replacement(
            text,
            with: replacement,
            id: id,
            matching: match,
            during: phase,
            caseSensitive: isCaseSensitive,
            forTextFormats: textFormats,
            forSourceFormats: sourceFormats,
            priority: priority
        )
    }
}

public struct TextProfileSnapshot: Codable, Sendable, Equatable {
    let id: String
    let name: String
    let replacements: [TextReplacementSnapshot]

    init(profile: TextForSpeech.Profile) {
        self.id = profile.id
        self.name = profile.name
        self.replacements = profile.replacements.map(TextReplacementSnapshot.init(replacement:))
    }

    func model() throws -> TextForSpeech.Profile {
        try .init(
            id: id,
            name: name,
            replacements: replacements.map { try $0.model() }
        )
    }
}

struct TextProfilesSnapshot: ResponseEncodable, Sendable, Equatable {
    let baseProfile: TextProfileSnapshot
    let activeProfile: TextProfileSnapshot
    let storedProfiles: [TextProfileSnapshot]
    let effectiveProfile: TextProfileSnapshot

    enum CodingKeys: String, CodingKey {
        case baseProfile = "base_profile"
        case activeProfile = "active_profile"
        case storedProfiles = "stored_profiles"
        case effectiveProfile = "effective_profile"
    }
}

struct TextProfileListResponse: ResponseEncodable, Sendable {
    let textProfiles: TextProfilesSnapshot

    enum CodingKeys: String, CodingKey {
        case textProfiles = "text_profiles"
    }
}

struct TextProfileResponse: ResponseEncodable, Sendable {
    let profile: TextProfileSnapshot
}

struct CreateTextProfileRequestPayload: Decodable {
    let id: String
    let name: String
    let replacements: [TextReplacementSnapshot]
}

struct StoreTextProfileRequestPayload: Decodable {
    let profile: TextProfileSnapshot
}

struct UseTextProfileRequestPayload: Decodable {
    let profile: TextProfileSnapshot
}

struct TextReplacementRequestPayload: Decodable {
    let replacement: TextReplacementSnapshot
}
