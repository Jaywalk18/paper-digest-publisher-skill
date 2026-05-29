# Security Reference

Never commit:

- GitHub tokens (`gho_`, `ghp_`, `github_pat_`)
- OpenAI/API keys
- MinerU JWTs or `MINERU_TOKEN`
- Feishu/Lark app secrets, access tokens, refresh tokens, or file tokens
- local `~/.mineru/config.yaml`
- local `lark-cli` config
- generated reports, paper PDFs, MinerU extraction outputs, or private site builds

Use environment variables or local config files outside the repository for credentials.

Before publishing:

```bash
python scripts/scan_for_secrets.py --root .
git status --short
git diff --cached --stat
```

If a secret was committed, rotate it. Removing it from the latest commit is not enough after a public push.
