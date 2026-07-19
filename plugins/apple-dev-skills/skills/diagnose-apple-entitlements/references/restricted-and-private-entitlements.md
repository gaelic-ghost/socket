# Restricted And Private Entitlements

## Classification

- **Public**: documented for third-party use with published value/platform constraints.
- **Restricted**: documented but requires an Apple approval, request, agreement, or account authorization beyond adding a key.
- **Private or undocumented**: observed in Apple/system artifacts or private interfaces without a supported third-party contract.
- **Development-only**: enables debugger/development behavior and is inappropriate or absent in distribution.
- **Environment-specific**: value binds development/production service state, team, container, or another environment.
- **Exception**: narrowly relaxes App Sandbox or Hardened Runtime behavior; never a general bypass.

## Decision rules

Verify the exact key, value type, platform/OS availability, required capability/approval, and provisioning support through current Apple documentation and the selected SDK. Do not infer availability from a symbol/string in another binary or from build success.

For restricted entitlements, route the account request to `apple-developer-provisioning-workflow` and preserve the response/profile evidence. Adding an unapproved key does not create authorization.

For private or undocumented entitlements, do not recommend them for an ordinary third-party product. Route legitimate exact-build research to `research-macos-security-control`, and distinguish Apple/platform-binary context from third-party feasibility.

App Sandbox exceptions and Hardened Runtime exceptions govern different systems. Name the specific restriction being relaxed, use the narrowest documented exception, inspect the final signature, and validate the runtime operation.
