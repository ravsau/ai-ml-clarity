# Why Does AI "Hallucinate" or Make Things Up?

## Short Answer

LLMs predict the **most likely next token**, not the truth. They're trained to sound plausible, not to be accurate. Confidence ≠ correctness.

## How Hallucination Happens

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  WHAT YOU THINK HAPPENS                                     │
│  ──────────────────────                                     │
│                                                             │
│  Question → [Look up facts] → Answer                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT ACTUALLY HAPPENS                                      │
│  ─────────────────────                                      │
│                                                             │
│  Question → [Predict most likely tokens] → Answer           │
│                    ↑                                        │
│                    │                                        │
│             No fact-checking                                │
│             No "I don't know" instinct                      │
│             Just pattern completion                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why It Happens

| Reason | Explanation |
|--------|-------------|
| Training objective | Predict next token, not verify truth |
| No knowledge retrieval | Can't look things up in real-time |
| Learned to be confident | Trained on authoritative text |
| Pattern matching | "Sounds right" ≠ "Is right" |
| No uncertainty signal | Equally confident about everything |

## Common Hallucination Types

| Type | Example |
|------|---------|
| Fake citations | Invents papers that don't exist |
| Wrong facts | Confident but incorrect dates/numbers |
| Non-existent APIs | Makes up function names |
| Imagined people | Creates fictional experts |
| Plausible nonsense | Sounds right, completely false |

## The Core Problem

```
LLM confidence is about FLUENCY, not ACCURACY

High confidence = "This sounds like natural text"
Not             = "This is factually true"
```

## How to Reduce Hallucinations

| Method | How it helps |
|--------|--------------|
| RAG | Ground responses in real documents |
| Citations required | Force model to reference sources |
| Lower temperature | Less creative = fewer fabrications |
| Fact-check prompts | "Only answer if certain" |
| Structured output | Constrain possible responses |

## One-Liner

```
LLMs predict plausible text, not truth
Confident ≠ correct
They're fluent bullshitters by design
```
