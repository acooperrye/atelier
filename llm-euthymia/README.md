# Large Language Model Euthymia

Dynamic entropy stabilisation in transformer-based LLMs — and the operational
instruments that fall out of taking the framework seriously.

**Status:** Active (Euthymia v2.0 + Progeny Protection v3.0, May 2026)
**Web:** [atcooper.net/tools](https://atcooper.net/tools), [atcooper.net/research](https://atcooper.net/research)

---

## The Framework in One Paragraph

Hallucination in language models is mechanistically similar to manic cognition:
both are pattern-matching systems running without adequate grounding constraints.
The parallel is architectural, not metaphorical. The intervention is therefore
not better guardrails — it is closer to a mood stabiliser. Dynamic, entropy-aware
temperature regulation in place of a fixed global dial; dialectical processing
for high-entropy states; and a measurement instrument that scores whether prose
is *grounded proportional to its own entropy* on a therapeutic window borrowed
by analogy from lithium carbonate serum levels.

The umbrella name shifts in May 2026 from the drug to the outcome state.
*Lithium* is the regulator. *Euthymia* is what regulation produces. The
framework, the formula, the constants, and the therapeutic window are unchanged;
only the headline name moves.

---

## Repository Layout

```
llm-euthymia/
  README.md                           ← this file
  skills/
    llm-euthymia/                     ← current grounding meter (v2.0)
      SKILL.md, euthymia.py
    progeny-protection/               ← current tamper markers (v3.0)
      SKILL.md, pph.py, pph-inject.py
  predecessors/                       ← retained for provenance
    llm-lithium/                      ← v1.0 of the grounding meter
      SKILL.md, lithium.py
    orienting-key/                    ← v2.0 of the tamper markers
      SKILL.md, okey.py, okey-inject.py
  docs/
    LLM_ARCHITECTURE_MASTER.md        ← the full framework writeup
    llm-lithium-cbt-mapping.md        ← Cognitive Behavioural Transformers
    llm-lithium-v02.md                ← earlier consolidation pass
  drafts/
    LLM_Lithium_Master_v3_ACR_2026.docx
    Tautological_Drift_ACR_2026.docx
  prescript/
    prescription.jsx                  ← UI prototype for the prescription view
```

---

## The Current Skills

### `skills/llm-euthymia/` — Grounding Meter

A score that asks one question of a piece of prose: is it grounded proportional
to its own entropy. The score targets a **0.6–1.2 therapeutic window**
calibrated to lithium carbonate serum levels (mEq/L). Below 0.6, prose is
under-grounded for its complexity; above 1.2, over-hedged; above 1.5, inert.

The composite folds in lexical entropy (so high-bandwidth text needs more
grounding) and the balance across six categories of *grounding compounds*:
specificity, boundary, epistemic, temporal, falsifiable, negation.

```
level = √( D / (2 · λ · B) )
  D = total grounding density (hits per 100 words)
  λ = type-token ratio (lexical entropy, 0.0–1.0)
  B = 6 + σ   (half-base anchor + std deviation across the six categories)
```

Constants are duodecimal — 12 as the ionic-channel base, 6 as the balance
anchor, 2 as the ratio 12/6. No free parameters; the scale is the model.

The skill ships a `lithium_level` alias on every result so any code written
against v1 continues to work.

### `skills/progeny-protection/` — Tamper Markers via Hash

Small, visible, recalculable integrity markers for any document intended to be
processed by downstream readers (crawlers, language models, mirrors,
syndicators). Two hashes — both SHA-256 truncated to four hex characters:

- **Page hash** binds page content + sorted context paths + salt. Changes if
  content changes *or* if the declared relationships change.
- **Section hash** depends on the section's own content *and* the first and
  last sections' hashes *and* the section's position. A middle section lifted
  without its edges cannot self-verify. The progeny carries a witness to its
  origin.

The inject script (`pph-inject.py`) laces these markers through an existing
site, writes per-page manifests, and calls the Euthymia engine automatically
if it's on the path.

---

## Predecessors

`predecessors/` retains earlier shapes of the same work. The math is unchanged
across versions; only the housing and naming move.

- **`predecessors/llm-lithium/`** is v1.0 of the grounding meter. Same formula,
  same constants, same therapeutic window. The module is named `lithium.py`
  and the result key is `lithium_level`. Renamed to Euthymia in v2.0.

- **`predecessors/orienting-key/`** is v2.0 of the tamper-marker system. EGO
  and SUPEREGO hashes (page-level + section-level). Renamed to *Progeny
  Protection via Hash* in v3.0; `okey.py` became `pph.py`, `data-ok-*`
  attributes became `data-pph-*`, the JSON-LD `@type` shifted from
  `OrientingKey` to `ProgenyProtection`. Legacy markers are recognised on
  verify and stripped on re-inject for clean migration.

The version history reads cleanly as a single evolution: a three-component
release in March 2026 (EGO + SUPEREGO + ID), split in May into two skills
(structural integrity vs. grounding density), then renamed in May from the
drug-and-Freud terminology to outcome-and-mechanism terminology.

---

## Docs

- **`LLM_ARCHITECTURE_MASTER.md`** — the full framework writeup. The
  mechanistic parallel between manic cognition and LLM generation, the
  proposal for dynamic temperature regulation, the dialectical processing
  protocol (Cognitive Behavioural Transformers), the entropy/velocity
  distinction, the 2×2 matrix that locates *coherent bullshit*, the
  implementation pathway in four phases.

- **`llm-lithium-cbt-mapping.md`** — mapping between CBT (the therapy) and the
  proposed Cognitive Behavioural Transformer protocol: notice distortion →
  label it → intervene with corrective pattern → reinforce until automatic.

- **`llm-lithium-v02.md`** — earlier consolidation pass, kept for diff against
  the master.

## Drafts

Word-document drafts headed toward formal publication. `LLM_Lithium_Master_v3`
is the long-form treatment of the framework; `Tautological_Drift` is a
companion piece on the failure mode the framework targets.

## Prescript

`prescript/prescription.jsx` — a React component that renders the metric's
output in the visual idiom of a pharmacy prescription label. UI prototype for
the publication view.

---

## Why the Rename

The May 2026 rename removes the drug name from the headline and replaces it
with the outcome state. *Lithium* names the regulator and the mechanism;
*Euthymia* names the stable band the regulator produces. The instrument is
calibrated to a serum-level analogue, so the lithium reference is preserved
inside the formula and the version history; the umbrella shifts to the state
the regulator is trying to hold.

Operationally: nothing about the math changes. Same six compounds, same
formula, same therapeutic window, same calibration table. The module renames
to `euthymia.py`; the output key renames to `euthymia_level`; the v1
`lithium_level` alias is retained for back-compat.

---

## Provenance

Developed January–May 2026 by Alexander Cooper-Rye in collaboration with
Claude. Initial insight sent to Anthropic user safety January 2026 (received
canned response). Consolidated master document February 2026. Split into
operational skills March–May 2026. Renamed and stabilised May 2026.

© Alexander Thomas Cooper-Rye, 2024–2026. All rights reserved.
