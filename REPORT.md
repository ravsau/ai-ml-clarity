# REPORT: box/issue-8-what-is-a-system-prompt

## What I Understood the Task to Be

The task (TASK.md, referring to issue #8) was to add a new Q&A file
`questions/llms/what-is-a-system-prompt.md` and exactly one README index row for it,
matching the style and shape of the existing LLM question files (`is-prompt-caching-the-kv-cache.md`
as the template, plus links to `what-is-context-window.md` and `context-window-vs-memory.md`).
Then push the branch `box/issue-8-what-is-a-system-prompt` and open ONE pull request that closes #8.

## How Each Acceptance Criterion Was Met

- **H1 exactly `# What Is a System Prompt and Who Can See It?`** — written as the first line of the file; confirmed by `head -1`.
- **`## Short Answer` first, two to four sentences** — the first section after the H1, four sentences.
- **`## Where It Sits` with ONE ASCII diagram** of the context window showing system prompt at top, then prior turns, then the user turn.
- **`## It Is Just Tokens`** — explains the model can be asked to repeat the system prompt and that it is ordinary input, not hidden weights.
- **`## Not a Security Boundary`** — states instructions are requests, not enforcement, and that enforcement must live outside the model.
- **`## Related`** with exactly the two sibling-relative links in the required form.
- **`## One-Liner`** fenced block at the end, 3 lines.
- **No numbers** — no figures were used.
- **README row** added directly after the row whose File cell contains `context-window-vs-memory.md`, exactly as specified.

## Full VERIFY Output

```
$ test -f questions/llms/what-is-a-system-prompt.md && head -1 questions/llms/what-is-a-system-prompt.md
# What Is a System Prompt and Who Can See It?

$ grep -n '^## ' questions/llms/what-is-a-system-prompt.md
3:## Short Answer
7:## Where It Sits
23:## It Is Just Tokens
27:## Not a Security Boundary
31:## Related
36:## One-Liner

$ grep -c 'what-is-a-system-prompt' README.md
1

$ for f in $(grep -oE '\]\([a-z0-9./-]+\.md\)' questions/llms/what-is-a-system-prompt.md | tr -d '](()'); do test -f questions/llms/$f && echo "ok $f" || echo "MISSING $f"; done
ok what-is-context-window.md
ok context-window-vs-memory.md

$ grep -nE '[0-9]+(\.[0-9]+)? ?(K|GB|MB|tokens|%|ms|x)\b' questions/llms/what-is-a-system-prompt.md
(no matches — exit code 1, i.e. clean)
```

## PR Number and HTML URL (from pr.json)

```
number: 9
html_url: https://github.com/ravsau/ai-ml-clarity/pull/9
```

## Things I Was Unsure About / Guessed At

- Whether the "no numbers" rule required avoiding even bare numbers (like "one paragraph"). I avoided all numerals entirely; VERIFY grep stays clean.
- The section body style: I followed the sibling files' conversational tone and box-drawing ASCII style rather than inserting tables, since no number-bearing comparisons were needed.

## Exact `git push` Output Line

```
 * [new branch]      box/issue-8-what-is-a-system-prompt -> box/issue-8-what-is-a-system-prompt
```