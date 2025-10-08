#!/usr/bin/env bash
set -euo pipefail
KIBANA_HOST=${KIBANA_HOST:-http://localhost:5601}
FILE=${1:-./kibana/dashboards/logs_saved_objects.json}
curl -X POST "$KIBANA_HOST/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@$FILE


