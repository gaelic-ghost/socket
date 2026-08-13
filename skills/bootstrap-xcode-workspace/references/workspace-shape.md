# Apple Product Workspace Shape

One Apple product repository has one root workspace and one root XcodeGen
project. The workspace is the stable opening and `xcodebuild` surface; the root
XcodeGen spec is the project source of truth.

| Surface | Owns |
| --- | --- |
| `.xcworkspace` | the root generated project entry point |
| `project.yml` | project graph, shared configurations, includes |
| `Apps/apps-shared.yml` | reusable app/test target and scheme templates |
| `Apps/<Target>/target.yml` | one target's source roots, platform, and dependencies |
| `Packages/packages-shared.yml` | local package registration with XcodeGen |
| `Package.swift` | each package's products, targets, dependencies, and tests |
| `.xcconfig` hierarchy | project, app-shared, and target/configuration build settings |

Use local package products for shared code. Do not use a second Xcode project,
groups, or folder references as a module boundary.
