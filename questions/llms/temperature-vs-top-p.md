# Temperature vs Top-p: What Actually Changes?

## Short Answer

Temperature and top-p are two different ways to make the model's next-token choice less predictable. Temperature rescales the whole probability distribution, making it flatter or sharper, while top-p cuts the low-probability tail so sampling only considers a focused set of likely tokens. Both control randomness, but they shape the distribution in different ways and are often used together.

## What Each Knob Does

| Knob | What it does |
|------|--------------|
| **Temperature** | Rescales the whole probability distribution — higher values flatten it (more random), lower values sharpen it (more focused) |
| **Top-p** | Cuts the tail and samples only from the smallest set of tokens whose probabilities add up to p — removes the long tail of unlikely tokens |

## The Picture

One bar chart, shown three times: raw distribution, after temperature, after top-p.

```
        RAW DISTRIBUTION
  ██
  ██
  ██
  ██
  ██        █
  ██        █     █        █    █    █   █ █ █ █
  ─────────────────────────────────────────────
   best    2nd   3rd   ...every token with a tail...

        AFTER TEMPERATURE (high temp)
  ███   ███   ██   ██    █   █    █    █   █   █
  ─────────────────────────────────────────────
  flats every bar — the whole shape melts

        AFTER TOP-P
  ███████
  ███████
  ███████
  ███████
  ────────────
  only the small set that together reaches p — the tail is gone
```

## When to Touch Which

- Reach for **temperature** when you want the whole response to feel more or less creative.
- Reach for **top-p** when you want to block absurd, off-the-wall tokens outright.
- Lower **temperature** on factual tasks to keep output tight and predictable.
- Raise **temperature** for brainstormy, open-ended writing.
- Keep **top-p** moderate to trim nonsense without flattening the sensible options.
- The common mistake: raising **both at once** — kind of like turning up the volume and the treble at the same time. Each already adds randomness on its own, and stacking them can push output into incoherence fast. Start by raising one.

## Related

- [tokens-vs-words.md](tokens-vs-words.md)
- [why-ai-hallucinates.md](why-ai-hallucinates.md)

## One-Liner

```
Temperature reshapes the whole curve
Top-p cuts the tail off that curve
Raise one at a time, not both
```