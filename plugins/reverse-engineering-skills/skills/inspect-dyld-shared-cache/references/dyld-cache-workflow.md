# dyld Shared Cache Workflow Reference

## Cache Manifest

- Source device, restore image, or system path.
- OS marketing version and build.
- Platform, hardware class, and architecture.
- Main cache hash and UUID.
- Subcache filenames, hashes, UUIDs, and relationship.
- Toolchain, extraction tool, and symbol-source versions.

## Address Record

Preserve:

- cache-native unslid address
- cache mapping and file offset
- image identity and image-relative offset
- ASLR slide and runtime address when observed
- extracted-image base and address
- analysis-database base and address

Do not infer one mapping from another without recording the tool or calculation.

## Extraction Limits

An extracted image can differ from an original standalone Mach-O because the cache may coalesce, optimize, rebase, bind, strip, or relocate content. Treat extraction as a transformation. Use the original cache for provenance and address evidence.

Cache layout, subcache naming, private structures, and available extraction commands are version-sensitive. Read installed tool help and exact dyld source revision when possible.

## Authoritative Sources

- [Apple dyld source](https://github.com/apple-oss-distributions/dyld)
- [Apple open-source distributions](https://github.com/apple-oss-distributions)
- [Apple security releases](https://support.apple.com/100100)
- [Apple developer release feed](https://developer.apple.com/news/releases/)

Use public source as architecture and format evidence, not as proof of byte-for-byte identity with a shipping cache.
