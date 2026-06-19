# Friend setup — learning KB MCP

**For:** Friends James invites (outside Keyflo)  
**Repo:** [`James-Server-Admin/kb-gateway`](https://github.com/James-Server-Admin/kb-gateway)  
**MCP URL:** `https://kb-mcp.waytie.com/mcp`

Query ~116 marketing/engineering courses from Cursor — read-only, no server access needed.

---

## What James sends you

1. **GitHub invite** — read access to `James-Server-Admin/kb-gateway` (accept the email)
2. **Bearer token** — private message (Signal, 1Password, etc.) — **never commit or paste in GitHub**

---

## Quick start (Cursor — 5 min)

### Option A — script (recommended)

```bash
git clone git@github.com:James-Server-Admin/kb-gateway.git
cd kb-gateway
export KB_GATEWAY_MCP_TOKEN="<paste token James sent you>"
chmod +x scripts/setup-friend-mcp.sh
./scripts/setup-friend-mcp.sh
cat config/mcp.json
```

Cursor → **Settings → MCP** → paste the `learning-kb` block from `config/mcp.json`.

### Option B — paste JSON only (no clone)

```json
{
  "mcpServers": {
    "learning-kb": {
      "url": "https://kb-mcp.waytie.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_HERE` with the token James sent you.

---

## Verify

**curl** (expect `406` or `200`, not `401`):

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://kb-mcp.waytie.com/mcp
```

**Cursor** — ask your agent:

> Use learning-kb route_query: what is PAS copy structure?

---

## Tools (what you can ask)

| Tool | Use when |
|------|----------|
| `route_query` | **Default** — not sure which store to use |
| `query_namespace` | How-to / passages (`course-transcripts`, `patterns`, `langchain-docs`) |
| `graph_query` | Coverage, topic depth, cross-course disputes |
| `list_namespaces` | See what's in the corpus |
| `health` | Check the service is up |

Full specs: [`docs/ENDPOINT-CATALOG.md`](ENDPOINT-CATALOG.md)

---

## Boundaries

- **Read-only** — no writes to the corpus
- **Learning corpus only** — not Keyflo product messaging or other businesses
- **Rate limited** — be reasonable; don't batch-scrape
- **Token is personal** — don't share; ask James for a new one if leaked

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `401` | Wrong or missing token — check `Authorization: Bearer …` |
| Cursor can't connect | URL must end with `/mcp`; restart Cursor |
| `502` / timeout | Service down — ping James |
| GitHub clone denied | Accept collaborator invite on `James-Server-Admin/kb-gateway` |

---

## Operator (James) — onboarding a friend

1. Add token to `learning-kb-api-keys.txt`:
   ```
   # friendname-2026-06
   <openssl rand -hex 32>
   ```
2. Invite on GitHub: `James-Server-Admin/kb-gateway` → Collaborators → Read
3. Send friend this file + token out of band
4. Optional smoke from server:
   ```bash
   KB_GATEWAY_PUBLIC_URL=https://kb-mcp.waytie.com/mcp ./scripts/verify_remote_mcp.sh
   ```

GitHub variable **`FRIEND_SETUP`** on the repo points here.
