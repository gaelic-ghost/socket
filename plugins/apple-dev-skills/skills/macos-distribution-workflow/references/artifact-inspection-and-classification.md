# Artifact Inspection And Classification

Start with the actual exported artifact and classify the evidence before changing project settings.

| Check | What it answers | Boundary |
| --- | --- | --- |
| `codesign -dvvv --entitlements :-` | identity, signature details, and embedded entitlements | Inspection only; do not infer distribution readiness from one field. |
| `codesign --verify --deep --strict --verbose=2` | signature integrity across nested code | Diagnose nested signing before re-signing. |
| `spctl -a -vv` | Gatekeeper assessment | Keep local execution and trust-policy results separate. |
| notarization status and stapling check | direct-distribution readiness | Validate the outermost delivered container for the chosen channel. |

Sign nested code from the inside out when the distribution process requires manual signing, then sign the containing app last. Prefer Xcode/archive export or the established release system over ad hoc artifact mutation. A successful local launch does not prove Gatekeeper or notarization readiness.
