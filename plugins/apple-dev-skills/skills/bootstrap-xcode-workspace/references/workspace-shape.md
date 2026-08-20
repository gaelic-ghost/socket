# Apple Product Workspace Shape

One Apple product repository has one root workspace and one root XcodeGen
project. The workspace is the stable opening and `xcodebuild` surface; the root
XcodeGen spec is the project source of truth.

| Surface | Owns |
| --- | --- |
| `.xcworkspace` | the root generated project entry point |
| `project.yml` | project graph, shared configurations, includes |
| `Apps/apps-shared.yml` | reusable app/test target and scheme templates |
| `Apps/<Target>/target.yml` | one application, extension, or test target's source roots, platform, and dependencies |
| `Packages/packages-shared.yml` | local package registration with XcodeGen |
| `Services/services-shared.yml` | deployable service-package registration with XcodeGen |
| `Package.swift` | each package's products, targets, dependencies, and tests |
| `.xcconfig` hierarchy | project, app-shared, and target/configuration build settings |
| `AGENTS.md` / `CONTRIBUTING.md` | managed header plus preserved repository-specific guidance |
| `Justfile` | setup, alignment, validation, test, and distribution command surface |

Use local package products for shared code and `Services/` SwiftPM executables
for deployable backends. Do not use a second Xcode project, groups, or folder
references as a module boundary. Do not classify the repository as Xcode,
SwiftPM, plain, or mixed; route each operation to the nearest package or root
workspace as appropriate. `just align` is the one
managed-guidance sync surface; it refreshes marked sections from Socket and
regenerates Xcode output.

App extensions live at `Apps/<ExtensionTarget>/`, adjacent to their containing
app and tests. The containing app's XcodeGen target dependency must name the
extension and set `embed: true`; a root `Extensions/` directory, separate
extension project, or name-derived host relationship is not canonical.

Existing repositories enter through a read-only `adopt` inventory and an
explicit reviewed component map. Application only stages canonical sources and
a candidate generated project under `.socket/`; it preserves original project
state until equivalence has been reviewed and final removal is explicitly
authorized.
