# Contributing

Every question lives as its own markdown file under `questions/`. Before adding one, read a few existing files and match their style: short sections, tables, ASCII diagrams, and a `## One-Liner` block at the end.

## File naming

The filename is lowercase, hyphen-separated, and compressed from the question (e.g. `why-first-token-slow.md`), always ending in `.md`.

## Directory choice

Pick a folder by this rule of thumb, following what the existing files show:

- `fundamentals/` — concepts that predate LLMs (parameters, embeddings, precision vs recall).
- `deep-learning/` — architecture and training (transformers, how huge models are trained).
- `llms/` — inference, serving, prompting, and RAG (KV cache, quantization, context window).

Questions on the edge lean toward `llms/`.

## Heading structure

Quoted from the existing files, every question follows the same skeleton:

1. `# <question>` — a single H1 line holding the question.
2. `## Short Answer` — the direct answer first.
3. Two to four body sections; tables and ASCII diagrams are welcome.
4. A fenced block under `## One-Liner`:

```
Model     = weights. Tokens in, tokens out.
Assistant = model + system prompt + memory + tools + UI.
```

## Length

Word counts of the existing files, measured with `wc -w` on 2026-09-02, range from 197 to 833 words. Stay inside that range.

## Cross-linking

- Inside `questions/`, link to a sibling by its bare filename, e.g. `[Why is the first token slow?](why-first-token-slow.md)`.
- From `README.md`, link root-relative, e.g. `[llms/why-first-token-slow.md](questions/llms/why-first-token-slow.md)`.
- External links are `http(s)://` and should be ignored by any link checker.

## No invented numbers

Cite a source next to the figure, or leave the figure out.

## Updating the README index

`scripts/build_index.py` does not exist yet, so update the index by hand: under `## Index`, add one row to the `| Question | File |` table, following the existing rows' format.