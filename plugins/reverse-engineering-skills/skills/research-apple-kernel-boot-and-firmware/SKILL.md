---
name: research-apple-kernel-boot-and-firmware
description: Inventory and correlate exact-build Apple kernel, kernel collection, KDK, panic, boot-chain, device-tree, IPSW, restore-image, LocalPolicy, SSV, AuxKC, personalization, and firmware artifacts. Use when Codex must compare public XNU or dyld source with shipping binaries, match KDK symbols and UUIDs, distinguish Mac restore from iPhone or iPad firmware, map Apple Silicon boot evidence, or preserve coprocessor and firmware payload metadata without assuming undocumented payload behavior.
---

# Research Apple Kernel Boot And Firmware

## Overview

Keep kernel, boot, and firmware research separate from app analysis. Require exact build, hardware identity, UUID, and provenance before correlating public source, symbols, or extracted components.

Read [references/apple-system-artifacts.md](references/apple-system-artifacts.md) for artifact identities, source-correlation rules, boot context, and authoritative sources.

## Workflow

1. Define the artifact family and question.
   - Separate kernel collection, KDK, panic report, device tree, boot object, LocalPolicy, restore manifest, IPSW component, and coprocessor firmware.

2. Preserve acquisition and exact identity.
   - Record hashes, source, date, container and member paths, device or Mac model, board and SoC identifiers, OS marketing version and build, component version, UUID, and signing or personalization metadata.

3. Match supporting material.
   - Match KDK and symbols by exact OS build, architecture, and UUID.
   - Match public XNU, dyld, Security, or distribution manifests by published release and preserve the limits of that match.

4. Map the system container.
   - Inventory kernel collections, extensions, symbols, manifests, device trees, boot objects, and firmware components before extracting.
   - Treat extraction as a recorded transformation.

5. Place evidence in boot and policy context.
   - Distinguish Boot ROM, later boot stages, LocalPolicy, secure boot policy, SSV, kernel collections, AuxKC, personalization, and runtime kernel state only where current Apple sources support the relationship.

6. Analyze the bounded target.
   - Use Mach-O, Apple Silicon, symbol, dyld-cache, decompiler-review, or version-comparison skills for the selected component.
   - Keep undocumented payload identity separate from inferred function.

7. Preserve historical comparisons.
   - Record exact intermediate builds checked, source publication gaps, symbol availability, and tool compatibility.

## Guardrails

- Do not use a mismatched KDK or symbol set as if it were exact.
- Do not claim public source is the shipping implementation without build and binary correlation.
- Do not mix Mac restore images with iPhone or iPad firmware procedures.
- Do not execute, flash, personalize, or restore firmware as an implied analysis step.
- Do not infer a coprocessor payload's function solely from filename or container position.

## Output

Return system artifact manifest, hardware/build identity, symbol and source matches, boot or policy context, extraction records, confirmed observations, correlation limits, and next bounded component.
