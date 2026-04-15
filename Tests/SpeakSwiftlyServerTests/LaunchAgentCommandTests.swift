import Foundation
import Testing
@testable import SpeakSwiftlyServer

// MARK: - Launch Agent Command Tests

@Test func launchAgentPromoteLiveParsesWithoutPreexistingStagedExecutable() throws {
    let repositoryRootURL = try makeLaunchAgentCommandTestRepository()

    let command = try LaunchAgentCommand.parse(
        arguments: ["promote-live"],
        currentDirectoryPath: repositoryRootURL.path,
        currentExecutablePath: "/tmp/SpeakSwiftlyServerTool"
    )

    switch command.action {
    case .promoteLive(let options):
        #expect(options.repositoryRootPath == repositoryRootURL.path)
        #expect(
            options.installOptions.toolExecutablePath
                == repositoryRootURL
                .appendingPathComponent(".release-artifacts/current/SpeakSwiftlyServerTool", isDirectory: false)
                .path
        )

    default:
        Issue.record("Expected `launch-agent promote-live` to parse into the promote-live action.")
    }
}

@Test func launchAgentInstallStillRejectsMissingStagedExecutableByDefault() throws {
    let repositoryRootURL = try makeLaunchAgentCommandTestRepository()

    do {
        _ = try LaunchAgentCommand.parse(
            arguments: ["install"],
            currentDirectoryPath: repositoryRootURL.path,
            currentExecutablePath: "/tmp/SpeakSwiftlyServerTool"
        )
        Issue.record("Expected `launch-agent install` to reject a missing staged executable.")
    } catch let error as LaunchAgentCommandError {
        #expect(error.message.contains("could not find the staged release artifact"))
    }
}

private func makeLaunchAgentCommandTestRepository() throws -> URL {
    let repositoryRootURL = URL(fileURLWithPath: NSTemporaryDirectory())
        .appendingPathComponent(UUID().uuidString, isDirectory: true)
    try FileManager.default.createDirectory(at: repositoryRootURL, withIntermediateDirectories: true)
    try FileManager.default.createDirectory(
        at: repositoryRootURL.appendingPathComponent("Sources/SpeakSwiftlyServerTool", isDirectory: true),
        withIntermediateDirectories: true
    )
    try "import PackageDescription\nlet package = Package(name: \"SpeakSwiftlyServer\")\n"
        .write(
            to: repositoryRootURL.appendingPathComponent("Package.swift", isDirectory: false),
            atomically: true,
            encoding: .utf8
        )
    return repositoryRootURL
}
