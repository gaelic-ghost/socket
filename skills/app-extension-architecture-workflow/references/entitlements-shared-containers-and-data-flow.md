# Entitlements, Shared Containers, and Data Flow

Capabilities and entitlements belong to individual targets. Give the containing app and every extension target the minimum privilege required by its own documented contract.

## App Groups

Use an App Group only for a concrete shared-data or documented IPC requirement between apps and supporting processes signed by the same team. Each participant must declare the group entitlement. Prefer `group.` identifiers for cross-platform app groups.

Use the group container for bounded, schema-owned data such as a small handoff record or coordinated file staging. It is not a substitute for the system host’s request APIs, an unrestricted shared database, or a privilege escalation path. On macOS, verify that the participant can access the underlying directory; `containerURL(forSecurityApplicationGroupIdentifier:)` alone does not prove authorization.

## Data Flow Review

For each message, file, or preference, record producer, consumer, storage location, schema version, retention, encryption/protection need, retry behavior, and deletion owner. Keep secrets out of logs and do not duplicate sensitive user data merely to make cross-process access convenient.

## Sources

- [Configuring app groups](https://developer.apple.com/documentation/xcode/configuring-app-groups)
- [Accessing app group containers in your existing macOS app](https://developer.apple.com/documentation/xcode/accessing-app-group-containers)
- [FileManager.containerURL(forSecurityApplicationGroupIdentifier:)](https://developer.apple.com/documentation/foundation/filemanager/containerurl(forsecurityapplicationgroupidentifier:))
