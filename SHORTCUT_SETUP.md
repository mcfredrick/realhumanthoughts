# Siri Shortcut Setup

One shortcut: **"Real Human Thought"** — say it to Siri, speak your thought, done.

## Prerequisites

- GitHub Personal Access Token (PAT) with `repo` scope
  - Create at: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
  - Required permissions: **Issues: Read and write** on the `realhumanthoughts` repo
- The shortcut is built in **Shortcuts.app on macOS**, then sent to iPhone

## Building the Shortcut (macOS recommended)

Open **Shortcuts.app** → **+** → name it `Real Human Thought`

Add these actions in order:

| # | Action | Settings |
|---|---|---|
| 1 | **Ask for Input** | Prompt: `What's the thought?` · Type: Text · Variable: **Thought** |
| 2 | **Get Contents of URL** | See below |
| 3 | **Show Notification** | Title: `Saved` · Body: **Thought** |

**Action 2 — Get Contents of URL:**
- URL: `https://api.github.com/repos/mcfredrick/realhumanthoughts/issues`
- Method: **POST**
- Headers:
  - `Authorization` → `token YOUR_PAT_HERE`
  - `Content-Type` → `application/json`
  - `Accept` → `application/vnd.github+json`
- Request Body: **JSON**
  - `title` → **Thought**
  - `body` → **Thought**

Replace `YOUR_PAT_HERE` with your actual token.

## Installing on iPhone

1. In Shortcuts.app on Mac: click shortcut name → **Share** → **Copy iCloud Link**
2. AirDrop or iMessage the link to your iPhone
3. Tap the link on iPhone → **Add Shortcut**
4. Open the shortcut → **⋯** → **Add to Siri** → say `Real Human Thought`

## Usage

> "Hey Siri, Real Human Thought"

Siri asks: *What's the thought?*

Speak your thought. Done — it's in the pool for tomorrow's post.
