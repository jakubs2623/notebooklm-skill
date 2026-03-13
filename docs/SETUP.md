# Setup Guide

Complete setup instructions for notebooklm-skill.

---

## Prerequisites

- **Python 3.10+** (`python3 --version`)
- **pip** (`pip --version`)
- **A Google account** with access to [NotebookLM](https://notebooklm.google.com/)

## 1. Install Dependencies

```bash
git clone https://github.com/anthropics/notebooklm-skill.git
cd notebooklm-skill
pip install -r requirements.txt
```

Verify the install:

```bash
python scripts/notebooklm_client.py --version
```

## 2. Google Authentication

notebooklm-skill uses Google OAuth to access NotebookLM on your behalf. You need to create OAuth credentials and authorize the app once.

### Step 2a: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** > **New Project**
3. Name it `notebooklm-skill` (or anything you prefer)
4. Click **Create**

### Step 2b: Enable the NotebookLM API

1. In your new project, go to **APIs & Services** > **Library**
2. Search for **NotebookLM API**
3. Click **Enable**

### Step 2c: Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **+ Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - **User Type**: External
   - **App name**: `notebooklm-skill`
   - **Scopes**: Add `https://www.googleapis.com/auth/notebooklm`
   - **Test users**: Add your Google email
4. For the OAuth client:
   - **Application type**: Desktop app
   - **Name**: `notebooklm-skill`
5. Click **Create**
6. Download the JSON file

### Step 2d: Run the Auth Helper

```bash
# Point to your downloaded credentials
python scripts/auth_helper.py setup --credentials ~/Downloads/client_secret_*.json
```

This will:
1. Copy credentials to `~/.config/notebooklm-skill/credentials.json`
2. Open your browser for Google authorization
3. Store the refresh token locally at `~/.config/notebooklm-skill/token.json`

Expected output:

```
[1/3] Copying credentials to ~/.config/notebooklm-skill/credentials.json
[2/3] Opening browser for authorization...
      → Authorize the app with your Google account
[3/3] Authorization successful!

Token saved to: ~/.config/notebooklm-skill/token.json
Authenticated as: you@gmail.com

Setup complete. Try: python scripts/notebooklm_client.py list
```

### Step 2e: Create the .env File

```bash
cp .env.example .env
```

Edit `.env` and set:

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_CREDENTIALS_PATH=~/.config/notebooklm-skill/credentials.json
```

## 3. Verify Setup

```bash
# List your existing NotebookLM notebooks (may be empty)
python scripts/notebooklm_client.py list

# Create a test notebook
python scripts/notebooklm_client.py create \
  --sources "https://en.wikipedia.org/wiki/Large_language_model" \
  --name "Test Notebook"

# Query it
python scripts/notebooklm_client.py query \
  --notebook "Test Notebook" \
  --questions "What is a large language model?"

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
      "cwd": "/absolute/path/to/notebooklm-skill",
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "~/.config/notebooklm-skill/credentials.json"
      }
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

If you prefer to use notebooklm-skill as a Claude Code skill (no MCP server required):

```bash
# From your project root
mkdir -p .claude/skills/notebooklm
cp /path/to/notebooklm-skill/SKILL.md .claude/skills/notebooklm/
cp -r /path/to/notebooklm-skill/scripts/ .claude/skills/notebooklm/scripts/
cp /path/to/notebooklm-skill/requirements.txt .claude/skills/notebooklm/

# Set up credentials
cp .claude/skills/notebooklm/.env.example .claude/skills/notebooklm/.env
# Edit .env with your credentials
```

Claude will auto-detect the skill. Trigger it by asking about NotebookLM research or content creation.

## 6. (Optional) trend-pulse Integration

[trend-pulse](https://github.com/anthropics/trend-pulse) provides trending topic discovery. To enable the integration:

1. Install and run trend-pulse (see its README)
2. Add to your `.env`:

```bash
TREND_PULSE_URL=http://localhost:3002
```

3. Verify:

```bash
python scripts/notebooklm_client.py trending --geo TW --count 5
```

## 7. Troubleshooting

### "Google credentials not found"

```
Error: No credentials found at ~/.config/notebooklm-skill/credentials.json
```

**Fix**: Run `python scripts/auth_helper.py setup --credentials /path/to/your/client_secret.json` again.

### "Token expired"

```
Error: Token has been expired or revoked
```

**Fix**: Delete the cached token and re-authorize:

```bash
rm ~/.config/notebooklm-skill/token.json
python scripts/auth_helper.py setup
```

### "NotebookLM API not enabled"

```
Error: API [notebooklm.googleapis.com] not enabled for project
```

**Fix**: Enable the NotebookLM API in [Google Cloud Console](https://console.cloud.google.com/apis/library) for your project.

### "Quota exceeded"

```
Error: Quota exceeded for NotebookLM API
```

**Fix**: NotebookLM has rate limits. Wait a few minutes and try again. For batch operations, use `--delay` flag:

```bash
python scripts/notebooklm_client.py query \
  --notebook "My Research" \
  --questions "Q1" "Q2" "Q3" \
  --delay 5  # 5 seconds between queries
```

### "MCP server not connecting"

**Fix**: Check that:
1. The `cwd` path in your MCP config is an absolute path
2. Python 3.10+ is available at the `python` command in your shell
3. Dependencies are installed (`pip install -r requirements.txt`)
4. `.env` file exists in the project root with valid credentials

### "Permission denied on auth"

If the browser auth flow shows "This app isn't verified":
1. Click **Advanced** > **Go to notebooklm-skill (unsafe)**
2. This is expected for development OAuth apps
3. For production use, complete Google's OAuth verification process

### Need More Help?

Open an issue at [github.com/anthropics/notebooklm-skill/issues](https://github.com/anthropics/notebooklm-skill/issues).
