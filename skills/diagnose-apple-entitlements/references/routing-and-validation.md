# Routing And Validation

| First mismatch | Owner | Required validation |
| --- | --- | --- |
| Desired behavior is unsupported or documentation differs | Product/design plus `explore-apple-swift-docs` | Current documented alternative or explicit unsupported state |
| Tracked capability, entitlement, Info.plist, target, or build setting | Xcode project/build workflow | Rebuilt intended configuration and inspected artifact |
| App ID, restricted approval, certificate, or profile | `apple-developer-provisioning-workflow` | Regenerated/refreshed profile plus rebuilt artifact |
| Signed main/nested code differs from source/profile | Xcode build/export or `macos-distribution-workflow` | Exact nested signatures and entitlements after clean export |
| Privacy consent or managed policy | `macos-privacy-permissions-workflow` | Public status/decision plus actual operation |
| Sandbox file authorization | `macos-sandbox-file-access-workflow` | Selection/bookmark/process-boundary result |
| Gatekeeper, notarization, Hardened Runtime, library validation | `macos-distribution-workflow` | Exported artifact assessment/runtime result |
| Private enforcement, platform-binary, SIP/Data Vault, unexplained exact-build policy | Reverse Engineering | Exact-build technical note with observation/inference split |

After correction, repeat all five states. A local build passing is not customer/distribution proof; an entitlement appearing in a signature is not runtime proof. Report the narrow validated environment and any other distribution, device, OS, helper, or account state that remains untested.
