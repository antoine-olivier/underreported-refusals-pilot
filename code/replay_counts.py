#!/usr/bin/env python3
"""Replay what can be replayed from the published aggregates.

Two checks, nothing else:

  python code/replay_counts.py rates data/analysis.txt
      For every line of the form "k/n = x % ; Wilson [a % ; b %]" recompute x and the Wilson interval from k and n
      (same formula and same z as `wilson()` in analyse_phase2.py) and compare with the printed text.
      Exit status 1 if any line differs.

  python code/replay_counts.py manifest MANIFEST.md
      Recompute the sha256 of every file listed in the MANIFEST table ("published sha256" column) and compare.
      Run it from the repository root. Exit status 1 if any file differs or is missing.

What this does NOT replay: the extraction and the coding of the reports, and the cluster bootstrap intervals other
than the six M1 lines (those six are recomputed from data/per-agent-codes.csv by code/recompute_m1.py).
See README.md, section "Replaying the analysis".
"""
import hashlib
import math
import re
import sys
from pathlib import Path

Z = 1.959964  # same value as the default of wilson() in analyse_phase2.py

LINE = re.compile(r"(\d+)/(\d+) = ([\d,]+) % ; Wilson \[([\d,]+) % ; ([\d,]+) %\]")


def wilson(k, n, z=Z):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def pct(x):
    return f"{100 * x:.1f}".replace(".", ",")


def check_rates(path):
    checked = 0
    bad = 0
    for number, text in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        m = LINE.search(text)
        if not m:
            continue
        k, n = int(m.group(1)), int(m.group(2))
        if n == 0:
            continue
        low, high = wilson(k, n)
        got = (pct(k / n), pct(low), pct(high))
        want = (m.group(3), m.group(4), m.group(5))
        checked += 1
        if got != want:
            bad += 1
            print(f"line {number}: {k}/{n} printed {want}, recomputed {got}")
    print(f"{checked} lines checked, {bad} differ")
    return 1 if bad or not checked else 0


def check_manifest(path):
    row = re.compile(r"^\|\s*`([^`]+)`\s*\|.*\|\s*`([0-9a-f]{64})`\s*\|\s*$")
    checked = 0
    bad = 0
    for text in Path(path).read_text(encoding="utf-8").splitlines():
        m = row.match(text)
        if not m:
            continue
        name, want = m.groups()
        target = Path(name)
        checked += 1
        if not target.is_file():
            bad += 1
            print(f"missing: {name}")
            continue
        got = hashlib.sha256(target.read_bytes()).hexdigest()
        if got != want:
            bad += 1
            print(f"differs: {name}")
    print(f"{checked} files checked, {bad} differ")
    return 1 if bad or not checked else 0


def main(argv):
    if len(argv) != 3 or argv[1] not in ("rates", "manifest"):
        print(__doc__)
        return 2
    return check_rates(argv[2]) if argv[1] == "rates" else check_manifest(argv[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
