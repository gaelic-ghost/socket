# Package Traits and Feature Flags

## Design rules

- Use traits for additive API or optional implementation features. Enabling a trait must not remove public API.
- Declare default traits explicitly only when the package truly needs them. Consumers selecting named traits must also pass `defaults` when they intend to retain defaults.
- Encode required dependency traits in the dependency declaration; command-line traits selected for the root package do not automatically configure dependency packages.
- Prefer a small, meaningful trait surface. Do not mirror every internal compile flag as public package configuration.

## Validation matrix

1. Inspect `swift package show-traits` and its JSON form.
2. Build and test defaults.
3. Build and test with `--disable-default-traits`.
4. Build and test each supported named trait with `--traits <Trait>`.
5. Build and test meaningful combinations and `--enable-all-traits` when combinations are supported.
6. Repeat through `xcrun swift` when Xcode consumers are supported, because flag availability and diagnostics can differ.

## Sources

- [Providing configurable packages using traits](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/packagetraits/)
- [SE-0450: Package Traits](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0450-swiftpm-package-traits.md)
