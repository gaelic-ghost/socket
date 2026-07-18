---
name: swift-compiler-inspection-workflow
description: Inspect Swift compiler selection, driver jobs, diagnostics, parsing, type checking, AST, SIL, LLVM IR, dependency scans, modules, and interfaces with swift, swiftc, swift-driver, and guarded swift-frontend use. Use for compiler behavior, lowering, diagnostic, build-job, or emitted-artifact investigations.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
  hermes:
    category: swift-language
    tags: [swift, compiler, swiftc, sil, llvm]
---

# Swift Compiler Inspection Workflow

Inspect the Swift compilation pipeline while distinguishing supported driver behavior from version-sensitive compiler internals.

## Workflow

1. Inspect repository guidance and determine whether SwiftPM, Xcode, another build system, or a standalone compiler invocation owns the real build.
2. Resolve toolchain ownership:
   - inspect Swiftly with `swiftly use --print-location` and `swift --version`
   - inspect Xcode with `xcode-select -p`, `xcrun --find swiftc`, and `xcrun swiftc --version`
   - choose the owner matching the actual build and keep all compiler, SDK, plugin, and module paths within it
3. Reproduce the narrowest compiler phase that answers the question:
   - parse
   - type check
   - print driver jobs
   - dependency scan
   - emit or inspect AST
   - emit SIL or LLVM IR
   - emit module, interface, or diagnostics
4. Run experiments against copied or temporary inputs unless the user asked to change the repository.
5. Capture the complete command, toolchain identity, target triple, SDK, language mode, conditional flags, module paths, and relevant environment.
6. Classify every surface using [references/compiler-surfaces.md](references/compiler-surfaces.md): supported CLI, version-sensitive diagnostic surface, or compiler-internal surface.
7. Compare artifacts only across intentionally matched configurations.
8. Hand full package or Xcode builds and tests to their owning workflow.

## Driver Boundary

- Treat `swift` and `swiftc` as compiler-driver entry points that plan and coordinate frontend and linker jobs.
- Treat `swift-driver` as the driver implementation, not a second compiler frontend.
- Prefer driver options over invoking `swift-frontend` directly.
- Use `swift-frontend` only when a documented compiler-development workflow or unavailable driver surface requires it, and label the command internal and version-sensitive.

## Toolchain Contract

- Use Swiftly-selected toolchains for Swift.org release or snapshot comparison, cross-platform compiler behavior, and `.swift-version`-controlled repositories.
- Use Xcode-selected tools through `xcrun` for Apple SDK imports, Xcode build reproduction, Xcode-bundled SourceKit behavior, and Apple target triples.
- Do not combine Swiftly's compiler with Xcode's private toolchain libraries or combine Xcode's compiler with Swiftly's host plugins.
- Recognize `swiftly use xcode` as a proxy into the selected Xcode toolchain and record both selectors.

## Output

Return the question, selected compiler phase, toolchain owner and version, exact invocation, artifact stability class, result, and limitations.

## Guardrails

- Do not claim compiler dump formats are stable interchange formats.
- Do not infer optimizer or runtime behavior from a Debug-only or parse-only artifact.
- Do not omit compiler arguments when reproducing a type-check or module failure.
- Do not run multiple SwiftPM or Xcode compiler validations concurrently.
- Do not mutate the global Swiftly or Xcode selection for inspection alone.
