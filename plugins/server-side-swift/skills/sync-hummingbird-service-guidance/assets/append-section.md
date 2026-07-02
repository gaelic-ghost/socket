<!-- BEGIN SOCKET HUMMINGBIRD GUIDANCE -->
## Socket Hummingbird Guidance

- Use `server-side-swift:sync-hummingbird-service-guidance` when this repository's Hummingbird guidance needs to be refreshed.
- Fresh Hummingbird services start with `server-side-swift:bootstrap-hummingbird-service` and the official `hb` CLI. Do not copy a fresh template over this existing repository without explicit approval.
- Preserve this repo's current Server, Lambda, or dual-adapter shape unless Gale explicitly asks for a migration.
- Keep Swift Package Manager as the source of truth for package structure, dependencies, builds, tests, and run commands.
- Preserve Hummingbird's generated `swift-configuration` support when it fits the repo.
- For `hb`-generated Lambda apps, keep `hummingbird-lambda` as the Lambda adapter. When OpenAPI is selected, keep `OpenAPIHummingbird` as the transport that registers generated handlers on the Hummingbird router.
- Treat `swift-openapi-lambda` as a separate valid OpenAPI Lambda transport, not as the default transport for current Hummingbird templates.
- Prefer `swift build` and `swift test` for baseline validation. Use `hb watch` only for local rebuild-and-run development in long-running Server apps.
<!-- END SOCKET HUMMINGBIRD GUIDANCE -->
