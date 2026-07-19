# Linux Development Guest Matrix

Use exact current docs and installed help; this matrix chooses a shape, not a brand default.

| Need | Container machine | Lima/Colima adapter | Full Virtualization framework VM |
| --- | --- | --- | --- |
| Persistent interactive Linux | primary fit | primary fit | supported with more ownership |
| OCI-image-backed root | primary model | tool-specific | custom image/disk work |
| Init and services | supported by compatible image | tool-specific | guest-owned |
| Custom kernel/boot | limited to documented machine/kernel controls | tool-specific | primary fit |
| Full disk/install lifecycle | not the primary model | tool-specific | primary fit |
| GUI Linux | not primary | tool-specific | explicit graphics/input/UI path |
| Host integration | automatic user/home conveniences require review | tool-specific mounts/sockets | explicitly selected devices/shares |
| Portable OCI deployment | hand off to Docker workflow | hand off to Docker workflow | hand off to Docker workflow |
| Hostile workload | disable home integration; still require lab review | require lab review | require lab profile and verified controls |

For every selected distro record: image/digest, OS release, architecture, kernel, init, toolchain, build/test result, services, filesystem, network, reboot persistence, reset, and removal.
