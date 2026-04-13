# Dash Swift Package Shortlist

Use this shortlist when the request is about a Swift package, Swift server package, Swift tooling package, or Apple-adjacent DocC package docs and local Dash coverage would help.

## How To Read This List

- Prefer the Dash docset display name, not a cached identifier, as the stable human-facing locator.
- Resolve the current machine-local Dash identifier at runtime with `list_installed_docsets` before calling `search_documentation` or `enable_docset_fts`.
- Most DocC package docsets in Dash currently appear with a display name shaped like `<owner>/<repo> main`.
- Treat this list as a high-value shortlist, not an exhaustive Swift package catalog.

## High-Value Package Docsets

- `swiftlang/swift-testing main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: Swift Testing APIs, traits, issue recording, parameterized tests, and test-organization questions.
  - Upstream: <https://github.com/swiftlang/swift-testing>

- `ml-explore/mlx-swift main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: MLX Swift core tensor, array, model, and runtime APIs.
  - Upstream: <https://github.com/ml-explore/mlx-swift>

- `ml-explore/mlx-swift-lm main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: MLX language-model helpers, inference flows, and package-specific LM utilities.
  - Upstream: <https://github.com/ml-explore/mlx-swift-examples/tree/main/Libraries/MLXLMCommon>

- `huggingface/swift-transformers main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: Hugging Face Swift model-loading, generation, and tokenizer integration surfaces.
  - Upstream: <https://github.com/huggingface/swift-transformers>

- `apple/swift-log main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: structured logging APIs, `Logger`, log-level handling, and backend integration.
  - Upstream: <https://github.com/apple/swift-log>

- `apple/swift-crypto main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: hashing, signatures, keys, and CryptoKit-compatible package APIs outside Apple-only SDK docs.
  - Upstream: <https://github.com/apple/swift-crypto>

- `apple/swift-collections main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: `Deque`, `OrderedSet`, `OrderedDictionary`, `Heap`, bit collections, and related package APIs.
  - Upstream: <https://github.com/apple/swift-collections>

- `apple/swift-nio main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: event loops, channels, buffers, HTTP primitives, and Swift server networking surfaces.
  - Upstream: <https://github.com/apple/swift-nio>

- `apple/swift-protobuf main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: generated protobuf message APIs, coding surfaces, and runtime behavior in Swift.
  - Upstream: <https://github.com/apple/swift-protobuf>

- `swift-otel/swift-otel main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: OpenTelemetry tracing, metrics, and telemetry-integration questions in Swift packages.
  - Upstream: <https://github.com/swift-otel/swift-otel>

- `swiftlang/swift-markdown main`
  - Dash location: installed DocC docset shown under that display name.
  - Use for: Markdown parsing, syntax trees, visitors, and rendering-oriented package behavior.
  - Upstream: <https://github.com/swiftlang/swift-markdown>

## Other Frequently Useful Swift Package Docsets

These are often worth checking too when installed, even though they are outside the shorter default package shortlist:

- `apple/swift-argument-parser main`
- `apple/swift-async-algorithms main`
- `apple/swift-system main`
- `apple/swift-atomics main`
- `apple/swift-service-context main`
- `pointfreeco/swift-snapshot-testing main`

Resolve them the same way: confirm the installed display name with `list_installed_docsets`, then use the returned identifier for search or FTS actions.
