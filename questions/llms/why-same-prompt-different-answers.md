# Why Does the Same Prompt Give Different Answers?

## Short Answer

An LLM is a probability machine, not a deterministic lookup. The same prompt can produce different answers because of random sampling, tiny floating-point differences on the GPU, changes rolling out behind the API, and plain caching behavior. Identical text in does not guarantee identical text out.

## Four Separate Causes

**1. Sampling (temperature / top-p).** Most LLMs don't pick one fixed answer — they sample from a probability distribution over the next token. Temperature and top-p shape how much randomness that distribution allows, so the same prompt can roll a different next token each time.

**2. Batching and floating-point order on GPUs.** GPUs sum numbers in different orders depending on how requests are batched together. Floating-point addition isn't exactly associative, so the tiny rounding differences can flip which token wins when two candidates are nearly tied.

**3. Model or system-prompt updates behind an API.** API providers iterate on their models and system prompts without changing the endpoint. The same call hashed out weeks apart can quietly be answered by a slightly different model.

**4. Prompt caching is a speed feature, not a determinism feature.** Prompt caching fast-forwards the KV cache, it doesn't pin the output. As the caching article notes, it reduces cost and latency — it says nothing about returning identical text.

## What Temperature 0 Guarantees

Temperature 0 means greedy decoding: the model picks the single top token at each step instead of sampling. That still does NOT guarantee bit-identical output across runs or hardware, because the arithmetic that decides "top" can round differently inside every batch and GPU kernel.

## Related

- [is-prompt-caching-the-kv-cache.md](is-prompt-caching-the-kv-cache.md)
- [why-ai-hallucinates.md](why-ai-hallucinates.md)

## One-Liner

```
Same prompt can roll different answers
Greedy is repeatable in theory, not bit-identical in practice
Caching speeds you up, it doesn't pin the output
```