---
name: preserve-binary-artifacts
description: Create preservation-grade inventories and immutable working practices for compiled artifacts and reverse-engineering research. Use when Codex must preserve binaries, app bundles, firmware, archives, symbols, crash logs, decompiler projects, historical software, research evidence, or FOSS analysis materials while recording provenance, hashes, identifiers, transformations, generated outputs, and redistribution status separately.
---

# Preserve Binary Artifacts

## Overview

Preserve the acquired object, its context, and every later transformation as separate layers. Make future verification possible without depending on one tool database or one analyst's notes.

## Workflow

1. Define the preservation unit.
   - Identify whether the original is a file, directory tree, bundle, disk image, archive, symbol set, crash package, firmware set, or tool project.
   - Preserve the original container shape when paths, metadata, signatures, or extended attributes matter.

2. Record acquisition context.
   - Record source, acquisition date, original name, version or build claims, and any available publication or catalog identifier.
   - Label the source as direct, mirrored, extracted, reconstructed, or unknown.

3. Create stable identifiers.
   - Record cryptographic hashes for files and a deterministic member inventory for containers when practical.
   - Define the inventory method: normalized relative path, member type, byte size, and content hash sorted by bytewise relative path is the portable baseline. Record any included metadata such as mode, timestamp, extended attributes, or symlink target separately so another pass can reproduce the same comparison.
   - Record platform identifiers such as Mach-O UUIDs, PE timestamps, PDB identities, managed assembly identities, bundle identifiers, firmware manifest identities, or code-signing hashes when relevant.

4. Separate storage layers.
   - Original: immutable acquired material.
   - Working copy: copied input used by tools.
   - Derived artifacts: extracted slices, decoded resources, normalized metadata, or re-signed and patched variants.
   - Analysis state: tool databases, projects, comments, renames, scripts, screenshots, and exports.
   - Notes: observations, inferences, open questions, and handoffs.

5. Record transformations.
   - Record the input identifier, exact command or tool action, tool version, output identifier, and reason.
   - Treat thinning, extraction, decompression, decryption, patching, re-signing, symbol application, and normalization as transformations rather than transparent access.

6. Record environment dependencies.
   - Capture platform, hardware, OS build, SDK or runtime, locale or time assumptions, and tool versions when they affect reproducibility.

7. Keep rights status separate.
   - Record preservation and technical provenance independently from license, publication, disclosure, or redistribution decisions.
   - Prefer metadata, hashes, and reproducible recipes when the artifact itself should not be redistributed.

8. Verify recoverability.
   - Confirm the original remains unchanged.
   - Confirm the inventory can locate every referenced derived artifact and analysis record.

## Output

Use the `artifact-manifest`, `environment-manifest`, and `transformation-record` shapes from `evidence-notes-workflow` when a durable handoff is needed.

End with:

```markdown
## Preservation Status
- Original retained unchanged:
- Stable identifiers recorded:
- Working and derived layers separated:
- Tool state preserved:
- Rights or redistribution status recorded separately:
- Recovery check:
```
