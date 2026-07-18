# Generated Source and Build Products

## Decision

- Check in source when it is authored, reviewed, or required by consumers that cannot run the generator.
- Generate during the build when output is mechanical, deterministic, tied to declared inputs, and needed by the compiling target.
- Use an explicit command plugin when generation is an intentional maintenance action rather than a prerequisite for every build.
- Skip a plugin when a small checked-in script or ordinary build setting solves the job without a reusable package extension.

## Reliability

- Prefer build commands with declared inputs and outputs over prebuild commands.
- Keep generated output out of source directories unless an explicitly invoked command plugin is meant to update checked-in source.
- Pin or otherwise record the generator version and include configuration files among the declared inputs.
- Ensure clean and incremental builds produce equivalent results.
- Never hand-edit derived output as the only fix; correct the generator or its inputs.

## Sources

- [Writing a build tool plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/writingbuildtoolplugin/)
- [PackagePlugin](https://docs.swift.org/swiftpm/documentation/packageplugin/)
