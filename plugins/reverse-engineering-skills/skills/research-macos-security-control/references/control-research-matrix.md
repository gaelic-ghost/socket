# macOS Security Control Research Matrix

| Control family | Public contract first | Private/exact-build evidence | Common confusion |
| --- | --- | --- | --- |
| TCC/privacy | Framework status/request APIs, System Settings, PPPC | TCC frameworks/services, attribution chains, private constants, schemas, logs | Usage description or entitlement is not consent; reset is not grant |
| App Sandbox/files | Container, documented entitlements, user selection, bookmarks | Seatbelt profiles/extensions, sandboxd/log behavior | Bookmark/path is not blanket access; TCC and mandatory controls remain |
| Entitlements/capabilities | Apple entitlement docs, account/profile rules | Private keys, platform-binary context, service checks | Signed declaration is not runtime authorization |
| Execution/distribution | Quarantine/provenance, signing, notarization, Gatekeeper, `syspolicy_check`/assessment docs | ExecutionPolicy/system-policy services, rule/evaluation internals | Gatekeeper, Hardened Runtime, Developer Tools, and malware response are distinct |
| Malware protection | Apple Platform Security, XProtect/update/Endpoint Security documentation | XProtect artifacts/config, remediation services, exact events/logs | Detection/block/remediation evidence does not alone prove execution or compromise |
| System integrity | SIP, signed system volume, recovery/boot security, system extensions | platform-binary policy, Data Vault enforcement, boot/service internals | Root/admin does not bypass mandatory controls |

Also record cross-cutting identity (path, signer, Team ID, designated requirement, parent/helper), hardware/architecture, security-data version, management state, and artifact transformations. Use `syspolicy_check distribution` only for its documented assessment purpose and record tool output/version; do not conflate its combined checks into one root cause.
