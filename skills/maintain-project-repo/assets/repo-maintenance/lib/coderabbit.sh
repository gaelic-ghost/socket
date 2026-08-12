#!/usr/bin/env sh

# Return success only when CodeRabbit explicitly reports that a review could
# not be produced because its quota, usage, or review limit was reached.
coderabbit_review_is_unavailable() {
  source_name="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  message="$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]')"

  case "$source_name" in
    *coderabbit*)
      ;;
    *)
      return 1
      ;;
  esac

  case "$message" in
    *quota*|*"usage limit"*|*"rate limit"*|*"review limit"*|*"limit reached"*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}
