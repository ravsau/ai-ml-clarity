# Tokens per Second vs Time to First Token: Which One Is Speed?

## Short Answer

Both, but they measure different stretches of the same run. **Time to First Token (TTFT)** is how long you wait before the model says anything — the prefill phase reading your whole prompt. **Tokens per second** is how fast the rest of the answer streams out — the decode phase. A fast first token can hide a slow stream, and vice versa.

## Two Clocks

One run, two clocks. TTFT watches the start line; tokens per second watches the finish line.

| Clock | What it measures |
|-------|------------------|
| **Time to First Token (TTFT)** | The **prefill** phase — reading the *entire* prompt in one big parallel pass |
| **Tokens per second** | The **decode** phase — generating *one* token per step and streaming it out |

## The Timeline

```
[prompt in] --prefill--> [first token] --decode, one token at a time--> [done]
              ^ TTFT         ^ tokens/sec measures this stretch
```

## Why They Move Separately

They're driven by different levers. A **longer prompt** makes prefill process more text, so TTFT goes up — while decode still steps one token at a time, so tokens/sec is barely affected. A **bigger model** has more math per step, which slows decode, so tokens/sec drops — while TTFT mostly tracks how much text had to be read before the first token.

A **chat user** feels TTFT: that pause before the answer starts decides whether it feels snappy. A **batch job** (processing thousands of prompts offline) cares about tokens/sec: it decides how long the whole job takes. "Speed" means two different things to each.

## Related

- [why-first-token-slow.md](why-first-token-slow.md)
- [why-kv-cache-needs-ram.md](why-kv-cache-needs-ram.md)

## One-Liner

```
TTFT = the pause before it starts (prefill, one big parallel pass)
Tokens/sec = the pace of the stream (decode, one token per step)
Chat users feel TTFT; batch jobs care about tokens/sec
```