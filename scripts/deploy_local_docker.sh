#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "Created .env from template. Edit values before running in real production."
fi

docker compose down || true
docker compose up --build -d

echo "Deployed with Docker Compose."
echo "App: http://localhost:8000"
echo "Health: http://localhost:8000/healthz"
