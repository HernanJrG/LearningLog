#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Missing venv at $ROOT_DIR/.venv."
  echo "Create it with: python3 -m venv .venv && source .venv/bin/activate && python -m pip install psycopg2-binary"
  exit 1
fi

if [[ -z "${DATABASE_URL:-}" ]]; then
  DEFAULT_USER="${USER:-$(id -un)}"
  DATABASE_URL="postgresql://${DEFAULT_USER}@localhost:5432/learninglog"
  export DATABASE_URL
fi

cd "$ROOT_DIR"
exec "$VENV_PYTHON" -m app.main
