# Workspace Sync Boundaries

The workspace root composes app projects and packages but does not merge their
ownership boundaries. Sync workspace-root guidance here, then use the app and
package sync skills for their own `AGENTS.md` policy.

- `Apps/*/*.xcodeproj`: generated/project-aware app integration.
- `Packages/*/Package.swift`: package target and product graph.
- `Services/*`: independent backend and deployment boundary.
- `.xcworkspace`: Xcode-managed composition surface; do not hand-write it.
