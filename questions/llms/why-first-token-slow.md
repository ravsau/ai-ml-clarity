# Why Is the First Token Slow but the Rest Are Fast?

## Short Answer

Because generating a response has **two phases with opposite costs**. **Prefill** reads your *entire* prompt in one shot before it can say anything — that's the wait for the first token. **Decode** then streams tokens one at a time, each cheap because the hard work is already cached. Long prompt → slow first token. The rest of the speed barely depends on prompt length.

## The Two Phases

```
   You hit enter
        │
        ▼
┌───────────────────────┐
│  PREFILL              │  Read the WHOLE prompt at once,
│  (build the KV cache) │  compute attention over every token.
│                       │  ⏳ This is your Time To First Token.
└───────────┬───────────┘
            ▼  first token appears
┌───────────────────────┐
│  DECODE               │  Generate one token, feed it back,
│  (one token at a time)│  repeat. Each step reuses the cache.
│                       │  ⚡ Fast, steady stream.
└───────────────────────┘
```

## Why Prefill Is the Slow Part

| | Prefill | Decode |
|-|---------|--------|
| Processes | All input tokens **at once** | **One** new token at a time |
| Parallel? | Yes — big matrix multiply | No — inherently sequential |
| Bottleneck | **Compute-bound** (GPU math) | **Memory-bound** (reading the KV cache) |
| Scales with | **Length of your prompt** | Length of the *output* |
| Feels like | The pause before it starts | The typing-out effect |

The first token can't appear until prefill has processed **the entire prompt** — system instructions, retrieved documents, chat history, and your question. Double the prompt, roughly double that initial wait.

## The Practical Consequence

- **Time To First Token (TTFT)** = basically your prefill time.
- A giant RAG context or long chat history makes the model feel *slow to respond*, even though it types just as fast once it starts.
- Want a snappier feel? Shrink what goes into the prompt (tighter retrieval, trimmed history), or reuse the prompt's opening via **prefix caching** so prefill can skip it.

## Why Decode Feels Fast

Each decode step only processes the single newest token — everything before it is read from the KV cache instead of recomputed. So per-token time is small and roughly constant, which is why output streams at a steady pace.

## One-Liner

```
Prefill = read the whole prompt first  → the wait for token #1 (TTFT)
Decode  = stream tokens one by one     → fast, cached, steady
Long PROMPT slows the start; long OUTPUT just takes more steps
```

See also: [Does a KV cache speed up your next prompt?](does-kv-cache-speed-up-next-prompt.md)

---

## Sources

- [Prefill vs Decode: LLM Inference Phases Explained — Redis](https://redis.io/blog/prefill-vs-decode/)
- [Understanding the Two Key Stages of LLM Inference: Prefill and Decode — Medium (Saiii)](https://medium.com/@sailakkshmiallada/understanding-the-two-key-stages-of-llm-inference-prefill-and-decode-29ec2b468114)
- [Prefill vs Decode: LLM Inference Optimization — Outcome School](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization)
- [Prefill-decode disaggregation — LLM Inference Handbook (BentoML)](https://bentoml.com/llm/inference-optimization/prefill-decode-disaggregation)
