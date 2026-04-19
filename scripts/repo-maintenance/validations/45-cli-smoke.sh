#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SELF_DIR/../lib/common.sh"

bin_path="$(swiftpm build --show-bin-path)"
tool_path="$bin_path/SpeakSwiftlyServerTool"
[ -x "$tool_path" ] || die "Expected the debug SpeakSwiftlyServerTool executable at $tool_path after the package build step."

log "Smoke-testing the executable help surface."
set +e
help_output="$(swiftpm run SpeakSwiftlyServerTool help 2>&1)"
help_status=$?
set -e
printf '%s\n' "$help_output"
[ "$help_status" -eq 2 ] || die "Expected 'swift run SpeakSwiftlyServerTool help' to exit with status 2, but it exited with $help_status."
printf '%s\n' "$help_output" | grep -F "Usage:" >/dev/null || die "Expected the help output to include a Usage: line."

log "Smoke-testing LaunchAgent plist rendering against the built debug tool."
set +e
plist_output="$(swiftpm run SpeakSwiftlyServerTool launch-agent print-plist --tool-executable-path "$tool_path" 2>&1)"
plist_status=$?
set -e
printf '%s\n' "$plist_output"
[ "$plist_status" -eq 0 ] || die "Expected 'swift run SpeakSwiftlyServerTool launch-agent print-plist' to exit with status 0, but it exited with $plist_status."
printf '%s\n' "$plist_output" | grep -F "<plist version=\"1.0\">" >/dev/null || die "Expected the printed LaunchAgent property list to include the plist header."
printf '%s\n' "$plist_output" | grep -F "com.gaelic-ghost.speak-swiftly-server" >/dev/null || die "Expected the printed LaunchAgent property list to mention the default LaunchAgent label."
