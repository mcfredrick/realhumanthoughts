"""
Writing agent: cleans up a raw thought (STT errors, formatting) and generates a Hugo post.

Reads thought.json, calls LLM, writes YYYY-MM-DD.md with Hugo frontmatter.
"""

import json
import os
import sys
from datetime import date as _date

from tenkai_lib.openrouter import LLMClient, ModelSelector

SYSTEM_PROMPT = (
    "You are an editor for a personal blog called 'Real Human Thoughts'. "
    "You receive raw thoughts captured via voice-to-text (spoken into a phone). "
    "Your job is to:\n"
    "1. Fix speech-to-text errors — wrong homophones, missing punctuation, run-on sentences\n"
    "2. Generate a short, evocative title (5 words or fewer — no clickbait, no questions)\n"
    "3. Lightly format the text with natural paragraph breaks — do NOT add new ideas or change meaning\n\n"
    "Return ONLY valid Hugo frontmatter + body in exactly this format:\n\n"
    "---\n"
    'title: "Your Generated Title"\n'
    "date: YYYY-MM-DD\n"
    "draft: false\n"
    "---\n\n"
    "The cleaned-up thought text here.\n\n"
    "Do not add commentary, preamble, or closing remarks. Return the markdown only."
)


def write_post(thought_path: str, post_path: str, api_key: str, date_str: str) -> None:
    with open(thought_path) as f:
        thought = json.load(f)

    raw_body = thought["body"].strip()
    user_prompt = f"Date: {date_str}\n\nRaw thought:\n{raw_body}"

    selector = ModelSelector(api_key=api_key)
    models = selector.fetch_free_models()
    if not models:
        raise RuntimeError("No free models available from OpenRouter")

    client = LLMClient(api_key=api_key, preferred_model=models[0]["id"])
    response = client.call(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

    # Replace the placeholder date with the actual date if LLM used the template literally
    response = response.replace("date: YYYY-MM-DD", f"date: {date_str}")

    with open(post_path, "w") as f:
        f.write(response)


if __name__ == "__main__":
    today = _date.today().isoformat()
    post_path = f"content/posts/{today}.md"
    write_post(
        thought_path="thought.json",
        post_path=post_path,
        api_key=os.environ["OPENROUTER_API_KEY"],
        date_str=today,
    )
    print(f"Post written: {post_path}")
