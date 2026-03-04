#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if ! command -v render >/dev/null 2>&1; then
  echo "Render CLI not found, using npx fallback..."
  NPX_RENDER=1
else
  NPX_RENDER=0
fi

echo "Starting Render Blueprint deployment..."
if [[ "$NPX_RENDER" -eq 1 ]]; then
  npx -y render blueprint launch --file render.yaml
else
  render blueprint launch --file render.yaml
fi
echo "Deployment request submitted. Verify /healthz after rollout."
