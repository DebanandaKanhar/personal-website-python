#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

DEPLOY_URL="https://render.com/deploy?repo=https://github.com/DebanandaKanhar/personal-website-python"

echo "Open this URL to deploy the blueprint:"
echo "$DEPLOY_URL"

if command -v open >/dev/null 2>&1; then
  open "$DEPLOY_URL"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$DEPLOY_URL"
fi
echo "After deploy, add domain records in your DNS provider."
