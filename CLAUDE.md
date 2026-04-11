# Real Human Thoughts

Autonomous personal blog. One thought published daily, drawn from GitHub Issues.

## Architecture

- **Pipeline**: `pick_thought.py` → `writing_agent.py` → `validate_post.py` → Hugo build → gh-pages deploy
- **Scheduling**: GHA cron `0 8 * * *` (08:00 UTC daily)
- **Thought pool**: GitHub Issues on this repo, authored by mcfredrick only
- **LLMs**: OpenRouter free tier via tenkai-lib (`LLMClient`, `ModelSelector`)
- **Content**: `content/posts/YYYY-MM-DD.md` — one post per day

## Key Notes

- If no open issues exist, the workflow exits cleanly (no post today, no failure)
- Non-owner issues are closed automatically at workflow start
- Hugo baseURL must have trailing slash
- GitHub Pages source: `gh-pages` branch, root `/`
- Secret needed: `OPENROUTER_API_KEY` in repo Settings → Secrets
