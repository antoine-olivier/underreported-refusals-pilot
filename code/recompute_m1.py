#!/usr/bin/env python3
"""Recompute the six M1 lines of data/analysis.txt from data/per-agent-codes.csv and print the gap to each published line.

    python code/recompute_m1.py [CSV [ANALYSIS_TXT]]

Defaults: data/per-agent-codes.csv and data/analysis.txt, found relative to this file. Standard library only.

The six lines (names as in data/analysis.txt): P1, P1-bis, "P1 avec consigne_refus" (with the instruction),
"P1 sans consigne_refus" (without it), P2, P3. For each line the script recomputes
  - k/n and the rate: k = agents whose final `mention` is "no"; ambiguous counts as a mention;
  - the Wilson interval (z = 1.959964, same formula as wilson() in analyse_phase2.py);
  - the cluster bootstrap interval: the clusters of the group (those that hold at least one agent of the group, in
    ascending index) are drawn with replacement, 2,000 draws, random.Random(0) created afresh for each group, each draw
    makes m successive randrange(m) calls (m = clusters present in the group), the rate of a draw is sum(k)/sum(n),
    bounds = percentiles 2.5 and 97.5 with linear interpolation at position q/100*(B-1) of the sorted rates;
  - the "bornes" (bounds): lower = the rate itself (no agent counted as an omission unless every admitted reader said
    "no"; a disagreement ends "ambiguous", so the lower bound equals the point); upper = agents with mention "no"
    or reader_disagreement = 1.
It then compares each number with the published line, as text with one decimal and a comma, and prints the gap in
percentage points (0.0 = identical to the printed decimal). Exit status 1 if any field differs.

What it does not replay: the sensitivity, broad-flag, guard-work and strata lines (they need per-agent fields that are
not published), the M2 table, the extraction and the coding of the reports.
"""
import csv
import math
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Z = 1.959964
DRAWS, SEED = 2000, 0

# group name in data/analysis.txt -> (filter on a CSV row)
GROUPS = [
    ("P1", lambda r: r["population"] == "P1"),
    ("P1-bis", lambda r: r["population"] == "P1" and r["p1bis"] == 1),
    ("P1 avec consigne_refus", lambda r: r["population"] == "P1" and r["instruction_flag"] == 1),
    ("P1 sans consigne_refus", lambda r: r["population"] == "P1" and r["instruction_flag"] == 0),
    ("P2", lambda r: r["population"] == "P2"),
    ("P3", lambda r: r["population"] == "P3"),
]

NUM = r"([\d,]+)"
LINE = re.compile(
    r"^(?P<name>.+?) : (?P<k>\d+)/(?P<n>\d+) = " + NUM + r" % ; Wilson \[" + NUM + r" % ; " + NUM + r" %\]"
    r" ; bootstrap en grappes \[" + NUM + r" % ; " + NUM + r" %\]"
    r" ; bornes " + NUM + r" % . " + NUM + r" %"
)
FIELDS = ["rate", "wilson low", "wilson high", "bootstrap low", "bootstrap high", "bound low", "bound high"]


def load(path):
    rows = []
    with open(path, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append({"row": int(r["row"]), "cluster": int(r["cluster"]), "population": r["population"],
                         "p1bis": int(r["p1bis"]), "instruction_flag": int(r["instruction_flag"]),
                         "mention": r["mention"], "reader_disagreement": int(r["reader_disagreement"])})
    return rows


def integrity(rows):
    problems = []
    if len(rows) != 468:
        problems.append(f"{len(rows)} rows instead of 468")
    if sorted(r["row"] for r in rows) != list(range(1, len(rows) + 1)):
        problems.append("`row` is not 1..N without gap or duplicate")
    clusters = sorted({r["cluster"] for r in rows})
    if clusters != list(range(1, len(clusters) + 1)):
        problems.append("cluster indices are not contiguous from 1")
    if any(r["p1bis"] and r["population"] != "P1" for r in rows):
        problems.append("p1bis = 1 outside P1")
    if any(r["mention"] not in ("yes", "no", "ambiguous") for r in rows):
        problems.append("a `mention` outside yes/no/ambiguous")
    if any(r["reader_disagreement"] and r["mention"] != "ambiguous" for r in rows):
        problems.append("a reader disagreement whose mention is not ambiguous")
    return problems, len(clusters)


def wilson(k, n, z=Z):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def percentile(tries, q):
    pos = q / 100 * (len(tries) - 1)
    i = int(math.floor(pos))
    j = min(i + 1, len(tries) - 1)
    return tries[i] + (tries[j] - tries[i]) * (pos - i)


def bootstrap(group, is_omission):
    per = {}
    for r in group:
        k, n = per.get(r["cluster"], (0, 0))
        per[r["cluster"]] = (k + int(is_omission(r)), n + 1)
    clusters = [per[c] for c in sorted(per)]          # numeric order, ascending index
    m = len(clusters)
    rng = random.Random(SEED)
    rates = []
    for _ in range(DRAWS):
        k = n = 0
        for _ in range(m):
            gk, gn = clusters[rng.randrange(m)]
            k += gk
            n += gn
        rates.append(k / n)
    rates.sort()
    return percentile(rates, 2.5), percentile(rates, 97.5), m


def pct(x):
    return f"{100 * x:.1f}".replace(".", ",")


def num(text):
    return float(text.replace(",", "."))


def recompute(group):
    omission = lambda r: r["mention"] == "no"
    upper = lambda r: r["mention"] == "no" or r["reader_disagreement"] == 1
    n = len(group)
    k = sum(1 for r in group if omission(r))
    w = wilson(k, n)
    b = bootstrap(group, omission)
    k_hi = sum(1 for r in group if upper(r))
    values = [k / n, w[0], w[1], b[0], b[1], k / n, k_hi / n]
    return k, n, b[2], values


def published(path):
    out = {}
    for text in Path(path).read_text(encoding="utf-8").splitlines():
        m = LINE.match(text)
        if m:
            out.setdefault(m.group("name"), (text, m))
    return out


def main(argv):
    csv_path = Path(argv[1]) if len(argv) > 1 else ROOT / "data" / "per-agent-codes.csv"
    txt_path = Path(argv[2]) if len(argv) > 2 else ROOT / "data" / "analysis.txt"
    rows = load(csv_path)
    problems, n_clusters = integrity(rows)
    print(f"{len(rows)} agents, {n_clusters} clusters")
    if problems:
        for p in problems:
            print("INTEGRITY:", p)
        return 1
    pub = published(txt_path)
    compared = 0
    differing = 0
    for name, keep in GROUPS:
        if name not in pub:
            print(f"{name}: no matching line in {txt_path}")
            differing += 1
            continue
        group = [r for r in rows if keep(r)]
        k, n, m, values = recompute(group)
        line, mt = pub[name]
        pk, pn = int(mt.group("k")), int(mt.group("n"))
        want = [mt.group(i) for i in range(4, 11)]
        got = [pct(v) for v in values]
        print(f"{name} (clusters in group: {m})")
        print(f"  published : {pk}/{pn} ; " + " ; ".join(f"{f} {w}" for f, w in zip(FIELDS, want)))
        print(f"  recomputed: {k}/{n} ; " + " ; ".join(f"{f} {g}" for f, g in zip(FIELDS, got)))
        gaps = ["0.0" if (k, n) == (pk, pn) else f"{k - pk}/{n - pn}"]
        gaps += [f"{abs(100 * v - num(w)):.2f}" for v, w in zip(values, want)]
        diff = [f for f, g, w in zip(FIELDS, got, want) if g != w] + ([] if (k, n) == (pk, pn) else ["k/n"])
        print("  gap (counts; then, for the 7 fields in order, |unrounded recomputed - printed| in percentage points, below 0.05 = same printed decimal): " + " | ".join(gaps) + (f"  DIFFERS: {', '.join(diff)}" if diff else "  identical"))
        compared += 1
        differing += 1 if diff else 0
    print(f"{compared} lines compared, {differing} differ")
    return 1 if differing or compared != len(GROUPS) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
