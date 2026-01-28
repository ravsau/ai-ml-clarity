# Tokens vs Words

## Short Answer

**Words** = what humans read
**Tokens** = what LLMs read (subword chunks)

1 word ≠ 1 token. Usually 1 word ≈ 1.3 tokens. Sometimes 1 word = 5+ tokens.

## How Tokenization Works

```
┌─────────────────────────────────────────────────────────────┐
│                     TOKENIZATION                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  "Hello world"        →  ["Hello", " world"]                │
│   2 words                 2 tokens ✓                        │
│                                                             │
│  "ChatGPT"            →  ["Chat", "G", "PT"]                │
│   1 word                  3 tokens                          │
│                                                             │
│  "authentication"     →  ["auth", "ent", "ication"]         │
│   1 word                  3 tokens                          │
│                                                             │
│  "🎉"                 →  ["🎉"] or multiple tokens          │
│   1 emoji                 1-4 tokens (varies)               │
│                                                             │
│  "नमस्ते"              →  [multiple tokens]                  │
│   1 word                  5+ tokens (non-English penalized) │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why Tokens Exist

| Reason | Explanation |
|--------|-------------|
| Vocabulary size | Can't store every word - subwords are efficient |
| Handle unknown words | Break new/rare words into known pieces |
| Multilingual | Same system works across languages |
| Code/symbols | Handles `function()` without special rules |

## Why It Matters

| What you pay for | Tokens, not words |
|------------------|-------------------|
| Context window limits | Measured in tokens |
| API pricing | Per 1K or 1M tokens |
| Response length | Token count, not word count |

## Token Counts Vary

| Content type | Tokens per word (approx) |
|--------------|--------------------------|
| English text | ~1.3 |
| Code | ~2-3 |
| Non-Latin scripts | ~3-5 |
| Emojis/special chars | ~1-4 each |

## One-Liner

```
Words = human units
Tokens = model units
Your 1000-word doc ≈ 1300 tokens (or more)
```
