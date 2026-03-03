#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-api}"

# Load local environment overrides (DATABASE_URL / DB_*).
if [[ -f "$ROOT_DIR/.env" ]]; then
  set -a
  source "$ROOT_DIR/.env"
  set +a
fi

if [[ -n "${VENV_DIR:-}" ]]; then
  SELECTED_VENV_DIR="$VENV_DIR"
else
  SELECTED_VENV_DIR="$ROOT_DIR/.venv"
  if [[ ! -e "$SELECTED_VENV_DIR" ]] && [[ ! -w "$ROOT_DIR" ]]; then
    SELECTED_VENV_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/learninglog/.venv"
    echo "Project directory is not writable. Using venv at $SELECTED_VENV_DIR"
  fi
fi

VENV_PYTHON="$SELECTED_VENV_DIR/bin/python"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required. Install Python 3 before running this script."
  exit 1
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Creating virtual environment at $SELECTED_VENV_DIR ..."
  mkdir -p "$SELECTED_VENV_DIR"
  python3 -m venv "$SELECTED_VENV_DIR"
fi

if [[ -z "${DATABASE_URL:-}" ]]; then
  if [[ -n "${DB_HOST:-}" || -n "${DB_PORT:-}" || -n "${DB_NAME:-}" || -n "${DB_USER:-}" || -n "${DB_PASSWORD:-}" ]]; then
    export DB_HOST="${DB_HOST:-localhost}"
    export DB_PORT="${DB_PORT:-5432}"
    export DB_NAME="${DB_NAME:-learninglog}"
    export DB_USER="${DB_USER:-postgres}"
  else
    DEFAULT_USER="${DB_USER:-postgres}"
    DATABASE_URL="postgresql://${DEFAULT_USER}@localhost:5432/learninglog"
    export DATABASE_URL
    echo "DATABASE_URL not set; using default local DSN without password."
    echo "If auth fails, set DATABASE_URL or DB_PASSWORD in .env."
  fi
fi

cd "$ROOT_DIR"
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r "$ROOT_DIR/requirements.txt"

case "$MODE" in
  api)
    exec "$VENV_PYTHON" -m uvicorn app.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
    ;;
  client)
    shift || true
    exec "$VENV_PYTHON" -m app.client.console_client "$@"
    ;;
  legacy-cli)
    exec "$VENV_PYTHON" -m app.main
    ;;
  *)
    echo "Usage: ./run.sh [api|client|legacy-cli]"
    exit 1
    ;;
esac
