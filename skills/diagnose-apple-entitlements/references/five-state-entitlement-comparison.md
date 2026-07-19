# Five-State Entitlement Comparison

| State | Capture | Proves | Does not prove |
| --- | --- | --- | --- |
| 1. Desired behavior | Operation/target, platform and OS, distribution, current Apple requirement, exact error | The capability being investigated | Project or account configuration |
| 2. Tracked source | Xcode capability, `.entitlements`, Info.plist, build settings, target membership, generated-project source, helper/extension config | What the repository intends for a configuration | Profile authorization or final signature |
| 3. Account authorization | Team/App ID capability, approval, certificate, profile entitlements, environment/device scope | What Apple/account/profile authorizes for that identity | What the build actually signed or runtime allows |
| 4. Signed result | Main and nested executable entitlements, code requirements, signer/Team ID, embedded profile, Hardened Runtime/signing flags | What the exact artifact declares | User consent, service authorization, or successful access |
| 5. Runtime result | Responsible process, sandbox/TCC/service/system policy, exact error/log, operation result | What this artifact did in this environment | Portable behavior on another build/artifact |

Compare exact values as well as key presence. Record Debug/Release/archive/export, development/distribution/ad hoc signing, original/re-signed state, and every nested target independently. Classify a mismatch at the first state where expected and observed evidence diverge.

Keep usage descriptions separate: they explain a privacy request but are not entitlements. Keep Xcode capabilities separate: they may coordinate project and account configuration but are not themselves the final signed value.
