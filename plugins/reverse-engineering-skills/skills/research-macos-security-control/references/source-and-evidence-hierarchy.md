# Source And Evidence Hierarchy

Use the strongest applicable source and label its scope.

1. Current Apple Platform Security, deployment, developer, support, and tool documentation.
2. Selected local SDK headers/module interfaces, command man pages/help, and Apple-open-source material for the exact release when available.
3. Exact-build original binaries/frameworks/services, code signatures, entitlements, provisioning, Mach-O/dyld metadata, exported symbols, and interface metadata.
4. Focused runtime observations, unified logs, Endpoint Security events, process ancestry, file/network effects, and exact errors from the recorded environment.
5. Matched cross-build comparison.
6. Hypothesis/inference supported by the above.

Public documentation describes the supported contract but may omit implementation. SDK presence does not prove deployment availability. A private symbol or schema proves only that the recorded artifact contains it. A runtime success/failure proves only the recorded operation, artifact, identity, and environment. Multiple agreeing private observations strengthen a hypothesis but do not create a supported API.

For each claim, cite the artifact/source and date/build. Keep copied excerpts minimal and preserve commands or exported metadata needed to reproduce the observation.
