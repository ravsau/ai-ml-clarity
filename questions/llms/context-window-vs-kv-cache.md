# What Is the Difference Between a Context Window and a KV Cache?

## Short Answer

**Context window** = the limit set by the model — the maximum amount of text it can see at once. **KV cache** = the memory holding the Key/Value attention vectors of tokens already processed. One is a boundary; the other is storage that lives inside it.

## One Thing, Two Confused Ideas

People say "I ran out of context" when they usually mean "I ran out of working memory." They're different:

| Aspect | Context window | KV cache |
|--------|----------------|----------|
| What it is | A **limit** set by the model | The **memory** holding K/V vectors of tokens already processed |
| Size | Fixed by the model | Grows with every token processed |
| Where it lives | The model definition | Your RAM / VRAM |
| Failure mode | Old tokens get pushed out | You can run out of memory |

## The Picture: A Fixed Box With Growing Contents

```
┌─────────────────────────────────────────────────────────────┐
│                 CONTEXT WINDOW (FIXED BOX)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 KV CACHE (GROWS INSIDE)              │  │
│  │                                                       │  │
│  │  [ token ▒ ]                                          │  │
│  │  [ token ▒▒ ]            ◆ conversation grows         │  │
│  │  [ token ▒▒▒ ]           ◆ cache grows with it        │  │
│  │  [ token ▒▒▒▒ ]                                      │  │
│  │  [ token ▒▒▒▒▒ ] ◆ chat keeps going                  │  │
│  │  [ token ▒▒▒▒▒▒ ] ◆ cache keeps filling              │  │
│  │                                                       │  │
│  │  ▲  the cache fills the box — it never overflows,     │  │
│  │  └  but it can fill the whole box                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  window size is set when the model is built — fixed.        │
└─────────────────────────────────────────────────────────────┘
```

The box has a fixed size you can't change; the cache grows to fill it.

## The Practical Consequence

The context window is **fixed by the model** — you cannot grow it, no matter how long the chat gets. The KV cache, by contrast, **grows with the conversation** and consumes RAM/VRAM the whole way. So a long chat can run out of memory *before* it runs out of window: the model could still "hold" more text, but the compute that's holding it has nowhere left to put it.

This is why long chats slow down and eventually stall — not because the model forgot anything, but because the memory behind it filled up first.

## Related

- [what-is-context-window.md](what-is-context-window.md)
- [why-kv-cache-needs-ram.md](why-kv-cache-needs-ram.md)
- [does-kv-cache-speed-up-next-prompt.md](does-kv-cache-speed-up-next-prompt.md)

## One-Liner

```
Context window = the limit set by the model
KV cache = the memory holding what it has already read
A long chat can run out of RAM before it runs out of window
```