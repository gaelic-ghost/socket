#!/bin/sh
set -eu

hook_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
plugin_root=$(dirname -- "$hook_dir")

exec node "$plugin_root/scripts/session-start-hook.mjs"
