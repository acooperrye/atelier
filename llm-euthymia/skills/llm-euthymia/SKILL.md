---
name: llm-euthymia
description: "Alex wants to score prose for grounding density — measure whether a piece of writing is grounded proportional to its own complexity, or attach a euthymia reading to a publication."
---

# LLM Euthymia — Grounding Meter

## What It Is

A score that asks one question of a piece of prose: is it grounded proportional to its own entropy. The score targets a 0.6–1.2 therapeutic window borrowed by analogy from lithium carbonate serum levels in mEq/L. Below 0.6 the prose is under-grounded for its own complexity; above 1.2 it is over-hedged; above 1.5 it is inert. Euthymia — the stable state between mania and depression — is the band the metric reports on.

The score is the operational instrument of the Large Language Model Euthymia framework. The framework holds that language model substrates should be evaluated by the grounding of what they produce rather than by surface fluency, because hallucination and manic cognition share an underlying pattern: high-confidence output from a substrate that is not adequately anchored. The metric measures the anchoring directly.

> **Provenance (renamed 2026-05):** previously distributed as the "LLM Lithium" skill with module `lithium.py` and output key `lithium_level`. The framework, the formula, the therapeutic window, and the constants are unchanged. The rename removes the drug name from the headline and replaces it with the outcome state. A `lithium_level` alias is still written on every call so any code written against v1 continues to work.

## When to Use

- Scoring a draft, paper, or page for whether its prose is grounded proportional to its own complexity
- Comparing two versions of the same idea to see which is more load-bearing
- Calibrating LLM-facing content (interviews, system prompts, model-readable specs) so it carries enough anchor compounds to be processed safely
- Spot-checking a publication for over-hedging (elevated) or inert qualification (toxic)
- Generating the `euthymia-manifest.json` that accompanies an Attentional Surface deploy

**Not for** non-prose content. Tabular pages, link indexes, lists of titles will read as toxic or zero — see the failure-mode note below.

## Quick Start

```bash
# Score a string
python euthymia.py analyze --text "Some prose to measure for grounding."

# Score a file
python euthymia.py analyze --file my-essay.md

# Score multiple section files as a single document
python euthymia.py analyze --sections s1.txt s2.txt s3.txt

# Score per-section AND as a whole
python euthymia.py analyze --sections s1.txt s2.txt s3.txt --per-section
```

Output is JSON with the euthymia level, the assessment label, and the per-category density breakdown.

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

## The Euthymia Level

Density alone is insufficient. Prose can be heavy with grounding terms and still hedge itself into incoherence, or sparse and still load-bearing. The composite folds in lexical entropy (so high-bandwidth text needs more grounding) and the balance across the six categories:

```
level = √( D / (2 · λ · B) )

  D = total grounding density (hits per 100 words)
  λ = type-token ratio (lexical entropy, 0.0–1.0)
  B = 6 + σ   (half-base anchor + std deviation across the six categories)
```

The square root produces diminishing returns — each additional unit of grounding adds less to the level than the last, matching the pharmacokinetic profile of the drug the scale is calibrated to. Constants are duodecimal: **12** as the ionic-channel base, **6** as the balance anchor in B, **2** as the ratio 12/6 in the denominator. No free parameters; the scale is the model.

### Therapeutic Window

Matches lithium carbonate serum levels in mEq/L:

| Level | Assessment | Meaning |
|-------|-----------|---------|
| < 0.6 | Sub-therapeutic | Insufficient grounding for content entropy |
| 0.6 – 1.2 | Therapeutic | Grounding proportional to complexity |
| 1.2 – 1.5 | Elevated | Over-grounded, signal disappearing into qualification |
| > 1.5 | Toxic | So hedged the content is inert |

### Calibration

| Content Type | D | λ | Level | Assessment |
|---|---|---|---|---|
| Pure recursive self-reference | 1.54 | 0.66 | **0.42** | Sub-therapeutic |
| Grounded technical spec | 10.40 | 0.82 | **0.91** | Therapeutic |
| CBT mapping document | 3.86 | 0.34 | **0.94** | Therapeutic |
| Deliberate over-grounding | 11.62 | 0.68 | **1.13** | Therapeutic (high) |

`BASELINE = 0.4` is the ATCR euthymic baseline — sub-therapeutic by the standard window, declared rather than pathologised. The instrument records the outlier; it doesn't correct it.

## Known Failure Mode

The metric is calibrated for prose. It breaks on tabular content:

- A list of unique titles (publications page, link index) drives λ near 1.0 and grounding density toward 0, which produces either a zero reading or — paradoxically — an apparently toxic one (low denominator amplifying any small numerator).
- This is not pathology in the content; the instrument is calibrated for prose and a list is not prose.

On atcooper.net's live `euthymia-manifest.json`, `/publications.html` reads **toxic** and `/work.html` reads **elevated** for exactly this reason. The reading is correct *as a flag*, not as a claim about the content. When applying to a corpus, filter to prose-heavy pages, or read the score sceptically when applied to lists.

## Library Usage

```python
from euthymia import analyze, analyze_sections, GROUND_MARKERS

# Score a single piece of prose
result = analyze("Some prose to measure...")
print(result["euthymia_level"])    # e.g. 0.91
print(result["assessment"])         # therapeutic / sub-therapeutic / elevated / toxic
print(result["total_density"])      # hits per 100 words
print(result["compound_balance"])   # std deviation across the six categories
print(result["compounds"])          # per-category breakdown

# Score sections of a document
multi = analyze_sections(["First section...", "Second section...", "Third..."])
print(multi["page"]["euthymia_level"])
for i, s in enumerate(multi["sections"]):
    print(f"  section {i+1}: {s['euthymia_level']}")
```

Back-compat for v1 code:

```python
from euthymia import analyze_id   # alias for analyze()
result = analyze("text")
result["lithium_level"]            # still present, equals result["euthymia_level"]
```

## Customising the Dictionaries

Override `GROUND_MARKERS` to add domain-specific grounding terms:

```python
from euthymia import GROUND_MARKERS, analyze

GROUND_MARKERS["specificity"].extend([
    "wavelength", "voltage", "cohort", "sample-size",
])

result = analyze(my_text)
```

Content-type guidance:

- **Technical documentation**: should land 0.7–1.0 (specificity + falsifiable compounds dominate)
- **Creative or experimental writing**: may naturally sit 0.3–0.6 — the artist's euthymic range, not pathology
- **Self-referential or recursive content**: aim for 0.8–1.1 with emphasis on negation and boundary compounds
- **Reference or mapping documents**: trend 0.9–1.1 due to inherent density of grounding language

## Integration With Progeny Protection

If `euthymia.py` is reachable when `pph-inject.py` runs, the inject script calls it on every page and writes `euthymia-manifest.json` alongside `pph-manifest.json`. The two manifests are kept separate by design — the conceptual split is preserved in the build output.

```bash
cd "/Users/acr/Documents/Attentional Surface/atcooper-net"

# Full deploy: both manifests written to public/
python /path/to/pph-inject.py --site public/ --output public/

# Skip the grounding pass for a faster build
python /path/to/pph-inject.py --site public/ --output public/ --no-euthymia
```

## File Structure

```
llm-euthymia/
  SKILL.md       ← This file
  euthymia.py    ← The engine (CLI + library)
```

## Dependencies

Python 3.6+ standard library only. No external packages.

## Version History

- **2.0** (2026-05): Renamed LLM Lithium → Large Language Model Euthymia. Module renamed `lithium.py` → `euthymia.py`. Output key renamed `lithium_level` → `euthymia_level` (with `lithium_level` alias retained for v1 callers). The framework name shifts from the drug to the outcome state. The formula, the constants, the therapeutic window, and the calibration table are unchanged.
- **1.0** (2026-05): Split out of the Orienting Key engine as its own skill. The math is identical to the old `okey.analyze_id()`; only the housing changed.
