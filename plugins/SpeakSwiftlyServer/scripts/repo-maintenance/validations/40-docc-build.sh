#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SELF_DIR/../lib/common.sh"

docc_output_dir="$REPO_ROOT/.build/docc"

swiftpm package \
  --allow-writing-to-directory "$docc_output_dir" \
  generate-documentation \
  --target SpeakSwiftlyServer \
  --disable-indexing \
  --output-path "$docc_output_dir"
