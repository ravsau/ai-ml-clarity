# REPORT — box/issue-3-context-window-vs-kv-cache

## What I understood the task to be

Issue #3 asks for a new Q&A file `questions/llms/context-window-vs-kv-cache.md` explaining the difference
between a context window and a KV cache, plus a row in the README index table. The repo already had
`what-is-context-window.md`, `why-kv-cache-needs-ram.md`, and `does-kv-cache-speed-up-next-prompt.md`
(the three files named in the issue), but nothing that stated the relationship directly. I was to:

- Introduce the two concepts as: context window = the limit set by the model; KV cache = the memory
  holding the K/V vectors of tokens already processed.
- Draw one ASCII diagram showing the window as a fixed box and the cache growing inside it.
- State the practical consequence: window is fixed by the model, cache grows with the conversation and
  consumes RAM/VRAM, so a long chat can run out of memory before it runs out of window.
- Cross-link to the three existing related files, sibling-relative.
- Add a README row directly after the "Does prompt caching use the KV cache?" row.
- Use no invented numbers, and cite any figure copied from one of the four packet files.
- Not push to main, not open a PR, not comment on the issue.

I modeled the file on `is-prompt-caching-the-kv-cache.md` (the template): H1, `## Short Answer`,
short prose/tables, one ASCII diagram, a Related section, and a `## One-Liner` fenced block at the end.

## How I met each acceptance criterion

| Criterion | How shown |
|-----------|-----------|
| Follows the exact structure of existing files in `questions/llms/` | Matched template section order (H1 → Short Answer → body → diagram → practical consequence → Related → One-Liner) and length (~55 lines vs template's 53). |
| Explains context window is a limit and KV cache is the memory | Stated verbatim in `## Short Answer` and in the Aspect table. |
| States the practical consequence | `## The Practical Consequence` section: window fixed by the model; cache grows with the conversation and consumes RAM/VRAM; a long chat can run out of memory before it runs out of window. |
| Cross-links to the three existing related files | `## Related` with `[what-is-context-window.md](what-is-context-window.md)`, `[why-kv-cache-needs-ram.md](why-kv-cache-needs-ram.md)`, `[does-kv-cache-speed-up-next-prompt.md](does-kv-cache-speed-up-next-prompt.md)` — all three files exist. |
| Added to the README index table | Row added directly below the "Does prompt caching use the KV cache?" row; `grep -c` confirms exactly 1 occurrence of `context-window-vs-kv-cache`. |
| No invented numbers / cite if used | File contains no numbers at all; the number-check grep returns zero hits. |

## Seeded-failure step

The packet says SEEDED FAILURE is not applicable to a docs task, and instead to paste the output of the
last VERIFY line and justify every number it finds (or remove it). Output of the last VERIFY line:

```
grep -nE '[0-9]+ ?(K|GB|MB|tokens)' questions/llms/context-window-vs-kv-cache.md   # no output; exit=1
```

There are zero numbers in the file, so nothing to justify. No seeded change was present to revert.

## Full VERIFY output

```
$ test -f questions/llms/context-window-vs-kv-cache.md && head -1 questions/llms/context-window-vs-kv-cache.md
# What Is the Difference Between a Context Window and a KV Cache?

$ grep -c 'context-window-vs-kv-cache' README.md
1

$ grep -oE '\]\([a-z0-9-]+\.md\)' questions/llms/context-window-vs-kv-cache.md
](what-is-context-window.md)
](why-kv-cache-needs-ram.md)
](does-kv-cache-speed-up-next-prompt.md)

$ for f in $(grep -oE '\]\([a-z0-9-]+\.md\)' questions/llms/context-window-vs-kv-cache.md | tr -d '](()'); do test -f questions/llms/$f && echo "ok $f" || echo "MISSING $f"; done
ok what-is-context-window.md
ok why-kv-cache-needs-ram.md
ok does-kv-cache-speed-up-next-prompt.md

$ grep -nE '[0-9]+ ?(K|GB|MB|tokens)' questions/llms/context-window-vs-kv-cache.md
(no output; exit=1 → zero matches)
```

`git status` after the self-check showed only the two intended changes: `README.md` (one row added) and
the new untracked `questions/llms/context-window-vs-kv-cache.md`.

## Things I was unsure about / guessed at

- **Related-section placement.** The template (`is-prompt-caching-the-kv-cache.md`) puts its links on a
  `See also:` line after the One-Liner, but the packet explicitly requires a `## Related` section, so I
  used that heading and placed it between the practical-consequence section and the One-Liner so the
  One-Liner stays at the end.
- **Link display text.** The packet specified the `[what-is-context-window.md](what-is-context-window.md)`
  form exactly (filename as link text), which differs from the friendlier "See also" wording used in other
  files. I followed the packet's exact form.
- **Three "related" files.** The issue text names `what-is-context-window.md`, `why-kv-cache-needs-ram.md`,
  and `does-kv-cache-speed-up-next-prompt.md` as the three related files; the template
  `is-prompt-caching-the-kv-cache.md` is excluded from Related since it is the template, not a target.

## git push output

```
To https://github.com/ravsau/ai-ml-clarity.git
 * [new branch]      box/issue-3-context-window-vs-kv-cache -> box/issue-3-context-window-vs-kv-cache
branch 'box/issue-3-context-window-vs-kv-cache' set up to track 'origin/box/issue-3-context-window-vs-kv-cache'.
```

The commit message used was `Add Q&A: context window vs KV cache`, per the packet.