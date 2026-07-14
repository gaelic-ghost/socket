# Script And Document Analysis

| Surface | Inspect | Avoid during static work |
| --- | --- | --- |
| Shell/AppleScript | interpreters, expansions, heredocs, pipelines, `osascript`, downloads, launch/persistence commands | sourcing or command substitution |
| JavaScript/Python/PowerShell | imports, eval/exec, network, filesystem, subprocess, encoded strings, environment gates | native interpreter execution |
| Office/Open XML | relationships, macros, embedded OLE, external templates, DDE, links | opening with macros or external content enabled |
| PDF | objects, streams, JavaScript, actions, forms, launch/URI entries, embedded files | native preview/browser rendering before parser review |
| Shortcuts/profiles | declared actions or payloads, permissions, certificates, URLs, management settings | importing, installing, or approving payloads |

Prefer format-aware parsers inside a disposable environment. Parser failure or malformed structure is evidence to preserve, not a reason to open the file normally.
