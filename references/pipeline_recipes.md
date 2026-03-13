# NotebookLM Pipeline Recipes

Common workflows combining NotebookLM research with content creation.
Each recipe includes the full command sequence, expected output, and tips.

---

## Recipe 1: Research a Topic and Write an Article

**Use case**: You have a topic idea and want to produce a well-researched blog post
backed by real sources.

### Commands

```bash
# Step 1: Create notebook with source URLs
python3 scripts/notebooklm_client.py create \
  --title "AI Agent Frameworks 2026" \
  --sources \
    "https://arxiv.org/abs/2401.12345" \
    "https://blog.openai.com/agents" \
    "https://docs.anthropic.com/agent-sdk" \
    "https://www.youtube.com/watch?v=abc123" \
  --wait

# Step 2: Get notebook description (AI overview + suggested questions)
python3 scripts/notebooklm_client.py describe \
  --notebook NOTEBOOK_ID

# Step 3: Ask research questions
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the main AI agent frameworks available in 2026?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "How do these frameworks compare in terms of capabilities?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the emerging trends and future directions?"

# Step 4: Generate a briefing doc for structured overview
python3 scripts/notebooklm_client.py generate report \
  --notebook NOTEBOOK_ID \
  --format briefing_doc

# Step 5: Full pipeline (combines steps 1-4)
python3 scripts/pipeline.py research-to-article \
  --sources "https://url1" "https://url2" "https://url3" \
  --topic "AI Agent Frameworks in 2026" \
  --questions \
    "What are the main frameworks?" \
    "How do they compare?" \
    "What trends are emerging?" \
  --output article.md
```

### Expected Output

- `article.md`: A 1000-2000 word markdown article with:
  - Introduction with hook
  - 3-5 sections covering key angles
  - Source citations inline (from NotebookLM answers)
  - Conclusion with takeaways
- Console: Research Q&A pairs with citation counts

### Tips

- **Start with 3-5 diverse sources** (mix of academic, blog, video) for balanced coverage.
- **Ask 3 questions minimum**: overview, comparison, and trends/future.
- **Use `--wait`** when adding sources to ensure they are processed before asking questions.
- **Review the notebook description first** -- it suggests great starting questions.
- The briefing doc from Step 4 provides a structured summary you can reference while writing.
- For technical topics, add the official documentation as a source for accuracy.

---

## Recipe 2: Monitor RSS Feeds and Produce Weekly Digest

**Use case**: Aggregate content from multiple RSS feeds or news sources into a
weekly curated digest with summaries and analysis.

### Commands

```bash
# Step 1: Create a weekly notebook
WEEK=$(date +%Y-W%V)
python3 scripts/notebooklm_client.py create \
  --title "Weekly Digest: $WEEK" \
  --sources \
    "https://news.ycombinator.com/rss" \
    "https://blog.anthropic.com/rss.xml" \
    "https://openai.com/blog/rss/" \
    "https://simonwillison.net/atom/everything/" \
    "https://www.theregister.com/software/ai/headlines.atom" \
  --wait

# Step 2: Ask for categorized summary
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "Categorize the top stories from these sources into: AI Models, Developer Tools, Industry News, and Research. List the 3 most important stories in each category."

# Step 3: Ask for trend analysis
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the common themes across all sources this week? What story had the most significance?"

# Step 4: Generate a structured report
python3 scripts/notebooklm_client.py generate report \
  --notebook NOTEBOOK_ID \
  --format custom \
  --prompt "Create a weekly digest newsletter with: 1) Top 5 stories with one-paragraph summaries, 2) Trend of the week, 3) Quick hits (5 notable but smaller stories), 4) What to watch next week."

# Step 5: Download the report
python3 scripts/notebooklm_client.py download report \
  --notebook NOTEBOOK_ID \
  --output "digest-$WEEK.md"

# Full pipeline version
python3 scripts/pipeline.py weekly-digest \
  --feeds feeds.json \
  --output "digest-$WEEK.md"
```

### Expected Output

- `digest-YYYY-WNN.md`: A structured newsletter with:
  - Top 5 stories with summaries
  - Trend analysis
  - Quick hits
  - Forward-looking section
- Each story links back to the original source

### Tips

- **RSS feeds as URL sources**: NotebookLM can extract content from RSS feed URLs.
- **Run every Monday**: Create a cron job or scheduled task for weekly automation.
- **Accumulate notebooks**: Keep weekly notebooks for historical trend analysis.
- **Use the custom report format** to match your newsletter template exactly.
- **For high-volume feeds**, limit to top stories by adding specific article URLs
  instead of feed URLs (use cf-browser or trend-pulse to pre-filter).

### feeds.json Example

```json
{
  "feeds": [
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss"},
    {"name": "Anthropic Blog", "url": "https://blog.anthropic.com/rss.xml"},
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/"},
    {"name": "The Register AI", "url": "https://www.theregister.com/software/ai/headlines.atom"}
  ],
  "max_sources_per_feed": 5,
  "date_range_days": 7
}
```

---

## Recipe 3: Trending Topics to Social Content

**Use case**: Discover what is trending in your niche, research it deeply using
NotebookLM, and produce platform-optimized social posts.

### Commands

```bash
# Step 1: Discover trending topics (requires trend-pulse MCP)
# Via MCP tool:
#   get_trending(sources="hackernews,reddit,google_trends", geo="TW", count=20)
# Or via CLI:
trend-pulse trending --geo TW --count 20 --sources hackernews,reddit

# Step 2: Pick a topic and find source URLs
# (Claude evaluates trends and selects the best topic for your niche)

# Step 3: Create notebook with trend sources
python3 scripts/notebooklm_client.py create \
  --title "Trending: Claude Code 2.0" \
  --sources \
    "https://news.ycombinator.com/item?id=12345" \
    "https://docs.anthropic.com/claude-code/changelog" \
    "https://x.com/AnthropicAI/status/..." \
  --wait

# Step 4: Research with targeted social-content questions
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the 3 most surprising or controversial aspects of this topic?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the practical implications for developers?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are people debating or disagreeing about?"

# Step 5: Claude writes social posts using research answers
# (Posts include platform-specific formatting and CTAs)

# Full pipeline version
python3 scripts/pipeline.py trend-to-content \
  --geo TW \
  --niche "AI/coding/tech" \
  --platforms threads instagram \
  --output content.json
```

### Expected Output

```json
{
  "trend": {"topic": "Claude Code 2.0", "source": "hackernews", "heat_score": 450},
  "posts": {
    "threads": "Claude Code 2.0 剛發布，3 個你必須知道的改變：\n\n1. ...\n\n你最期待哪個功能？",
    "instagram": "Claude Code 2.0: Everything You Need to Know\n\n...\n\n#ClaudeCode #AI #DevTools",
    "article": "# Claude Code 2.0: What Developers Need to Know\n\n..."
  }
}
```

### Tips

- **Ask "controversial" questions** -- social engagement comes from debate potential.
- **Focus on practical implications** -- "what does this mean for me?" drives saves/shares.
- **Threads posts under 500 chars** -- end with a question or A/B poll.
- **Instagram needs an image** -- generate a quote card from the strongest insight.
- **Post within 2-4 hours** of trend discovery for maximum relevance.
- **If combining with threads-viral-agent**, pipe directly to `threads_api.py publish`.

---

## Recipe 4: Compare Sources and Produce Analysis Report

**Use case**: Compare multiple products, papers, or frameworks by loading their
documentation/reviews into NotebookLM and generating a structured comparison.

### Commands

```bash
# Step 1: Create notebook with sources to compare
python3 scripts/notebooklm_client.py create \
  --title "LLM Framework Comparison" \
  --sources \
    "https://docs.langchain.com/docs/get_started/introduction" \
    "https://docs.llamaindex.ai/en/stable/" \
    "https://docs.anthropic.com/agent-sdk/overview" \
    "https://python.langchain.com/docs/concepts/" \
  --wait

# Step 2: Ask comparison questions
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "Compare these frameworks across: ease of use, documentation quality, community size, and key features."

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the unique strengths of each framework that the others lack?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "For a developer building an AI agent from scratch, which framework would you recommend and why?"

# Step 3: Generate a data table for structured comparison
python3 scripts/notebooklm_client.py generate data-table \
  --notebook NOTEBOOK_ID \
  --instructions "Compare frameworks across: Language support, RAG capabilities, Agent support, Tool integration, Pricing, Documentation quality"

# Step 4: Generate a detailed report
python3 scripts/notebooklm_client.py generate report \
  --notebook NOTEBOOK_ID \
  --format custom \
  --prompt "Create a detailed comparison report with: Executive Summary, Feature Matrix, Pros/Cons for each framework, Use Case Recommendations, and Final Verdict."

# Step 5: Get the data table and report
python3 scripts/notebooklm_client.py download report \
  --notebook NOTEBOOK_ID \
  --output comparison-report.md
```

### Expected Output

- `comparison-report.md`: A structured comparison with:
  - Executive summary
  - Feature comparison matrix (from data table)
  - Pros/cons per framework
  - Use case recommendations
  - Verdict
- Console: Cited answers with specific quotes from documentation

### Tips

- **Add official documentation** as sources -- NotebookLM indexes the full content.
- **Use data tables** for structured feature matrices that are easy to export.
- **Ask for "unique strengths"** -- this surfaces differentiators that generic comparisons miss.
- **Follow up on citations** -- use `get_fulltext()` to verify specific claims.
- **For products**, add both the official docs AND third-party reviews for balanced perspective.
- **Export the data table to CSV** for spreadsheet use.

---

## Recipe 5: Deep Dive into a Topic and Generate Podcast Episode

**Use case**: Create a podcast-quality audio discussion from research sources,
complete with show notes and a summary article.

### Commands

```bash
# Step 1: Create notebook with deep-dive sources
python3 scripts/notebooklm_client.py create \
  --title "Deep Dive: The Future of AI Coding Assistants" \
  --sources \
    "https://arxiv.org/abs/2401.99999" \
    "https://github.blog/ai-coding-assistant-report-2026" \
    "https://youtube.com/watch?v=keynote123" \
    "https://stackoverflow.blog/2026/ai-coding-survey" \
    "https://docs.anthropic.com/claude-code" \
  --wait

# Step 2: Use deep research to find additional sources
python3 scripts/notebooklm_client.py research \
  --notebook NOTEBOOK_ID \
  --query "AI coding assistants developer productivity impact 2026" \
  --source web \
  --mode deep

# Step 3: Poll and import research results
python3 scripts/notebooklm_client.py research-poll \
  --notebook NOTEBOOK_ID \
  --import-top 5

# Step 4: Ask probing questions for show notes
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the most surprising statistics about AI coding assistant adoption?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What are the main arguments for and against AI coding assistants?"

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What predictions are being made about the future of coding with AI?"

# Step 5: Generate the audio podcast
python3 scripts/notebooklm_client.py generate audio \
  --notebook NOTEBOOK_ID \
  --language en \
  --format deep_dive \
  --length long \
  --instructions "Focus on the debate between optimists and skeptics. Include specific statistics and developer quotes. Make it conversational and engaging."

# Step 6: Wait for audio generation and download
python3 scripts/notebooklm_client.py download audio \
  --notebook NOTEBOOK_ID \
  --output "podcast-ai-coding.mp4"

# Step 7: Generate study guide for show notes
python3 scripts/notebooklm_client.py generate report \
  --notebook NOTEBOOK_ID \
  --format study_guide

# Step 8: Generate a blog post companion article
python3 scripts/notebooklm_client.py generate report \
  --notebook NOTEBOOK_ID \
  --format blog_post

# Step 9: Download both reports
python3 scripts/notebooklm_client.py download report \
  --notebook NOTEBOOK_ID \
  --artifact STUDY_GUIDE_ID \
  --output show-notes.md

python3 scripts/notebooklm_client.py download report \
  --notebook NOTEBOOK_ID \
  --artifact BLOG_POST_ID \
  --output companion-article.md
```

### Expected Output

- `podcast-ai-coding.mp4`: 15-30 minute audio discussion between two AI hosts
- `show-notes.md`: Structured notes with key concepts, quotes, and glossary
- `companion-article.md`: Blog post version of the same content
- Console: Deep research report with additional sources discovered

### Tips

- **Start with 5+ high-quality sources** -- podcast quality depends on source depth.
- **Use deep research** (`--mode deep`) for comprehensive source discovery.
- **The `--instructions` parameter is powerful** -- guide the podcast tone and focus.
- **Audio formats**: `deep_dive` (detailed, ~20min), `brief` (~5min), `debate` (opposing views), `critique` (critical analysis).
- **Generate a study guide** alongside the podcast for listeners who prefer reading.
- **Audio generation takes 3-10 minutes** -- use `wait_for_completion()` or poll periodically.
- **The blog post report** makes a great companion piece for SEO and accessibility.
- **Share the notebook** (`--public`) to let listeners explore sources themselves.

### Podcast Audio Formats

| Format | Duration | Style | Best For |
|---|---|---|---|
| `deep_dive` | 15-30 min | Thorough exploration | Complex topics |
| `brief` | 3-5 min | Quick overview | News updates |
| `critique` | 10-20 min | Critical analysis | Reviews, evaluations |
| `debate` | 10-20 min | Two opposing views | Controversial topics |

### Audio Length Options

| Length | Duration | Notes |
|---|---|---|
| `short` | ~5 min | Quick briefing |
| `default` | ~10-15 min | Standard episode |
| `long` | ~20-30 min | Deep exploration |

---

## Recipe 6: Automated Daily Research Brief

**Use case**: Every morning, automatically research your focus areas and produce
a concise brief of what happened overnight.

### Commands

```bash
#!/bin/bash
# daily-research.sh -- Run as cron: 0 8 * * * /path/to/daily-research.sh

DATE=$(date +%Y-%m-%d)

# Step 1: Create today's notebook
NOTEBOOK_ID=$(python3 scripts/notebooklm_client.py create \
  --title "Daily Brief: $DATE" \
  --json | jq -r '.id')

# Step 2: Add curated sources (top stories from each feed)
# Use trend-pulse or cf-browser to pre-filter
URLS=$(trend-pulse trending --sources hackernews,reddit --count 10 --format urls)
for url in $URLS; do
  python3 scripts/notebooklm_client.py add-source \
    --notebook $NOTEBOOK_ID \
    --url "$url"
done

# Step 3: Wait for all sources to process
python3 scripts/notebooklm_client.py wait \
  --notebook $NOTEBOOK_ID \
  --timeout 180

# Step 4: Generate briefing
python3 scripts/notebooklm_client.py generate report \
  --notebook $NOTEBOOK_ID \
  --format custom \
  --prompt "Create a morning briefing with: Top 3 stories (2 sentences each), Key numbers/stats mentioned today, One thing to watch today. Keep it under 500 words."

# Step 5: Download
python3 scripts/notebooklm_client.py download report \
  --notebook $NOTEBOOK_ID \
  --output "briefs/$DATE.md"

echo "Daily brief ready: briefs/$DATE.md"
```

### Expected Output

- `briefs/YYYY-MM-DD.md`: A concise daily brief (~500 words)
- Archived notebooks for historical reference

### Tips

- **Keep source count manageable** (5-10 sources) for fast processing.
- **Use custom report prompts** to match your preferred briefing format.
- **Combine with email/Slack** delivery for morning routine integration.
- **Accumulate daily notebooks** -- query across them for weekly trends.
- **Rate limit awareness**: With 10 sources + 1 report per day, you are well within safe limits.

---

## Recipe 7: Turn Meeting Notes into Action Items

**Use case**: Upload meeting recording transcripts or notes, and extract structured
action items, decisions, and follow-ups.

### Commands

```bash
# Step 1: Create notebook with meeting content
python3 scripts/notebooklm_client.py create \
  --title "Team Standup 2026-03-14"

# Step 2: Add transcript (text or file)
python3 scripts/notebooklm_client.py add-source \
  --notebook NOTEBOOK_ID \
  --text "Team Standup Notes" \
  --content "$(cat meeting-transcript.txt)" \
  --wait

# Or upload the file directly
python3 scripts/notebooklm_client.py add-source \
  --notebook NOTEBOOK_ID \
  --file meeting-transcript.pdf \
  --wait

# Step 3: Extract structured information
python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "List all action items mentioned in this meeting. For each, note: the task, who is responsible, and the deadline if mentioned."

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What decisions were made in this meeting? List each decision and the rationale."

python3 scripts/notebooklm_client.py ask \
  --notebook NOTEBOOK_ID \
  --question "What topics need follow-up discussion? What was left unresolved?"

# Step 4: Generate a data table of action items
python3 scripts/notebooklm_client.py generate data-table \
  --notebook NOTEBOOK_ID \
  --instructions "Create a table with columns: Action Item, Owner, Deadline, Status, Notes"

# Step 5: Generate quiz to test understanding (optional, for training)
python3 scripts/notebooklm_client.py generate quiz \
  --notebook NOTEBOOK_ID \
  --instructions "Create questions about the key decisions and action items from this meeting"
```

### Expected Output

- Cited list of action items with responsible persons
- Decision log with rationale
- Data table exportable to project management tools
- Optional quiz for team alignment

### Tips

- **YouTube meeting recordings** work as sources (NotebookLM extracts transcripts).
- **Google Drive integration** lets you add Google Docs meeting notes directly.
- **The data table export** can be imported into Jira, Notion, or Google Sheets.
- **For recurring meetings**, create a notebook per meeting and ask cross-meeting
  questions like "What action items from last week are still pending?"

---

## Quick Reference: Pipeline Commands

| Pipeline | Command | Input | Output |
|---|---|---|---|
| Research to Article | `pipeline.py research-to-article` | URLs + topic | Markdown article |
| Research to Social | `pipeline.py research-to-social` | Notebook + topic | Platform-specific posts |
| Trend to Content | `pipeline.py trend-to-content` | Geo + niche | Multi-format content |
| Weekly Digest | `pipeline.py weekly-digest` | Feed list | Newsletter markdown |
| Compare Sources | Manual (Steps 1-5) | Docs/reviews | Comparison report |
| Deep Dive Podcast | Manual (Steps 1-9) | Mixed sources | Audio + show notes |
| Daily Brief | `daily-research.sh` | Trending URLs | Morning briefing |
| Meeting Actions | Manual (Steps 1-5) | Transcript | Action items table |

## Common Flags

| Flag | Description | Example |
|---|---|---|
| `--wait` | Block until source is processed | `add-source --wait` |
| `--json` | Output as JSON | `list --json` |
| `--output FILE` | Save to file | `download --output report.md` |
| `--notebook ID` | Target notebook | `ask --notebook abc123` |
| `--format FMT` | Output/generation format | `generate report --format briefing_doc` |
| `--language LANG` | Content language | `generate audio --language zh-TW` |
| `--instructions TEXT` | Custom instructions | `generate audio --instructions "Focus on..."` |
