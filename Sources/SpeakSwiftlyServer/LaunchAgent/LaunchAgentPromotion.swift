import Foundation

struct LaunchAgentPromoteOptions {
    let installOptions: LaunchAgentOptions
    let repositoryRootPath: String

    static func parse(
        arguments: [String],
        currentDirectoryPath: String,
        currentExecutablePath: String,
    ) throws -> LaunchAgentPromoteOptions {
        let repositoryRootPath = try LaunchAgentOptions.resolveRepositoryRoot(startingAt: currentDirectoryPath)
        let installOptions = try LaunchAgentOptions.parse(
            arguments: arguments,
            currentDirectoryPath: currentDirectoryPath,
            currentExecutablePath: currentExecutablePath,
            requireToolExecutableExists: false,
        )
        return .init(
            installOptions: installOptions,
            repositoryRootPath: repositoryRootPath,
        )
    }

    func promoteLive() throws {
        let stagingResult = try ReleaseArtifactPromoter.promoteLive(
            repositoryRootPath: repositoryRootPath,
            stagedExecutablePath: installOptions.toolExecutablePath,
        )

        print(
            """
            Promoted the live staged release artifact from '\(stagingResult.builtExecutablePath)' to '\(stagingResult.stagedExecutablePath)'.
            Refreshed staged metallib at '\(stagingResult.stagedMetallibPath)'.
            Refreshed staged code signature for '\(stagingResult.stagedExecutablePath)'.
            """,
        )

        let refreshedInstallOptions = try LaunchAgentOptions(
            label: installOptions.label,
            toolExecutablePath: installOptions.toolExecutablePath,
            plistPath: installOptions.plistPath,
            configFilePath: installOptions.configFilePath,
            reloadIntervalSeconds: installOptions.reloadIntervalSeconds,
            workingDirectory: installOptions.workingDirectory,
            profileRootPath: installOptions.profileRootPath,
            standardOutPath: installOptions.standardOutPath,
            standardErrorPath: installOptions.standardErrorPath,
            launchctlPath: installOptions.launchctlPath,
            userDomain: installOptions.userDomain,
        )
        try refreshedInstallOptions.install()
    }
}

private struct ReleaseArtifactPromotionResult {
    let builtExecutablePath: String
    let stagedExecutablePath: String
    let stagedMetallibPath: String
}

private enum ReleaseArtifactPromoter {
    static func promoteLive(
        repositoryRootPath: String,
        stagedExecutablePath: String,
    ) throws -> ReleaseArtifactPromotionResult {
        try buildReleaseTool(repositoryRootPath: repositoryRootPath)

        let builtExecutablePath = try builtReleaseExecutablePath(repositoryRootPath: repositoryRootPath)
        let builtMetallibURL = try builtReleaseMetallibURL(
            productsURL: URL(fileURLWithPath: builtExecutablePath, isDirectory: false)
                .deletingLastPathComponent(),
        )
        let stagedExecutableURL = URL(fileURLWithPath: stagedExecutablePath, isDirectory: false)
        let stagedDirectoryURL = stagedExecutableURL.deletingLastPathComponent()
        let stagedMetallibURL = stagedDirectoryURL
            .appendingPathComponent("Resources", isDirectory: true)
            .appendingPathComponent("default.metallib", isDirectory: false)

        try FileManager.default.createDirectory(at: stagedDirectoryURL, withIntermediateDirectories: true)
        try replaceItem(
            at: stagedExecutableURL,
            with: URL(fileURLWithPath: builtExecutablePath, isDirectory: false),
            permissions: 0o755,
        )
        try FileManager.default.createDirectory(
            at: stagedMetallibURL.deletingLastPathComponent(),
            withIntermediateDirectories: true,
        )
        try replaceItem(
            at: stagedMetallibURL,
            with: builtMetallibURL,
        )
        try refreshAdHocSignature(for: stagedExecutableURL)

        return .init(
            builtExecutablePath: builtExecutablePath,
            stagedExecutablePath: stagedExecutableURL.path,
            stagedMetallibPath: stagedMetallibURL.path,
        )
    }

    private static func buildReleaseTool(repositoryRootPath: String) throws {
        _ = try runProcess(
            executablePath: "/usr/bin/xcrun",
            arguments: ["swift", "build", "-c", "release", "--product", speakSwiftlyServerToolName],
            currentDirectoryPath: repositoryRootPath,
            failureSummary: "\(speakSwiftlyServerToolName) could not build the release executable from repository root '\(repositoryRootPath)'.",
        )
    }

    private static func builtReleaseExecutablePath(repositoryRootPath: String) throws -> String {
        let showBinPathResult = try runProcess(
            executablePath: "/usr/bin/xcrun",
            arguments: ["swift", "build", "-c", "release", "--show-bin-path"],
            currentDirectoryPath: repositoryRootPath,
            failureSummary: "\(speakSwiftlyServerToolName) could not determine the SwiftPM release bin path from repository root '\(repositoryRootPath)'.",
        )
        let binPath = showBinPathResult.standardOutput
        guard binPath.isEmpty == false else {
            throw LaunchAgentCommandError(
                "\(speakSwiftlyServerToolName) asked SwiftPM for the release bin path, but SwiftPM returned an empty path.",
            )
        }

        let executablePath = URL(fileURLWithPath: binPath, isDirectory: true)
            .appendingPathComponent(speakSwiftlyServerToolName, isDirectory: false)
            .path
        guard FileManager.default.isExecutableFile(atPath: executablePath) else {
            throw LaunchAgentCommandError(
                "\(speakSwiftlyServerToolName) completed a release build, but the expected executable '\(executablePath)' was missing or not executable.",
            )
        }

        return executablePath
    }

    private static func builtReleaseMetallibURL(productsURL: URL) throws -> URL {
        let candidates = [
            productsURL.appendingPathComponent(
                "SpeakSwiftly_SpeakSwiftly.bundle/mlx-swift_Cmlx.bundle/Contents/Resources/default.metallib",
                isDirectory: false,
            ),
            productsURL.appendingPathComponent(
                "SpeakSwiftly_SpeakSwiftlyCore.bundle/mlx-swift_Cmlx.bundle/Contents/Resources/default.metallib",
                isDirectory: false,
            ),
            productsURL.appendingPathComponent("Resources/default.metallib", isDirectory: false),
        ]

        if let metallibURL = candidates.first(where: { FileManager.default.fileExists(atPath: $0.path) }) {
            return metallibURL
        }

        throw LaunchAgentCommandError(
            "\(speakSwiftlyServerToolName) completed a release build, but no SpeakSwiftly MLX metallib was found in SwiftPM product directory '\(productsURL.path)'. Expected the SpeakSwiftly package dependency to bundle mlx-swift_Cmlx.bundle in the release build products.",
        )
    }

    private static func replaceItem(
        at destinationURL: URL,
        with sourceURL: URL,
        permissions: NSNumber? = nil,
    ) throws {
        if FileManager.default.fileExists(atPath: destinationURL.path) {
            try FileManager.default.removeItem(at: destinationURL)
        }
        try FileManager.default.copyItem(at: sourceURL, to: destinationURL)
        if let permissions {
            try FileManager.default.setAttributes([.posixPermissions: permissions], ofItemAtPath: destinationURL.path)
        }
    }

    private static func refreshAdHocSignature(for executableURL: URL) throws {
        _ = try runProcess(
            executablePath: "/usr/bin/codesign",
            arguments: ["--force", "--sign", "-", executableURL.path],
            failureSummary: "\(speakSwiftlyServerToolName) could not refresh the staged ad-hoc code signature for '\(executableURL.path)'.",
        )
    }
}
