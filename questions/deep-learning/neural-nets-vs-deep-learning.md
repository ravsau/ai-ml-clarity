# Are All Deep Learning Models Based on Neural Networks?

## Short Answer

**Yes.** All deep learning = neural networks. That's the definition.

## The Hierarchy

```
┌─────────────────────────────────────────────────────┐
│                 MACHINE LEARNING                     │
├────────────────────────┬────────────────────────────┤
│   Not Neural Networks  │      Neural Networks       │
├────────────────────────┼────────────────────────────┤
│ • Linear Regression    │  ┌──────────────────────┐  │
│ • Decision Trees       │  │   Shallow NN         │  │
│ • Random Forests       │  │   (1 hidden layer)   │  │
│ • XGBoost/LightGBM     │  ├──────────────────────┤  │
│ • SVM                  │  │   DEEP LEARNING      │  │
│ • k-means              │  │   (many layers)      │  │
│ • PCA                  │  │   • CNN              │  │
│                        │  │   • RNN/LSTM         │  │
│                        │  │   • Transformer      │  │
│                        │  │   • Diffusion        │  │
│                        │  └──────────────────────┘  │
└────────────────────────┴────────────────────────────┘
```

## Key Distinctions

| Term | Definition |
|------|------------|
| Neural Network | Layers of neurons: `input → transform → nonlinearity → repeat → output` |
| Shallow NN | 1 hidden layer |
| Deep Learning | Many hidden layers - learns hierarchical features automatically |

## Common Deep Learning Architectures

| Architecture | Primary Use |
|--------------|-------------|
| CNN | Images, vision |
| RNN/LSTM | Sequences, time series |
| Transformer | Language, vision, multimodal |
| Diffusion | Image/video generation |

All share the same foundation: **neurons + weights + backprop**

## One-Liner

```
All deep learning = neural networks
Not all neural networks = deep learning
Not all ML = neural networks
```
