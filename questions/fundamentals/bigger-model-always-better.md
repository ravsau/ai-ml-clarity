# Is a Bigger Model Always Better?

## Short Answer

**No.** Bigger helps, but only to a point. After that: diminishing returns, higher costs, and sometimes worse performance for your task.

## The Reality

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Performance                                                │
│       ▲                                                     │
│       │                    ┌─── Diminishing returns         │
│       │                   /                                 │
│       │              ____/                                  │
│       │           __/                                       │
│       │        __/                                          │
│       │      _/                                             │
│       │    _/                                               │
│       │  _/                                                 │
│       │_/                                                   │
│       └──────────────────────────────────────────► Size     │
│         1B    7B    70B    405B                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## When Bigger Helps

| Use case | Why bigger wins |
|----------|-----------------|
| Complex reasoning | More parameters = more capacity |
| Rare knowledge | Bigger models memorize more |
| Multi-step tasks | Better at maintaining context |

## When Bigger Hurts

| Problem | Why |
|---------|-----|
| Latency | More weights = slower inference |
| Cost | 10x params ≈ 10x cost |
| Overfitting | Too powerful for simple tasks |
| Deployment | Can't fit on smaller hardware |

## The Right Question

Not "how big?" but "big enough for what?"

| Task | Good enough |
|------|-------------|
| Classification | Small model, fine-tuned |
| Summarization | 7-13B often sufficient |
| Complex reasoning | 70B+ helps |
| Coding | Depends on complexity |

## Scaling Laws Say

Performance scales with:
- Model size (parameters)
- Data size
- Compute

But they scale **logarithmically** - 10x bigger ≠ 10x better.

## One-Liner

```
Bigger = more capable, not always better
Right-size for your task
10x params ≠ 10x performance
```
