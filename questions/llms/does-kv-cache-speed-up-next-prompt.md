# Does a KV Cache Speed Up Your Next Prompt?

## Short Answer

**Not by default — but yes if the two prompts share an identical opening.** A KV cache's main job is speeding up the *current* response. A brand-new, unrelated prompt starts cold. The exception is **prefix caching / prompt caching**, which reuses the cache across requests — *only* for the exact shared prefix.

## First, What the KV Cache Actually Does

As the model reads your prompt, attention computes a **Key** and **Value** for every token. The KV cache stores them so the model never recomputes the past — at each new token it only processes the *newest* token and looks up the rest.

```
Without cache: token 100 → re-process tokens 1…100   (wasteful)
With cache:    token 100 → process token 100, read 1…99 from cache  ✅
```

That's the whole point: it makes **generating each next token within one response** fast.

## The Misconception

> "So my *next prompt* will be faster because the cache is warm, right?"

Usually **no**. In naive serving, the KV cache lives for the duration of **one request** and is then freed. Send a different prompt and the model rebuilds the cache from scratch — cold start.

```
Prompt A: [long system prompt + question 1]  → builds cache → freed
Prompt B: [different prompt entirely]         → cold, no reuse
```

## The Real Exception: Prefix Caching

Modern inference servers (vLLM automatic prefix caching, and provider "prompt caching" from Anthropic / OpenAI) **do** carry the cache across requests — but with a strict rule:

> The shared prefix must be **exactly identical**, down to whitespace. One different character breaks it.

Because the KV cache of any token depends only on the tokens before it, two requests that begin with the same text can reuse that prefix's cache and skip re-processing it.

```
Request 1: [SAME 5,000-token system prompt] + "Summarize doc A"
Request 2: [SAME 5,000-token system prompt] + "Summarize doc B"
                     ▲
            prefix reused → only the new part is processed
```

**When it kicks in:** long, fixed system prompts, a big document you ask several questions about, multi-turn chats. Anthropic reports up to **~90% cost** and **~85% latency** reduction on long cached prompts.

**When it doesn't:** the shared part is short, or the beginning of the prompt changes (even slightly). Only a *matching prefix* is reused — never the middle or a divergent tail.

## So, Straight Answer

| Situation | Faster from the cache? |
|-----------|------------------------|
| Generating tokens *within* one response | ✅ Always — that's its job |
| A totally different next prompt | ❌ No — cold start |
| Next prompt shares an **identical prefix** + prefix caching is on | ✅ Yes — the shared prefix is skipped |

## One-Liner

```
KV cache = don't recompute past tokens (speeds THIS response)
A different next prompt = cold start by default
Identical prefix + prefix caching = the shared start is reused, not the whole thing
```

See also: [Why is the first token slow but the rest are fast?](why-first-token-slow.md)

---

## Sources

- [KV Cache Explained: The Complete Guide — Medium (Luv Bansal)](https://luv-bansal.medium.com/the-evolution-of-kv-cache-from-simple-buffers-to-distributed-memory-systems-df51cb8ce26f)
- [Prefix caching — LLM Inference Handbook (BentoML)](https://bentoml.com/llm/inference-optimization/prefix-caching)
- [Automatic Prefix Caching — vLLM docs](https://docs.vllm.ai/en/stable/design/prefix_caching/)
- [Prompt Caching Infrastructure Guide 2025 — Introl](https://introl.com/blog/prompt-caching-infrastructure-llm-cost-latency-reduction-guide-2025)
