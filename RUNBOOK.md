# Runbook — kb-gateway

**Owner:** James Smith · **Backup:** Cole  
**Last reviewed:** 2026-06-19 · **Production:** false (enable after smoke + token issued)

## 1. System overview

HTTP MCP gateway for learning corpus queries. Entry: `python -m kb_gateway --transport streamable-http`.

## 2. Owners & escalation

| Severity | Response | Action |
|---|---|---|
| P1 — gateway down | 4h | Restart systemd; check Neo4j + Pinecone |
| P2 — auth failures | 24h | Rotate `KB_GATEWAY_API_TOKEN`; update clients |
| P3 — stale answers | best effort | Check graph rebuild; corpus ingest drift |

## 3. SLAs & monitoring

| Metric | Target |
|---|---|
| `health` tool returns ok | 99% when server up |
| p95 route_query latency | < 45s (LLM + retrieval) |
| Auth reject rate | alert if spike (bad token rollout) |

## 4. Change process

Draft → `scripts/smoke_test.sh` → PR review → merge → `systemctl restart kb-gateway` → monitor health

## 5. MCP config

See `docs/client-setup.md`. Token in secrets registry only.

## 6. Data & compliance

- Read-only gateway; learning corpus may include course transcripts
- No PII indexing policy change via this service
- Log MCP calls at reverse proxy (Tailscale/CF) when enabled

## 7. Incident response

| Failure | Signal | Fix |
|---|---|---|
| Neo4j down | health.checks.neo4j error | `docker start learning-kg-neo4j` |
| Pinecone auth | query_namespace ERROR | Check `LEARNING_PINECONE_API_KEY` in global.env |
| LC import fail | langchain_course check | Verify `/root/langchain-course` + venv |
| 401 on MCP | Bearer mismatch | Sync token with clients |

## Smoke test

```bash
scripts/smoke_test.sh
```
