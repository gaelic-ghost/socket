# Apple Symbol And Crash Correlation Reference

## Minimum Identity Set

- OS marketing version and build.
- Device or Mac model and architecture.
- App bundle identifier, version, and build.
- Crashed image UUID and load address.
- Candidate binary UUID for the same slice.
- Candidate dSYM DWARF UUID for the same slice.
- Crash timestamp and incident identifier.

## Narrow Commands

```bash
dwarfdump --uuid <binary>
dwarfdump --uuid <dSYM>
atos -arch <architecture> -o <binary-or-dsym-dwarf> -l <load-address> <runtime-address>
```

Use Xcode's supported symbolication flow when an archive, Organizer record, downloaded device symbols, or source mapping is required. Record the exact Xcode build because symbol availability and report handling can change.

## Address Relationship

For an ordinary image mapping:

```text
image-relative offset = runtime address - runtime image load address
runtime address = preferred address + ASLR slide + image-relative adjustment
```

Do not apply this mechanically when the report already provides an offset, when a cache or translated image uses a different mapping, or when pointer authentication/tag bits must be normalized for the tool. Record the actual convention from the report and tool.

## Partial Symbolication Causes

- Missing or UUID-mismatched dSYM.
- Wrong architecture slice.
- System symbols unavailable for the exact OS build.
- Stripping, optimization, inlining, outlining, or tail calls.
- Corrupt or truncated crash evidence.
- Incorrect image load address or slide.
- Static analysis database loaded at a different base.
- Pointer-authenticated or tagged address not presented in the expected form.

## Authoritative Sources

- [Analyzing a crash report](https://developer.apple.com/documentation/xcode/analyzing-a-crash-report)
- [Adding identifiable symbol names to a crash report](https://developer.apple.com/documentation/xcode/adding-identifiable-symbol-names-to-a-crash-report)
- [Building an app to include debugging information](https://developer.apple.com/documentation/xcode/building-your-app-to-include-debugging-information)
- [LLVM dsymutil](https://llvm.org/docs/CommandGuide/dsymutil.html)

Use the local Xcode documentation and tool help for the installed version when their behavior is more specific than a web overview.
