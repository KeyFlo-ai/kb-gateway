# Client setup — wire remote agents to kb-gateway

## Remote via jamess-mac-mini (recommended)

kb-gateway runs on the blockstorage server. **jamess-mac-mini** proxies it on the tailnet.

**Prerequisite:** one-time Tailscale Serve on the Mac — see [`mac-mini-proxy.md`](mac-mini-proxy.md).

```json
{
  "mcpServers": {
    "keyflo-learning-kb": {
      "url": "http://jamess-mac-mini:8790/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_KB_GATEWAY_API_TOKEN"
      }
    }
  }
}
```

Or use the HTTPS URL from `tailscale serve status` on the Mac.

Traffic stays inside the tailnet. Keyflo learning KB only — not VETRIQ.

## Cursor on jamess-mac-mini (stdio via SSH)

No HTTP proxy needed — MCP runs on the server over SSH:

```json
{
  "mcpServers": {
    "keyflo-learning-kb": {
      "command": "ssh",
      "args": [
        "blockstorage-server",
        "/root/.venv-langchain-course/bin/python",
        "-m", "kb_gateway",
        "--transport", "stdio",
        "--no-auth"
      ]
    }
  }
}
```

Replace `blockstorage-server` with your SSH host alias for the blockstorage box.

## Cursor / Claude on the blockstorage server (stdio)

```json
{
  "mcpServers": {
    "keyflo-learning-kb": {
      "command": "/root/.venv-langchain-course/bin/python",
      "args": ["-m", "kb_gateway", "--transport", "stdio", "--no-auth"],
      "cwd": "/mnt/blockstorage/business/Keyflo_AI/08_Development/kb-gateway",
      "env": {}
    }
  }
}
```

Env loads from `bootstrap.load_env()` via langchain-course — no keys in config JSON.

## Python (scripts on server)

```python
from kb_gateway.tools import route_query, query_namespace, graph_query

print(route_query("how do I structure a Meta lead gen campaign?")["answer"])
```

Requires server env + `LANGCHAIN_COURSE_REPO`.

## Which tool to call

When unsure → **`route_query`**. See [`routing.md`](routing.md).

Read [`AGENTS.md`](../AGENTS.md) in repo — agents should load it for routing rules.
