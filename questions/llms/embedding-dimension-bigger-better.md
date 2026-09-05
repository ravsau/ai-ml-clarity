# Is a Bigger Embedding Dimension Better?

## Short Answer

**Bigger isn't automatically better.** A higher dimension gives each embedding more room to store information, but it grows index size, memory, and per-query cost. What actually decides retrieval quality is training data and task fit, not vector length. Choose the smallest dimension that does the job.

## What the Dimension Is

The **dimension** is the length of the vector each piece of text becomes — how many numbers are used to represent its meaning. It is set by the embedding model, not by you, and different models output vectors of different lengths.

## What Grows With It

The more numbers each text needs, the more space and computation every step takes.

| What grows | Why |
|------------|-----|
| **Index size** | every stored vector is longer, so the index takes more room |
| **Memory** | more numbers per vector must be held in RAM to run search |
| **Per-query cost** | comparing your query against longer vectors does more work |

What does **NOT** automatically grow with dimension: **retrieval quality**. A longer vector does not mean a better or more relevant match.

## What Actually Decides Quality

Retrieval quality comes from **training data and task fit**. A model trained on data like yours, for the kind of matching you do, at a smaller dimension, beats a generic model with a bigger one. Truncatable (Matryoshka-style) embeddings let you shorten the vectors after training without retraining.

## Related

- [../fundamentals/what-are-embeddings.md](../fundamentals/what-are-embeddings.md)
- [vector-search-vs-semantic-search-vs-rag.md](vector-search-vs-semantic-search-vs-rag.md)

## One-Liner

```
Bigger dimension = bigger index, memory, and query cost — not better quality
Quality comes from training data and task fit
Pick the smallest dimension that does the job
```