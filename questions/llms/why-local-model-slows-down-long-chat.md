# Why Does My Local Model Get Slower the Longer We Chat?

## Short Answer

Because every message adds to the **KV cache** — the model's memory of the conversation so far — and generating each new token means **reading that entire growing cache**. Token generation is limited by memory bandwidth, so a bigger cache = slower tokens. And on local hardware there's a **cliff**: once the cache no longer fits in VRAM, it spills into ordinary system RAM and everything crawls.

## What's Actually Growing

Each token the model has seen leaves behind Key/Value attention vectors in the KV cache. The cache **grows linearly with the length of the conversation** — for an 8B model at 32K tokens it can hit ~4 GB, nearly the size of the model weights themselves.

```
Turn 1:  [▓▓]                    small cache → fast
Turn 5:  [▓▓▓▓▓▓▓▓]              bigger cache → slower
Turn 20: [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]    huge cache → crawling
          ▲ every token must read ALL of this to make the next one
```

## Why a Bigger Cache = Slower Tokens

Generating text (the **decode** phase) is **memory-bandwidth-bound**, not compute-bound. To produce one token, the GPU reads the model weights *and* the whole KV cache. More conversation → more cache bytes to stream per token → fewer tokens per second.

(Attention cost also grows with length — roughly O(n) per token — but the felt bottleneck on local machines is usually the memory traffic, then the cliff below.)

## The Cliff: Spilling Out of VRAM

This is the part that feels like a sudden crash, not a gentle slowdown:

| State | Speed |
|-------|-------|
| Model + KV cache fit in **VRAM** | Fast (the happy path) |
| Cache grows past VRAM → spills to **system RAM / CPU** | **Crawls** — every token now pays for slow host-memory access and CPU↔GPU shuffling |

> *"What looks like 'context doubled and performance crashed' is often really a case of the data path falling out of VRAM and into much slower memory."*

That's why the slowdown often isn't gradual — you chat fine for a while, then hit a wall.

## Then Why Don't Cloud Models Seem to Slow Down?

They're **not immune** — the same physics apply, and their cost and time-to-first-token *do* rise with context. Cloud just has the headroom and engineering to hide it:

| Local pain | How cloud masks it |
|------------|--------------------|
| Cache spills out of 8–24 GB VRAM | Datacenter GPUs (e.g. 80 GB H100) + far higher memory bandwidth — the cache rarely overflows, so **no cliff** |
| Cache wastes/fragments memory | **PagedAttention** packs the KV cache like OS virtual memory (<4% waste) |
| Re-processing the history each turn | **Prefix caching** reuses the KV cache for the unchanged conversation prefix |
| One long chat monopolizes the GPU | **Continuous batching + chunked prefill** spread the load and bound latency spikes |

So cloud creeps up slowly and invisibly; a local machine hits a hard memory wall.

## What Helps Locally

- **KV cache quantization** (e.g. 8-bit/4-bit KV) — shrinks the cache so it stays in VRAM longer
- **Smaller context window** — don't reserve more than you need (llama.cpp pre-allocates for the full window)
- **A smaller / more quantized model** — leaves more VRAM for the cache
- **Trim the conversation** — summarize or drop old turns instead of carrying everything

## One-Liner

```
Longer chat → bigger KV cache → more bytes to read per token → slower
Local: cache spills out of VRAM into RAM → sudden crawl (the cliff)
Cloud: same physics, but big VRAM + PagedAttention + prefix caching hide it
```

See also: [Does a KV cache speed up your next prompt?](does-kv-cache-speed-up-next-prompt.md) · [Why is the first token slow but the rest are fast?](why-first-token-slow.md)

---

## Sources

- [Why Ollama and llama.cpp crawl when models spill into RAM — PopularAI](https://www.popularai.org/p/why-ollama-and-llama-cpp-crawl-when-models-spill-into-ram-and-how-to-fix-it)
- [KV Cache Memory Calculation for LLMs — Lyceum Technology](https://lyceum.technology/magazine/kv-cache-memory-calculation-llm/)
- [How KV Caching Slashes LLM Inference Costs at Scale — DigitalOcean](https://www.digitalocean.com/community/conceptual-articles/how-kv-caching-slashes-llm-inference-costs-at-scale)
- [How to Tune llama.cpp on 8GB VRAM: KV Cache Quantization — Knightli](https://knightli.com/en/2026/04/23/llama-cpp-8g-vram-32k-64k-kv-cache-tuning/)
- [LLM Serving Optimization: Continuous Batching, PagedAttention, Chunked Prefill — Spheron](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/)
