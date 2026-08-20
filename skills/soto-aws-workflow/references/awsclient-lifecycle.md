# Soto AWSClient Lifecycle Patterns

These patterns make ownership visible. Adapt the surrounding server or Lambda
entrypoint to the framework version in the repository; do not move client
creation into a request handler.

## Long-Running Service

The application bootstrap creates one resource owner, injects its service
objects into handlers, and shuts the owner down after the server exits:

```swift
import SotoCore
import SotoS3

final class AWSResources: @unchecked Sendable {
    let client: AWSClient
    let s3: S3

    init() {
        let client = AWSClient()
        self.client = client
        self.s3 = S3(client: client)
    }

    func shutdown() async throws {
        try await client.shutdown()
    }
}

let aws = AWSResources()
defer { try? aws.client.syncShutdown() } // use only in a synchronous owner

// Inject aws.s3 into application services and route handlers.
// The application owner—not those consumers—performs shutdown exactly once.
```

Prefer the asynchronous `shutdown()` path when the framework exposes an async
shutdown hook. The synchronous `defer` form illustrates ownership for a
synchronous process entrypoint; do not use both forms.

## Warm Lambda Environment

Create the client and service objects during Lambda initialization, outside the
per-invocation handler. Attach the one shutdown call to the runtime's environment
shutdown hook:

```swift
struct Handler {
    let client: AWSClient
    let s3: S3

    init() {
        let client = AWSClient()
        self.client = client
        self.s3 = S3(client: client)
    }

    func handle(_ request: Request) async throws -> Response {
        // Warm invocations reuse s3 and its client.
    }

    func shutdown() async throws {
        try await client.shutdown()
    }
}
```

Wire `Handler.init` to the runtime's cold-start initialization and
`Handler.shutdown` to its environment shutdown lifecycle. Never create or shut
down an `AWSClient` inside `handle`.

## Review Checklist

- Exactly one `AWSClient` is created for the application or warm Lambda environment.
- Every Soto service object receives that same client.
- Request handlers and domain adapters do not own shutdown.
- Exactly one application/runtime lifecycle hook calls `shutdown()` or
  `syncShutdown()`.
- Tests replace the first-party domain boundary and do not start LocalStack or a
  container runtime locally.

The ownership rules follow Soto's [AWSClient guide](https://soto.codes/user-guides/awsclient.html),
[service-object guide](https://soto.codes/user-guides/service-objects.html), and
[Lambda lifecycle guide](https://soto.codes/user-guides/using-soto-on-aws-lambda.html).
