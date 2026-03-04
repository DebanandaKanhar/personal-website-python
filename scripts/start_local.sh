#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "Virtualenv not found. Run ./scripts/bootstrap.sh first."
  exit 1
fi

source .venv/bin/activate

PORT="${APP_PORT:-8000}"
set +e
uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --reload
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -ne 0 ]]; then
  FALLBACK_PORT=$((PORT + 1))
  echo "Port $PORT unavailable. Retrying on $FALLBACK_PORT..."
  uvicorn app.main:app --host 0.0.0.0 --port "$FALLBACK_PORT" --reload
fi
