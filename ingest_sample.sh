#!/usr/bin/env bash
set -euo pipefail

API_BASE=${API_BASE:-http://localhost:8000}

if [ -t 0 ]; then
  python scripts/generate_sample_logs.py | while read -r line; do
    curl -s -X POST "$API_BASE/api/logs/ingest" -H 'Content-Type: application/json' -d "$line" >/dev/null || true
  done
else
  while read -r line; do
    curl -s -X POST "$API_BASE/api/logs/ingest" -H 'Content-Type: application/json' -d "$line" >/dev/null || true
  done
fi

echo "Done."


