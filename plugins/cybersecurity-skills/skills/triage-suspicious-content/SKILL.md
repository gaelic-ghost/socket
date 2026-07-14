---
name: triage-suspicious-content
description: Safely classify suspicious files, archives, installers, packages, scripts, documents, configuration profiles, browser extensions, URLs, QR codes, messages, and nested payloads before execution. Use when someone receives or discovers sketchy content and needs to know what it is, what active behavior it may contain, and the smallest safe next analysis step.
---

# Triage Suspicious Content

## Overview

Identify the content and its active surfaces without opening, installing, importing, previewing, or following it through a handler that may execute code. Preserve the original and route the smallest useful next check.

Read [references/content-preflight.md](references/content-preflight.md) for format-specific active-content clues.

## Workflow

1. Preserve intake context.
   - Record sender/source, delivery channel, claimed purpose, filenames, timestamps, quarantine metadata, URLs as text, and why it looked suspicious.
   - Hash files and work from a copy.

2. Identify containers before content.
   - Determine file type from bytes and structure, not extension alone.
   - List archive/package members without broad extraction and note traversal paths, symlinks, nested archives, password protection, or misleading double extensions.

3. Inventory active surfaces.
   - Look for executables, scripts, macros, embedded files, links, forms, JavaScript, launch/install metadata, configuration payloads, extension permissions, shortened/redirecting URLs, and QR destinations.
   - Treat preview generators and importers as parsers that may be vulnerable.

4. Check local provenance.
   - Record signatures, signer identity, notarization/quarantine evidence, package receipts/metadata, document producer, URL host and certificate context, and expected vendor distribution channel.
   - Do not infer trust from any one field.

5. Route without execution.
   - Use reputation checking for hash/domain/vendor context, script/document analysis for active text, static malware analysis for capabilities, and reverse engineering for binary internals.
   - Select isolation before any dynamic behavior.

## Output

Return intake identity, actual type/container, active surfaces, provenance observations, suspicious and benign explanations, confidence, and the first safe next workflow.
