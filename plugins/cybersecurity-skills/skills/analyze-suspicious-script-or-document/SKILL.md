---
name: analyze-suspicious-script-or-document
description: Decode and analyze suspicious scripts and active documents without triggering them. Use for shell, AppleScript, JavaScript, Python, PowerShell, shortcuts, Office files, PDFs, configuration profiles, encoded commands, macros, embedded objects, external templates, staged downloads, or mixed document-to-script payload chains.
---

# Analyze Suspicious Script Or Document

## Overview

Recover the execution chain as data. Use parsers and text extraction in isolation, avoid native handlers, and make each decoding transformation reproducible.

Read [references/script-document-analysis.md](references/script-document-analysis.md) for language and document-specific checks.

## Workflow

1. Preserve the original and identify the real container/type.
2. Extract without activation.
   - List document members and relationships; extract text, metadata, macros, JavaScript, forms, links, embedded files, and external references with non-executing tooling.
   - Render URLs and commands as inert text.
3. Normalize one layer at a time.
   - Decode base64/hex/URL escapes, string concatenation, compression, character arithmetic, environment substitution, and generated commands.
   - Record input, operation, tool, and output hash for every layer.
4. Reconstruct control and data flow.
   - Identify entry conditions, interpreter, downloaded content, execution methods, persistence, credential/file access, network destinations, cleanup, and environment gates.
5. Separate capability from execution.
   - State which branches are present, which inputs activate them, and which behaviors remain inferred.
6. Route payloads.
   - Send recovered binaries to static/reverse analysis and use dynamic analysis only inside chosen isolation.

## Guardrails

- Do not paste decoded commands into an executing shell.
- Do not enable macros, install profiles, follow links, or import shortcuts during static analysis.
- Do not use a cloud document parser for private content without approval.

## Output

Return container identity, recovered layers, execution chain, indicators, activation conditions, likely impact, uncertainty, and safe next step.
