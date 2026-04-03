import Foundation
import Hummingbird

// MARK: - Entry Point

@main
enum SpeakSwiftlyServer {
    static func main() async throws {
        let configuration = try ServerConfiguration.load()
        let state = await ServerState.live(configuration: configuration)
        let app = makeApplication(configuration: configuration, state: state)
        defer {
            Task {
                await state.shutdown()
            }
        }
        try await app.runService()
    }
}
