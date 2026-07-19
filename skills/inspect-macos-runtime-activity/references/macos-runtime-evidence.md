# macOS Runtime Evidence

| Source | Useful evidence | Boundary |
| --- | --- | --- |
| `ps`, Activity Monitor, process inspection | identity, ancestry, arguments, user, runtime state | short-lived processes may disappear |
| `lsof`, filesystem metadata | open/mapped files and sockets | permission and timing dependent |
| `nettop`, packet/DNS tools | process traffic and endpoints | encrypted content and capture privileges limit visibility |
| unified logging | subsystem events and timelines | privacy redaction, retention, and predicates affect coverage |
| `eslogger` / Endpoint Security client | process, file, Gatekeeper bypass, XProtect events on supported builds | event type, entitlement, root/FDA, and client configuration matter |
| TCC/system settings | declared or granted privacy access | grant presence does not prove use |

Record failed commands and missing permissions. Do not silently substitute missing telemetry with assumptions.

Record the exact collecting executable, permission class, approval state, event subscription, time window, filter, retention, and privacy redaction. If collection needs a supported privacy decision, hand implementation to `apple-dev-skills:macos-privacy-permissions-workflow`; do not treat granting a broad terminal or agent host as equivalent to authorizing a narrow collector.
