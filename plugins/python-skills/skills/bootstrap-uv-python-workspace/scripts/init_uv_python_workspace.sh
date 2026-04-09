#!/usr/bin/env zsh
emulate -L zsh
set -euo pipefail

usage() {
  cat <<'USAGE'
Bootstrap a uv Python workspace.

Usage:
  init_uv_python_workspace.sh --name <workspace-name> [options]

Required:
  --name <name>                    Workspace name

Options:
  --path <path>                    Target directory (default: ./<name>)
  --members "a,b,c"                Workspace member names (default: core-lib,api-service)
  --profile-map "a=package,b=service"
                                   Member profile assignments
  --python <version>               Python version (default: 3.13)
  --config <path>                  Explicit YAML config path
  --bypassing-all-profiles         Ignore global and repo profile files for this run
  --bypassing-repo-profile         Ignore repo-local profile file for this run
  --deleting-repo-profile          Delete repo-local profile file before execution
  --force                          Allow non-empty target directory
  --initial-commit                 Create initial git commit on success
  --no-git-init                    Skip git init (default is enabled)
  -h, --help                       Show help
USAGE
}

fail() {
  echo "[ERROR] $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command '$1'. Install it and re-run the workspace scaffold."
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
    *) fail "Invalid boolean value '$1' in customization data." ;;
  esac
}

apply_config_value() {
  local key="$1"
  local value="$2"

  case "$key" in
    name) NAME="$value" ;;
    path) TARGET="$value" ;;
    members) MEMBERS_CSV="$value" ;;
    profile_map) PROFILE_MAP="$value" ;;
    python) PYTHON_VERSION="$value" ;;
    force) FORCE="$(bool_to_int "$value")" ;;
    initial_commit) INITIAL_COMMIT="$(bool_to_int "$value")" ;;
    no_git_init)
      if [[ "$(bool_to_int "$value")" -eq 1 ]]; then
        GIT_INIT=0
      else
        GIT_INIT=1
      fi
      ;;
    *) fail "Unknown config key '$key' in customization file." ;;
  esac
}

load_config_file() {
  local path="$1"
  local required="$2"

  if [[ ! -f "$path" ]]; then
    [[ "$required" -eq 1 ]] && fail "Config file not found: $path"
    return 0
  fi

  local line
  local lineno=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    lineno=$((lineno + 1))
    line="$(trim "$line")"
    [[ -z "$line" || "$line" == \#* ]] && continue
    [[ "$line" == *:* ]] || fail "Invalid config line at $path:$lineno. Expected 'key: value'."

    local key="${line%%:*}"
    local value="${line#*:}"
    key="$(trim "$key")"
    value="${value%%#*}"
    value="$(trim "$value")"
    value="$(strip_quotes "$value")"

    [[ -n "$key" ]] || fail "Empty config key at $path:$lineno."
    apply_config_value "$key" "$value"
  done < "$path"
}

abs_path() {
  local input="$1"
  if [[ -d "$input" ]]; then
    (cd "$input" && pwd)
  else
    local parent="$(dirname "$input")"
    local base="$(basename "$input")"
    mkdir -p "$parent"
    (cd "$parent" && printf '%s/%s\n' "$(pwd)" "$base")
  fi
}

normalize_module_name() {
  local raw="${1//-/_}"
  printf '%s' "$raw" | tr -c '[:alnum:]_' '_'
}

target_from_python() {
  local v="$1"
  local major="$(printf '%s' "$v" | cut -d. -f1)"
  local minor="$(printf '%s' "$v" | cut -d. -f2)"
  printf 'py%s%s\n' "$major" "$minor"
}

append_tooling_config() {
  local pyproject="$1"
  local py_version="$2"

  if grep -q '^\[tool\.ruff\]' "$pyproject"; then
    return
  fi

  cat >>"$pyproject" <<EOF_CFG

[tool.ruff]
line-length = 100
target-version = "$(target_from_python "$py_version")"

[tool.ruff.lint]
select = ["E", "F", "UP", "B"]

[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]

[tool.mypy]
python_version = "$py_version"
warn_unused_configs = true
check_untyped_defs = true
no_implicit_optional = true
EOF_CFG
}

ensure_gitignore_entry() {
  local file_path="$1"
  local entry="$2"

  touch "$file_path"
  if ! grep -Fqx "$entry" "$file_path"; then
    printf '%s\n' "$entry" >>"$file_path"
  fi
}

write_env_files() {
  local member_root="$1"
  local app_name="$2"

  cat >"$member_root/.env" <<EOF_ENV
APP_NAME="$app_name"
APP_ENVIRONMENT="development"
EOF_ENV

  cat >"$member_root/.env.local" <<'EOF_ENV_LOCAL'
# Local overrides for developer-specific or secret values.
# This file is ignored by git on purpose.
EOF_ENV_LOCAL

  ensure_gitignore_entry "$member_root/.gitignore" ".env.local"
}

write_package_settings() {
  local module_dir="$1"
  local member_name="$2"

  cat >"$module_dir/config.py" <<EOF_CFG
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    name: str = "$member_name"
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
EOF_CFG
}

write_service_settings() {
  local app_dir="$1"
  local member_name="$2"

  cat >"$app_dir/config.py" <<EOF_CFG
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    name: str = "$member_name"
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
EOF_CFG
}

render_readme() {
  local template="$1"
  local out="$2"
  local name="$3"
  local run_cmds="$4"
  local test_cmds="$5"
  local notes="$6"

  sed \
    -e "s|__NAME__|$name|g" \
    -e "s|__TYPE__|workspace|g" \
    -e "s|__RUN_COMMANDS__|$run_cmds|g" \
    -e "s|__TEST_COMMANDS__|$test_cmds|g" \
    -e "s|__NOTES__|$notes|g" \
    "$template" >"$out"
}

profile_for_member() {
  local member="$1"
  local default_profile="$2"
  local map="$3"

  if [[ -z "$map" ]]; then
    printf '%s\n' "$default_profile"
    return
  fi

  local old_ifs="$IFS"
  IFS=','
  for entry in ${(s:,:)map}; do
    local key="${entry%%=*}"
    local value="${entry#*=}"
    if [[ "$key" == "$member" ]]; then
      IFS="$old_ifs"
      printf '%s\n' "$value"
      return
    fi
  done
  IFS="$old_ifs"

  printf '%s\n' "$default_profile"
}

NAME=""
TARGET=""
MEMBERS_CSV="core-lib,api-service"
PROFILE_MAP=""
PYTHON_VERSION="3.13"
FORCE=0
INITIAL_COMMIT=0
GIT_INIT=1

SKILL_NAME="bootstrap-uv-python-workspace"
SCRIPT_DIR="${0:A:h}"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GLOBAL_PROFILE="$HOME/.config/gaelic-ghost/python-skills/$SKILL_NAME/customization.yaml"
REPO_PROFILE="$REPO_ROOT/.codex/profiles/$SKILL_NAME/customization.yaml"

CONFIG_PATH=""
BYPASS_ALL_PROFILES=0
BYPASS_REPO_PROFILE=0
DELETE_REPO_PROFILE=0

ORIGINAL_ARGS=("$@")

while [[ "$#" -gt 0 ]]; do
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
    -h|--help)
      usage
      exit 0
      ;;
    --name|--path|--members|--profile-map|--python)
      [[ "$#" -ge 2 ]] || fail "$1 requires a value"
      shift 2
      ;;
    --force|--initial-commit|--no-git-init)
      shift
      ;;
    *)
      shift
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
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --name) NAME="$2"; shift 2 ;;
    --path) TARGET="$2"; shift 2 ;;
    --members) MEMBERS_CSV="$2"; shift 2 ;;
    --profile-map) PROFILE_MAP="$2"; shift 2 ;;
    --python) PYTHON_VERSION="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --initial-commit) INITIAL_COMMIT=1; shift ;;
    --no-git-init) GIT_INIT=0; shift ;;
    --config) shift 2 ;;
    --bypassing-all-profiles|--bypassing-repo-profile|--deleting-repo-profile) shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown argument: $1" ;;
  esac
done

[[ -n "$NAME" ]] || fail "--name is required."
[[ "$GIT_INIT" -eq 0 && "$INITIAL_COMMIT" -eq 1 ]] && fail "--initial-commit requires git initialization."

if [[ -z "$TARGET" ]]; then
  TARGET="./$NAME"
fi
TARGET="$(abs_path "$TARGET")"

require_cmd uv
if [[ "$GIT_INIT" -eq 1 || "$INITIAL_COMMIT" -eq 1 ]]; then
  require_cmd git
fi

if [[ -e "$TARGET" ]]; then
  if [[ -n "$(ls -A "$TARGET" 2>/dev/null || true)" && "$FORCE" -ne 1 ]]; then
    fail "Target directory '$TARGET' is not empty. Re-run with --force if you want to scaffold into a populated path."
  fi
  if [[ -f "$TARGET/pyproject.toml" && "$FORCE" -eq 1 ]]; then
    fail "Refusing to overwrite existing '$TARGET/pyproject.toml' even with --force."
  fi
else
  mkdir -p "$TARGET"
fi

README_TEMPLATE="$SCRIPT_DIR/../assets/README.md.tmpl"
[[ -f "$README_TEMPLATE" ]] || fail "Missing README template at '$README_TEMPLATE'."

mkdir -p "$TARGET"
cd "$TARGET"

cat > pyproject.toml <<'EOF_WORKSPACE'
[tool.uv.workspace]
members = ["packages/*"]
EOF_WORKSPACE

ensure_gitignore_entry ".gitignore" ".venv"

typeset -a MEMBERS=()
typeset -a PACKAGE_MEMBERS=()
typeset -a SERVICE_MEMBERS=()

old_ifs="$IFS"
IFS=','
for raw in ${(s:,:)MEMBERS_CSV}; do
  member="$(trim "$raw")"
  [[ -n "$member" ]] || continue
  MEMBERS+=("$member")
done
IFS="$old_ifs"

[[ "${#MEMBERS[@]}" -gt 0 ]] || fail "No valid workspace members were provided."

mkdir -p packages

idx=1
for member in "${MEMBERS[@]}"; do
  default_profile="service"
  if [[ "$idx" -eq 1 ]]; then
    default_profile="package"
  fi

  profile="$(profile_for_member "$member" "$default_profile" "$PROFILE_MAP")"
  [[ "$profile" == "package" || "$profile" == "service" ]] || fail "Invalid profile '$profile' for member '$member'."

  member_path="packages/$member"
  module_name="$(normalize_module_name "$member")"
  if [[ "$profile" == "package" ]]; then
    uv init --package --lib --name "$member" --python "$PYTHON_VERSION" --vcs none "$member_path"
    PACKAGE_MEMBERS+=("$member")
  else
    uv init --app --name "$member" --python "$PYTHON_VERSION" --vcs none "$member_path"
    SERVICE_MEMBERS+=("$member")
  fi

  uv add --package "$member" --group dev pytest ruff mypy
  uv add --package "$member" pydantic-settings python-dotenv
  append_tooling_config "$member_path/pyproject.toml" "$PYTHON_VERSION"
  write_env_files "$member_path" "$member"

  if [[ "$profile" == "service" ]]; then
    uv add --package "$member" fastapi --extra standard
    mkdir -p "$member_path/app" "$member_path/tests"
    touch "$member_path/app/__init__.py"
    write_service_settings "$member_path/app" "$member"

    cat > "$member_path/app/main.py" <<'PY'
from typing import Annotated

from fastapi import Depends, FastAPI

from app.config import Settings, get_settings

app = FastAPI(title="Workspace Service")


@app.get("/health")
def health(settings: Annotated[Settings, Depends(get_settings)]) -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.name,
        "environment": settings.environment,
    }
PY

    cat > "$member_path/tests/test_${module_name}_service.py" <<'PY'
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import get_settings
from app.main import app


def test_app_exists() -> None:
    assert app is not None


def test_settings_load_defaults() -> None:
    settings = get_settings()
    assert settings.name
    assert settings.environment == "development"
PY
  else
    mkdir -p "$member_path/tests"
    write_package_settings "$member_path/src/$module_name" "$member"

    cat > "$member_path/tests/test_${module_name}_import.py" <<PY
from ${module_name} import __name__ as imported_name
from ${module_name}.config import get_settings


def test_package_import() -> None:
    assert imported_name == "${module_name}"


def test_settings_load_defaults() -> None:
    settings = get_settings()
    assert settings.name == "${member}"
    assert settings.environment == "development"
PY
  fi
  idx=$((idx + 1))
done

if [[ "${#PACKAGE_MEMBERS[@]}" -gt 0 && "${#SERVICE_MEMBERS[@]}" -gt 0 ]]; then
  shared_pkg="${PACKAGE_MEMBERS[1]}"
  for svc in "${SERVICE_MEMBERS[@]}"; do
    uv add --package "$svc" "$shared_pkg"
  done
fi

uv lock
uv sync --all-packages
uv run --all-packages pytest

for member in "${MEMBERS[@]}"; do
  (
    cd "packages/$member"
    uv run ruff check .
    uv run mypy .
  )
done

render_readme \
  "$README_TEMPLATE" \
  "README.md" \
  "$NAME" \
  "uv run --all-packages pytest" \
  "uv run --all-packages pytest; (cd packages/<member> && uv run ruff check . && uv run mypy .)" \
  "Members are created under packages/. Every member ships a committed .env, an ignored .env.local, and typed settings via pydantic-settings. If both package and service profiles exist, services depend on the first package member via workspace sources."

if [[ "$GIT_INIT" -eq 1 ]]; then
  if [[ ! -d .git ]]; then
    git init
  fi
  git add .
  if [[ "$INITIAL_COMMIT" -eq 1 ]]; then
    git commit -m "Initial workspace scaffold from bootstrap-uv-python-workspace"
  fi
fi

echo "[OK] Workspace scaffold complete: $TARGET"
