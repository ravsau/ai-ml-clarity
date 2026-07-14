# Why Does the KV Cache Eat So Much GPU RAM?

## Short Answer

The **KV cache** stores the Key and Value vectors for every token already generated, so the model doesn't recompute attention over the whole sequence on every step. It grows **linearly with sequence length × batch size** — and at long context it dwarfs the model weights.

## Why the Cache Exists

Attention needs every previous token's K and V to generate the next one. Without a cache, generating token 1000 means recomputing K/V for tokens 1–999 — every step. Summed over the whole generation, that's O(n²) recompute instead of O(n).

```
Decode step N:
  new query  ──┐
               ├──► attention over ALL past K,V ──► next token
  cached K,V ──┘   (K,V for tokens 1..N-1 already computed)

Compute each token's K,V once, reuse forever.
```

Trade compute for memory. The memory bill is the catch.

## The Memory Formula

```
KV bytes = 2 × layers × kv_heads × head_dim × seq_len × batch × bytes_per_value
           ▲
           K and V (two tensors)
```

Every new token appends one K and one V vector **per layer**. Deep model + long context + big batch = the cache explodes.

### Worked example (Llama-3-70B-ish, FP16)

| Term | Value |
|------|-------|
| Layers | 80 |
| KV heads (GQA) | 8 |
| Head dim | 128 |
| Bytes/value | 2 (FP16) |
| **Per token** | 2 × 80 × 8 × 128 × 2 ≈ **327 KB** |
| **32K context** | ≈ **10.7 GB** — for *one* sequence |

Batch 20 users at 32K → ~214 GB of cache alone, on top of 140 GB of weights.

## FP16 vs FP8: Half the Bytes, Half the Cache

The `bytes_per_value` term is a direct multiplier, so quantizing the cache is a clean lever:

| Precision | Bytes/value | Relative KV memory |
|-----------|-------------|--------------------|
| FP16 | 2 | 1.0× (baseline) |
| FP8   | 1 | **0.5×** |

16 bits → 8 bits is exactly half the footprint *and* half the memory bandwidth per step. Quality impact on KV is usually small, but it depends on the kernel and workload — validate, don't assume.

## Why This Dominates at Scale

```
Weights:    fixed cost, loaded once
KV cache:   grows with EVERY token, EVERY concurrent user
                                    ▲
                    this is what limits how many
                    users you can serve per GPU
```

Throughput at long context is a **KV-cache memory** problem, not a FLOPs problem.

## The Levers (what you actually reach for in serving)

| Lever | Effect |
|-------|--------|
| **GQA / MQA** | Fewer KV heads → smaller cache (biggest structural win) |
| **KV quantization (FP8/INT8)** | Halve bytes/value |
| **PagedAttention (vLLM)** | Kill memory fragmentation, pack more sequences |
| **Sliding window / eviction** | Cap effective seq_len |
| **Shorter context / RAG** | Don't pay for tokens you don't need |

## One-Liner

Weights are a one-time bill; the KV cache is a per-token, per-user tax — and at long context the tax, not the model, decides how many users fit on the GPU.
