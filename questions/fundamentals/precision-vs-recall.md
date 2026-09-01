# Precision vs Recall — And Why RAG Lives or Dies by Them

## Short Answer

**Precision asks: of what I returned, how much was right? Recall asks: of what was right, how much did I return?**

In a RAG system the retriever sets both numbers. Low recall means the answer is impossible, because the correct chunk never reached the model. Low precision means the answer is unreliable, because the model must read noise to find the fact.

## The Formulas

```
Precision = true positives / (true positives + false positives)
            "How clean is what I returned?"

Recall    = true positives / (true positives + false negatives)
            "How complete is what I returned?"

F1        = 2 * (Precision * Recall) / (Precision + Recall)
            "One number when you need both."
```

## Analogy 1: The Fishing Net

You fish in a pond. You want fish. You do not want weeds, sticks, or old boots.

| Net | Result | Metric |
|-----|--------|--------|
| A wide net with big holes | You catch a lot of junk with the fish | High recall, low precision |
| A tiny, careful net | Everything you catch is a fish, but most fish stay in the pond | High precision, low recall |
| The right net | Mostly fish, and most of the fish | Good F1 |

A RAG retriever is the net. `top_k = 50` is the wide net. `top_k = 2` with a strict similarity threshold is the tiny net.

## Analogy 2: Airport Security

The scanner must find every weapon and stop few passengers.

- **Recall failure:** a weapon passes through. The system missed it. Nothing later in the process can fix this.
- **Precision failure:** the scanner stops 200 people who carry keys and belts. Nothing is missed, but the queue is long and staff stop trusting the alarm.

RAG behaves the same way. A missed chunk is unrecoverable. A noisy chunk is expensive and it distracts the model.

## How They Map to a RAG Pipeline

```
Question
   |
   v
[ RETRIEVER ]  <- recall is decided here. A missed chunk is gone forever.
   |
   v
[ RERANKER ]   <- precision is repaired here. Cut the junk, keep the fish.
   |
   v
[ LLM ]        <- reads the context and writes the answer
```

| Metric | Where it is set | What it costs you when it is low |
|--------|-----------------|----------------------------------|
| **Context recall** | Embedding model, chunk size, `top_k`, hybrid search | The model cannot answer, or it hallucinates a plausible answer |
| **Context precision** | Reranker, similarity threshold, metadata filters | More tokens, higher cost, higher latency, distraction |

## The Standard RAG Pattern

Retrieve wide, then rerank narrow.

1. Retrieve `top_k = 50` with hybrid search (vector + BM25). This maximizes recall.
2. Rerank those 50 with a cross-encoder. Keep the best 5. This restores precision.
3. Send 5 clean chunks to the model.

This works because recall is lost forever at step 1, but precision can still be repaired at step 2.

## Diagnose Your RAG With Two Questions

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| "I know that fact is in the docs, but the answer says it is not" | Low recall | Bigger `top_k`, hybrid search, smaller chunks, better embedding model |
| "The answer is padded, off-topic, or cites the wrong page" | Low precision | Add a reranker, raise the threshold, filter by metadata |
| "Answers are slow and expensive" | Low precision | Cut `top_k` after reranking |
| Both symptoms | Chunking is wrong | Re-chunk with overlap, then re-measure |

Measure recall first. There is no point in tuning precision on a set that does not contain the answer.

## Related Terms You Will Meet

| Term | Meaning |
|------|---------|
| **Recall@k** | Did the correct chunk appear in the top *k* results? |
| **MRR** | How high in the list did the first correct chunk appear? |
| **NDCG** | Rank quality when several chunks are relevant, with the best ones weighted highest |
| **Faithfulness** | Does the answer stay inside the retrieved context? A generation metric, not a retrieval one |
| **Answer relevance** | Does the answer address the question that was asked? |

## One-Liner

```
Precision = of what I returned, how much was right?  (noise)
Recall    = of what was right, how much did I return? (misses)
RAG rule  : retrieve wide for recall, rerank narrow for precision.
A missed chunk is fatal. A noisy chunk is only expensive.
```

---

## Sources

- [Precision and Recall in the context of RAG, Explained](https://saiphani09.substack.com/p/precision-and-recall-in-the-context)
- [RAG Evaluation Simplified — Part 2: Deep Dive into Recall & Precision — Medium](https://medium.com/@fassha08/rag-evaluation-simplified-part-2-deep-dive-into-recall-precision-4853709630bb)
- [Precision and Recall: The Fisherman's Guide to Classification Metrics — Medium](https://medium.com/@oojas2/precision-and-recall-the-fishermans-guide-to-classification-metrics-9054d478f4fa)
- [RAG Recall vs Precision: A Practical Diagnostic Guide — DEV Community](https://dev.to/optyxstack/rag-recall-vs-precision-a-practical-diagnostic-guide-for-reliable-retrieval-26oh)
- [Evaluation of Retrieval-Augmented Generation: A Survey — arXiv](https://arxiv.org/html/2405.07437v2)
