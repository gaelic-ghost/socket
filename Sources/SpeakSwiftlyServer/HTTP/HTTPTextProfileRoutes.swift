import Hummingbird

// MARK: - Text Profile Routes

func registerHTTPTextProfileRoutes(
    on router: Router<BasicRequestContext>,
    host: ServerHost
) {
    router.get("text-profiles") { _, _ -> TextProfileListResponse in
        .init(textProfiles: await host.textProfilesSnapshot())
    }

    router.get("text-profiles/style") { _, _ -> TextProfileStyleResponse in
        .init(textProfileStyle: await host.textProfileStyleSnapshot())
    }

    router.get("text-profiles/base") { _, _ -> TextProfileResponse in
        .init(profile: (await host.textProfilesSnapshot()).baseProfile)
    }

    router.get("text-profiles/active") { _, _ -> TextProfileResponse in
        .init(profile: (await host.textProfilesSnapshot()).activeProfile)
    }

    router.get("text-profiles/effective") { _, _ -> TextProfileResponse in
        .init(profile: await host.effectiveTextProfile(nil))
    }

    router.get("text-profiles/effective/:profile_id") { _, context -> TextProfileResponse in
        let profileID = try context.parameters.require("profile_id")
        return .init(profile: await host.effectiveTextProfile(profileID))
    }

    router.get("text-profiles/stored/:profile_id") { _, context -> TextProfileResponse in
        let profileID = try context.parameters.require("profile_id")
        guard let profile = await host.storedTextProfile(profileID) else {
            throw HTTPError(
                .notFound,
                message: "Text profile '\(profileID)' was not found in the persisted SpeakSwiftly text-profile set."
            )
        }
        return .init(profile: profile)
    }

    router.post("text-profiles/stored") { request, context -> TextProfileResponse in
        let payload = try await request.decode(as: CreateTextProfileRequestPayload.self, context: context)
        let profile = try await host.createTextProfile(
            id: payload.id,
            name: payload.name,
            replacements: try payload.replacements.map { try $0.model() }
        )
        return .init(profile: profile)
    }

    router.post("text-profiles/load") { _, _ -> TextProfileListResponse in
        .init(textProfiles: try await host.loadTextProfiles())
    }

    router.post("text-profiles/save") { _, _ -> TextProfileListResponse in
        .init(textProfiles: try await host.saveTextProfiles())
    }

    router.put("text-profiles/style") { request, context -> TextProfileListResponse in
        let payload = try await request.decode(as: SetTextProfileStyleRequestPayload.self, context: context)
        return .init(textProfiles: try await host.setTextProfileStyle(payload.styleModel()))
    }

    router.put("text-profiles/stored/:profile_id") { request, context -> TextProfileResponse in
        let profileID = try context.parameters.require("profile_id")
        let payload = try await request.decode(as: StoreTextProfileRequestPayload.self, context: context)
        guard payload.profile.id == profileID else {
            throw HTTPError(
                .badRequest,
                message: "Stored text profile route id '\(profileID)' did not match body profile id '\(payload.profile.id)'."
            )
        }
        return .init(profile: try await host.storeTextProfile(try payload.profile.model()))
    }

    router.put("text-profiles/active") { request, context -> TextProfileResponse in
        let payload = try await request.decode(as: UseTextProfileRequestPayload.self, context: context)
        return .init(profile: try await host.useTextProfile(try payload.profile.model()))
    }

    router.post("text-profiles/active/reset") { _, _ -> TextProfileResponse in
        .init(profile: try await host.resetTextProfile())
    }

    router.delete("text-profiles/stored/:profile_id") { _, context -> TextProfileListResponse in
        let profileID = try context.parameters.require("profile_id")
        return .init(textProfiles: try await host.removeTextProfile(id: profileID))
    }

    router.post("text-profiles/active/replacements") { request, context -> TextProfileResponse in
        let payload = try await request.decode(as: TextReplacementRequestPayload.self, context: context)
        return .init(profile: try await host.addTextReplacement(try payload.replacement.model()))
    }

    router.post("text-profiles/stored/:profile_id/replacements") { request, context -> TextProfileResponse in
        let profileID = try context.parameters.require("profile_id")
        let payload = try await request.decode(as: TextReplacementRequestPayload.self, context: context)
        return .init(profile: try await host.addTextReplacement(try payload.replacement.model(), toStoredTextProfileID: profileID))
    }

    router.put("text-profiles/active/replacements/:replacement_id") { request, context -> TextProfileResponse in
        let replacementID = try context.parameters.require("replacement_id")
        let payload = try await request.decode(as: TextReplacementRequestPayload.self, context: context)
        guard payload.replacement.id == replacementID else {
            throw HTTPError(
                .badRequest,
                message: "Active text replacement route id '\(replacementID)' did not match body replacement id '\(payload.replacement.id)'."
            )
        }
        return .init(profile: try await host.replaceTextReplacement(try payload.replacement.model()))
    }

    router.put("text-profiles/stored/:profile_id/replacements/:replacement_id") { request, context -> TextProfileResponse in
        let profileID = try context.parameters.require("profile_id")
        let replacementID = try context.parameters.require("replacement_id")
        let payload = try await request.decode(as: TextReplacementRequestPayload.self, context: context)
        guard payload.replacement.id == replacementID else {
            throw HTTPError(
                .badRequest,
                message: "Stored text replacement route id '\(replacementID)' did not match body replacement id '\(payload.replacement.id)'."
            )
        }
        return .init(profile: try await host.replaceTextReplacement(try payload.replacement.model(), inStoredTextProfileID: profileID))
    }

    router.delete("text-profiles/active/replacements/:replacement_id") { _, context -> TextProfileResponse in
        let replacementID = try context.parameters.require("replacement_id")
        return .init(profile: try await host.removeTextReplacement(id: replacementID))
    }

    router.delete("text-profiles/stored/:profile_id/replacements/:replacement_id") { _, context -> TextProfileResponse in
        let profileID = try context.parameters.require("profile_id")
        let replacementID = try context.parameters.require("replacement_id")
        return .init(profile: try await host.removeTextReplacement(id: replacementID, fromStoredTextProfileID: profileID))
    }
}
