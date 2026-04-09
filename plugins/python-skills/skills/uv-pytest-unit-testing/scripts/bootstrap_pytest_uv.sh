#!/usr/bin/env zsh
emulate -L zsh
set -euo pipefail

WORKSPACE_ROOT="$(pwd)"
PACKAGE_NAME=""
WITH_COV=0
DRY_RUN=0

SKILL_NAME="uv-pytest-unit-testing"
SCRIPT_DIR="${0:A:h}"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GLOBAL_PROFILE="$HOME/.config/gaelic-ghost/python-skills/$SKILL_NAME/customization.yaml"
REPO_PROFILE="$REPO_ROOT/.codex/profiles/$SKILL_NAME/customization.yaml"

CONFIG_PATH=""
BYPASS_ALL_PROFILES=0
BYPASS_REPO_PROFILE=0
DELETE_REPO_PROFILE=0

usage() {
  cat <<'USAGE'
Usage: bootstrap_pytest_uv.sh [--workspace-root PATH] [--package NAME] [--with-cov] [--dry-run] [--config PATH]

Options:
  --workspace-root PATH      Repository root containing pyproject.toml (default: cwd)
  --package NAME             Workspace member package name for package-scoped install
  --with-cov                 Also install pytest-cov and add coverage defaults when creating config
  --dry-run                  Print planned commands and file changes without mutating files
  --config PATH              Explicit YAML config path
  --bypassing-all-profiles   Ignore global and repo profile files for this run
  --bypassing-repo-profile   Ignore repo-local profile file for this run
  --deleting-repo-profile    Delete repo-local profile file before execution
  -h, --help                 Show this help
USAGE
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: required command not found: $1" >&2
    exit 1
  fi
}

fail() {
  echo "error: $*" >&2
  exit 1
}

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

strip_quotes() {
  local value="$1"
  if [[ "$value" == \"*\" && "$value" == *\" ]]; then
    value="${value:1:${#value}-2}"
  elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
    value="${value:1:${#value}-2}"
  fi
  printf '%s' "$value"
}

bool_to_int() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    1|true|yes|on) printf '1\n' ;;
    0|false|no|off) printf '0\n' ;;
    *) fail "invalid boolean value '$1'" ;;
  esac
}

apply_config_value() {
  local key="$1"
  local value="$2"

  case "$key" in
    workspace_root) WORKSPACE_ROOT="$value" ;;
    package) PACKAGE_NAME="$value" ;;
    with_cov) WITH_COV="$(bool_to_int "$value")" ;;
    dry_run) DRY_RUN="$(bool_to_int "$value")" ;;
    *) fail "unknown config key '$key'" ;;
  esac
}

load_config_file() {
  local path="$1"
  local required="$2"

  if [[ ! -f "$path" ]]; then
    [[ "$required" -eq 1 ]] && fail "config file not found: $path"
    return 0
  fi

  local line
  local lineno=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    lineno=$((lineno + 1))
    line="$(trim "$line")"
    [[ -z "$line" || "$line" == \#* ]] && continue
    [[ "$line" == *:* ]] || fail "invalid config line at $path:$lineno"

    local key="${line%%:*}"
    local value="${line#*:}"
    key="$(trim "$key")"
    value="${value%%#*}"
    value="$(trim "$value")"
    value="$(strip_quotes "$value")"

    [[ -n "$key" ]] || fail "empty config key at $path:$lineno"
    apply_config_value "$key" "$value"
  done < "$path"
}

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

append_pytest_config_if_missing() {
  local pyproject_path="$1"
  local addopts_value="-ra"

  if [[ "$WITH_COV" -eq 1 ]]; then
    addopts_value="-ra --cov --cov-report=term-missing"
  fi

  if rg -n "^\[tool\.pytest\.ini_options\]" "$pyproject_path" >/dev/null 2>&1; then
    echo "info: [tool.pytest.ini_options] already exists in $pyproject_path; leaving config unchanged"
    return 0
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] append baseline [tool.pytest.ini_options] to $pyproject_path"
    return 0
  fi

  cat >>"$pyproject_path" <<EOF_CFG

[tool.pytest.ini_options]
addopts = "$addopts_value"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
EOF_CFG

  echo "info: added [tool.pytest.ini_options] to $pyproject_path"
}

ORIGINAL_ARGS=("$@")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config)
      CONFIG_PATH="${2:-}"
      [[ -n "$CONFIG_PATH" ]] || fail "--config requires a value"
      shift 2
      ;;
    --bypassing-all-profiles)
      BYPASS_ALL_PROFILES=1
      shift
      ;;
    --bypassing-repo-profile)
      BYPASS_REPO_PROFILE=1
      shift
      ;;
    --deleting-repo-profile)
      DELETE_REPO_PROFILE=1
      shift
      ;;
    --workspace-root|--package)
      [[ $# -ge 2 ]] || fail "$1 requires a value"
      shift 2
      ;;
    --with-cov|--dry-run)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$DELETE_REPO_PROFILE" -eq 1 ]]; then
  rm -f "$REPO_PROFILE"
fi

if [[ "$BYPASS_ALL_PROFILES" -eq 0 ]]; then
  load_config_file "$GLOBAL_PROFILE" 0
  if [[ "$BYPASS_REPO_PROFILE" -eq 0 ]]; then
    load_config_file "$REPO_PROFILE" 0
  fi
fi

if [[ -n "$CONFIG_PATH" ]]; then
  load_config_file "$CONFIG_PATH" 1
fi

set -- "${ORIGINAL_ARGS[@]}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace-root)
      WORKSPACE_ROOT="$2"
      shift 2
      ;;
    --package)
      PACKAGE_NAME="$2"
      shift 2
      ;;
    --with-cov)
      WITH_COV=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --config)
      shift 2
      ;;
    --bypassing-all-profiles|--bypassing-repo-profile|--deleting-repo-profile)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_cmd uv
require_cmd rg

if [[ ! -d "$WORKSPACE_ROOT" ]]; then
  echo "error: workspace root does not exist: $WORKSPACE_ROOT" >&2
  exit 1
fi

PYPROJECT_PATH="$WORKSPACE_ROOT/pyproject.toml"
if [[ ! -f "$PYPROJECT_PATH" ]]; then
  echo "error: missing pyproject.toml at $PYPROJECT_PATH" >&2
  exit 1
fi

cd "$WORKSPACE_ROOT"

typeset -a deps
if [[ "$WITH_COV" -eq 1 ]]; then
  deps=(pytest pytest-cov)
else
  deps=(pytest)
fi

if [[ -n "$PACKAGE_NAME" ]]; then
  run_cmd uv add --package "$PACKAGE_NAME" --dev "${deps[@]}"
else
  run_cmd uv add --dev "${deps[@]}"
fi

append_pytest_config_if_missing "$PYPROJECT_PATH"

echo "info: bootstrap complete"
