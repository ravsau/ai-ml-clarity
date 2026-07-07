# Does Prompt Caching Use the KV Cache?

## Short Answer

**Yes — prompt caching *is* KV-cache reuse.** There's no separate cache. The thing being stored and reused is the **KV tensors** (the Key/Value attention vectors) computed during prefill. "Prompt caching" is just the provider's product name for keeping that KV cache around between requests.

## The Terms Stack

They sound like three things. They're one thing at three altitudes.

| Term | What it means |
|------|---------------|
| **KV cache** | The underlying **data** — the K/V attention tensors for tokens already processed |
| **Prefix caching** | The **technique** of keeping that KV cache around and reusing it for a new request whose prefix matches (e.g. vLLM's "automatic prefix caching") |
| **Prompt caching** | The **provider product name** for the same technique (Anthropic, OpenAI, Google) — you flag a prefix, they persist its KV cache server-side |

```
        prompt caching   ← what the provider sells you
              │  (same thing, marketing name)
        prefix caching    ← what the technique is called
              │  (reuses…)
          KV cache        ← the actual bytes being reused
```

## Why This Trips People

"Prompt caching" *sounds* like it caches the prompt text, or the model's answer. It doesn't. It caches the **intermediate attention state** the model built while reading the prefix — so the model can skip re-reading that prefix next time.

> From the docs: *"Prompt caching refers to provider-managed features that reuse KV tensors across API requests when prompts share common prefixes."*

That's the KV cache, persisted.

## The Catch (Same as Plain KV Cache)

Reuse only happens when the prefix is **byte-for-byte identical** — same tokens, same order, same whitespace. Change one character near the start and there's nothing to reuse; the model rebuilds the KV cache from scratch.

## One-Liner

```
Prompt caching  = prefix caching = reusing the KV cache
It caches the attention state, not the prompt text or the answer
Works only when the prefix matches exactly
```

See also: [Does a KV cache speed up your next prompt?](does-kv-cache-speed-up-next-prompt.md) · [Why is the first token slow but the rest are fast?](why-first-token-slow.md)

---

## Sources

- [Prefix caching — LLM Inference Handbook (BentoML)](https://bentoml.com/llm/inference-optimization/prefix-caching)
- [Automatic Prefix Caching — vLLM docs](https://docs.vllm.ai/en/stable/design/prefix_caching/)
- [Prompt Caching Infrastructure Guide 2025 — Introl](https://introl.com/blog/prompt-caching-infrastructure-llm-cost-latency-reduction-guide-2025)
