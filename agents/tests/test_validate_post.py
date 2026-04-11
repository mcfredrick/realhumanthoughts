import pytest
from agents.validate_post import validate


def test_valid_post(tmp_path):
    p = tmp_path / "2026-04-10.md"
    p.write_text(
        '---\ntitle: "A Thought"\ndate: 2026-04-10\ndraft: false\n---\n\nSome content here.\n'
    )
    assert validate(str(p)) is True


def test_missing_frontmatter(tmp_path):
    p = tmp_path / "2026-04-10.md"
    p.write_text("Just some text with no frontmatter.\n")
    assert validate(str(p)) is False


def test_missing_title(tmp_path):
    p = tmp_path / "2026-04-10.md"
    p.write_text(
        '---\ndate: 2026-04-10\ndraft: false\n---\n\nSome content here.\n'
    )
    assert validate(str(p)) is False


def test_empty_body(tmp_path):
    p = tmp_path / "2026-04-10.md"
    p.write_text(
        '---\ntitle: "A Thought"\ndate: 2026-04-10\ndraft: false\n---\n\n   \n'
    )
    assert validate(str(p)) is False


def test_title_must_be_nonempty_string(tmp_path):
    p = tmp_path / "2026-04-10.md"
    p.write_text(
        '---\ntitle: ""\ndate: 2026-04-10\ndraft: false\n---\n\nSome content.\n'
    )
    assert validate(str(p)) is False
