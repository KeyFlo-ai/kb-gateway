# GitHub — KeyFlo-ai/kb-gateway

**Live:** https://github.com/KeyFlo-ai/kb-gateway

Created under the **KeyFlo-ai** org using the **okrealai** GitHub user (James). Add Cole as org member or repo collaborator.

## Push updates

```bash
cd /mnt/blockstorage/business/Keyflo_AI/08_Development/kb-gateway
unset GH_TOKEN GITHUB_TOKEN   # use okrealai gh auth, not agent-smithj
git push origin main
```

## Create repo (one-time, already done)

```bash
unset GH_TOKEN GITHUB_TOKEN
gh auth switch --user okrealai
gh repo create KeyFlo-ai/kb-gateway --public --description "..."
git remote set-url origin git@github.com:KeyFlo-ai/kb-gateway.git
git push -u origin main
```
