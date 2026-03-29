# Workflow Customization

Use skill-local customization to control supported workflow defaults for `speak-with-profile`.

## Files
- Optional overrides: `config/customization.yaml`
- Template defaults: `config/customization.template.yaml`

## Precedence
1. Explicit user input and wrapper flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. Workflow defaults in `SKILL.md` and `wrapper-contract.md`

## Supported settings
### Runtime-backed in the local wrapper
- `defaultProfilesFile`: used when `--profiles-file` is not passed.
- `defaultDisclosure`: used when the selected profile does not provide `disclosure`.
- `localCli.defaultOutputDir`: used when `--out` is not passed.
- `localCli.defaultPlaybackBackend`: used when `--playback` is not passed.
- `localCli.autoplayGeneratedAudio`: used when `--autoplay` / `--no-autoplay` is not passed.

### Documentation-only for now
- `preferredExecutionMode`: documented workflow preference only. The current wrapper script does not execute `delegate` mode.

## Runtime behavior
The local wrapper reads `config/customization.yaml` and `config/customization.template.yaml` at runtime and applies supported settings using the documented precedence rules. In conversational usage, prefer `delegate` unless deterministic local CLI behavior is explicitly required.
