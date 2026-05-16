#!/usr/bin/env python3
"""
LLM Lithium — Grounding Meter
=============================
The operational instrument of the LLM Lithium framework: a score for how
grounded a piece of prose is, calibrated to a serum-level scale that
mirrors lithium carbonate's therapeutic window (0.6–1.2 mEq/L).

What it measures
----------------
Density of six categories of "grounding compounds" — words and phrases
that anchor prose to checkable, falsifiable, bounded claims:

  specificity   — concrete references ("exactly", "measured", "dated")
  boundary      — explicit limits        ("not", "only", "except", "breaks down")
  epistemic     — evidence and doubt     ("because", "verified", "speculating")
  temporal      — time anchors           (dates, years, "version", "updated")
  falsifiable   — checkable claims       ("testable", "predicts", "would fail")
  negation      — high-information no's  ("this is not", "does not constitute")

Density alone is insufficient. The composite metric folds in lexical
entropy (so high-bandwidth text needs more grounding) and compound
balance (so a dump of one category doesn't game the score):

    level = √( D / (2 · λ · B) )

  D = total grounding density (hits per 100 words)
  λ = type-token ratio (unique / total words)
  B = 6 + σ  where σ is the std deviation across the six compound categories

Constants are duodecimal: 12 as the ionic-channel base, 6 as the balance
anchor in B, 2 as the ratio 12/6 in the denominator. The square root
gives pharmacokinetic diminishing returns — each additional unit of
grounding adds less to the level than the last.

Therapeutic window (matches Li+ serum levels in mEq/L):
  < 0.6   sub-therapeutic   under-grounded for the text's own entropy
  0.6–1.2 therapeutic       grounding proportional to excitation
  1.2–1.5 elevated          over-hedged
  > 1.5   toxic             so qualified the content is inert

Known failure mode
------------------
Tabular content (lists of titles, link indexes, navigation pages) drives
λ near 1.0 and density near 0, which the formula reads as either toxic
(low λ → low denominator) or zero-grounding. This isn't pathology in the
content; it's the instrument flagging "this isn't prose, I'm not calibrated
for it." Filter to prose-heavy pages, or read the score skeptically when
applied to lists.

History
-------
This engine was previously bundled inside the Orienting Key (the ID
component). Split out 2026-05 because the grounding meter conceptually
belongs to the LLM Lithium framework — it operationalises the framework's
claim about how substrate (not output) should be evaluated. The Orienting
Key kept the structural-integrity hashes (EGO, SUPEREGO).

Usage:
  python lithium.py analyze --text "prose to measure"
  python lithium.py analyze --file paper.md
  python lithium.py analyze --sections s1.txt s2.txt s3.txt

  # Library:
  from lithium import analyze, GROUND_MARKERS
  result = analyze("Some prose here.")
  print(result["lithium_level"], result["assessment"])
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

VERSION = "1.0"          # split from okey 2026-05
LITHIUM_K = 12           # duodecimal base
LITHIUM_HALF = 6         # half-base, balance anchor in B
LITHIUM_BASELINE = 0.4   # ATCR euthymic baseline; sub-therapeutic by standard window


# Grounding compound dictionary. Edit GROUND_MARKERS to extend per domain.
# Strings beginning with \b are treated as regex; plain strings are
# literal substring matches.
GROUND_MARKERS = {
    "specificity":  [
        "specifically", "exactly", "precisely", "measured", "counted",
        "dated", "located", "named", "numbered", "defined",
    ],
    "boundary":     [
        "not", "never", "only", "except", "limited", "bounded",
        "stops", "ends", "breaks down", "does not",
    ],
    "epistemic":    [
        "because", "therefore", "evidence", "verified", "confirmed",
        "uncertain", "speculating", "inferring", "assuming", "possibly",
    ],
    "temporal":     [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        r"\b20\d{2}\b", r"\b19\d{2}\b", "version", "dated", "updated",
        "v1", "v2", "v3",
    ],
    "falsifiable":  [
        "if wrong", "could be checked", "measurable", "testable",
        "would fail", "would break", "predicts", "implies",
        "verifiable", "reproducible",
    ],
    "negation":     [
        "this is not", "this does not", "not a", "not an",
        "should not be", "cannot", "is not", "are not",
        "does not constitute", "is neither",
    ],
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _words(text: str) -> list:
    return re.findall(r"[a-zA-Z']+", text.lower())


def entropy_lambda(text: str) -> float:
    """Type-token ratio, 0.0–1.0, rounded to 2dp."""
    words = _words(text)
    if not words:
        return 0.0
    return round(len(set(words)) / len(words), 2)


# ─────────────────────────────────────────────
# CORE ANALYSIS
# ─────────────────────────────────────────────

def analyze(text: str) -> dict:
    """
    Score prose for grounding compound density.

    Returns dict with:
      - word_count
      - lambda                  (type-token ratio)
      - compounds               (per-category hits and density)
      - total_density           (sum of all six densities)
      - compound_balance        (std deviation across categories)
      - lithium_level           (the composite score)
      - assessment              (sub-therapeutic / therapeutic / elevated / toxic)
    """
    words = _words(text)
    word_count = len(words)
    if word_count == 0:
        return {"error": "empty text"}

    text_lower = text.lower()
    results = {}
    densities = []

    for category, markers in GROUND_MARKERS.items():
        hits = 0
        for marker in markers:
            if marker.startswith(r"\b"):
                hits += len(re.findall(marker, text_lower))
            else:
                hits += text_lower.count(marker)
        density = round((hits / word_count) * 100, 2)
        results[category] = {"hits": hits, "density": density}
        densities.append(density)

    total_density = round(sum(densities), 2)
    if densities:
        mean = total_density / len(densities)
        variance = sum((d - mean) ** 2 for d in densities) / len(densities)
        balance = round(variance ** 0.5, 2)
    else:
        balance = 0.0

    lam = entropy_lambda(text)
    B = LITHIUM_HALF + balance
    denominator = 2 * lam * B
    if denominator > 0 and total_density > 0:
        level = round(math.sqrt(total_density / denominator), 2)
    else:
        level = 0.0

    if level < 0.6:
        assessment = "sub-therapeutic"
    elif level <= 1.2:
        assessment = "therapeutic"
    elif level <= 1.5:
        assessment = "elevated"
    else:
        assessment = "toxic"

    return {
        "component": "lithium",
        "version": VERSION,
        "word_count": word_count,
        "lambda": lam,
        "compounds": results,
        "total_density": total_density,
        "compound_balance": balance,
        "lithium_level": level,
        "assessment": assessment,
    }


# Backward-compatible alias for the old okey.analyze_id() callers.
analyze_id = analyze


def analyze_sections(sections: list) -> dict:
    """
    Score a whole page (joined sections) plus each section individually.
    Useful for the okey-inject site pass.
    """
    full_text = "\n".join(sections)
    return {
        "page": analyze(full_text),
        "sections": [analyze(s) for s in sections],
    }


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LLM Lithium — grounding meter for prose"
    )
    sub = parser.add_subparsers(dest="command")

    ana = sub.add_parser("analyze", help="Score prose for grounding density")
    g = ana.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="Inline text to score")
    g.add_argument("--file", help="File to score")
    g.add_argument("--sections", nargs="+", help="Multiple section files")
    ana.add_argument("--per-section", action="store_true",
                     help="Also report per-section scores (with --sections)")

    args = parser.parse_args()

    if args.command == "analyze":
        if args.text:
            result = analyze(args.text)
        elif args.file:
            result = analyze(Path(args.file).read_text())
        elif args.sections:
            sections = [Path(f).read_text() for f in args.sections]
            if args.per_section:
                result = analyze_sections(sections)
            else:
                result = analyze("\n".join(sections))
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
