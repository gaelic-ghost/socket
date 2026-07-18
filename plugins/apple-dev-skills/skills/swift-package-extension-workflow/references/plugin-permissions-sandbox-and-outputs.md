# Plugin Permissions, Sandbox, and Outputs

## Permission model

- Expect plugins to run in a sandbox on supported hosts.
- Build tool plugins write generated files to plugin-controlled build output directories; they cannot modify package source.
- Command plugins may declare package-directory write or network permissions. Give each permission a concrete, user-readable reason.
- At invocation, grant only the required scope: package directory, a specific additional directory, or the narrowest network scope supported by the active toolchain.
- Treat `--disable-sandbox` as an exceptional diagnostic step that requires explicit justification, never the normal run command.

## Output discipline

- Make generation deterministic for identical inputs, tool versions, trait selection, and environment.
- Declare predictable input and output paths so the build graph can skip unchanged work.
- For prebuild commands, keep an internal cache because they are evaluated before every build.
- Keep diagnostics actionable: name the plugin, target, input, expected output, and likely remedy.
- In CI, record the toolchain identity and permission flags rather than relying on a prior interactive grant.

## Sources

- [SwiftPM Plugins](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/plugins/)
- [PluginPermission](https://docs.swift.org/swiftpm/documentation/packagedescription/pluginpermission/)
- [swift package plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/packageplugin/)
