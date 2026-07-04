#!/bin/sh
set -eu

hook_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

exec sh "$hook_dir/run-thread-title-hook.sh"
