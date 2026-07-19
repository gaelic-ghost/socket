# Responsible Code And Attribution

## Identity record

Capture the executable path, bundle ID, Team ID, designated requirement, signing flags, CDHash when useful, parent/launcher, target process/resource, and transformation history. For a helper, extension, XPC service, script interpreter, or command-line tool, record both the initiating app and the process that performs the protected operation.

Useful non-mutating inspection commands include:

```bash
codesign --display --verbose=4 /path/to/App.app
codesign --display --entitlements :- /path/to/App.app
codesign --verify --deep --strict --verbose=2 /path/to/App.app
ps -axo pid,ppid,user,comm,args
```

Do not rely on `--deep` verification alone to explain nested-code identity; enumerate the actual helper/extension/XPC executables when attribution matters.

## Attribution traps

- A grant to Terminal, an IDE, or an agent host authorizes that signed host in the recorded context; it does not prove the built app or helper is authorized.
- Rebuilding, relocating, changing signing identity, re-signing, or launching through a different host can change the identity that TCC evaluates.
- Automation is about the controlling-target pair and requested Apple Event, not one global permission.
- A helper or XPC service can be the responsible code even when the parent app owns the UI.
- Unsigned, ad hoc, or unstable development tools make authorization evidence difficult to reproduce. Preserve the exact artifact instead of generalizing one result.
- A Settings entry is not proof that the original operation now succeeds; reproduce the operation after any required relaunch, helper restart, or logout.

## Result statement

Report: `artifact identity -> protected operation and target -> class/status evidence -> user or managed decision -> lifecycle transition -> reproduced result`. State whether attribution is documented, observed, or inferred.
