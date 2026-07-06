# Is All of the MoE Loaded in RAM?

## Short Answer

**Yes.** Every expert's weights must sit in memory (GPU VRAM or system RAM) to run the model. Only a few experts *fire* per token, but the router can pick any of them, so all of them have to be loaded and ready.

## The Confusion

> "MoE only activates 2 experts per token — so it's smaller, right?"

Not in memory. MoE splits **compute**, not **storage**.

```
┌──────────────────────────────────────────────────────────┐
│  What gets LOADED          vs      What gets USED          │
│                                                            │
│  ████████████████████            ██░░░░░░░░░░░░░░░░░░       │
│  ALL experts in RAM              ~2 experts per token      │
│  (100% resident)                 (a fraction computed)     │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

## Storage vs Compute

| | Static size (RAM/VRAM) | Per-token compute (FLOPs) |
|-|------------------------|---------------------------|
| **Dense model** | All params loaded | All params used |
| **MoE model** | All params loaded | Only active experts used |

MoE is **heavier** on memory, **lighter** on compute.

## Example: Mixtral 8x7B

| Metric | Value |
|--------|-------|
| Total params (must load) | ~47B |
| Active params per token | ~13B |
| Memory footprint | Like a 47B model |
| Speed / cost per token | Like a 13B model |

You pay 47B's rent, but only 13B's electricity bill.

## So What Makes It "Lighter" Than Dense?

Not size — **execution**. For each token the router activates only a couple of experts:

- **Fewer FLOPs** — less math per token
- **Faster generation** — tokens come out at small-model speed
- **Lower power** — each prompt costs less to run

You get the *knowledge* of a giant model at the *speed* of a small one.

## Fitting It On Your Hardware

| Technique | What it does |
|-----------|--------------|
| **Offloading** | Keep base layers on GPU, push experts to system RAM (e.g. `llama.cpp -ngl`) |
| **Quantization** | Compress weights (GGUF Q4/Q5) to shrink the footprint with minimal quality loss |

## One-Liner

```
MoE = all weights loaded, few weights used
Heavier in RAM, lighter in compute
Trades cheap memory space for expensive compute speed
```
