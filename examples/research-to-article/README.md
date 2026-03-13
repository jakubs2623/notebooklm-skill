# Example: Research to Article

Take 3 URLs, create a NotebookLM notebook, ask 5 research questions, and generate a structured article draft.

## Overview

```
3 source URLs → NotebookLM notebook → 5 research queries → Structured JSON → Article draft
```

## Prerequisites

- notebooklm-skill installed and authenticated (see [docs/SETUP.md](../../docs/SETUP.md))

## Step 1: Create a Notebook with Sources

Pick 3 URLs covering different angles on a topic. For this example, we'll research AI coding assistants.

```bash
python scripts/notebooklm_client.py create \
  --name "AI Coding Assistants 2026" \
  --sources \
    "https://www.anthropic.com/research/claude-code" \
    "https://github.blog/2024-06-05-github-copilot-research/" \
    "https://cursor.com/blog/building-with-ai"
```

Expected output:

```json
{
  "status": "created",
  "notebook": {
    "id": "nb_a1b2c3d4e5",
    "name": "AI Coding Assistants 2026",
    "sources": 3,
    "created_at": "2026-03-14T10:00:00Z"
  }
}
```

## Step 2: Ask Research Questions

Ask 5 targeted questions that will give you material for a well-rounded article.

```bash
python scripts/notebooklm_client.py query \
  --notebook "AI Coding Assistants 2026" \
  --questions \
    "What are the key differences between the major AI coding assistants?" \
    "What metrics exist for measuring AI coding assistant effectiveness?" \
    "What workflows do developers use with AI coding tools?" \
    "What are the main criticisms and limitations of AI coding assistants?" \
    "What trends are emerging for the future of AI-assisted development?"
```

Expected output:

```json
{
  "notebook": "AI Coding Assistants 2026",
  "queries": [
    {
      "question": "What are the key differences between the major AI coding assistants?",
      "answer": "Based on the sources, the major differences center on three axes: (1) Architecture — inline completion vs. chat-based vs. agentic approaches...",
      "citations": [
        {"source": "anthropic.com", "excerpt": "Claude Code takes an agentic approach..."},
        {"source": "github.blog", "excerpt": "Copilot focuses on inline suggestions..."}
      ]
    },
    {
      "question": "What metrics exist for measuring AI coding assistant effectiveness?",
      "answer": "The sources reference several metrics: acceptance rate (% of suggestions kept), time-to-completion for tasks, lines of code generated vs. manually written...",
      "citations": [
        {"source": "github.blog", "excerpt": "In our study, developers completed tasks 55% faster..."}
      ]
    },
    {
      "question": "What workflows do developers use with AI coding tools?",
      "answer": "Three primary workflows emerge: (1) autocomplete-driven — developer writes, AI suggests completions; (2) chat-driven — developer describes intent, AI generates blocks; (3) agent-driven — developer specifies goal, AI plans and executes...",
      "citations": [
        {"source": "cursor.com", "excerpt": "The most productive developers alternate between..."}
      ]
    },
    {
      "question": "What are the main criticisms and limitations of AI coding assistants?",
      "answer": "Key criticisms include: code quality concerns (generated code may have subtle bugs), over-reliance reducing learning, context window limitations, and security risks from training data leakage...",
      "citations": []
    },
    {
      "question": "What trends are emerging for the future of AI-assisted development?",
      "answer": "Emerging trends include: multi-file agentic editing, MCP-based tool integration, background autonomous agents, and spec-driven development where AI implements from specifications...",
      "citations": [
        {"source": "anthropic.com", "excerpt": "The shift toward agentic coding..."}
      ]
    }
  ]
}
```

## Step 3: Export Research

Export the research results as structured JSON for Claude to use as context.

```bash
python scripts/notebooklm_client.py export \
  --notebook "AI Coding Assistants 2026" \
  --format json \
  --output research.json
```

The `research.json` file now contains all questions, answers, and source citations in a structured format.

## Step 4: Generate the Article

Use the research to generate an article. You can do this via the CLI:

```bash
python scripts/notebooklm_client.py generate \
  --notebook "AI Coding Assistants 2026" \
  --format article \
  --style technical-blog \
  --output draft.md
```

Or, hand `research.json` directly to Claude with a prompt like:

> Using the attached research, write a 1500-word technical blog post titled "AI Coding Assistants in 2026: A Landscape Review." Structure it with an introduction, 3-4 main sections based on the research themes, and a forward-looking conclusion. Cite sources inline.

## Step 5: Review the Output

The generated `draft.md` will have:

- A structured outline derived from your 5 questions
- Key findings synthesized across all 3 sources
- Source citations mapped back to the original URLs
- A coherent narrative connecting the research themes

## Tips

- **Ask contrasting questions.** "What are the strengths?" + "What are the criticisms?" gives balanced coverage.
- **Use specific questions.** "What metrics exist for X?" yields more concrete material than "Tell me about X."
- **3-7 sources is the sweet spot.** Too few lacks depth; too many dilutes focus.
- **Export before generating.** The JSON export lets you inspect and curate the research before content generation.

## Next Steps

- [Research to Threads](../research-to-threads/) — Turn research into social posts
- [Trend to Content](../trend-to-content/) — Start from trending topics instead of manual URLs
