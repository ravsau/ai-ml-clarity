# Context Window vs Memory

## Short Answer

**Context window** = temporary, dies after the conversation
**Memory** = external system you build, persists across sessions

LLMs have no built-in memory. They only see what's in the current context.

## The Reality

```
┌─────────────────────────────────────────────────────────────┐
│                    WHAT PEOPLE THINK                        │
│                                                             │
│   User: "Remember I like Python"                            │
│   Model: stores this forever ❌                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    WHAT ACTUALLY HAPPENS                    │
│                                                             │
│   ┌─────────────────────────────────────────┐               │
│   │         CONTEXT WINDOW                  │               │
│   │         (e.g., 128K tokens)             │               │
│   │                                         │               │
│   │  [System prompt]                        │               │
│   │  [User msg 1]                           │               │
│   │  [Assistant msg 1]                      │               │
│   │  [User msg 2]  ← "I like Python"        │               │
│   │  [Assistant msg 2]                      │               │
│   │  ...                                    │               │
│   │                                         │               │
│   │  ⚠️ DELETED WHEN CONVERSATION ENDS      │               │
│   └─────────────────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Context vs Memory

| Aspect | Context Window | Memory |
|--------|----------------|--------|
| Duration | Single session | Persistent |
| Built-in | Yes | No - you build it |
| Size limit | Fixed (8K-128K+ tokens) | You decide |
| Implementation | Automatic | RAG, vector DB, user profiles |

## Why It Matters for Product Design

| Broken assumption | What actually happens |
|-------------------|----------------------|
| "The AI knows my preferences" | Only if you inject them into context |
| "It remembers past conversations" | Only if you store and retrieve them |
| "It learns from my feedback" | Only within current session |

## Building Real Memory

```
User query
    ↓
Retrieve relevant history (vector DB)
    ↓
Inject into context window
    ↓
LLM generates response
    ↓
Store interaction (for future retrieval)
```

## One-Liner

```
Context window = RAM (temporary)
Memory = hard drive (you build it)
```
