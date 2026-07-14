# Apple Artifact And Mach-O Reference

## Inspection Order

1. Container identity and manifest.
2. Bundle metadata and nested-code inventory.
3. Executable identity and universal slices.
4. Mach-O load commands and address layout.
5. Symbols, runtime metadata, signing, and encryption clues.
6. Derived extraction or tool import only after the original is recorded.

## Common Artifact Shapes

- `.app`, `.appex`, `.framework`, `.dylib`, `.a`, executable, bundle, and XCFramework.
- IPA or ZIP containing `Payload/*.app` and nested code.
- dSYM containing DWARF files whose UUIDs must match binaries.
- `.ips` or crash report containing binary-image UUID and load-address evidence.
- dyld shared cache and subcaches tied to an OS build and architecture.
- kernel collection, KDK symbols, IPSW, restore image, and build manifest.

## Narrow Local Checks

Use only the checks needed for the artifact:

```bash
file <artifact>
shasum -a 256 <artifact>
plutil -p <bundle>/Contents/Info.plist
lipo -archs <binary>
dwarfdump --uuid <binary-or-dsym>
otool -l <binary>
otool -L <binary>
nm -m <binary>
codesign -dvvv --entitlements - <bundle-or-binary>
```

On iOS-family bundles, adjust the bundle-relative executable path rather than assuming the macOS `Contents/` layout. Prefer `vtool`, `dyld_info`, or LLVM object tools when their output more directly answers build-version, fixup, export, or disassembly questions.

For universal binaries, query `codesign` once per recorded architecture with `--arch <slice>` when collecting CDHashes or slice-specific CodeDirectory facts. If an Apple command-line tool has no working version flag, record its resolved toolchain path together with the macOS and Xcode build instead of inventing a version.

## Address Terms

- File offset: byte position in the file.
- Unslid VM address: preferred virtual address encoded by the image.
- Image-relative offset: address relative to the image base.
- ASLR slide: runtime adjustment applied to the preferred mapping.
- Slid runtime address: observed address after mapping and slide.

Record the conversion used. Do not paste an address from a crash log into a static database without confirming image, architecture, load address, and slide.

## Evidence Limits

- Stripped symbols do not remove all runtime metadata, imports, strings, or unwind information.
- An encrypted executable may expose headers and metadata while keeping executable pages unsuitable for ordinary static decompilation.
- Chained fixups and dyld-cache optimizations can make legacy relocation assumptions wrong.
- A tool may accept a CPU family while mishandling a newer subtype or pointer-authenticated representation.

## Authoritative Sources

- [Apple Mach-O APIs](https://developer.apple.com/documentation/kernel/mach-o)
- [Archived Mach-O Runtime Architecture](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/MachORuntime/)
- [Apple dyld source](https://github.com/apple-oss-distributions/dyld)
- [LLVM object dumper](https://llvm.org/docs/CommandGuide/llvm-objdump.html)
- [Apple open-source distributions](https://github.com/apple-oss-distributions)

Use local SDK headers and tool help for the installed build before relying on an archived format narrative. Treat open-source distributions as reference and historical evidence unless correlated to the shipping artifact.
