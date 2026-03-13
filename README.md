# notebooklm-skill

> NotebookLM does the research, Claude writes the content.

The only tool that connects trending topic discovery -> NotebookLM deep research -> AI content creation -> multi-platform publishing. Works as a Claude Code Skill or standalone MCP server.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this?

**notebooklm-skill** bridges NotebookLM's research capabilities with Claude's content generation. Feed it URLs, PDFs, or trending topics. It creates a NotebookLM notebook, runs deep research queries, and hands structured findings to Claude for polished output -- articles, social posts, newsletters, podcasts, or any format you need.

Built on [notebooklm-py](https://pypi.org/project/notebooklm-py/) v0.3.4 -- pure async Python, no OAuth setup needed.

```
Sources (URLs, PDFs)          NotebookLM                Claude               Artifacts & Platforms
+-----------------+    +------------------+    +-----------------+    +----------------------+
| Web articles    |--->| Create notebook  |--->| Draft article   |--->| Blog / CMS           |
| Research papers |    | Add sources      |    | Social posts    |    | Threads / X          |
| YouTube videos  |    | Ask questions    |    | Newsletter      |    | Newsletter           |
| Trending topics |    | Extract insights |    | Any format      |    | Any platform         |
+-----------------+    +------------------+    +-----------------+    +----------------------+
     Phase 1                Phase 2                Phase 3                  Phase 4
                                |
                                v
                       +------------------+
                       | Generate artifacts|
                       | Audio (podcast)   |
                       | Video             |
                       | Slides            |
                       | Report            |
                       | Quiz              |
                       | Flashcards        |
                       | Mind map          |
                       | Infographic       |
                       | Data table        |
                       | Study guide       |
                       +------------------+
                            Phase 2b
```

## Quick Start

```bash
# 1. Install
git clone https://github.com/anthropics/notebooklm-skill.git
cd notebooklm-skill
pip install -r requirements.txt   # installs notebooklm-py v0.3.4

# 2. Authenticate with Google (one-time, opens browser)
python3 -m notebooklm login
# -> Opens Chromium, sign in to Google
# -> Saves session to ~/.notebooklm/storage_state.json
# -> All subsequent calls use pure HTTP (no browser needed)

# 3. Create your first notebook from a URL
python scripts/notebooklm_client.py create \
  --title "My Research" \
  --sources https://example.com/article

# 4. Ask research questions
python scripts/notebooklm_client.py ask \
  --notebook "My Research" \
  --query "What are the key findings?"

# 5. Generate an audio podcast from the research
python scripts/notebooklm_client.py generate \
  --notebook "My Research" \
  --type audio

# 6. Verify auth status anytime
python scripts/auth_helper.py verify
```

See [docs/SETUP.md](docs/SETUP.md) for the full setup guide.

## Authentication

notebooklm-py uses browser-based Google login (no OAuth client ID needed):

| Step | Command | What happens |
|------|---------|-------------|
| **Login** | `python3 -m notebooklm login` | Opens headed Chromium, user logs into Google |
| **Session storage** | Automatic | Saved to `~/.notebooklm/storage_state.json` |
| **Subsequent use** | `NotebookLMClient.from_storage()` | Reads saved session, pure HTTP calls |
| **Verify** | `python scripts/auth_helper.py verify` | Loads client + calls `notebooks.list()` |
| **Clear** | `python scripts/auth_helper.py clear` | Removes `~/.notebooklm/` directory |

Session typically lasts weeks. Re-run `login` if you get authentication errors.

## Two Ways to Use

| | **Claude Code Skill** | **MCP Server** |
|---|---|---|
| **Best for** | Claude Code users who want NotebookLM in their workflow | Any MCP-compatible client (Cursor, Gemini CLI, etc.) |
| **Setup** | Copy skill to `.claude/skills/` | Add server to MCP config |
| **Invocation** | Claude auto-detects when relevant | Tools appear in client tool list |
| **Config** | `SKILL.md` + `.env` | `mcp.json` + `.env` |
| **Dependencies** | Python 3.10+, notebooklm-py | Python 3.10+, notebooklm-py |

## Features

| Feature | Description | Status |
|---|---|---|
| **Notebook CRUD** | Create, list, delete notebooks | Available |
| **Source ingestion** | Add URLs, PDFs, YouTube links, plain text | Available |
| **Research queries** | Ask questions against notebook sources with citations | Available |
| **Structured extraction** | Get key facts, arguments, timelines | Available |
| **Content generation** | Use research output as context for Claude | Available |
| **Batch operations** | Process multiple sources or queries at once | Available |
| **trend-pulse integration** | Auto-discover trending topics to research | Available |
| **threads-viral-agent integration** | Publish research-backed social posts | Available |

### Artifact Generation (10 types)

| Artifact | Format | Description |
|---|---|---|
| **Audio** | MP3 | AI-generated podcast discussion |
| **Video** | MP4 | Video summary with visuals |
| **Slides** | PDF | Presentation deck |
| **Report** | PDF | Comprehensive written report |
| **Quiz** | JSON | Multiple-choice assessment questions |
| **Flashcards** | JSON | Study flashcard deck |
| **Mind map** | SVG | Visual concept map |
| **Infographic** | PNG | Visual data summary |
| **Data table** | CSV | Structured data extraction |
| **Study guide** | PDF | Structured learning material |

All artifacts support language selection (e.g., `--language zh-TW`).

## Architecture

```
+---------------------------------------------------------------+
|                      notebooklm-skill                          |
|                                                                |
|  +---------+  +--------------+  +----------+  +------------+  |
|  | Phase 1 |  |   Phase 2    |  |  Phase 3 |  |  Phase 4   |  |
|  | Collect  |->|  Research    |->| Generate  |->|  Publish   |  |
|  +---------+  +--------------+  +----------+  +------------+  |
|      |              |                |               |         |
|  +--------+  +-------------+  +-----------+  +-----------+    |
|  | URLs   |  | NotebookLM  |  |  Claude    |  | Threads   |    |
|  | PDFs   |  | (via        |  |  Content   |  | Blog      |    |
|  | RSS    |  |  notebooklm |  |  Engine    |  | Email     |    |
|  | Trends |  |  -py 0.3.4) |  |            |  | CMS       |    |
|  +--------+  | - notebooks |  +-----------+  +-----------+    |
|              | - sources   |        |                          |
|              | - chat/ask  |  +-----------+                    |
|              | - artifacts |  | Artifacts |                    |
|              +-------------+  | audio     |                    |
|                               | video     |                    |
|                               | slides    |                    |
|                               | report    |                    |
|                               | quiz      |                    |
|                               | flashcards|                    |
|                               | mind-map  |                    |
|                               | infographic|                   |
|                               | data-table|                    |
|                               | study-guide|                   |
|                               +-----------+                    |
|                                                                |
|  +-----------------------------------------------------------+ |
|  |  Interfaces                                                | |
|  |  +-- scripts/          CLI tools (notebooklm-py direct)   | |
|  |  +-- mcp-server/       MCP protocol server                | |
|  |  +-- SKILL.md          Claude Code skill definition        | |
|  +-----------------------------------------------------------+ |
+---------------------------------------------------------------+
         ^                                          ^
         |                                          |
   +-----------+                             +-----------+
   |trend-pulse|                             |threads-   |
   |(optional) |                             |viral-agent|
   +-----------+                             |(optional) |
                                             +-----------+
```

## Usage Examples

### 1. Research to Article

Take multiple sources, research them, and generate a structured article.

```bash
# Full pipeline (creates notebook, researches, drafts article)
python scripts/pipeline.py research-to-article \
  --sources "https://arxiv.org/abs/2401.00001" \
            "https://blog.example.com/ai-agents" \
            "https://youtube.com/watch?v=xyz" \
  --title "AI Agent Survey"

# Or step-by-step with the client:

# Create a notebook with 3 sources
python scripts/notebooklm_client.py create \
  --title "AI Agent Survey" \
  --sources "https://arxiv.org/abs/2401.00001" \
            "https://blog.example.com/ai-agents" \
            "https://youtube.com/watch?v=xyz"

# Ask research questions
python scripts/notebooklm_client.py ask \
  --notebook "AI Agent Survey" \
  --query "What are the main agent architectures?"

python scripts/notebooklm_client.py ask \
  --notebook "AI Agent Survey" \
  --query "How do agents handle tool use?"

python scripts/notebooklm_client.py ask \
  --notebook "AI Agent Survey" \
  --query "What are the unsolved challenges?"
```

### 2. Research to Social Posts

Research a topic and generate platform-optimized social posts.

```bash
python scripts/pipeline.py research-to-social \
  --sources "https://example.com/ai-news" \
  --platform threads \
  --title "AI News This Week"
```

### 3. Trending Topic to Content Pipeline

Combine with trend-pulse to automate the full discovery-to-publish pipeline.

```bash
python scripts/pipeline.py trend-to-content \
  --geo TW \
  --count 5 \
  --platform threads
```

### 4. Batch RSS Digest

Turn an RSS feed into a newsletter-style digest.

```bash
python scripts/pipeline.py batch-digest \
  --rss "https://example.com/feed.xml" \
  --title "Weekly AI Digest" \
  --max-entries 15 \
  --qa-count 5
```

### 5. Generate All Artifacts

Create a notebook and generate all 10 artifact types.

```bash
# Generate everything
python scripts/pipeline.py generate-all \
  --sources "https://example.com/article1" \
            "https://example.com/article2" \
  --title "Research" \
  --output-dir ./output \
  --language zh-TW

# Or generate specific types only
python scripts/pipeline.py generate-all \
  --sources "https://example.com/article" \
  --types audio slides report \
  --output-dir ./output

# Generate audio directly via client
python scripts/notebooklm_client.py generate \
  --notebook "Research" \
  --type audio
```

## Pipeline Workflows

| Workflow | Input | Output | Steps |
|---|---|---|---|
| `research-to-article` | URLs, text | Article draft JSON | Create notebook -> 5 research questions -> article draft |
| `research-to-social` | URLs, text | Social post draft | Create notebook -> summarize -> platform-specific post |
| `trend-to-content` | Geo, count | Content per trend | Fetch trends -> create notebooks -> research -> draft |
| `batch-digest` | RSS URL | Newsletter digest | Fetch RSS -> create notebook -> digest + Q&A |
| `generate-all` | URLs, text | Audio, video, PDF, etc. | Create notebook -> generate all artifacts -> download |

## MCP Server Setup

The MCP server exposes NotebookLM operations as tools accessible by any MCP-compatible client.

### Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": ["-m", "mcp-server"],
      "cwd": "/path/to/notebooklm-skill"
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": ["-m", "mcp-server"],
      "cwd": "/path/to/notebooklm-skill"
    }
  }
}
```

### Gemini CLI

Add to your Gemini CLI settings:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": ["-m", "mcp-server"],
      "cwd": "/path/to/notebooklm-skill"
    }
  }
}
```

## Claude Code Skill Setup

To install as a Claude Code skill, copy the skill directory into your project:

```bash
# From your project root
mkdir -p .claude/skills/notebooklm
cp /path/to/notebooklm-skill/SKILL.md .claude/skills/notebooklm/
cp /path/to/notebooklm-skill/scripts/*.py .claude/skills/notebooklm/scripts/
cp /path/to/notebooklm-skill/requirements.txt .claude/skills/notebooklm/

# Authenticate (one-time)
python3 -m notebooklm login
```

Claude will automatically detect the skill when you ask about research, NotebookLM, or content creation from sources.

## Configuration

Create a `.env` file in the project root (or skill directory):

```bash
# Optional: Default settings
NOTEBOOKLM_DEFAULT_DEPTH=5          # Number of research queries (1-10)
NOTEBOOKLM_DEFAULT_FORMAT=json      # Output format: json, markdown, text
NOTEBOOKLM_MAX_SOURCES=50           # Max sources per notebook

# Optional: trend-pulse integration
TREND_PULSE_URL=http://localhost:3002  # trend-pulse MCP server URL

# Optional: threads-viral-agent integration
THREADS_TOKEN=your-threads-token       # For auto-publishing to Threads
```

Note: No Google OAuth credentials needed. Auth is handled via browser login (`python3 -m notebooklm login`).

## API Reference

### CLI Commands

| Command | Description |
|---|---|
| `create` | Create a notebook with URL/text sources |
| `ask` | Ask a research question against a notebook (returns text + citations) |
| `generate` | Generate an artifact (audio, video, slides, etc.) from a notebook |
| `list` | List all notebooks |
| `delete` | Delete a notebook |

### Pipeline Workflows

| Workflow | Description |
|---|---|
| `research-to-article` | Sources -> notebook -> 5 research questions -> article draft |
| `research-to-social` | Sources -> notebook -> summary -> platform-specific social post |
| `trend-to-content` | Fetch trends -> create notebooks -> research -> content per trend |
| `batch-digest` | RSS feed -> notebook -> newsletter digest + Q&A |
| `generate-all` | Sources -> notebook -> generate + download all artifact types |

### MCP Tools (15)

| Tool | Description |
|---|---|
| `notebooklm_create` | Create a notebook with sources |
| `notebooklm_add_source_url` | Add a URL source to an existing notebook |
| `notebooklm_add_source_text` | Add a text source to an existing notebook |
| `notebooklm_ask` | Ask a question against a notebook (returns text + citations) |
| `notebooklm_list` | List all notebooks |
| `notebooklm_delete` | Delete a notebook |
| `notebooklm_generate_audio` | Generate audio podcast from notebook |
| `notebooklm_generate_video` | Generate video summary from notebook |
| `notebooklm_generate_slides` | Generate presentation slides from notebook |
| `notebooklm_generate_report` | Generate written report from notebook |
| `notebooklm_generate_quiz` | Generate quiz questions from notebook |
| `notebooklm_generate_flashcards` | Generate flashcard deck from notebook |
| `notebooklm_generate_mind_map` | Generate mind map from notebook |
| `notebooklm_generate_infographic` | Generate infographic from notebook |
| `notebooklm_download_artifact` | Download a generated artifact by type |
| `notebooklm_auth_status` | Check authentication status |

For detailed API docs, see [docs/](docs/).

## Integrations

### trend-pulse

[trend-pulse](https://github.com/anthropics/trend-pulse) provides real-time trending topic discovery. When configured, notebooklm-skill can automatically:

- Fetch trending topics from 7 sources (Google Trends, HN, Reddit, etc.)
- Create NotebookLM notebooks from top trending URLs
- Feed research results into the content pipeline

### threads-viral-agent

When paired with a Threads publishing tool, the pipeline extends to auto-publish research-backed social posts with engagement optimization.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/anthropics/notebooklm-skill.git
cd notebooklm-skill
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Testing & linting

# Authenticate
python3 -m notebooklm login

# Run tests
python -m pytest tests/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
