#!/usr/bin/env python3
"""Check that every internal markdown link in the given files resolves.

Finds links of the form [text](target) and ![alt](target). Images use the
same rule as plain links. Links inside fenced code blocks are treated like
any other link (no special-casing). Targets starting with http://, https://,
or mailto: are ignored. Any #anchor suffix is stripped before checking.

A relative target is resolved against the directory of the file that
contains the link, so repo-root-relative links from README.md and
sibling-relative links inside question files both work.

Each broken link is reported on stdout as:

    <source path>:<line number>: <target>

Exits 1 if any link is broken, 0 otherwise. On success prints
"OK: <n> links checked".
"""

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]*)\)")
IGNORED_PREFIXES = ("http://", "https://", "mailto:")


def check_paths(paths):
    """Yield every broken link as '<source>:<line>: <target>'."""
    for path in paths:
        for lineno, line in enumerate(Path(path).read_text().splitlines(), start=1):
            for target in LINK_RE.findall(line):
                target = target.split("#", 1)[0]
                if not target or target.startswith(IGNORED_PREFIXES):
                    continue
                if not (Path(path).parent / target).is_file():
                    yield f"{path}:{lineno}: {target}"


def count_links(paths):
    """Count internal (non-external, non-empty) links across the files."""
    total = 0
    for path in paths:
        for line in Path(path).read_text().splitlines():
            for target in LINK_RE.findall(line):
                target = target.split("#", 1)[0]
                if not target or target.startswith(IGNORED_PREFIXES):
                    continue
                total += 1
    return total


def main(argv):
    if argv:
        paths = argv
    else:
        paths = ["README.md"] + sorted(Path("questions").glob("**/*.md"))

    broken = list(check_paths(paths))
    if broken:
        for message in broken:
            print(message)
        return 1

    print(f"OK: {count_links(paths)} links checked")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))