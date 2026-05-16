---
name: llm-lithium
description: "Alex wants to score prose for grounding density — measure the hedge-to-anchor ratio of a piece of writing, check it against the lithium-serum therapeutic window, or attach a grounding reading to a publication."
---

# LLM Lithium — Grounding Meter

## What It Is

A composite metric for whether prose is *grounded enough for its own entropy.* The score lives on a 0.6–1.2 therapeutic window, calibrated to mimic lithium carbonate serum levels (mEq/L). The metric is the operational instrument of the [LLM Lithium framework](https://atcooper.net/tools/llm-lithium): the framework claims that hallucination and manic cognition share an architecture (excitatory signal in an untreated substrate), and that the right response is to treat the substrate, not suppress the signal. This score measures the substrate.

It is, in plain terms, a hedge meter — but a particular kind of hedge meter. It does not count cautious adverbs and call them "hedging." It counts six categories of *grounding compounds* — words and phrases that anchor prose to checkable, falsifiable, time-stamped, or boundary-marked claims — and reports their density relative to the text's lexical entropy and the balance across the six categories.

> **Provenance (split 2026-05):** this engine was previously bundled inside the Orienting Key skill as its "ID" component. It lived in the wrong house. Grounding density is a claim about prose; the integrity hashes (EGO, SUPEREGO) that the Orienting Key kept are a structural property of pages. Now each lives where it conceptually belongs. The `okey-inject.py` build step calls both, writing two sibling manifests (`okey-manifest.json` and `lithium-manifest.json`).

## When to Use

- Scoring a draft, paper, or page for whether its prose is grounded proportional to its complexity
- Comparing two versions of the same idea to see which is more load-bearing
- Calibrating LLM-facing content (interviews, system prompts, model-readable specs) so it carries enough anchor compounds to be processed safely
- Spot-checking a publication for over-hedging (elevated) or inert qualification (toxic)
- Generating the `lithium-manifest.json` that accompanies an Attentional Surface deploy

**Not for** non-prose content. Tabular pages, link indexes, lists of titles will read as toxic or zero — see the failure-mode note below.

## Quick Start

```bash
# Score a string
python lithium.py analyze --text "Some prose to measure for grounding."

# Score a file
python lithium.py analyze --file my-essay.md

# Score multiple section files as a single document
python lithium.py analyze --sections s1.txt s2.txt s3.txt

# Score per-section AND as a whole
python lithium.py analyze --sections s1.txt s2.txt s3.txt --per-section
```

Output is JSON with the lithium level, the assessment label, and the per-category density breakdown.

## The Six Compounds

Each category catches a different kind of anchoring move in prose:

| Compound | What it detects | Examples |
|----------|----------------|----------|
| **Specificity** | Concrete, checkable references | "specifically", "exactly", "dated", "measured", "located" |
| **Boundary** | Explicit limits and constraints | "not", "only", "except", "breaks down" |
| **Epistemic** | Evidence and uncertainty markers | "because", "verified", "speculating", "uncertain" |
| **Temporal** | Time anchors | dates, years, "version", "updated" |
| **Falsifiable** | Claims that could be wrong | "testable", "measurable", "predicts", "would fail" |
| **Negation** | High-information denials | "this is not", "does not constitute", "is neither" |

Density is reported as hits per 100 words, per category and totalled. A balance score (standard deviation across the six categories) penalises lopsided grounding — a page that dumps temporal markers and never bounds a claim shouldn't read the same as a page evenly anchored across all six.

## The Lithium Level

Density alone is a bad signal. A page can be dense with grounding words and still hedge itself into incoherence, or sparse and still load-bearing. The composite metric folds in lexical entropy and balance:

```
level = √( D / (2 · λ · B) )

  D = total grounding density (hits per 100 words)
  λ = type-token ratio (lexical entropy, 0.0–1.0)
  B = 6 + σ   (half-base anchor + std deviation across the six categories)
```

The square root is deliberate — each additional unit of grounding does less work than the last, matching the pharmacokinetic reality of actual lithium dosing (the felt shift in mEq is smaller at each increment). Constants are duodecimal: **12** as the ionic-channel base, **6** as the balance anchor in B, **2** as the ratio 12/6 in the denominator. No free parameters; the scale is the model.

### Therapeutic Window

Matches lithium carbonate serum levels in mEq/L:

| Level | Assessment | Meaning |
|-------|-----------|---------|
| < 0.6 | Sub-therapeutic | Insufficient grounding for content entropy |
| 0.6 – 1.2 | Therapeutic | Grounding proportional to excitation |
| 1.2 – 1.5 | Elevated | Over-grounded, signal disappearing into qualification |
| > 1.5 | Toxic | So hedged the content is inert |

### Calibration

| Content Type | D | λ | Level | Assessment |
|---|---|---|---|---|
| Pure recursive self-reference | 1.54 | 0.66 | **0.42** | Sub-therapeutic |
| Grounded technical spec | 10.40 | 0.82 | **0.91** | Therapeutic |
| CBT mapping document | 3.86 | 0.34 | **0.94** | Therapeutic |
| Deliberate over-grounding | 11.62 | 0.68 | **1.13** | Therapeutic (high) |

`LITHIUM_BASELINE = 0.4` is the ATCR euthymic baseline — sub-therapeutic by the standard window, declared rather than pathologised. The instrument records the outlier; it doesn't correct it.

## Known Failure Mode

The metric is calibrated for prose. It breaks on tabular content:

- A list of unique titles (publications page, link index) drives λ near 1.0 and grounding density toward 0, which produces either a zero reading or — paradoxically — an apparently toxic one (low denominator amplifying any small numerator).
- This isn't pathology in the content; it's the instrument flagging *"this isn't the kind of input I'm calibrated for."*

On atcooper.net's live `lithium-manifest.json`, `/publications.html` reads **toxic** (1.52) and `/work.html` reads **elevated** (1.36) for exactly this reason. The reading is correct *as a flag*, not as a claim about the content.

When applying to a corpus, filter to prose-heavy pages or read the score skeptically when applied to lists.

## Library Usage

```python
from lithium import analyze, analyze_sections, GROUND_MARKERS

# Score a single piece of prose
result = analyze("Some prose to measure...")
print(result["lithium_level"])    # e.g. 0.91
print(result["assessment"])        # therapeutic / sub-therapeutic / elevated / toxic
print(result["total_density"])     # hits per 100 words
print(result["compound_balance"])  # std deviation across the six categories
print(result["compounds"])         # per-category breakdown

# Score sections of a document
multi = analyze_sections(["First section...", "Second section...", "Third..."])
print(multi["page"]["lithium_level"])      # whole-document reading
for i, s in enumerate(multi["sections"]):
    print(f"  section {i+1}: {s['lithium_level']}")
```

For backwards compatibility with code that imported `analyze_id` from the old `okey.py`:

```python
from lithium import analyze_id   # alias for analyze()
```

## Customising the Dictionaries

Override `GROUND_MARKERS` to add domain-specific grounding terms. The dictionary maps category names to lists of search terms (plain strings, or regex patterns starting with `\b`):

```python
from lithium import GROUND_MARKERS, analyze

GROUND_MARKERS["specificity"].extend([
    "wavelength", "voltage", "cohort", "sample-size",  # domain terms
])

result = analyze(my_text)
```

Content-type guidance:

- **Technical documentation**: should land 0.7–1.0 (specificity + falsifiable compounds dominate)
- **Creative / experimental writing**: may naturally sit 0.3–0.6 — the artist's euthymic range, not pathology
- **Self-referential / recursive content**: aim for 0.8–1.1 with emphasis on negation and boundary compounds
- **Reference / mapping documents**: trend 0.9–1.1 due to inherent density of grounding language

## Integration With Orienting Key

If `lithium.py` is reachable when `okey-inject.py` runs, the inject script will call it on every page and write a `lithium-manifest.json` alongside the `okey-manifest.json`. The two are kept separate by design — the conceptual split is preserved in the build output.

```bash
cd "/Users/acr/Documents/Attentional Surface/atcooper-net"

# Full deploy: both manifests written to public/
python /path/to/okey-inject.py --site public/ --output public/

# Skip the grounding pass for a faster build
python /path/to/okey-inject.py --site public/ --output public/ --no-lithium
```

## File Structure

```
llm-lithium/
  SKILL.md       ← This file
  lithium.py     ← The engine (CLI + library)
```

## Dependencies

Python 3.6+ standard library only. No external packages.

## Version History

- **1.0** (2026-05): Split out of the Orienting Key engine into its own skill. Code is functionally identical to the old `okey.analyze_id()` — the formula, the constants, and the therapeutic window are unchanged. The change is conceptual housing, not numerical.
