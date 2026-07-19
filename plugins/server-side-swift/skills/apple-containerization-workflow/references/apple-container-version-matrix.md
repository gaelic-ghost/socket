# Apple Container Version Matrix

Use exact current release notes, tagged source, current docs when explicitly linked by a release, and installed CLI help. Never infer one project's stability from the other's version.

| Surface | Version rule | Important 1.x or stability boundary |
| --- | --- | --- |
| `apple/container` CLI | discover installed version; use matching release docs and command help | 1.0 adds persistent `container machine`, TOML configuration, structured-output changes, `container cp`, and removes version-zero XPC compatibility |
| `container machine` docs | current-branch docs may be linked from the 1.0 release | pair current docs with installed `container machine --help`; do not assume unreleased flags |
| `apple/containerization` Swift package | pin exact 0.x release/revision and inspect its source/DocC | public API remains pre-1.0; compile/test the selected version and expect source changes |
| OCI image/Dockerfile | pin tags/digests according to project policy | keep portable image authoring independent from the local Apple runtime |
| Linux kernel/init filesystem | record exact provenance and compatibility | runtime, Rosetta, init, and nested-virtualization behavior may depend on these artifacts |

## 1.x Migration Decisions

- Replace removed `container system property` automation with the documented TOML configuration path; do not keep a duplicate compatibility command path.
- Re-check parsers that consume structured `list` output instead of assuming the pre-1.0 shape.
- Use `container cp` only after confirming installed help and source/destination semantics.
- Treat ordinary container mounts and a machine's user/home integration as different security and lifecycle surfaces.

## Required Record

Record CLI version, package version/revision when applicable, docs/tag/commit consulted, host macOS/architecture, image digest, kernel/init provenance, and every relied-on help surface.
