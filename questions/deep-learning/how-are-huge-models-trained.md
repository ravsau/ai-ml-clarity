# How Do You Train a Model Too Big for One GPU?

## Short Answer

**You don't fit it on one GPU — you split it across many.** A top training GPU holds ~80 GB. Models can be hundreds of GB. So the model itself is cut into pieces across GPUs, and then that whole group is cloned to train on more data at once.

## The Confusion

> "They must use one massive GPU, right?"

No such thing. It is always many separate GPUs wired together with very fast links, working in sync.

## Two Ways to Split

| Split | What it means | Why |
|-------|---------------|-----|
| **Model parallel** | Different GPUs hold different layers | The model is too big to fit in one GPU's memory |
| **Data parallel** | Each GPU (or group) holds a full copy and trains on a different slice of data | Chew through more data at once = faster |

Big runs use both: a group of GPUs holds one full model, and many such groups run side by side. A cluster of clusters.

## The Memory Surprise

Training needs about **4× the model's size** in memory, not 1×:

```
weights          the model itself
gradients        one per weight
optimizer state  Adam keeps 2 more per weight
activations      saved layer outputs for backprop
```

A 100 GB model can need 400 GB+ to actually train.

## The Bottleneck

Every step, the GPUs must sync (share gradients). If they can't talk fast enough, they sit idle. That is why these clusters use special interconnects (NVLink, InfiniBand) — the coordination, not the math, is often the hard part.

## One-Liner

```
Too big for one GPU = split the model across many
Want it faster = clone that group across data
Training memory = ~4x the model (weights + gradients + optimizer + activations)
```
