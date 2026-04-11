import json
from unittest.mock import patch

from agents.writing_agent import SYSTEM_PROMPT, write_post


def test_write_post_produces_valid_file(tmp_path):
    thought = {"number": 7, "body": "i think the internet is like a nervous system for society"}
    thought_file = tmp_path / "thought.json"
    thought_file.write_text(json.dumps(thought))
    post_file = tmp_path / "2026-04-10.md"

    llm_response = (
        '---\ntitle: "The Internet as Nervous System"\n'
        "date: 2026-04-10\ndraft: false\n---\n\n"
        "I think the internet is like a nervous system for society.\n"
    )

    with patch("agents.writing_agent.ModelSelector") as MockSelector, \
         patch("agents.writing_agent.LLMClient") as MockClient:
        MockSelector.return_value.fetch_free_models.return_value = [{"id": "test-model"}]
        MockClient.return_value.call.return_value = llm_response

        write_post(
            thought_path=str(thought_file),
            post_path=str(post_file),
            api_key="fake",
            date_str="2026-04-10",
        )

    assert post_file.exists()
    content = post_file.read_text()
    assert 'title: "The Internet as Nervous System"' in content
    assert "nervous system" in content


def test_system_prompt_addresses_stt():
    assert any(
        phrase in SYSTEM_PROMPT.lower()
        for phrase in ["speech-to-text", "voice", "stt", "spoken"]
    )


def test_write_post_injects_date(tmp_path):
    thought = {"number": 1, "body": "some raw thought"}
    thought_file = tmp_path / "thought.json"
    thought_file.write_text(json.dumps(thought))
    post_file = tmp_path / "2026-04-10.md"

    llm_response = (
        '---\ntitle: "Some Raw Thought"\n'
        "date: YYYY-MM-DD\ndraft: false\n---\n\nSome raw thought.\n"
    )

    with patch("agents.writing_agent.ModelSelector") as MockSelector, \
         patch("agents.writing_agent.LLMClient") as MockClient:
        MockSelector.return_value.fetch_free_models.return_value = [{"id": "test-model"}]
        MockClient.return_value.call.return_value = llm_response

        write_post(
            thought_path=str(thought_file),
            post_path=str(post_file),
            api_key="fake",
            date_str="2026-04-10",
        )

    content = post_file.read_text()
    assert "date: 2026-04-10" in content
