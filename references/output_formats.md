# NotebookLM Output Formats Reference

All JSON output formats for notebooklm-py API responses and pipeline outputs.

---

## Core API Responses

### Create Notebook Response

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "AI Agents Research",
  "created_at": "2026-03-14T10:30:00",
  "sources_count": 0,
  "is_owner": true
}
```

### List Notebooks Response

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "AI Agents Research",
    "created_at": "2026-03-14T10:30:00",
    "sources_count": 5,
    "is_owner": true
  },
  {
    "id": "f9e8d7c6-b5a4-3210-fedc-ba0987654321",
    "title": "Shared Notebook",
    "created_at": "2026-03-13T08:00:00",
    "sources_count": 3,
    "is_owner": false
  }
]
```

### Add Source Response

```json
{
  "id": "src-uuid-1234-5678-abcd-ef1234567890",
  "title": "Example Article",
  "url": "https://example.com/article",
  "kind": "web_page",
  "status": 1,
  "status_label": "processing"
}
```

When `wait=True`, status will be `2` (ready):

```json
{
  "id": "src-uuid-1234-5678-abcd-ef1234567890",
  "title": "Example Article Title (extracted)",
  "url": "https://example.com/article",
  "kind": "web_page",
  "status": 2,
  "status_label": "ready",
  "created_at": "2026-03-14T10:31:00"
}
```

### List Sources Response

```json
[
  {
    "id": "src-uuid-1111",
    "title": "Research Paper on AI Agents",
    "url": "https://arxiv.org/abs/2401.12345",
    "kind": "web_page",
    "status": 2,
    "created_at": "2026-03-14T10:31:00"
  },
  {
    "id": "src-uuid-2222",
    "title": "uploaded_doc.pdf",
    "url": null,
    "kind": "pdf",
    "status": 2,
    "created_at": "2026-03-14T10:32:00"
  },
  {
    "id": "src-uuid-3333",
    "title": "How to Build AI Agents",
    "url": "https://youtube.com/watch?v=abc123",
    "kind": "youtube",
    "status": 2,
    "created_at": "2026-03-14T10:33:00"
  }
]
```

### Source Guide Response

```json
{
  "summary": "This article discusses the **evolution of AI agents** from simple rule-based systems to sophisticated **autonomous frameworks**. Key topics include **ReAct prompting**, **tool use**, and **multi-agent coordination**. The author argues that...",
  "keywords": [
    "AI agents",
    "ReAct",
    "tool use",
    "multi-agent systems",
    "autonomous frameworks"
  ]
}
```

### Source Fulltext Response

```json
{
  "source_id": "src-uuid-1111",
  "title": "Research Paper on AI Agents",
  "content": "Full indexed text content of the source...\n\nThis can be thousands of characters long...",
  "kind": "web_page",
  "url": "https://arxiv.org/abs/2401.12345",
  "char_count": 15432
}
```

---

## Ask Response (with Citations)

```json
{
  "answer": "Based on the sources, there are three main differences between ReAct and Reflexion agents:\n\n1. **Reasoning approach**: ReAct interleaves reasoning and acting in a single loop [1], while Reflexion adds a self-reflection step after each episode [2].\n\n2. **Memory**: ReAct operates without persistent memory across episodes. Reflexion maintains an episodic memory of past failures and reflections [2].\n\n3. **Error correction**: ReAct relies on the environment for feedback. Reflexion generates verbal self-critique to improve future attempts [2][3].",
  "conversation_id": "conv-uuid-1234-5678",
  "turn_number": 1,
  "is_follow_up": false,
  "references": [
    {
      "source_id": "src-uuid-1111",
      "citation_number": 1,
      "cited_text": "ReAct prompting synergizes reasoning and acting by generating both verbal reasoning traces and task-specific actions in an interleaved manner",
      "start_char": 1245,
      "end_char": 1398,
      "chunk_id": "chunk-abc123"
    },
    {
      "source_id": "src-uuid-2222",
      "citation_number": 2,
      "cited_text": "Reflexion introduces linguistic reinforcement where the agent reflects on prior failures and stores these reflections in episodic memory",
      "start_char": 890,
      "end_char": 1044,
      "chunk_id": "chunk-def456"
    },
    {
      "source_id": "src-uuid-3333",
      "citation_number": 3,
      "cited_text": "The self-critique mechanism allows the agent to identify specific failure modes without requiring additional training",
      "start_char": 2100,
      "end_char": 2230,
      "chunk_id": "chunk-ghi789"
    }
  ]
}
```

### Follow-up Answer

```json
{
  "answer": "Expanding on point 3, the error correction mechanism in Reflexion works in three stages...",
  "conversation_id": "conv-uuid-1234-5678",
  "turn_number": 2,
  "is_follow_up": true,
  "references": [...]
}
```

---

## Artifact Generation Responses

### Generate Audio (Podcast) Response

```json
{
  "task_id": "art-uuid-audio-1234",
  "status": "in_progress",
  "url": null,
  "error": null,
  "error_code": null,
  "metadata": null
}
```

After completion (via `poll_status` or `wait_for_completion`):

```json
{
  "task_id": "art-uuid-audio-1234",
  "status": "completed",
  "url": "https://notebooklm.google.com/audio/...",
  "error": null,
  "error_code": null,
  "metadata": null
}
```

Failed generation:

```json
{
  "task_id": "art-uuid-audio-1234",
  "status": "failed",
  "url": null,
  "error": "Rate limit exceeded. Please try again later.",
  "error_code": "USER_DISPLAYABLE_ERROR",
  "metadata": null
}
```

### Generate Report Response

Same structure as audio. After completion, retrieve content via:

```json
{
  "task_id": "art-uuid-report-5678",
  "status": "completed",
  "url": null,
  "error": null,
  "error_code": null,
  "metadata": null
}
```

Report content (via `get_report_content()`):

```
# Briefing Doc: AI Agent Frameworks

## Executive Summary
This briefing document analyzes the current landscape of AI agent frameworks...

## Key Themes

### 1. Tool-Use Paradigm
Sources describe a shift toward agents that can use external tools...

### 2. Multi-Agent Coordination
Several papers discuss how multiple agents can collaborate...

## Important Quotes
> "ReAct prompting synergizes reasoning and acting..." - Source 1
> "The future of AI agents lies in their ability to..." - Source 3

## Actionable Insights
1. Consider implementing tool-use capabilities...
2. Multi-agent architectures show promise for...
```

### Generate Quiz Response

After completion, structured data (via `get_quiz_data()`):

```json
{
  "title": "AI Agents Quiz",
  "format": "markdown",
  "content": "# AI Agents Quiz\n\n## Question 1\nWhat is the key innovation of ReAct prompting?\n\n- [ ] Using only reasoning traces\n- [x] Interleaving reasoning and acting\n- [ ] Eliminating the need for tools\n- [ ] Using reinforcement learning\n\n**Hint:** Think about how reasoning and action are combined.\n\n## Question 2\n...",
  "questions": [
    {
      "question": "What is the key innovation of ReAct prompting?",
      "answerOptions": [
        {"text": "Using only reasoning traces", "isCorrect": false},
        {"text": "Interleaving reasoning and acting", "isCorrect": true},
        {"text": "Eliminating the need for tools", "isCorrect": false},
        {"text": "Using reinforcement learning", "isCorrect": false}
      ],
      "hint": "Think about how reasoning and action are combined."
    }
  ]
}
```

### Generate Flashcards Response

After completion, structured data (via `get_flashcard_data()`):

```json
{
  "title": "AI Agents Flashcards",
  "format": "markdown",
  "content": "# AI Agents Flashcards\n\n## Card 1\n\n**Q:** What is ReAct prompting?\n\n**A:** A framework that interleaves verbal reasoning traces and task-specific actions...\n\n---\n\n## Card 2\n...",
  "cards": [
    {
      "f": "What is ReAct prompting?",
      "b": "A framework that interleaves verbal reasoning traces and task-specific actions, allowing the model to reason about what to do next and then take action."
    },
    {
      "f": "How does Reflexion improve upon ReAct?",
      "b": "Reflexion adds an episodic memory and self-reflection mechanism, allowing the agent to learn from past failures and improve future attempts."
    }
  ]
}
```

### Generate Mind Map Response

```json
{
  "mind_map": {
    "name": "AI Agent Frameworks",
    "children": [
      {
        "name": "ReAct",
        "children": [
          {"name": "Reasoning traces"},
          {"name": "Action generation"},
          {"name": "Interleaved execution"}
        ]
      },
      {
        "name": "Reflexion",
        "children": [
          {"name": "Self-reflection"},
          {"name": "Episodic memory"},
          {"name": "Error correction"}
        ]
      }
    ]
  },
  "note_id": "note-uuid-1234"
}
```

### Generate Data Table Response

After completion (via `get_data_table()`):

```json
{
  "title": "Framework Comparison",
  "format": "csv",
  "headers": ["Framework", "Year", "Key Feature", "Memory", "Tool Use"],
  "rows": [
    ["ReAct", "2023", "Interleaved reasoning+action", "No", "Yes"],
    ["Reflexion", "2023", "Self-reflection loop", "Episodic", "Yes"],
    ["AutoGPT", "2023", "Autonomous task decomposition", "Long-term", "Yes"],
    ["Claude Agent", "2025", "Extended thinking + tools", "Context window", "Yes"]
  ],
  "csv_content": "Framework,Year,Key Feature,Memory,Tool Use\nReAct,2023,..."
}
```

### List Artifacts Response

```json
[
  {
    "id": "art-uuid-audio-1234",
    "title": "Audio Overview",
    "kind": "audio",
    "status": 3,
    "status_str": "completed",
    "created_at": "2026-03-14T11:00:00",
    "url": "https://..."
  },
  {
    "id": "art-uuid-report-5678",
    "title": "Briefing Doc: AI Agents",
    "kind": "report",
    "status": 3,
    "status_str": "completed",
    "created_at": "2026-03-14T11:05:00",
    "report_subtype": "briefing_doc"
  },
  {
    "id": "art-uuid-quiz-9012",
    "title": "Quiz",
    "kind": "quiz",
    "status": 3,
    "status_str": "completed",
    "created_at": "2026-03-14T11:10:00"
  }
]
```

---

## Research Responses

### Start Research Response

```json
{
  "task_id": "research-task-uuid-1234",
  "report_id": "research-report-uuid-5678",
  "notebook_id": "notebook-uuid",
  "query": "latest advances in AI agents",
  "mode": "fast"
}
```

### Poll Research Response (In Progress)

```json
{
  "task_id": "research-task-uuid-1234",
  "status": "in_progress",
  "query": "latest advances in AI agents",
  "sources": [],
  "summary": "",
  "report": "",
  "tasks": [
    {
      "task_id": "research-task-uuid-1234",
      "status": "in_progress",
      "query": "latest advances in AI agents",
      "sources": [],
      "summary": "",
      "report": ""
    }
  ]
}
```

### Poll Research Response (Completed -- Fast)

```json
{
  "task_id": "research-task-uuid-1234",
  "status": "completed",
  "query": "latest advances in AI agents",
  "sources": [
    {
      "url": "https://arxiv.org/abs/2401.12345",
      "title": "A Survey of AI Agent Frameworks",
      "result_type": 1,
      "research_task_id": "research-task-uuid-1234"
    },
    {
      "url": "https://blog.example.com/agents-2026",
      "title": "The State of AI Agents in 2026",
      "result_type": 1,
      "research_task_id": "research-task-uuid-1234"
    }
  ],
  "summary": "Research found 8 relevant sources covering AI agent frameworks...",
  "report": "",
  "tasks": [...]
}
```

### Poll Research Response (Completed -- Deep)

```json
{
  "task_id": "research-task-uuid-1234",
  "status": "completed",
  "query": "comparison of agent frameworks",
  "sources": [
    {
      "url": "",
      "title": "Deep Research Report: Agent Framework Comparison",
      "result_type": 5,
      "research_task_id": "research-task-uuid-1234",
      "report_markdown": "# Agent Framework Comparison\n\n## Executive Summary\n..."
    },
    {
      "url": "https://source1.com",
      "title": "Source Article 1",
      "result_type": 1,
      "research_task_id": "research-task-uuid-1234"
    }
  ],
  "summary": "Deep research analysis of agent frameworks...",
  "report": "# Agent Framework Comparison\n\n## Executive Summary\n...",
  "tasks": [...]
}
```

### Import Sources Response

```json
[
  {
    "id": "src-uuid-imported-1111",
    "title": "A Survey of AI Agent Frameworks"
  },
  {
    "id": "src-uuid-imported-2222",
    "title": "The State of AI Agents in 2026"
  }
]
```

---

## Notebook Description Response

```json
{
  "summary": "This notebook contains research on AI agent frameworks including ReAct, Reflexion, and modern autonomous agents. Key topics include tool use, memory mechanisms, and multi-agent coordination.",
  "suggested_topics": [
    {
      "question": "What are the main AI agent frameworks discussed?",
      "prompt": "List and compare the main AI agent frameworks covered in these sources."
    },
    {
      "question": "How do agents use tools?",
      "prompt": "Explain how different agent frameworks implement tool use capabilities."
    },
    {
      "question": "What are the trends in AI agents?",
      "prompt": "Identify emerging trends in AI agent development based on these sources."
    }
  ]
}
```

---

## Sharing Status Response

```json
{
  "notebook_id": "notebook-uuid",
  "is_public": true,
  "access": "anyone_with_link",
  "view_level": "full_notebook",
  "shared_users": [
    {
      "email": "collaborator@example.com",
      "permission": "editor",
      "display_name": "Alice",
      "avatar_url": "https://..."
    }
  ],
  "share_url": "https://notebooklm.google.com/notebook/notebook-uuid"
}
```

---

## Pipeline Output Formats

### research-to-article Output

```json
{
  "pipeline": "research-to-article",
  "notebook_id": "notebook-uuid",
  "topic": "AI Agent Frameworks in 2026",
  "sources_count": 5,
  "questions_asked": 3,
  "research": {
    "questions": [
      {
        "question": "What are the main frameworks?",
        "answer": "Based on the sources...",
        "citations": 4
      },
      {
        "question": "How do they compare?",
        "answer": "The key differences...",
        "citations": 3
      }
    ],
    "report_summary": "Briefing doc content..."
  },
  "article": {
    "title": "AI Agent Frameworks in 2026: A Comprehensive Guide",
    "content": "# AI Agent Frameworks in 2026\n\n...",
    "word_count": 1500,
    "reading_time_minutes": 6
  },
  "metadata": {
    "created_at": "2026-03-14T12:00:00",
    "pipeline_duration_seconds": 120
  }
}
```

### research-to-social Output

```json
{
  "pipeline": "research-to-social",
  "notebook_id": "notebook-uuid",
  "topic": "AI Agents",
  "posts": {
    "threads": {
      "text": "3 things I learned researching AI agents today:\n\n1. ReAct vs Reflexion isn't about which is better — it's about when each shines.\n\n2. Memory is the real differentiator...\n\n你覺得哪個 framework 最有潛力？",
      "char_count": 245
    },
    "instagram": {
      "caption": "AI Agent Frameworks: What You Need to Know in 2026\n\nThe landscape of AI agents has evolved dramatically...\n\n#AIAgents #MachineLearning #ReAct #Reflexion #TechTrends",
      "char_count": 890,
      "image_prompt": "Futuristic diagram showing AI agent frameworks connected in a network"
    },
    "facebook": {
      "message": "I spent the afternoon researching AI agent frameworks and here's what I found...\n\n## The Big Picture\n...",
      "char_count": 1200
    }
  },
  "source_citations": [
    "Based on research from: arxiv.org/abs/2401.12345, blog.example.com/agents-2026"
  ]
}
```

### trend-to-content Output

```json
{
  "pipeline": "trend-to-content",
  "trend": {
    "topic": "Claude Code 2.0 release",
    "source": "hackernews",
    "heat_score": 450,
    "geo": "TW"
  },
  "notebook_id": "notebook-uuid",
  "research_summary": "Claude Code 2.0 introduces...",
  "content": {
    "threads": "...",
    "instagram": "...",
    "article": "..."
  },
  "metadata": {
    "created_at": "2026-03-14T12:00:00",
    "trend_discovered_at": "2026-03-14T11:30:00"
  }
}
```
