# What Is a Reranker and Why Add One After Vector Search?

## Short Answer

A **reranker** is a second, smaller-but-slow model that scores the relevance of a query against each candidate passage individually. Vector search returns a fast, approximate first guess; the reranker then re-scores just those candidates, reorders them, and sends only the best ones to the LLM. You add one after vector search to repair precision without losing the recall of a wide first pass.

## Two Passes

RAG retrieval happens in two passes. The first pass is **vector search**: it embeds the query and scans the whole corpus approximately, returning the passages whose embeddings are nearest — fast and wide, but it judges similarity in vector space, not by reading the words. The second pass is the **reranker**: a cross-encoder that takes the query and one candidate passage at a time, reads the pair together with full attention, and produces a much sharper relevance score. It reorders the top results so the strongest passages reach the model first.

## The Pipeline

```
Query
  │
  ▼
Vector search ───────────────▶  top N candidates
(one fast, approximate pass
 over the whole corpus)
  │
  ▼
Reranker ────────────────────▶  top k passages
(scores each (query, passage)
 pair with full attention)
  │
  ▼
LLM
(reads only the top k
 passages as context)
```

## Why Not Rerank Everything

Full-attention scoring reads the query and the passage together, token by token, so the cost mounts quickly with every extra candidate. Running that over the whole corpus would be far too slow; running it over the top few dozen candidates is cheap. That asymmetry is the whole design — the fast wide pass finds the candidates, the slow narrow pass ranks the few that matter.

## Related

- [what-is-rag.md](what-is-rag.md)
- [../fundamentals/precision-vs-recall.md](../fundamentals/precision-vs-recall.md)

## One-Liner

```
Vector search: fast, approximate, one pass over the whole corpus
Reranker: full attention on each (query, passage) pair, reorders the top
Rerank the top few dozen — never the whole corpus
```