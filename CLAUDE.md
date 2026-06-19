# kb-gateway — operating manual

> AGENTS.md is a symlink to this file.

## Identity

HTTP MCP gateway exposing the **learning KB** (Pinecone + Neo4j + agentic router) to remote agents. Keyflo org repo: `KeyFlo-ai/kb-gateway`.

## Gated execution routine

- **Routine:** gated-execution-routine v1.2 → `/root/.claude/references/gated-execution-routine.md`
- **Run dir:** `/mnt/blockstorage/business/Keyflo_AI/09_Projects/kb-gateway/run/`
- **Resume:** read `run/STATE.md` → `run/CONTINUE.md`

## Parent context

- Business: Keyflo → `/mnt/blockstorage/business/Keyflo_AI/CLAUDE.md`
- Runtime deps: `/root/langchain-course` (okrealai/langchain-course)
- Env: `source /mnt/blockstorage/env/load.sh global`

## Run (operator)

```bash
cd /mnt/blockstorage/business/Keyflo_AI/08_Development/kb-gateway
source /mnt/blockstorage/env/load.sh global
export KB_GATEWAY_API_TOKEN="<from secrets registry>"
/root/.venv-langchain-course/bin/python -m kb_gateway --transport streamable-http
```

Smoke: `scripts/smoke_test.sh`

## Hard rules

- READ ONLY at gateway layer — no ingest, no Neo4j writes
- Remote clients get MCP tools only — never Pinecone/Neo4j keys
- Namespace whitelist enforced in `kb_gateway/config.py`
- Default remote tool: `route_query` when routing ambiguous

## Owners

- Primary: James Smith
- Backup: Cole (after token issued)
