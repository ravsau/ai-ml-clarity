# Is Fine-Tuning Part of Post-Training?

## Short Answer

**Yes.** Post-training is the umbrella term for *everything you do after pre-training* — and fine-tuning is one of the main things under that umbrella.

## The Two Phases

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PRE-TRAINING                                               │
│  ────────────                                               │
│  Learn language from raw internet-scale text                │
│  Random weights ──► a "base model" that predicts next token │
│  Weeks/months · massive data · $$$$$$$                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  POST-TRAINING  (everything after)                          │
│  ─────────────                                              │
│  Shape the base model into something useful & safe          │
│     ├─ Supervised fine-tuning (SFT)                         │
│     ├─ RLHF / DPO (preference alignment)                    │
│     └─ Domain / task fine-tuning                            │
│  Hours/days · small curated data · $                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## What Lives Under Post-Training

| Step | What it does |
|------|--------------|
| **Supervised fine-tuning (SFT)** | Teach the base model to follow instructions |
| **RLHF / DPO** | Align outputs with human preferences |
| **Task/domain fine-tuning** | Specialize for your data (legal, medical, code) |

All of these are forms of fine-tuning or build on it — so fine-tuning sits squarely inside post-training.

## The Relationship

```
Training
 ├─ Pre-training      (build the base model)
 └─ Post-training     (refine it)
      └─ Fine-tuning  ← you are here
```

Fine-tuning is a **subset** of post-training. Post-training is a **subset** of training overall.

## Careful With Wording

- "Fine-tuning is *a* post-training method" ✅
- "Post-training *is* fine-tuning" ❌ (post-training also covers RLHF, DPO, etc.)

## One-Liner

```
Pre-training  = build the base model
Post-training = refine it (the umbrella)
Fine-tuning   = one tool under that umbrella
```

See also: [Is fine-tuning the same as training?](fine-tuning-vs-training.md)
