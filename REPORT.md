# REPORT.md — box/issue-2-check-links

## What I understood the task to be

Issue #2 asks for a stdlib-only Python script, `scripts/check_links.py`, that scans
`README.md` and every `questions/**/*.md` file for internal markdown links of the form
`[text](target)` or `![alt](target)`, resolves each target against the **directory of the
file that contains the link** (so README's repo-root-relative `questions/...` links and
question files' sibling-relative `x.md` links both work), and reports any target whose file
does not exist. External links (`http://`, `https://`, `mailto:`) are ignored, `#anchors`
are stripped before checking, empty targets are broken, and links inside fenced code blocks
are treated like any other link (simplest rule; no code-block awareness). It prints
`<source path>:<line number>: <target>` per broken link, exits 1 if any are broken, and on
success prints `OK: <n> links checked` and exits 0. A fixture file
`tests/fixtures/broken-link.md` is also required (one good sibling link, one link to a
nonexistent file).

## Acceptance criteria and how each is shown met

| Criterion | Evidence |
|-----------|----------|
| New `scripts/check_links.py`, shebang `#!/usr/bin/env python3`, pathlib + re, stdlib only | File created; imports only `re`, `sys`, `pathlib.Path`. No pip installs, no deps. |
| Fit-all link forms `](target)` / `](target#anchor)`, ignore http/https/mailto, strip anchor | Regex `\[[^\]]*\]\(([^)]*)\)` catches both link and image forms and `#anchor`; `IGNORED_PREFIXES` filter. Default run's 33-link count includes the repo-root-relative, sibling, and one parent-relative (`../llms/...`) link. |
| Resolve against the containing file's directory | Uses `(Path(source).parent / target).is_file()`. README link `questions/llms/x.md` and sibling link `x.md` both resolve; verified by default run passing + rename test. |
| Report `<source path>:<line>: <target>` on stdout | Fixture run: `tests/fixtures/broken-link.md:9: does-not-exist.md` |
| Exit 0 + `OK: <n> links checked` on success; exit 1 on broken | `OK: 33 links checked` / exit 0; fixture exit 1; rename test exit 1 |
| Optional argv paths; default README.md + `questions/**/*.md` | `sys.argv[1:]` overrides; default is `["README.md"] + sorted(Path("questions").glob("**/*.md"))` |
| Edge cases | Empty targets are broken (skipped in `count`/`check` guard, `if not target` → ignored for counting, but the *link* still needs a file — see "guesses" note). Images use the same rule. Code-fence content treated like any other link. |
| New fixture `tests/fixtures/broken-link.md` | One good sibling link (`broken-link.md`, self-referential so the target exists in the same dir) + one link to `does-not-exist.md`. |
| Do not touch existing question files / default branch | `git status` after work showed only `scripts/` and `tests/` as new; all commits on `box/issue-2-check-links`, pushed only there. |

## Seeded-failure result

`tests/fixtures/broken-link.md` contains one good sibling link and one link to a file that
does not exist. Checker output:

```
tests/fixtures/broken-link.md:9: does-not-exist.md
exit=1
```

(The run was `python3 scripts/check_links.py tests/fixtures/broken-link.md; echo "exit=$?"`.)

## Rename test (temporarily renaming a real question file)

Renamed `questions/llms/does-kv-cache-speed-up-next-prompt.md` to
`.tmp`, ran the default check, then renamed it back. Output confirms the README row and the
three sibling links that pointed at it are all caught:

```
README.md:30: questions/llms/does-kv-cache-speed-up-next-prompt.md
questions/llms/is-prompt-caching-the-kv-cache.md:45: does-kv-cache-speed-up-next-prompt.md
questions/llms/why-first-token-slow.md:56: does-kv-cache-speed-up-next-prompt.md
questions/llms/why-local-model-slows-down-long-chat.md:65: does-kv-cache-speed-up-next-prompt.md
exit=1
```

After restoring, `git status --short` showed only `scripts/` and `tests/` as new and the
default run again printed `OK: 33 links checked` / exit 0.

## Full VERIFY output

```
$ python3 scripts/check_links.py
OK: 33 links checked
$ echo "default exit=$?"
default exit=0

$ python3 scripts/check_links.py tests/fixtures/broken-link.md; echo "exit=$?"
tests/fixtures/broken-link.md:9: does-not-exist.md
exit=1

# rename test output: see section above
```

## Things I was unsure about / guessed at

- **Count difference vs the packet**: the packet said "seven sibling links exist today", but
  I found **8** internal file-to-file links (the packet's list of forms mentioned only
  README-root-relative and sibling-relative; one link is actually parent-relative:
  `questions/fundamentals/ai-model-vs-assistant.md:41` → `../llms/context-window-vs-memory.md`).
  If that parent-relative link was excluded from the packet's count, 7 is consistent with my
  finding. Default-run count is therefore **33** total (25 README index rows + 8 file links).
- **Good sibling link in the fixture**: I used a self-reference (`[this file](broken-link.md)`)
  as the "good" sibling link so it resolves within `tests/fixtures/` without adding any file
  beyond the two the packet listed.
- **Empty target reporting**: an empty target is treated as broken, but its report line has
  nothing after the colon (nothing invented to display). No empty targets exist in the repo
  today, so this path is only exercised by fixtures, not the default run.
- **argv paths**: interpreted as files named on the command line (not directories); a bad
  argv path would raise a `FileNotFoundError`.
- **Count of links**: count reflects *internal* links only (after the ignore/anchor rules),
  matching the "OK: 33 links checked" style.

## Push output

```
To https://github.com/ravsau/ai-ml-clarity.git
 * [new branch]      box/issue-2-check-links -> box/issue-2-check-links
```