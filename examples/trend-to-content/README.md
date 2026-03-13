# Example: Trending Topic to Content

Use trend-pulse to discover what's trending, research the top topic with NotebookLM, and generate content for multiple platforms.

## Overview

```
trend-pulse discovery → Pick top topic → NotebookLM research → Multi-platform content
```

## Prerequisites

- notebooklm-skill installed and authenticated (see [docs/SETUP.md](../../docs/SETUP.md))
- [trend-pulse](https://github.com/anthropics/trend-pulse) running (MCP server or CLI)

## Step 1: Discover Trending Topics

Fetch trending topics from multiple sources.

```bash
python scripts/notebooklm_client.py trending \
  --geo TW \
  --count 10
```

Expected output:

```json
{
  "geo": "TW",
  "timestamp": "2026-03-14T08:00:00Z",
  "topics": [
    {
      "rank": 1,
      "title": "Claude Code 2.0 Released",
      "source": "hacker_news",
      "score": 482,
      "url": "https://www.anthropic.com/news/claude-code-2",
      "related_urls": [
        "https://news.ycombinator.com/item?id=12345678",
        "https://www.reddit.com/r/ClaudeAI/comments/abc123"
      ]
    },
    {
      "rank": 2,
      "title": "Apple WWDC 2026 Announcements",
      "source": "google_trends",
      "score": 350,
      "url": "https://developer.apple.com/wwdc26/"
    },
    {
      "rank": 3,
      "title": "Open Source AI Models Benchmark",
      "source": "reddit",
      "score": 275,
      "url": "https://huggingface.co/spaces/open-llm-leaderboard"
    }
  ]
}
```

If trend-pulse is running as an MCP server, you can also use it directly from Claude Code by asking "What's trending in Taiwan today?"

## Step 2: Research the Top Topic

Take the top trending topic and run deep research on it.

```bash
python scripts/notebooklm_client.py quick-research \
  --topic "Claude Code 2.0 Released" \
  --sources \
    "https://www.anthropic.com/news/claude-code-2" \
    "https://news.ycombinator.com/item?id=12345678" \
    "https://www.reddit.com/r/ClaudeAI/comments/abc123" \
  --depth 5
```

Expected output:

```json
{
  "topic": "Claude Code 2.0 Released",
  "notebook_id": "nb_k1l2m3n4o5",
  "sources_found": 3,
  "research": {
    "summary": "Claude Code 2.0 introduces background agents, improved MCP support, and a new multi-file editing mode. Community reception is largely positive with some concerns about pricing changes.",
    "key_insights": [
      "Background agents can run tasks autonomously while the developer works on other things",
      "Multi-file editing mode handles cross-file refactors in a single operation",
      "MCP server management is now built into the UI",
      "Pricing moved to a usage-based model",
      "Performance benchmarks show 40% faster task completion vs. 1.x"
    ],
    "notable_facts": [
      "Available on all plans including free tier (with limits)",
      "Background agents require explicit permission grants",
      "Extension ecosystem grew to 500+ MCP servers"
    ],
    "community_sentiment": {
      "positive": ["faster", "background agents are game-changing", "MCP support"],
      "negative": ["pricing concerns", "context window still limited"],
      "neutral": ["migration from 1.x is straightforward"]
    }
  }
}
```

## Step 3: Generate Multi-Platform Content

Generate content tailored for each platform in one command.

```bash
python scripts/notebooklm_client.py generate \
  --notebook "Claude Code 2.0 Released" \
  --platforms threads,blog,newsletter \
  --output output/
```

Expected output:

```json
{
  "notebook": "Claude Code 2.0 Released",
  "generated": {
    "threads": {
      "file": "output/threads-post.txt",
      "text": "Claude Code 2.0 just dropped and the killer feature is background agents.\n\nTell it what to do, go work on something else, come back to a finished PR.\n\nAlso: multi-file refactors in one shot, built-in MCP server management.\n\n40% faster than 1.x in benchmarks.",
      "character_count": 263,
      "link_comment": "Full announcement: https://www.anthropic.com/news/claude-code-2"
    },
    "blog": {
      "file": "output/blog-draft.md",
      "title": "Claude Code 2.0: Background Agents, Multi-File Editing, and What It Means for Developers",
      "word_count": 1200,
      "sections": ["Introduction", "Background Agents", "Multi-File Editing", "MCP Improvements", "Pricing Changes", "Community Reception", "Conclusion"]
    },
    "newsletter": {
      "file": "output/newsletter-section.md",
      "title": "This Week: Claude Code 2.0",
      "word_count": 350,
      "format": "newsletter-item"
    }
  }
}
```

## Step 4: Review and Publish

Each file is saved to the `output/` directory. Review them before publishing.

```bash
# Preview all generated content
ls output/
# threads-post.txt
# blog-draft.md
# newsletter-section.md

# Publish the Threads post (with dry-run first)
python scripts/notebooklm_client.py publish \
  --platform threads \
  --file output/threads-post.txt \
  --dry-run

# When satisfied, publish for real
python scripts/notebooklm_client.py publish \
  --platform threads \
  --file output/threads-post.txt \
  --account your-account \
  --link-comment "https://www.anthropic.com/news/claude-code-2"
```

## Alternative: Full Automated Pipeline

Run the entire flow from trending topic discovery to content generation in one command:

```bash
python scripts/notebooklm_client.py pipeline \
  --trend "top" \
  --geo TW \
  --platforms threads,blog,newsletter \
  --output output/ \
  --dry-run
```

This will:
1. Fetch trending topics from trend-pulse
2. Pick the top topic
3. Create a NotebookLM notebook with related URLs
4. Run 5 research queries
5. Generate platform-specific content
6. Save to `output/` (or publish with `--publish` flag)

## Weekly Digest Variant

For a weekly content digest from multiple trending topics:

```bash
# Research the top 5 trends
python scripts/notebooklm_client.py pipeline \
  --trend "top-5" \
  --geo TW \
  --platforms newsletter \
  --output output/weekly/ \
  --style digest
```

This creates a notebook per topic, researches each, and compiles a digest-format newsletter section covering all 5 topics.

## Tips

- **Research before the crowd.** Trending topics have a 24-48 hour window of peak interest. Research early, publish fast.
- **Add your own sources.** Use `--sources` alongside the trend's URLs to include your unique perspective.
- **Platform priority matters.** If a topic is visually compelling, prioritize Instagram. If it's discussion-worthy, lead with Threads.
- **Batch your content week.** Run the pipeline on Monday for 5 topics, schedule posts throughout the week.
- **Check community sentiment.** The `community_sentiment` field in research output helps you calibrate your tone.

## Next Steps

- [Research to Article](../research-to-article/) — Deep dive on a single topic
- [Research to Threads](../research-to-threads/) — Optimize for social engagement
