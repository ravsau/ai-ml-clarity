# What Is RAG and Why Is It Used?

## Short Answer

**RAG** (Retrieval-Augmented Generation) = fetch relevant info, then generate. It gives LLMs access to your data without retraining.

## The Problem RAG Solves

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  WITHOUT RAG                                                │
│  ──────────                                                 │
│                                                             │
│  User: "What's our refund policy?"                          │
│  LLM: "I don't have access to your company's policies."     │
│       (or worse: hallucinated answer)                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WITH RAG                                                   │
│  ────────                                                   │
│                                                             │
│  User: "What's our refund policy?"                          │
│           ↓                                                 │
│  [Retrieve relevant docs from your knowledge base]          │
│           ↓                                                 │
│  LLM: "Based on your policy doc, refunds are available      │
│        within 30 days with receipt..."                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## How RAG Works

```
1. EMBED your documents (once)
   Docs → Chunks → Embeddings → Vector DB

2. RETRIEVE at query time
   User query → Embed → Find similar chunks

3. GENERATE with context
   [System prompt + Retrieved chunks + User query] → LLM → Answer
```

## Why RAG vs Fine-Tuning

| Aspect | RAG | Fine-tuning |
|--------|-----|-------------|
| Data updates | Instant (just re-index) | Retrain required |
| Cost | Cheap | Expensive |
| Hallucination | Reduced (has sources) | Can still hallucinate |
| Custom knowledge | Easy to add | Baked into weights |
| Transparency | Can cite sources | Black box |

## When to Use RAG

| Good for | Not ideal for |
|----------|---------------|
| Company docs/FAQs | Teaching new skills |
| Up-to-date information | Changing model behavior |
| Domain-specific knowledge | Style/tone changes |
| Citing sources matters | Simple factual recall |

## RAG Components

| Component | Purpose |
|-----------|---------|
| Chunking | Split docs into retrievable pieces |
| Embeddings | Convert chunks to vectors |
| Vector DB | Store and search embeddings |
| Retriever | Find relevant chunks |
| LLM | Generate answer from context |

## One-Liner

```
RAG = retrieval + generation
Fetch relevant docs, then answer
Your data + LLM power, no retraining
```
