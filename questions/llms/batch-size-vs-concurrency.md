# Batch Size vs Concurrency in LLM Serving: Same Thing?

## Short Answer

**No.** They sound like one idea but count different things. Concurrency is how many requests are in flight in the serving system at once; batch size is how many sequences a single forward pass processes. A bigger batch can let a server accept more concurrent requests, but the two numbers don't move in lockstep.

## Two Different Counts

**Concurrency is a serving-system number.** It counts how many requests are in flight at any moment — queued, doing their first-token pass, or generating. A server with concurrency N can hold N conversations open at the same time, across N different users.

**Batch size is a single-forward-pass number.** It counts how many independent sequences the GPU stuffs into one forward pass, sharing the same weight matrices. One pass produces one token for every sequence in the batch, so reading the weights costs as much as reading them once but pays off many outputs.

## Continuous Batching

The naive way to serve is **static batching**: collect requests until the batch is "full", run the whole batch to the end, then start the next. **Continuous batching** (iteration-level scheduling) removes that barrier. At the end of each decode iteration the scheduler can drop sequences that finished and add sequences that just arrived — so a new request can join a batch that is already mid-generation and get its first token from the very next forward pass, without waiting for the whole batch to drain.

```
                   running batch (already generating)
            ┌────────────────────────────────────────────────┐
            │  Pass 10:   [A][B][C]  →  each advances a token │
            │  Pass 11:   [A][B][C][D]  ← D joins mid-run     │
            │             D gets its FIRST token right here   │
            └────────────────────────────────────────────────┘
                     ▲
          a new request arrives while the batch is running
```

Because a request can slide into a batch that is already running, **concurrency and batch size are decoupled**: concurrency can climb as requests keep arriving while the batch stays capped by a memory limit, or the server can run a few very large batches at low concurrency.

## The Trade

**A bigger batch raises total throughput.** More sequences per pass means the weight matrices are reused by more tokens in the same pass, so the hardware does more useful output per read of weights — total tokens per second for the server goes up.

**A bigger batch also raises per-token latency for each request.** Every token in the batch waits for the whole pass — the prefill of newly joined sequences plus every other sequence's decode — to finish. A token from a long request can stall on short requests sharing the batch, so each individual request feels slower at the same moment the server as a whole gets faster.

## Related

- [why-local-model-slows-down-long-chat.md](why-local-model-slows-down-long-chat.md)
- [is-moe-loaded-in-ram.md](is-moe-loaded-in-ram.md)

## One-Liner

```
Concurrency = requests in flight; batch size = sequences per forward pass
Continuous batching lets a new request join a batch that is already running
Bigger batch: more total throughput, slower per-token latency
```