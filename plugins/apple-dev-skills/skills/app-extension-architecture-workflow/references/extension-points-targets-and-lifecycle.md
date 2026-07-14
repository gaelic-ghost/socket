# Extension Points, Targets, and Lifecycle

Apple documents an app extension as a separate bundle that runs in a separate process. The host selects when to run it and defines the extension-point API. Start by naming that extension point and host; do not begin from a generic shared-process assumption.

## Target Map

- The containing app owns onboarding, user-facing settings, durable app UI, and app-only capabilities.
- Each extension target owns one extension-point entry and its short, host-driven work.
- Shared code is a narrow library or package for pure domain rules and typed data that both targets truly need. It must not provide an implicit lifecycle bridge.

## Lifecycle Questions

Before implementation, answer where activation originates, whether the host may terminate or restart the extension, what is safe to retry, how cancellation reaches in-flight work, and whether the containing app can be absent. Treat every answer as extension-point specific.

For app extensions built with `ExtensionFoundation`, Apple documents host-to-extension process startup and XPC as explicit APIs. That does not authorize substituting a custom XPC layer for a system extension point that supplies a different contract.

## Sources

- [Adding support for app extensions to your app](https://developer.apple.com/documentation/extensionfoundation/adding-support-for-app-extensions-to-your-app)
- [Building an app extension to support a host app](https://developer.apple.com/documentation/extensionfoundation/building-an-app-extension-to-support-a-host-app)
- [Discovering app extensions from your app](https://developer.apple.com/documentation/extensionfoundation/discovering-app-extensions-from-your-app)
