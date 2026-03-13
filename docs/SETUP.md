# Setup Guide

Complete setup instructions for notebooklm-skill.

**[繁體中文版](SETUP.zh-TW.md)**

---

## Prerequisites

- **Python 3.10+** (`python3 --version`)
- **pip** (`pip --version`)
- **A Google account** with access to [NotebookLM](https://notebooklm.google.com/)

## 1. Install Dependencies

```bash
git clone https://github.com/claude-world/notebooklm-skill.git
cd notebooklm-skill
pip install -r requirements.txt
```

Verify the install:

```bash
python scripts/notebooklm_client.py list
```

## 2. Google Authentication

notebooklm-py uses browser-based Google login. No OAuth Client ID or Google Cloud project needed.

### Step 2a: Run Login

```bash
python3 -m notebooklm login
```

This will:
1. Open a Chromium browser
2. Show the Google login page — sign in with your Google account
3. Automatically save the session to `~/.notebooklm/storage_state.json`
4. All subsequent operations use pure HTTP calls (no browser needed)

### Step 2b: Verify Login

```bash
python scripts/auth_helper.py verify
```

Expected output:

```
[auth] Verifying NotebookLM authentication...
[auth] Authentication OK — found N notebooks.
```

### Step 2c: (Optional) Create .env

```bash
cp .env.example .env
```

Edit `.env` to set defaults:

```bash
# Optional: Default settings
NOTEBOOKLM_DEFAULT_DEPTH=5
NOTEBOOKLM_DEFAULT_FORMAT=json
NOTEBOOKLM_MAX_SOURCES=50

# Optional: trend-pulse integration
TREND_PULSE_URL=http://localhost:3002

# Optional: threads-viral-agent integration
THREADS_TOKEN=your-threads-token
```

> **Note**: No Google API keys or OAuth credentials needed. Authentication is handled entirely via browser session.

## 3. Verify Setup

```bash
# List existing NotebookLM notebooks (may be empty)
python scripts/notebooklm_client.py list

# Create a test notebook
python scripts/notebooklm_client.py create \
  --title "Test Notebook" \
  --sources "https://en.wikipedia.org/wiki/Large_language_model"

# Ask a question
python scripts/notebooklm_client.py ask \
  --notebook "Test Notebook" \
  --query "What is a large language model?"

# Clean up
python scripts/notebooklm_client.py delete --notebook "Test Notebook"
```

If all commands succeed, your setup is complete.

## 4. (Optional) MCP Server Setup

The MCP server lets any MCP-compatible client (Claude Code, Cursor, Gemini CLI) use NotebookLM as a tool.

### Start the Server

```bash
python -m mcp-server
```

The server runs on stdio by default (standard MCP transport).

### Register with Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": ["-m", "mcp-server"],
      "cwd": "/absolute/path/to/notebooklm-skill"
    }
  }
}
```

Restart Claude Code. You should see `notebooklm` tools available.

### Register with Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": ["-m", "mcp-server"],
      "cwd": "/absolute/path/to/notebooklm-skill"
    }
  }
}
```

## 5. (Optional) Claude Code Skill Installation

```bash
mkdir -p .claude/skills/notebooklm
cp /path/to/notebooklm-skill/SKILL.md .claude/skills/notebooklm/
cp -r /path/to/notebooklm-skill/scripts/ .claude/skills/notebooklm/scripts/
cp /path/to/notebooklm-skill/requirements.txt .claude/skills/notebooklm/
```

Claude will auto-detect the skill when you mention NotebookLM research or content creation.

## 6. (Optional) trend-pulse Integration

[trend-pulse](https://github.com/claude-world/trend-pulse) provides trending topic discovery.

1. Install and run trend-pulse (see its README)
2. Add to your `.env`:

```bash
TREND_PULSE_URL=http://localhost:3002
```

## 7. Troubleshooting

### "Browser not opening"

```
Error: Browser not found
```

**Fix**: Install Playwright browsers:

```bash
python3 -m playwright install chromium
```

### "Session expired"

```
Error: Authentication failed
```

**Fix**: Re-login:

```bash
python scripts/auth_helper.py clear
python3 -m notebooklm login
```

### "MCP server not connecting"

**Fix**: Check that:
1. The `cwd` path in your MCP config is an absolute path
2. Python 3.10+ is available (`python --version`)
3. Dependencies are installed (`pip install -r requirements.txt`)

### "Artifact generation timeout"

Audio and video generation may take 5-10 minutes. If your client times out (600s), the artifact may still be generating on NotebookLM's servers. Try downloading later:

```bash
python scripts/notebooklm_client.py download \
  --notebook "Your Notebook" \
  --type audio \
  --output podcast.m4a
```

### "Audio won't play"

NotebookLM returns audio in MPEG-4 (M4A) format, not MP3. Use the `.m4a` extension:

```bash
# If saved as .mp3, just rename
mv podcast.mp3 podcast.m4a
```

### Need More Help?

Open an issue at [github.com/claude-world/notebooklm-skill/issues](https://github.com/claude-world/notebooklm-skill/issues).
