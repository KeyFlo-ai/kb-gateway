#!/usr/bin/env bash
# Build config/mcp.json from env (friend handoff — token from James, not GitHub variables).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${ROOT}/config/mcp.json"

URL="${KB_GATEWAY_MCP_URL:-https://kb-mcp.waytie.com/mcp}"
TOKEN="${KB_GATEWAY_MCP_TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
  echo "error: set KB_GATEWAY_MCP_TOKEN to the bearer token James sent you" >&2
  echo "  export KB_GATEWAY_MCP_TOKEN=\"...\"" >&2
  echo "  See docs/FRIEND-SETUP.md" >&2
  exit 1
fi

mkdir -p "${ROOT}/config"
python3 - <<PY
import json
from pathlib import Path
cfg = {
    "mcpServers": {
        "learning-kb": {
            "url": "${URL}",
            "headers": {"Authorization": "Bearer ${TOKEN}"},
        }
    }
}
Path("${OUT}").write_text(json.dumps(cfg, indent=2) + "\n")
PY
chmod 600 "$OUT"
echo "Wrote $OUT"
echo "Add the learning-kb block to Cursor → Settings → MCP."
