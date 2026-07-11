# Customization Flow

The template records non-security preferences only. `preferredDiscoveryMode` may be `xcode-local` or `rest-first`; `preferredCloudKitAdapter` may be `cktool` or `cktool-js`.

Preferences do not authorize mutation, relax secret handling, convert a portal-only operation into API work, or suppress operation-specific confirmation. Store a durable customization file outside the repository through `scripts/customization_config.py`. Use `effective` to inspect it, `apply --input <yaml-file>` to persist a validated override, and `reset` to remove it.
