# Swift Macro Package Shape

## Boundaries

- Keep the public macro declaration in a normal library target.
- Keep compiler-side expansion logic in a `.macro` target.
- Expose the library product, not the compiler plugin implementation, to ordinary clients.
- Use the `swift-syntax` products required by the active macro template and support window; do not guess a dependency version from a different Swift toolchain.

## Workflow

1. Inspect both `swift package init --type macro` and `xcrun swift package init --type macro` when the package must support Swiftly and Xcode.
2. Confirm the package tools-version and compiler-plugin support before changing the manifest.
3. Keep syntax transformation pure and deterministic. Emit diagnostics at the source construct that the user can fix.
4. Test expansion text and diagnostics with the supported macro test facilities, then compile at least one real client use.
5. When expansion differs by host compiler, capture the exact toolchain version and reduce the case before changing expected output.

## Sources

- [SE-0394: Package Manager Support for Custom Macros](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0394-swiftpm-expression-macros.md)
- [SwiftSyntax](https://github.com/swiftlang/swift-syntax)
- [Swift macros](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/macros/)
