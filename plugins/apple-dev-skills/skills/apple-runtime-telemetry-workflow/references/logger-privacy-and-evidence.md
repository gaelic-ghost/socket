# Logger Privacy and Evidence

Apple's local OS documentation checked through Xcode DocumentationSearch on 2026-07-12 says unified logging is a performant system-wide facility for debugging and performance analysis. It is visible through Console, the `log` command, Xcode's debug console, and selected OSLog APIs.

`Logger` accepts subsystem and category values. Use the subsystem for a broad app area and the category for the specific feature or operation so capture can filter unrelated events. Interpolated strings and custom objects are redacted by default. Treat this as the correct default; make a value public only after deliberate data classification.

`OSLogStore.local()` is not an ordinary in-app log-reader fallback: Apple documents an admin-account and `com.apple.logging.local-store` entitlement requirement.

Sources read through Xcode-local documentation:

- `doc://com.apple.documentation/documentation/os/logging`
- `doc://com.apple.documentation/documentation/os/Logger`
- `doc://com.apple.documentation/documentation/os/viewing-log-messages`
- `doc://com.apple.documentation/documentation/OSLog/OSLogStore/local()`
