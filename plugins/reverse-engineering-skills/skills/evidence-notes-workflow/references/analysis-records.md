# Analysis Record Shapes

Use only the records needed for the current analysis. Keep identifiers stable across notes so later tools and sessions can refer to the same input and generated state.

## Artifact Manifest

```markdown
## Artifact Manifest: <artifact-id>
- Role: original | working-copy | derived | generated
- Source or parent:
- Acquisition date:
- Original name or container path:
- Type and size:
- SHA-256:
- Platform/runtime:
- Architecture/slice:
- UUID/build ID/assembly identity:
- Bundle/version/build identity:
- Signing or encryption state:
```

## Environment Manifest

```markdown
## Environment Manifest: <environment-id>
- Host hardware:
- Target hardware:
- OS marketing version and build:
- SDK/runtime/KDK build:
- Native, translated, Simulator, VM, or physical device:
- Security state relevant to the result:
- Locale/time assumptions:
```

## Tool Context

```markdown
## Tool Context: <tool-context-id>
- Tool and version:
- Project/database/session:
- Input artifact ID:
- Loader, image, slice, and base address:
- Analysis settings/plugins:
- Symbol/type inputs:
- Commands or scripts:
- Generated outputs:
```

## Transformation Record

```markdown
## Transformation: <transformation-id>
- Input artifact ID:
- Operation and reason:
- Tool/version or exact command:
- Output artifact ID:
- Output SHA-256:
- Signature, entitlement, or metadata changes:
- Reversible from preserved inputs: yes/no
```

## Symbol Map

```markdown
## Symbol Map
| Address/identity | Original or runtime name | Tool-generated name | Proposed name | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
```

## Signature Report

```markdown
## Signature Report
- Artifact ID:
- Code-directory or signing hash:
- Authorities and Team ID:
- Designated requirement:
- Provisioning profile:
- Declared entitlements:
- Hardened runtime/library validation/sandbox clues:
- Notarization or platform-binary observation:
- Original or transformed signature:
```

## Mach-O Map

```markdown
## Mach-O Map
- Artifact ID and selected slice:
- UUID, file type, CPU type/subtype:
- Minimum OS and linked SDK clues:
- Segments/sections:
- Imports/exports/rpaths:
- Fixups/relocations/function starts/unwind data:
- Code-signature and encryption load commands:
- Address convention: file offset | unslid VM | slid runtime
```

## Version Diff

```markdown
## Version Diff
- Comparison question:
- Build A artifact/environment/tool IDs:
- Build B artifact/environment/tool IDs:
- Matching and normalization method:
- Confirmed differences:
- Confirmed unchanged context:
- Ambiguous or unmatched items:
- Temporal claim and checked range:
- Next intermediate build or runtime check:
```
