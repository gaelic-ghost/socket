---
name: use-objective-see-tools
description: Use installed Objective-See macOS security tools as thin evidence adapters. Use for KnockKnock persistence inventory, BlockBlock persistence alerts, LuLu network decisions, ProcessMonitor or FileMonitor activity, WhatsYourSign signature inspection, TaskExplorer process review, or related Objective-See tools while exact version, permissions, user actions, tool limits, and owning investigation workflow remain explicit.
---

# Use Objective-See Tools

## Overview

Select the Objective-See tool that observes the needed surface, record its current capabilities, and return evidence to the owning macOS workflow. Do not treat one tool's label or UI color as a threat verdict.

Read [references/objective-see-routing.md](references/objective-see-routing.md) and recheck the official tool page before use.

## Workflow

1. Name the unresolved observation: persistence, process, file, network, signing, or process inventory.
2. Discover local capability.
   - Verify official source, installed app/path, version, supported macOS build, permissions/system extensions, running state, and export format.
   - Do not install, approve extensions, or grant privacy access without an explicit operator decision.
3. Select one tool and bounded action.
4. Preserve context.
   - Record scan time, filters, exclusions, baseline, UI/CLI actions, alerts, raw/exported output, and tool errors.
5. Correlate independently.
   - Verify signer/path/hash, process ancestry, persistence registration, socket, or file change with native evidence where practical.
6. Route conclusions.
   - Send evidence to persistence, runtime, threat assessment, or containment workflows.

## Guardrails

- Do not enable blocking rules or terminate/delete items during evidence collection unless containment is separately approved.
- Do not claim historical coverage when the tool was installed after the event.
- Do not assume every Objective-See tool exposes a stable CLI or accessible GUI automation surface.

## Output

Return tool/version/capability, permissions, action, observations/export, independent correlation, limitations, and owning workflow.
