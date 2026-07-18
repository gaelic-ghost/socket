# Package Plugins: Build, Command, and Xcode

## Choose the capability

- Use a build tool plugin for work that belongs in the build graph, especially generated source. Prefer a build command when inputs and outputs are predictable; reserve a prebuild command for outputs whose names cannot be known until execution.
- Use a command plugin for an explicit user action unrelated to every build, such as formatting, documentation generation, or project maintenance.
- Declare a plugin product only when direct dependent packages should discover and use the plugin. A package-local plugin target does not need a public plugin product.
- Attach a build tool plugin to each consuming target through target plugin usage. Command plugins operate at package scope and are invoked explicitly.

## Keep the implementation narrow

- Put plugin entry points under `Plugins/<PluginName>/` unless an intentional manifest path overrides the convention.
- Depend on executable targets, executable products, or supported binary tools. The plugin constructs commands; the executable tool performs substantial work.
- Keep plugin code limited to package-model inspection, argument formation, command declaration, and diagnostics.

## Xcode context

SwiftPM's `PackagePlugin` API can receive IDE-provided context, and supported command plugins can participate in Xcode package/project workflows. Treat that as a separate host path: verify the selected Xcode version and inspect behavior in the real workspace before claiming parity with `swift package plugin`.

## Sources

- [SwiftPM Plugins](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/plugins/)
- [Writing a build tool plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/writingbuildtoolplugin/)
- [Writing a command plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/writingcommandplugin/)
- [SE-0303: Package Manager Extensible Build Tools](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0303-swiftpm-extensible-build-tools.md)
- [SE-0332: Package Manager Command Plugins](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0332-swiftpm-command-plugins.md)
