#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "Created .env from template. Update credentials before production."
fi

# Backward compatibility: switch old default local Postgres URL to SQLite.
python - <<'PY'
from pathlib import Path

env_path = Path(".env")
text = env_path.read_text(encoding="utf-8")
old = "DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/personal_website"
new = "DATABASE_URL=sqlite:///./personal_website.db"
if old in text:
    env_path.write_text(text.replace(old, new), encoding="utf-8")
    print("Updated .env to SQLite default for local run.")
PY

echo "Bootstrap complete."
echo "Run: source .venv/bin/activate && uvicorn app.main:app --reload"
