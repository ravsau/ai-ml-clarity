# What Does Q2, Q4, Q5, Q8 Mean in Local AI Models?

## Short Answer

**They're quantization levels — the number is roughly how many bits each weight uses.** Lower Q = smaller file and less RAM, but more quality loss. Higher Q = closer to the original model, but bigger.

## The Idea

A model's weights are trained as 16-bit (or 32-bit) numbers. **Quantization** squeezes them into fewer bits so the model fits on your hardware.

```
Original weight:  0.7182631...  (16 bits, full precision)
        Q8:       0.718         (8 bits, ~identical)
        Q4:       0.72          (4 bits, small rounding)
        Q2:       0.7           (2 bits, blurry)
```

Fewer bits = less storage per number = smaller model.

## The Levels

| Level | Bits/weight | Size vs original | Quality |
|-------|-------------|------------------|---------|
| **Q8** | ~8-bit | ~50% | Near-perfect |
| **Q5** | ~5-bit | ~35% | Very good |
| **Q4** | ~4-bit | ~28% | Good — the sweet spot |
| **Q2** | ~2-bit | ~16% | Noticeably degraded |

Rule of thumb: **each step down halves quality loss forgiveness** — Q2 is where models start getting visibly dumber.

## Rough Memory (7B model)

| Level | File size on disk |
|-------|-------------------|
| FP16 (unquantized) | ~13 GB |
| Q8 | ~7 GB |
| Q5 | ~4.5 GB |
| Q4 | ~3.8 GB |
| Q2 | ~2.5 GB |

## What About the Extra Letters? (Q4_K_M, Q5_0…)

The suffixes describe *how* the quantization is done:

| Suffix | Meaning |
|--------|---------|
| `_0`, `_1` | Older/legacy schemes |
| `_K` | "K-quant" — smarter, mixed precision |
| `_S` / `_M` / `_L` | Small / Medium / Large variant of a K-quant |

`Q4_K_M` is the most common default — 4-bit K-quant, medium size, best balance.

## Which Should You Pick?

| Situation | Pick |
|-----------|------|
| Plenty of RAM/VRAM | Q8 or Q6 |
| Balanced (most people) | **Q4_K_M** |
| Tight on memory | Q3 / Q2 (expect quality drop) |

## One-Liner

```
Q# = bits per weight
Lower Q = smaller + faster + dumber
Q4_K_M = the default sweet spot
```
