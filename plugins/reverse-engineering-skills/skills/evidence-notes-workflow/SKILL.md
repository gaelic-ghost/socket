---
name: evidence-notes-workflow
description: Create reproducible reverse-engineering notes from artifacts, copied working files, commands, tool versions, decompiler or disassembler output, observations, inferences, open questions, and follow-up checks. Use when Codex needs to document a binary analysis session, preserve an evidence trail, compare tool output, or hand off reverse-engineering findings to a later agent or human pass.
---

# Evidence Notes Workflow

## Overview

Use this skill when reverse-engineering work needs a durable notes file, handoff summary, comparison between tools, or a record of what was inspected. The goal is to make future analysis easier without turning uncertain tool output into overstated source-level claims.

## Workflow

1. Establish the session frame.
   - Name the artifact set, source path, working copy path if any, and date.
   - Record the question being investigated in one sentence.
   - Note whether the current pass is triage, deeper decompilation, disassembly review, symbol matching, crash-log correlation, or comparison between tools.

2. Inventory the inputs.
   - List original artifacts separately from copied working files.
   - Record file names, relevant paths, sizes, versions, UUIDs, checksums, bundle identifiers, target frameworks, architectures, or archive members when useful.
   - Keep generated outputs, exports, screenshots, and renamed-symbol notes separate from original inputs.

3. Record tool context.
   - Name each tool, command, version, project file, database, or exported view that produced evidence.
   - For GUI tools such as Cutter, Ghidra, Malimite, or Hopper, record the project/session name, imported file, analysis options when known, and exported snippets or screenshots.
   - For CLI tools, record the exact command when it matters and summarize noisy output instead of pasting whole logs.

4. Separate observations from inferences.
   - Observation: directly seen in metadata, command output, exported symbols, strings, decompiler output, disassembly, crash logs, or resources.
   - Inference: a likely conclusion drawn from observations.
   - Open question: something plausible but not confirmed by the current evidence.
   - Do not erase uncertainty just because multiple tools produce similar pseudo-code.

5. Keep names and transformations traceable.
   - When renaming symbols, functions, variables, files, or notes, record the original name and the new name.
   - When comparing tools, state which tool produced which name, type, control-flow shape, or pseudo-code.
   - When generated output changes after re-analysis, record the trigger for the change if known.

6. End with a handoff.
   - Summarize the most useful confirmed findings.
   - List blocked or uncertain areas.
   - Name the next artifact, tool, command, or owner skill to use.

## Notes Template

Use this compact template unless the user or repo already has a preferred format:

```markdown
# Reverse Engineering Notes: <artifact or question>

## Session
- Date:
- Question:
- Current pass:
- Original artifact path:
- Working copy path:

## Artifact Inventory
| Item | Role | Type | Identifier |
| --- | --- | --- | --- |
|  | original/input/output |  |  |

## Tool Context
| Tool | Version/session | Input | Output or observation |
| --- | --- | --- | --- |
|  |  |  |  |

## Observations
- ...

## Inferences
- ...

## Open Questions
- ...

## Renames Or Transformations
| Original | New | Reason | Source |
| --- | --- | --- | --- |
|  |  |  |  |

## Handoff
- Confirmed:
- Next check:
- Suggested owner skill:
```

## Writing Rules

- Prefer short notes that can be extended over elaborate reports that go stale.
- Quote only the minimum generated output needed to anchor a finding.
- Say which artifact and tool support each important claim.
- Preserve disagreement between tools instead of smoothing it away.
- Do not place generated decompiler output beside original-source language unless the note clearly labels it as generated output.
