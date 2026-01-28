# What Is a Context Window and Why Does It Matter?

## Short Answer

**Context window** = the maximum amount of text an LLM can see at once. Everything outside it is invisible to the model.

## The Mental Model

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    CONTEXT WINDOW                           │
│              (e.g., 128K tokens for GPT-4)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                       │  │
│  │  [System prompt]                                      │  │
│  │  [Previous messages...]                               │  │
│  │  [Retrieved documents (RAG)]                          │  │
│  │  [Current user message]                               │  │
│  │                                                       │  │
│  │  ▲                                                    │  │
│  │  │ Everything here = model can see                    │  │
│  │  ▼                                                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ════════════════════════════════════════════════════════   │
│                                                             │
│  [Older messages]     ← INVISIBLE (pushed out)              │
│  [Other documents]    ← INVISIBLE (never included)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Context Window Sizes

| Model | Context window |
|-------|----------------|
| GPT-3.5 | 4K-16K tokens |
| GPT-4 | 8K-128K tokens |
| Claude 3 | 200K tokens |
| Gemini 1.5 | 1M+ tokens |
| Llama 3 | 8K-128K tokens |

## Why It Matters

| Impact | Consequence |
|--------|-------------|
| Long conversations | Old messages get dropped |
| Document Q&A | Can't fit entire codebase |
| RAG design | Limits how much you can retrieve |
| Cost | More tokens = more $ |

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Model remembers everything" | Only what's in context |
| "Bigger context = better" | Attention degrades with length |
| "I can dump my whole repo" | Still need smart retrieval |

## The "Lost in the Middle" Problem

```
Context: [Beginning ... Middle ... End]
                       ↑
              Model attention weakest here
```

LLMs pay less attention to the middle of long contexts.

## One-Liner

```
Context window = LLM's working memory
Outside the window = doesn't exist
Bigger window ≠ infinite memory
```
