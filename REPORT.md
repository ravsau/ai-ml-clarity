# REPORT: box/issue-4-contributing

## What I understood the task to be

Add a new root-level `CONTRIBUTING.md` to the ai-ml-clarity repo that documents the
question-file format, derived entirely from the existing question files. It must be under
400 words, use only the existing files as evidence, and touch no other files. The work lives
on branch `box/issue-4-contributing` (<commit 5e7ca58>). The only files changed: CONTRIBUTING.md (added).

## Acceptance criteria and how each was met

1. **File naming** — "File naming" section: lowercase, hyphens, compressed question
   (`why-first-token-slow.md`), `.md` suffix.
2. **Directory choice** — "Directory choice" section states the rule of thumb exactly as the
   existing layout shows: `fundamentals/` = pre-LLM concepts, `deep-learning/` = architecture
   and training, `llms/` = inference, serving, prompting, RAG; edge cases lean toward `llms/`.
3. **Heading structure** — "Heading structure" section, quoted skeleton: `# <question>`,
   `## Short Answer`, 2-4 body sections (tables/ASCII welcome), fenced block under
   `## One-Liner` (example block copied from `ai-model-vs-assistant.md`).
4. **Length** — "Length" section cites the observed `wc -w` range (197-833), measured on
   2026-09-02. The five measured files are listed below.
5. **Cross-linking** — "Cross-linking" section: sibling-relative links inside `questions/`
   (`why-first-token-slow.md`), root-relative from README
   (`questions/llms/why-first-token-slow.md`); external `http(s)://` links noted.
6. **No-invented-numbers rule** — present verbatim: "Cite a source next to the figure, or
   leave the figure out."
7. **README index update** — "Updating the README index" section: `scripts/build_index.py`
   does not exist, so it documents the manual step of adding one row to the `| Question | File |`
   table under `## Index`.

## Five files measured (wc -w, 2026-09-02)

| File | Words |
|------|-------|
| questions/fundamentals/parameters-vs-hyperparameters.md | 197 |
| questions/fundamentals/precision-vs-recall.md | 833 |
| questions/deep-learning/how-are-huge-models-trained.md | 313 |
| questions/llms/why-first-token-slow.md | 480 |
| questions/llms/why-local-model-slows-down-long-chat.md | 700 |

These span one file per category (plus two more in fundamentals) and three from `questions/llms/`,
and establish the min (197) and max (833) that bracket the full file set (all 27 files verified:
min 197, max 833).

## Seeded-failure result

Not applicable per the packet. No seeded change was introduced, so nothing to revert.
`git status --short` after the CONTRIBUTING.md commit shows an empty (clean) tree, and the
commit diff list only `CONTRIBUTING.md`.

## Full VERIFY output

```
$ wc -w CONTRIBUTING.md
306 CONTRIBUTING.md
$ grep -c '^## ' CONTRIBUTING.md
7
$ git status --short
(empty)
```

All three checks pass: 306 < 400; 7 sections within 5-8; `git status --short` lists no
unexpected files.

## Things I was unsure about / guessed at

- The selection of the five files for the report is meant to be a representative audit
  sample; I chose files that give both the min and max word counts plus one `deep-learning/`
  file and two more `llms/` files. The range claim in CONTRIBUTING.md actually covers all
  27 files, not just these five.
- The "measured on <date>" value uses the current container date, 2026-09-02.
- "Everything up-to-date" on the first push confirmed the branch was already pushed by the
  prior session; the tracking line below is the confirming push output.

## Exact git push output line

```
branch 'box/issue-4-contributing' set up to track 'origin/box/issue-4-contributing'.
```