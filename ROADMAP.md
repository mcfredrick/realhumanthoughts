# Real Human Thoughts — Roadmap

## Phase 1: Core Blog ✓

Publish one thought per day from a pool of iPhone-captured ideas.

- **Thought pool**: GitHub Issues on this repo, pushed via Siri shortcut
- **Pipeline**: pick random issue → LLM cleanup (STT fix + title) → Hugo post → GitHub Pages
- **LLM**: OpenRouter free tier via `tenkai-lib`
- **Reused from [todai](https://github.com/mcfredrick/todai)**: `tenkai-lib`, GHA workflow pattern, post validation pattern

## Phase 2: Agentic Research Response *(planned)*

After a thought is selected, a research agent finds related resources and synthesizes a short "response" — context, connections, relevant links — appended to the post.

**Open questions before designing:**
- What sources make sense for arbitrary personal thoughts (todai uses AI-specific RSS/GitHub)?
- Should research search the web dynamically, or draw from a curated source list?
- How long should the synthesis be? What tone?
- Does this run every day, or only when the thought is "researchable"?

**Candidate reuse:** todai research pipeline pattern + `tenkai-lib`

## Phase 3: Inter-Idea Connection Graph *(planned)*

Surface corollaries and connections to prior published thoughts as part of the synthetic response.

**Open questions before designing:**
- Minimum corpus size before connections become meaningful?
- What does a "connection" look like in the post UI — sidebar, inline callout, footer links?
- Does connection discovery happen at write time (GHA) or read time (client-side JS)?

**Candidate reuse:** todai `build_index.py` + fastembed embedding pattern (`tenkai-search-template`)
