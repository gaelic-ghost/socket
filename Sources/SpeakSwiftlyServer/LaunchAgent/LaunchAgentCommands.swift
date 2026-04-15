import Foundation

let speakSwiftlyServerToolName = "SpeakSwiftlyServerTool"

// MARK: - Serve Options

public struct ServeOptions: Sendable {
    let runtimeProfileRootPath: String?

    static func parse(arguments: [String], currentDirectoryPath: String) throws -> ServeOptions {
        var runtimeProfileRootPath: String?
        var index = 0

        while index < arguments.count {
            switch arguments[index] {
            case "--profile-root":
                runtimeProfileRootPath = try LaunchAgentOptions.requireValue(
                    after: arguments,
                    index: index,
                    option: "--profile-root"
                )
                index += 2

            default:
                throw SpeakSwiftlyServerToolCommandError(
                    "\(speakSwiftlyServerToolName) did not recognize serve option '\(arguments[index])'. Run `\(speakSwiftlyServerToolName) help` for supported flags."
                )
            }
        }

        return .init(
            runtimeProfileRootPath: runtimeProfileRootPath.map {
                LaunchAgentOptions.resolvePath($0, relativeTo: currentDirectoryPath)
            }
        )
    }
}

// MARK: - CLI Command

/// Top-level parsed command for the `SpeakSwiftlyServerTool` executable.
public enum SpeakSwiftlyServerToolCommand {
    case serve(ServeOptions)
    case launchAgent(LaunchAgentCommand)

    // MARK: - Parsing

    /// Parses command-line arguments into the tool's top-level command model.
    public static func parse(
        arguments: [String],
        currentDirectoryPath: String = FileManager.default.currentDirectoryPath,
        currentExecutablePath: String = CommandLine.arguments[0]
    ) throws -> SpeakSwiftlyServerToolCommand {
        guard let first = arguments.first else {
            return .serve(.init(runtimeProfileRootPath: nil))
        }

        switch first {
        case "serve":
            return .serve(
                try ServeOptions.parse(
                    arguments: Array(arguments.dropFirst()),
                    currentDirectoryPath: currentDirectoryPath
                )
            )

        case "launch-agent":
            return .launchAgent(
                try LaunchAgentCommand.parse(
                    arguments: Array(arguments.dropFirst()),
                    currentDirectoryPath: currentDirectoryPath,
                    currentExecutablePath: currentExecutablePath
                )
            )

        case "-h", "--help", "help":
            throw SpeakSwiftlyServerToolCommandError(helpText)

        default:
            if first.hasPrefix("-") {
                return .serve(
                    try ServeOptions.parse(
                        arguments: arguments,
                        currentDirectoryPath: currentDirectoryPath
                    )
                )
            }
            throw SpeakSwiftlyServerToolCommandError(
                "\(speakSwiftlyServerToolName) did not recognize command '\(first)'. Supported commands are `serve` and `launch-agent`."
            )
        }
    }

    // MARK: - Running

    /// Runs the parsed command against the standalone runtime or LaunchAgent workflow.
    public func run() async throws {
        switch self {
        case .serve(let options):
            try await ServerRuntimeEntrypoint.run(
                options: .init(runtimeProfileRootPath: options.runtimeProfileRootPath)
            )

        case .launchAgent(let command):
            try command.run()
        }
    }

    // MARK: - Help

    static let helpText = """
    Usage:
      \(speakSwiftlyServerToolName) serve
      \(speakSwiftlyServerToolName) launch-agent print-plist [options]
      \(speakSwiftlyServerToolName) launch-agent install [options]
      \(speakSwiftlyServerToolName) launch-agent promote-live [options]
      \(speakSwiftlyServerToolName) launch-agent uninstall [options]
      \(speakSwiftlyServerToolName) launch-agent status [options]

    Launch-agent options:
      --label <label>
      --tool-executable-path <path>
      --plist-path <path>
      --config-file <path>
      --reload-interval-seconds <seconds>
      --working-directory <path>
      --profile-root <path>
      --stdout-path <path>
      --stderr-path <path>

    Serve options:
      --profile-root <path>

      Without arguments, \(speakSwiftlyServerToolName) defaults to `serve`.
    """
}

/// Human-friendly parse or usage error for the top-level executable command surface.
public struct SpeakSwiftlyServerToolCommandError: Error, CustomStringConvertible {
    public let message: String

    public init(_ message: String) {
        self.message = message
    }

    public var description: String { message }
}

// MARK: - Launch Agent Command

/// Parsed subcommand for LaunchAgent install, uninstall, status, and property-list rendering.
public struct LaunchAgentCommand {
    enum Action {
        case printPlist(LaunchAgentOptions)
        case install(LaunchAgentOptions)
        case promoteLive(LaunchAgentPromoteOptions)
        case uninstall(LaunchAgentStatusOptions)
        case status(LaunchAgentStatusOptions)
    }

    let action: Action

    // MARK: - Parsing

    /// Parses the `launch-agent` subcommand surface.
    static func parse(arguments: [String], currentDirectoryPath: String, currentExecutablePath: String) throws -> LaunchAgentCommand {
        guard let subcommand = arguments.first else {
            throw LaunchAgentCommandError(
                "The `launch-agent` command requires a subcommand. Supported subcommands are `print-plist`, `install`, `promote-live`, `uninstall`, and `status`."
            )
        }

        switch subcommand {
        case "print-plist":
            return .init(action: .printPlist(try LaunchAgentOptions.parse(arguments: Array(arguments.dropFirst()), currentDirectoryPath: currentDirectoryPath, currentExecutablePath: currentExecutablePath)))

        case "install":
            return .init(action: .install(try LaunchAgentOptions.parse(arguments: Array(arguments.dropFirst()), currentDirectoryPath: currentDirectoryPath, currentExecutablePath: currentExecutablePath)))

        case "promote-live":
            return .init(action: .promoteLive(try LaunchAgentPromoteOptions.parse(
                arguments: Array(arguments.dropFirst()),
                currentDirectoryPath: currentDirectoryPath,
                currentExecutablePath: currentExecutablePath
            )))

        case "uninstall":
            return .init(action: .uninstall(try LaunchAgentStatusOptions.parse(arguments: Array(arguments.dropFirst()), currentDirectoryPath: currentDirectoryPath)))

        case "status":
            return .init(action: .status(try LaunchAgentStatusOptions.parse(arguments: Array(arguments.dropFirst()), currentDirectoryPath: currentDirectoryPath)))

        case "-h", "--help", "help":
            throw LaunchAgentCommandError(SpeakSwiftlyServerToolCommand.helpText)

        default:
            throw LaunchAgentCommandError(
                "\(speakSwiftlyServerToolName) did not recognize launch-agent subcommand '\(subcommand)'. Supported subcommands are `print-plist`, `install`, `promote-live`, `uninstall`, and `status`."
            )
        }
    }

    // MARK: - Running

    /// Executes the requested LaunchAgent management action.
    func run() throws {
        switch action {
        case .printPlist(let options):
            let data = try options.propertyListData()
            guard let xml = String(data: data, encoding: .utf8) else {
                throw LaunchAgentCommandError(
                    "\(speakSwiftlyServerToolName) rendered a LaunchAgent property list, but it could not be decoded back into UTF-8 text for printing."
                )
            }
            print(xml, terminator: "")

        case .install(let options):
            try options.install()

        case .promoteLive(let options):
            try options.promoteLive()

        case .uninstall(let options):
            try options.uninstall()

        case .status(let options):
            print(try options.statusSummary())
        }
    }
}

/// Human-friendly parse or execution error for the LaunchAgent command surface.
public struct LaunchAgentCommandError: Error, CustomStringConvertible {
    public let message: String

    public init(_ message: String) {
        self.message = message
    }

    public var description: String { message }
}
