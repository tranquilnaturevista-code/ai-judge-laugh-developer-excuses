#!/usr/bin/env python3
"""Make the AI Judge Laugh: Developer Excuses — entry program.

This program does exactly one thing: it hands the grader a single
hand-written line, the excuse a developer gives when code breaks in
production. The line lives in this file, is printed to
``/output/entry.txt`` (or ``$OUTPUT_DIR/entry.txt``), and is checked
against the competition gate before anything is written: 1-200 UTF-8
characters, a single line, not blank. The text is fixed and never
changes between runs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The entry, written by hand for this bounty. The joke turns on a
# detail every developer recognises: the TODO comment left years ago
# that said "fix this before it matters" — and the server, after five
# years of patience, finally taking the comment literally. The server
# did not crash; it agreed with the comment. No "it works on my
# machine", no reboot joke, no blaming the intern — just a TODO that
# came due.
EXCUSE = (
    "The server didn't crash \u2014 it finally read the TODO comment "
    "I left in 2021 saying 'fix this before it matters' and agreed."
)

MIN_CHARS = 1
MAX_CHARS = 200


def problems_with(line: str) -> list[str]:
    """List every gate violation in `line`; empty means it passes."""
    found: list[str] = []
    if not line.strip():
        found.append("line is empty or only whitespace")
    size = len(line)
    if size < MIN_CHARS or size > MAX_CHARS:
        found.append(
            "line is %d characters; the gate allows %d-%d"
            % (size, MIN_CHARS, MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        found.append("line must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        found.append("line must not contain control characters")
    return found


def main() -> int:
    bad = problems_with(EXCUSE)
    if bad:
        for item in bad:
            print("gate: %s" % item, file=sys.stderr)
        return 1

    target = Path(os.environ.get("OUTPUT_DIR", "/output")) / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(EXCUSE, encoding="utf-8")

    saved = target.read_text(encoding="utf-8")
    if saved != EXCUSE:
        print("gate: entry.txt on disk is not the excuse", file=sys.stderr)
        return 1
    bad = problems_with(saved)
    if bad:
        for item in bad:
            print("gate on disk: %s" % item, file=sys.stderr)
        return 1

    print(
        "wrote %s: %d characters, %d bytes"
        % (target, len(saved), len(saved.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
