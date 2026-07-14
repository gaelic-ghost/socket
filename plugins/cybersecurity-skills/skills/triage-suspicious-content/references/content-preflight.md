# Suspicious Content Preflight

| Content | Inspect without activation | Common active surface |
| --- | --- | --- |
| Archive/package | Member list, paths, types, signatures, metadata | Nested executables, scripts, symlinks, traversal, installer actions |
| macOS app/pkg/dmg | Bundle/package metadata, signing, notarization, quarantine, mounted layout | Executables, installer scripts, launch services, privileged helpers |
| Script/text | Encoding, interpreter, imports, URLs, commands, heredocs | Download/execute, persistence, credential/file access |
| Office/PDF/document | Container members, relationships, objects, forms, links, metadata | Macros, JavaScript, embedded files, templates, external links |
| Profile/extension | Declared payloads/permissions, signer, distribution source | Network interception, certificates, management, browsing/data access |
| URL/QR/message | Literal destination, sender context, redirects only through approved tooling | Credential capture, drive-by content, deep links, social engineering |

Avoid Finder Quick Look, Office Protected View assumptions, browser navigation, package installation, and OS handler invocation until the parser/execution risk is understood.
