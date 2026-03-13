# Example: Research to Threads

Research a topic with NotebookLM, then generate a Threads-optimized social post backed by real sources.

## Overview

```
Topic → NotebookLM research → Key insights → Threads post → (Optional) Publish
```

## Prerequisites

- notebooklm-skill installed and authenticated (see [docs/SETUP.md](../../docs/SETUP.md))
- (Optional) Threads API token for publishing (see threads-viral-agent setup)

## Step 1: Quick Research on a Topic

Use the `quick-research` command to create a notebook, find sources, and extract key insights in one step.

```bash
python scripts/notebooklm_client.py quick-research \
  --topic "MCP servers for Claude Code" \
  --depth 5
```

Expected output:

```json
{
  "topic": "MCP servers for Claude Code",
  "notebook_id": "nb_f6g7h8i9j0",
  "sources_found": 4,
  "research": {
    "summary": "MCP (Model Context Protocol) servers extend Claude Code with external tool access. Key developments include standardized tool definitions, stdio transport, and growing ecosystem of community servers.",
    "key_insights": [
      "MCP uses a client-server architecture where Claude Code is the client and tools are exposed by servers",
      "Transport options: stdio (local) and SSE (remote), with stdio being the default for local tools",
      "The ecosystem has grown to 100+ community servers covering databases, APIs, file systems, and more",
      "Configuration lives in .mcp.json at the project root",
      "Security model: servers run locally with the user's permissions"
    ],
    "notable_facts": [
      "MCP was open-sourced by Anthropic in late 2024",
      "Claude Code, Cursor, Windsurf, and Gemini CLI all support MCP",
      "The protocol supports tool discovery, resource access, and prompt templates"
    ],
    "sources": [
      {"url": "https://modelcontextprotocol.io/docs", "title": "MCP Documentation"},
      {"url": "https://docs.anthropic.com/claude-code/mcp", "title": "Claude Code MCP Guide"},
      {"url": "https://github.com/modelcontextprotocol/servers", "title": "MCP Servers Repository"},
      {"url": "https://www.anthropic.com/news/model-context-protocol", "title": "MCP Announcement"}
    ]
  }
}
```

## Step 2: Generate a Threads Post

Transform the research into a Threads-optimized post (500 characters, conversational tone, no URLs in body).

```bash
python scripts/notebooklm_client.py generate \
  --notebook "MCP servers for Claude Code" \
  --format threads \
  --tone conversational
```

Expected output:

```json
{
  "platform": "threads",
  "post": {
    "text": "MCP servers are quietly becoming the most important feature in AI coding tools.\n\nThe idea: your AI assistant can call external tools — databases, APIs, file search — through a standard protocol.\n\nClaude Code, Cursor, Gemini CLI all support it now.\n\n100+ community servers and growing.",
    "character_count": 289,
    "link_comment": "Deep dive on MCP: https://modelcontextprotocol.io/docs",
    "hashtags": []
  },
  "research_backing": {
    "claims_verified": 4,
    "sources_cited": 3
  }
}
```

Note: The post body avoids URLs (which reduce reach on Threads). The link goes in a separate reply comment.

## Step 3: Review and Edit

Before publishing, review the generated post:

- Is every claim backed by the research?
- Does the tone match your voice?
- Is it under 500 characters?
- Would you engage with this post?

Edit as needed. The research JSON is available for fact-checking.

## Step 4: (Optional) Publish to Threads

If you have a Threads API token configured:

```bash
# Publish the post
python scripts/notebooklm_client.py publish \
  --platform threads \
  --account your-account \
  --text "MCP servers are quietly becoming the most important feature in AI coding tools.

The idea: your AI assistant can call external tools — databases, APIs, file search — through a standard protocol.

Claude Code, Cursor, Gemini CLI all support it now.

100+ community servers and growing." \
  --link-comment "Deep dive on MCP: https://modelcontextprotocol.io/docs"
```

Expected output:

```json
{
  "status": "published",
  "post_id": "12345678901234567",
  "url": "https://www.threads.net/@your-account/post/abc123",
  "link_comment_id": "12345678901234568"
}
```

Or use the threads-viral-agent directly:

```bash
python scripts/threads_api.py publish \
  --account cw \
  --text "Your post text here" \
  --link-comment "https://link.com"
```

## Alternative: One-Command Pipeline

Combine research and generation in a single command:

```bash
python scripts/notebooklm_client.py pipeline \
  --topic "MCP servers for Claude Code" \
  --platforms threads \
  --tone conversational \
  --dry-run  # Preview without publishing
```

## Tips

- **Keep posts under 300 characters for best engagement.** Threads rewards concise, punchy content.
- **Never put URLs in the post body.** Use `--link-comment` to add a link as the first reply.
- **Lead with a bold claim.** The research gives you confidence to make strong, accurate statements.
- **One insight per post.** Save the other insights for follow-up posts throughout the week.
- **Use `--dry-run` first.** Always preview before publishing.

## Next Steps

- [Research to Article](../research-to-article/) — Turn research into long-form content
- [Trend to Content](../trend-to-content/) — Start from what's trending instead of a manual topic
