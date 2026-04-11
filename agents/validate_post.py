import re
import sys


def validate(path: str) -> bool:
    text = open(path).read()
    if not text.startswith("---"):
        return False
    end = text.find("---", 3)
    if end == -1:
        return False
    frontmatter = text[3:end]
    body = text[end + 3:].strip()
    has_title = bool(re.search(r'^title:\s+".+?"', frontmatter, re.MULTILINE))
    has_body = bool(body)
    return has_title and has_body


if __name__ == "__main__":
    path = sys.argv[1]
    if validate(path):
        print(f"✓ {path} is valid")
    else:
        print(f"✗ {path} failed validation", file=sys.stderr)
        sys.exit(1)
