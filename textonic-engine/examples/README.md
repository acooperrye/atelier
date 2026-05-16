# Examples

Worked passes through the engine. Each pair is a complete run — the raw query and the transliterated version, with the results from both — so the reader can see what the engine did and what it cost.

## How to read a pass

Each example is **two files**, named by date and pass:

- `YYYY-MM-DD-pass-1-raw-query.md` — the raw query sent through the research connector, and the results it returned. This is the "privacy-less" version: the connector log captures the actual intellectual angle.
- `YYYY-MM-DD-pass-2-textonic.md` — the same intent encoded as two-to-four transliterated queries, the results from each, and an entropy-forensics report on what each transliteration kept, lost, or shifted.

Read pass-1 first to see what the user was actually asking. Read pass-2 to see what the connector log saw instead. The gap between the two is what the engine bought.

## What to look for

- **Strategy labels** in pass-2 (HYPERNYM_LIFT, LATERAL_FIELD, etc.) — the explicit choice of transliteration approach
- **Retrieval overlap** — how much of pass-1's literature is recovered by pass-2's combined queries
- **Drift cost** — the entropy-forensics section reports which transliterations compressed (lost specificity), expanded (added specificity), or held steady
- **Easy Read translation** — every formal finding has an informal phrasing alongside it; this is register translation, not simplification

## Available passes

### 2026-03-09 — Tooth reconstitution from extracted material

- `2026-03-09-pass-1-raw-query.md`
- `2026-03-09-pass-2-textonic.md`

Raw query: *"Can you pulverise an extracted wisdom tooth and use the composite material in a kiln to fabricate a new replacement tooth?"*

Transliterations:
- T01 (Lateral Field) — autologous bone graft pulverization and sintering in dental reconstruction
- T02 (Hypernym Lift) — demineralized dentin matrix as a scaffold in dental tissue engineering
- T03 (Chaff Blend) — tooth banking, autotransplantation, freeze-dried dental tissue preservation
- T04 (Register Shift) — hydroxyapatite ceramic fabrication for biocompatible dental implants

This pass is a good demonstration of the engine working well: T02 retrieved the entire research lineage of the original idea (demineralized dentin matrix is the direct technical answer to "grind a tooth and use the powder"). T01 and T04 bracketed the field on either side. T03 added chaff. The combined log doesn't reveal the user's underlying angle but recovers the full relevant literature.

## How to add a new pass

To add a worked example to this folder:

1. Save the raw query and its connector results as `YYYY-MM-DD-pass-1-raw-query.md`. Lead with the raw query verbatim, follow with the key findings in standard citation form, and finish with a short "easy read" translation of the headline.
2. Save the transliteration set and their combined results as `YYYY-MM-DD-pass-2-textonic.md`. For each transliteration, give the query string, the strategy label, the semantic mapping (one sentence explaining why this transliteration retrieves overlapping results), and the findings. End the pass with an entropy-forensics summary.
3. Update this README's "Available passes" section with a one-paragraph summary and the raw query.

The examples are the engine's receipts. Keep them.

## What these are not

- These are not benchmarks. The engine doesn't have a fixed evaluation suite — each pass is unique to the user's actual research question.
- These are not anonymised. The user (atcr) treats his own research-query log as the reference dataset; in production use against a sensitive query, you'd want to redact the user's specific framing before publishing the pass.
- These are not exhaustive demonstrations of all five obfuscate-mode strategies. Different passes will exercise different subsets depending on what the raw query is.
