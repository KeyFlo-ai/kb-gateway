# Mac mini proxy — jamess-mac-mini

kb-gateway runs on the **blockstorage server** (localhost `127.0.0.1:8790`).  
**jamess-mac-mini** is the Tailscale front door for remote MCP clients (Cole, Cursor on Mac).

## One-time setup (on jamess-mac-mini)

1. Ensure Tailscale is connected to **smithjsfamily@** tailnet.
2. Enable Tailscale Serve on the tailnet (admin): https://login.tailscale.com/f/serve
3. Proxy the server gateway through the Mac:

```bash
tailscale serve --bg http://100.122.28.113:8790
tailscale serve status
```

Use the HTTPS URL from `serve status` in client MCP config, or MagicDNS:

```
http://jamess-mac-mini:8790/mcp
```

4. Clients send `Authorization: Bearer <KB_GATEWAY_API_TOKEN>`.

## Verify (from jamess-mac-mini)

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer $KB_GATEWAY_API_TOKEN" \
  http://jamess-mac-mini:8790/mcp
```

Expect `406` or similar (MCP handshake), not `401`.

## Alternative: SSH stdio (no HTTP)

On jamess-mac-mini, Cursor / Claude Desktop can run MCP over SSH to the server — see [`client-setup.md`](client-setup.md).

No VETRIQ involvement — `jamess-mac-mini` is James's Mac on the personal tailnet.
