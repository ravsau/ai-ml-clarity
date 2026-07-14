# Distillation vs Quantization vs Pruning

## Short Answer
Three axes of model compression: quantization changes how numbers are stored, pruning deletes parts of the network, distillation trains a new smaller model to imitate the big one. They compose — production pipelines usually prune → distill → quantize, not pick one.

## Diagram
```
                    BIG MODEL (FP32, dense, N layers)
                              |
        +---------------------+---------------------+
        |                     |                     |
   QUANTIZATION           PRUNING              DISTILLATION
   same weights,          same precision,      new architecture,
   fewer bits             fewer weights        trained on teacher's
                                               soft targets
        |                     |                     |
   FP32 -> INT8/INT4     dense -> sparse       teacher -> student
   (~75% smaller         (structured or        (best perf/size,
    at INT8, cheap)       unstructured)         most expensive)
```

## Key Distinctions

| | Quantization | Pruning | Distillation |
|---|---|---|---|
| What changes | Number precision (bits per weight) | Which weights/heads/layers exist | The entire architecture |
| Training needed | Often none (PTQ); QAT for low bits | Fine-tune to recover accuracy | Full training run |
| Memory win | Direct and guaranteed (INT8 = 4x vs FP32) | Only if structured or hardware supports sparsity | Direct — the model is just smaller |
| Latency win | Large (memory-bandwidth bound inference) | Only structured pruning reliably helps | Large |
| Cost to apply | Low | Medium | High (compute + a good dataset) |
| Failure mode | Accuracy cliff below ~4 bits; outlier activations | One-shot pruning destroys quality | Student inherits teacher's mistakes; capacity ceiling |

The non-obvious parts:

- **Unstructured pruning is often a paper win.** Zeroing 50% of individual weights gives you nothing on a GPU unless the kernel exploits sparsity (e.g. 2:4 semi-structured on Ampere+). Structured pruning (whole heads, whole layers) actually speeds things up.
- **Quantization wins because LLM inference is memory-bandwidth bound.** Fewer bits = fewer bytes moved per token. That's why INT8/INT4 helps even when compute doesn't drop.
- **Distillation isn't "training on teacher outputs."** Classic KD trains on soft targets — the full probability distribution — which carries dark knowledge (how wrong the wrong answers are). For LLMs it's often sequence-level: generate with the teacher, SFT the student.
- **Order matters.** Prune first (shrink the active set), distill to recover quality in the smaller space, quantize last for deployment. Quantizing before pruning wastes the precision budget on weights you're about to delete.

## One-Liner
Quantization is shorthand, pruning is deleting, distillation is teaching — and in production you do all three, in that reverse order of cost.
