# Sandbox And Filesystem Control Map

Evaluate controls in order and preserve the exact error at each boundary.

| Layer | Question | Typical evidence | Correct owner |
| --- | --- | --- | --- |
| Resource identity | Does the URL still identify the intended file after move, rename, symlink, alias, volume remount, or replacement? | Standardized/resolved URL, resource identifiers, volume identity | App data model |
| POSIX and ACL | Does the process identity have discretionary access? | `stat`, `ls -le`, ownership/mode/ACL, exact `errno` | File owner/admin/user |
| App container | Does a container-relative location satisfy the feature? | Container path, bundle identity, sandbox container | App architecture |
| App Sandbox | Does the signed process have a static entitlement or current sandbox extension? | Final signed entitlements, process boundary, selection event, sandbox-denial log | Apple Dev workflow |
| Security-scoped bookmark | Was durable authorization created, stored, resolved, checked for staleness, and activated? | Bookmark lifecycle and Foundation errors | Apple Dev workflow |
| TCC | Is the location separately protected by Files and Folders or Full Disk Access? | Responsible code, public/Settings state, operation result | Privacy workflow |
| Mount/volume | Is the volume present, writable, unlocked, and compatible with the requested semantics? | Mount flags, filesystem, availability/eject state | App/OS/storage |
| Coordination/service | Does another process or service own coordinated access? | `NSFileCoordinator`/presenter or service error | Framework owner |
| Data Vault/SIP/mandatory policy | Is a mandatory system policy denying the operation despite root or discretionary permission? | Exact OS build, path class, logs, SIP/system state | Public docs or exact-build research |

Static sandbox entitlements include the app container, documented standard-folder exceptions, App Groups, and user-selected access classes. A user interaction can issue a temporary sandbox extension; a security-scoped bookmark preserves supported authorization for later resolution. Neither is a universal filesystem capability.

Downloads/media-folder entitlements are version- and distribution-sensitive. Verify the current [App Sandbox entitlement documentation](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.app-sandbox) and final signature before recommending one.
