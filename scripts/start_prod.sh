#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"
HOST="${APP_HOST:-0.0.0.0}"

echo "Starting production server on ${HOST}:${PORT}"
exec uvicorn app.main:app --host "$HOST" --port "$PORT"
