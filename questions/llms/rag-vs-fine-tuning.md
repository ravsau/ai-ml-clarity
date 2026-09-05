# RAG vs Fine-Tuning: When Do You Use Which?

## Short Answer

**RAG and fine-tuning solve different problems and are often used together.** RAG injects fresh context into the prompt at answer time, while fine-tuning adjusts the model's weights. Use RAG when you need up-to-date or private facts you can retrieve. Use fine-tuning when you want a permanent change in behavior, style, or format.

## Different Problems

**RAG changes what the model can see.** At answer time it retrieves relevant chunks from an external store — docs, FAQs, your private files — and drops them into the context window before generation. The weights never change; the model stays the same and simply reads more information for that single request.

**Fine-tuning changes how the model behaves.** It updates the weights themselves, so the model answers in a certain tone, follows an output format, or reliably performs a task even when no extra context is supplied. The change is baked into the model and is permanent, which is why it takes training time and why it is slow to refresh.

## Decision Table

| When you need... | RAG | Fine-tuning |
|------------------|-----|-------------|
| Fresh facts | Re-index and the next query sees them | Retrain to bake them into weights |
| Private documents | Retrieved chunks stay inside your system | Weights may memorize snippets |
| Style and tone | Prompt can nudge, but weakly | Tunes the voice directly |
| Output format | Instructions in the prompt, depends on the model | Can make a format reliable |
| Latency | Adds a retrieval step up front | Adds no latency at answer time |
| Cost of updating | Cheap, just re-embed and re-index | Expensive, needs retraining |

## Common Mistake

**Fine-tuning to teach facts.** Facts change all the time, so training them into static weights means retraining every time they change — and risks stale or memorized answers. Facts from a retrievable store belong in RAG. Fine-tuning is for behavior, not information.

## Related

- [what-is-rag.md](what-is-rag.md)
- [../fundamentals/fine-tuning-vs-training.md](../fundamentals/fine-tuning-vs-training.md)

## One-Liner

```
RAG = feed it the facts it can't see
Fine-tuning = change how it behaves
Put facts in RAG, behavior in fine-tuning
```