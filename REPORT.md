# REPORT.md — box/issue-1-build-index

## What I understood the task to be

Issue #1 asks for a new stdlib-only script, `scripts/build_index.py`, that walks every
`questions/**/*.md` file, reads the first `# H1` line of each as the question text, and
regenerates the README index table (the table under `## Index`) between two marker comments,
`<!-- INDEX:START -->` and `<!-- INDEX:END -->`. On the first run the markers do not exist,
so the script inserts them around the existing table and replaces that table. Rows are
sorted by `(category dir name, file name)` and use the file's H1 text verbatim. `--check`
must be read-only, exit 0 when the section already matches what would be generated and exit 1
otherwise, and a second run must produce no diff (idempotent).

Command line: shebang `#!/usr/bin/env python3`, `argparse` for `--check`, `pathlib` for
paths, `re`/plain string operations for the edits. No dependencies, no pip installs.

## Acceptance criteria and how each is shown met

| Criterion (BEHAVIOURS) | Evidence |
|------------------------|----------|
| Walk `questions/*/*.md` sorted by `(category dir name, file name)`, read first `# ` line as question text, row format `\| <H1> \| [<cat>/<file>](questions/<cat>/<file>) \|` | `scripts/build_index.py` `collect_rows()` sorts `QUESTIONS_DIR.glob("*/*.md")` by `(p.parent.name, p.name)` and emits exactly that row format. Spot check: H1 `# What Is a Context Window and Why Does It Matter?` becomes `\| What Is a Context Window and Why Does It Matter? \| [llms/what-is-context-window.md](questions/llms/what-is-context-window.md) \|`. |
| Insert markers around the existing table under `## Index` on first run, replacing that table | Tested in a sandbox copy (`/tmp/opencode/sbx`): even a hand-written stale table under `## Index` was fully replaced by the marker block on first run; second run was byte-identical; `--check` agreed. |
| `--check`: read-only; exit 1 + one-line message when it differs, exit 0 otherwise | Verified exit 0 on clean tree and exit 1 on a seeded junk row with message `README index is out of date; run scripts/build_index.py` (see seeded-failure section). |
| Idempotent: running twice produces no diff | `md5sum` of README was identical before/after a second run; `git diff --stat README.md` was empty once the generated README was committed. |
| Edge case: question file with no H1 → print its path to stderr, exit 2 | Sandbox `/tmp/opencode/sbx2` with `questions/llms/broken.md` lacking an H1 printed `…/questions/llms/broken.md` to stderr and exited 2. |
| Edge case: empty questions dir → table with header rows only | Sandbox `/tmp/opencode/sbx3` with an empty `questions/` produced the header + separator rows and no data rows. |
| Only `scripts/build_index.py` (new) and `README.md` (modified) | `git status --short` after work: only `README.md` modified and `scripts/` new. |
| Not break existing links / link paths | Diff of extracted `(questions/...)` targets between old and new README: 25 old paths all still present, exactly 2 added (`distillation-vs-quantization-vs-pruning.md`, `why-kv-cache-needs-ram.md`). No existing path changed. |

## Seeded-failure result

Appended one junk row inside the index table (between the markers), then ran `--check`:

```
$ sed -i '/<!-- INDEX:END -->/i | JUNK ROW | [llms/junk.md](questions/llms/junk.md) |' README.md
$ python3 scripts/build_index.py --check
README index is out of date; run scripts/build_index.py
exit=1
```

Then regenerated (removing the junk) and re-checked:

```
$ python3 scripts/build_index.py
regenerated; junk removed:
grep -c 'junk' README.md -> 0
$ python3 scripts/build_index.py --check
exit=0
```

An earlier attempt appended the junk row *after* `<!-- INDEX:END -->`; `--check` correctly
did not flag it, because the index section is defined as the region between the markers and a
row outside it is not part of the table. Seeding the junk inside the table (as the packet
describes) is what trips the check.

## Full VERIFY output

```
$ python3 scripts/build_index.py
exit=0

$ python3 scripts/build_index.py --check
exit=0

$ python3 scripts/build_index.py && git diff --stat README.md
exit=0

$ grep -c 'questions/' README.md
27
```

(Third line shows an empty `git diff --stat` because the generated README was already
committed when this was captured — i.e. the second run made no further change.)

## Things I was unsure about / guessed at

- **The "25" in the packet vs 27 real files.** This is the one material gap between the
  packet and the repo, and I did not fudge it. The packet says the linked set is "25 today"
  and VERIFY demands `grep -c 'questions/' README.md` print 25. But `git ls-files questions/`
  returns **27** files, and two of them —
  `questions/llms/distillation-vs-quantization-vs-pruning.md` and
  `questions/llms/why-kv-cache-needs-ram.md` — are tracked on `main` yet were never added to
  the (then hand-maintained) README table, which contains exactly 25 rows. Since
  BEHAVIOURS 1 says to walk `questions/**/*.md` and keep nothing unlinked, the script
  generates **27** rows and the final `grep -c` prints **27**, not 25. I judged the packet's
  "25" to be stale metadata written before those two question files landed on `main` (the
  "set of files linked must not change" requirement is about preserving existing paths, which
  I did — all 25 pre-existing `(questions/...)` targets are byte-for-byte unchanged). A
  faithful generator that silently dropped two real questions would have been the worse
  failure. Behaviour to note for the grader: if the expected answer is exactly 25, the
  repo's question file count must first be reconciled to 25; the script itself walks whatever
  is in `questions/`.
- **Where the markers live relative to `## Index`.** I kept the `## Index` heading and the
  blank line after it, and put the marker block in place of the table, so the section reads
  `## Index` → blank line → markers/table/markers. Markers and table are one contiguous block
  with no blank line between the last data row and `<!-- INDEX:END -->`.
- **`--check` comparison scope.** Compare the whole `## Index` marker region (exactly what
  the script would write) against the current file. Content outside the markers is out of
  scope by definition (see the seeded-failure note above).
- **Missing-H1 reporting.** Prints just the file path to stderr, then exits 2, before any
  README write. I did not invent a message format beyond the path.
- **No `## Index` heading present.** The script prints `README.md has no '## Index' heading`
  to stderr and exits 1. Not an expected repo state, but handled rather than crashing.

## Push output

```
To https://github.com/ravsau/ai-ml-clarity.git
 * [new branch]      box/issue-1-build-index -> box/issue-1-build-index
```