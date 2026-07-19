# macOS VM Artifact Lifecycle

Keep these artifacts separate; no single file is “the VM snapshot.”

| Artifact | Owns | Lifecycle rule |
| --- | --- | --- |
| Restore image | installer and supported macOS build metadata | verify compatibility and provenance; cache/remove independently |
| Hardware model | supported virtual Mac hardware description | bind to compatible configuration and guest install |
| Machine identifier | virtual Mac identity | generate/persist deliberately; do not casually duplicate |
| Auxiliary storage | platform boot/security state | persist with its VM identity and installed guest |
| Disk image | guest filesystem and installed software | coordinate shutdown/copy semantics; saved state does not replace it |
| VM bundle metadata | configuration and artifact locations | keep portable paths and explicit schema/version ownership |
| Saved machine state | paused/stopped runtime state | restore only with documented state and compatible configuration/artifacts |
| Clone/checkpoint | tool-specific copy of required artifacts | name the exact copy/revert operation; do not imply framework snapshots |
| Evidence export | intentionally selected logs/artifacts | export narrowly, hash/scan as required, and keep separate from control state |

Record ownership, permissions, size, source/digest, creation time, compatible host/guest versions, and removal semantics for every artifact.
