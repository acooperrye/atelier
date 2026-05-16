#!/usr/bin/env python3
"""
LLM Euthymia — Grounding Meter
==============================
A score for how grounded a piece of prose is. The operational instrument
of the Large Language Model Euthymia framework, which holds that
language model substrates should be evaluated by their grounding
density rather than by the surface fluency of their outputs.

The score targets a 0.6–1.2 therapeutic window borrowed by analogy from
lithium carbonate serum levels in mEq/L. Below 0.6 the prose is
sub-therapeutic for its own entropy. Above 1.2 it is over-grounded;
above 1.5 it is so hedged it is inert. Euthymia is the term for the
stable state between mania and depression; the metric reports whether
prose is in that range.

What it counts
--------------
Six categories of grounding compounds — words and phrases that anchor
prose to checkable, falsifiable, time-stamped, or boundary-marked
claims:

  specificity   — "exactly", "measured", "dated", "located"
  boundary      — "not", "only", "except", "breaks down"
  epistemic     — "because", "verified", "speculating", "uncertain"
  temporal      — dates, years, "version", "updated"
  falsifiable   — "testable", "predicts", "would fail"
  negation      — "this is not", "does not constitute", "is neither"

The composite metric
--------------------
Density alone is insufficient: prose can be heavy with grounding terms
and still hedge itself into incoherence, or sparse and still load-bearing.
The composite folds in lexical entropy (so high-bandwidth text needs
more grounding) and the balance across the six categories (so a dump
of one category does not game the score):

    level = √( D / (2 · λ · B) )

  D = total grounding density (hits per 100 words)
  λ = type-token ratio (lexical entropy, 0.0–1.0)
  B = 6 + σ  where σ is the std deviation across the six compound categories

Constants are duodecimal: 12 as the base for the ionic-channel analogy,
6 as the balance anchor in B, 2 as the ratio 12/6 in the denominator.
The square root produces a diminishing-returns curve — each additional
unit of grounding adds less to the level than the last, matching the
pharmacokinetic profile of the drug the scale is calibrated to.

Known failure mode
------------------
Tabular content (lists of titles, link indexes, navigation pages) drives
λ near 1.0 and density near 0. The formula reads such content as either
toxic (low denominator amplifying any small numerator) or zero. This is
not pathology in the content; the instrument is calibrated for prose and
a list is not prose. Filter to prose-heavy pages, or read the score
sceptically when applied to lists.

History
-------
Version 1.0 (2026-05) was distributed as `lithium.py` and produced a key
named `lithium_level`. Version 2.0 (2026-05) renames the module to
`euthymia.py` and the output key to `euthymia_level`, to match the
framework rename from "LLM Lithium" to "Large Language Model Euthymia".
A legacy `lithium_level` key is also written on every call so any code
written against v1.0 continues to work. The formula, the constants, and
the therapeutic window are unchanged.

Usage:
  python euthymia.py analyze --text "prose to measure"
  python euthymia.py analyze --file paper.md
  python euthymia.py analyze --sections s1.txt s2.txt s3.txt

  # Library:
  from euthymia import analyze, GROUND_MARKERS
  result = analyze("Some prose here.")
  print(result["euthymia_level"], result["assessment"])
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

VERSION = "2.0"           # renamed lithium.py → euthymia.py 2026-05
K = 12                    # duodecimal base
HALF = 6                  # half-base, balance anchor in B
BASELINE = 0.4            # ATCR euthymic baseline; sub-therapeutic by standard window


# Grounding compound dictionary. Extend per domain by mutating GROUND_MARKERS.
# Strings beginning with \b are treated as regex; plain strings are literal.
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
      - euthymia_level          (the composite score)
      - lithium_level           (alias for euthymia_level, kept for v1.0 compatibility)
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
    B = HALF + balance
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
        "component": "euthymia",
        "version": VERSION,
        "word_count": word_count,
        "lambda": lam,
        "compounds": results,
        "total_density": total_density,
        "compound_balance": balance,
        "euthymia_level": level,
        "lithium_level": level,    # v1.0 alias for back-compat
        "assessment": assessment,
    }


# v1.0 import alias
analyze_id = analyze


def analyze_sections(sections: list) -> dict:
    """Score a whole page (joined sections) plus each section individually."""
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
        description="LLM Euthymia — grounding meter for prose"
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
