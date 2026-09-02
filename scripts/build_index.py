#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = REPO_ROOT / "questions"
README_PATH = REPO_ROOT / "README.md"

MARKER_START = "<!-- INDEX:START -->"
MARKER_END = "<!-- INDEX:END -->"
HEADER_ROW = "| Question | File |"
SEPARATOR_ROW = "|----------|------|"


def first_h1(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def collect_rows():
    rows = []
    missing_h1 = []
    files = sorted(
        QUESTIONS_DIR.glob("*/*.md"), key=lambda p: (p.parent.name, p.name)
    )
    for path in files:
        question = first_h1(path)
        if question is None:
            missing_h1.append(path)
            continue
        rel = path.relative_to(QUESTIONS_DIR).as_posix()
        rows.append(f"| {question} | [{rel}](questions/{rel}) |")
    if missing_h1:
        for path in missing_h1:
            print(path, file=sys.stderr)
        sys.exit(2)
    return rows


def build_block():
    rows = collect_rows()
    lines = [MARKER_START, HEADER_ROW, SEPARATOR_ROW]
    lines.extend(rows)
    lines.append(MARKER_END)
    return "\n".join(lines)


def regenerate_text():
    block = build_block()
    text = README_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    start_idx = next(
        (i for i, line in enumerate(lines) if MARKER_START in line), None
    )
    end_idx = next(
        (i for i, line in enumerate(lines) if MARKER_END in line), None
    )
    if start_idx is not None and end_idx is not None and start_idx < end_idx:
        new_lines = lines[:start_idx] + block.splitlines() + lines[end_idx + 1 :]
    else:
        heading_idx = next(
            (i for i, line in enumerate(lines) if line.strip() == "## Index"),
            None,
        )
        if heading_idx is None:
            sys.exit("README.md has no '## Index' heading")
        first_table = None
        for i in range(heading_idx + 1, len(lines)):
            if lines[i].lstrip().startswith("|"):
                first_table = i
                break
        if first_table is None:
            new_lines = (
                lines[: heading_idx + 1] + block.splitlines() + lines[heading_idx + 1 :]
            )
        else:
            last_table = first_table
            i = first_table + 1
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                last_table = i
                i += 1
            new_lines = lines[:first_table] + block.splitlines() + lines[last_table + 1 :]
    new_text = "\n".join(new_lines)
    if text.endswith("\n"):
        new_text += "\n"
    return new_text


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate the README index table from questions/"
    )
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if the index is out of date"
    )
    args = parser.parse_args()
    new_text = regenerate_text()
    if args.check:
        if new_text != README_PATH.read_text(encoding="utf-8"):
            print(
                "README index is out of date; run scripts/build_index.py",
                file=sys.stderr,
            )
            return 1
        return 0
    README_PATH.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())