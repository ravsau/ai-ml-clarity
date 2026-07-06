# Does Multi-Token Prediction (MTP) Lower Quality?

## Short Answer

**No — usually the opposite.** MTP is a *training* technique where the model learns to predict several future tokens at once. It tends to **improve** quality, and at inference it's used to go faster without changing what the model would have said.

## The Confusion

> "If it predicts multiple tokens at once, it must be guessing more — so quality drops, right?"

That mixes up two different things: **how MTP trains** and **how it's used at inference**.

## What MTP Actually Is

Standard training teaches the model **one** job: predict the next token.
MTP adds **extra heads** so it also predicts the token after that, and the one after that.

```
Normal:   [The cat sat on the] ──► ?        (predict 1 token)

MTP:      [The cat sat on the] ──► ? ? ?     (predict next 3)
                                   │ │ └─ head 3
                                   │ └─── head 2
                                   └───── head 1 (the "real" one)
```

Predicting further ahead forces the model to **plan**, which sharpens its internal representations — a *better* learning signal, not a noisier one.

## Two Places It Shows Up

| Where | Effect on quality |
|-------|-------------------|
| **During training** | Auxiliary MTP heads → often **better** base model (DeepSeek-V3 uses this) |
| **During inference (speculative-style)** | Extra tokens are **verified** by the main head → output is identical, just faster |

## Why Inference Stays Lossless

The extra heads only *propose* future tokens. The main model still **checks** each one:

- Guess accepted → you got it for free (speed ↑)
- Guess wrong → it's thrown away, model falls back to normal decoding

Either way the final text is what the model would have produced anyway.

```
Draft:   the  →  mat  →  and    (proposed by MTP heads)
Verify:  ✅      ✅      ❌       ← wrong one rejected
Output:  the mat  (then continue normally)
```

## When Quality *Could* Dip

MTP itself doesn't hurt quality. Watch out only when it's **combined** with lossy tricks:

| Setup | Risk |
|-------|------|
| MTP as a verified draft | None — lossless |
| Accepting draft tokens **without** verifying | Quality drops (not real MTP anymore) |
| MTP + aggressive quantization of the draft head | Fewer accepts, slower — not worse output |

## One-Liner

```
MTP in training  = better model (learns to plan ahead)
MTP at inference = same output, faster (drafts get verified)
It lowers quality only if you skip the verification step
```
