# Parameters vs Hyperparameters

## Short Answer

**Parameters** = learned by the model during training (weights, biases)
**Hyperparameters** = chosen by you before training (learning rate, batch size)

## The Distinction

```
┌─────────────────────────────────────────────────────────────┐
│                      YOUR ML MODEL                          │
├─────────────────────────────┬───────────────────────────────┤
│       PARAMETERS            │       HYPERPARAMETERS         │
│       (Learned)             │       (Chosen)                │
├─────────────────────────────┼───────────────────────────────┤
│ • Weights                   │ • Learning rate               │
│ • Biases                    │ • Batch size                  │
│ • Embeddings                │ • Number of layers            │
│ • Attention matrices        │ • Hidden units                │
│                             │ • Dropout rate                │
│                             │ • Optimizer (Adam, SGD)       │
├─────────────────────────────┼───────────────────────────────┤
│ Set by: Backpropagation     │ Set by: You (or tuning)       │
│ When: During training       │ When: Before training         │
│ Count: Millions/Billions    │ Count: Dozens                 │
└─────────────────────────────┴───────────────────────────────┘
```

## Why It Matters

| Problem | Likely Cause |
|---------|--------------|
| Loss not decreasing | Learning rate too high/low (hyperparameter) |
| Model not converging | Bad optimizer choice (hyperparameter) |
| Overfitting | Not enough regularization (hyperparameter) |
| Underfitting | Too few layers/units (hyperparameter) |

Bad hyperparameters prevent good parameters from being learned.

## One-Liner

```
Parameters: what the model learns
Hyperparameters: how the model learns
```
