---
name: inspect-dyld-shared-cache
description: Inspect, map, extract from, or compare Apple dyld shared caches and subcaches while preserving cache-native identity and addresses. Use when Codex must identify a cache by platform, architecture, UUID, and OS build; inventory images, mappings, slide information, local symbols, chained fixups, closures, or subcaches; correlate a cache image with crash or static-analysis evidence; or compare exact cache builds without confusing extracted Mach-O addresses with cache-native locations.
---

# Inspect dyld Shared Cache

## Overview

Treat a dyld shared cache as a build-specific container and address space. Preserve the complete cache set and its UUIDs before extracting individual images.

Read [references/dyld-cache-workflow.md](references/dyld-cache-workflow.md) for cache records, address rules, extraction limits, and canonical source guidance.

## Workflow

1. Preserve cache identity.
   - Record source device or restore image, OS marketing version and build, platform, hardware class, architecture, main-cache hash and UUID, and every subcache filename, hash, and UUID.
   - Keep the complete cache set together.

2. Discover the installed tool surface.
   - Record tool and version, supported cache generation, commands, extraction behavior, and symbol inputs.
   - Prefer tools from the matching Apple toolchain or dyld source when available, but verify exact-build compatibility.

3. Map the container.
   - Record mappings, images, subcache relationships, slide information, local-symbol regions, and available fixup or closure metadata.
   - Inventory images before extracting.

4. Preserve address spaces.
   - Label cache-native unslid address, mapping-relative offset, runtime slid address, extracted-image address, and static-database address.
   - Record every conversion used to correlate a crash frame or extracted image.

5. Extract only when needed.
   - Treat extracted images as derived artifacts with hashes, source cache UUID, extraction tool, version, and command.
   - Do not assume an extracted image recreates the original standalone file or retains all cache optimizations and symbols.

6. Correlate or compare.
   - Match by exact build, architecture, cache and image identity, and tool method.
   - Use `compare-binary-versions` for cross-build deltas and preserve unchanged context plus unmatched images.

7. Route language, symbols, or instruction analysis to the focused Apple skills after cache identity and address mapping are sound.

## Guardrails

- Do not mix subcaches from different builds.
- Do not use an extracted file's address without recording its cache-native origin.
- Do not assume public dyld source exactly matches a shipping cache format.
- Do not call an unsupported parser result proof that an image, symbol, or fixup is absent.

## Output

Return cache manifest, mappings and image inventory, address-conversion record, derived extraction records, symbol sources, comparison bounds, tool limits, and next check.
