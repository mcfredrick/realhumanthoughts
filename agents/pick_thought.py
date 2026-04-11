"""
Pick a random thought from the GitHub Issues pool.

- Closes any issues not authored by OWNER
- Picks one random valid issue
- Writes thought.json: {number, body}
- Exits 0 with THOUGHT_SELECTED=false in GITHUB_ENV if no valid issues
- Exits 0 with THOUGHT_SELECTED=true + THOUGHT_NUMBER=N in GITHUB_ENV otherwise
"""

import json
import os
import random
import subprocess
import sys

OWNER = "mcfredrick"


def gh(args: list[str]) -> str:
    result = subprocess.run(["gh"] + args, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def set_env(key: str, value: str) -> None:
    env_file = os.environ.get("GITHUB_ENV")
    if env_file:
        with open(env_file, "a") as f:
            f.write(f"{key}={value}\n")
    else:
        # Local run: just print
        print(f"[env] {key}={value}")


def main() -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", f"{OWNER}/realhumanthoughts")

    raw = gh(["issue", "list", "--repo", repo, "--json", "number,body,author", "--limit", "100"])
    issues = json.loads(raw)

    valid = []
    for issue in issues:
        if issue["author"]["login"] != OWNER:
            gh(["issue", "close", str(issue["number"]), "--repo", repo,
                "--comment", "Closed: not authored by repo owner."])
        else:
            valid.append(issue)

    if not valid:
        print("No thoughts in pool. Skipping today.", file=sys.stderr)
        set_env("THOUGHT_SELECTED", "false")
        return

    thought = random.choice(valid)
    with open("thought.json", "w") as f:
        json.dump({"number": thought["number"], "body": thought["body"]}, f)

    set_env("THOUGHT_SELECTED", "true")
    set_env("THOUGHT_NUMBER", str(thought["number"]))
    print(f"Selected issue #{thought['number']}")


if __name__ == "__main__":
    main()
