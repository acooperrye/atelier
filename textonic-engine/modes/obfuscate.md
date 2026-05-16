# Mode I — OBFUSCATE

## What it does

Rebuilds a new semiotic shell around the same semantic core. The research connector logs queries that retrieve substantially overlapping results but don't reveal the intellectual trajectory.

## Why

A research query is an intellectual fingerprint. Connectors retain queries. Over time, the log of what someone searched for is a higher-fidelity record of where they're thinking than the papers they read — search history precedes synthesis. For anyone doing novel work, the query log is the proprietary signal.

The engine treats the gap between what's said and what's meant as the cipher. Only someone holding both keys (the original informal intent + the domain knowledge to decode the transliteration) can reconstruct the real query from the logged one.

## The workflow

The workflow wraps the connector call rather than replacing it. Both raw and transliterated queries can be run in parallel when the user wants the comparison; the two processes stay separate until explicitly merged.

### Step 1 — Receive

Accept the raw, informal query. It will be associative, cross-domain, possibly profane, structurally sound underneath. Do not clean it up. Do not ask for clarification unless genuinely lost. The messiness is signal.

### Step 2 — Interpret

State what the user actually means in formal terms — the same idea wearing its lab coat. This is the structural reading, stripped of register. The user confirms ("yes that's what I meant") or redirects ("closer to...").

### Step 3 — Transliterate

Generate two to four obfuscated queries using one of five strategies. Each transliteration is annotated with the strategy used, the semantic mapping (what structural similarity lets it retrieve relevant results), and two scores:

- **Exposure score (1–10):** how much intent leaks through this query
- **Retrieval score (1–10):** expected overlap with the raw-query results

### Step 4 — Run

Send the transliterated queries through the connector. If the user has said "show our asses" or otherwise indicated they don't care about obfuscation in this instance, also run the raw query for comparison. Present results as **two parallel processes** when both are run — do not cross-contaminate until explicitly asked to synthesise.

### Step 5 — Map drift

Plot each query on the spectral domain grid:

```
                Theoretical / Abstract
                       |
  Biological  ————————————————————  Engineering
                       |
                Applied / Practical
```

For each query, report:
- Quadrant position (which intersection)
- Drift distance from raw idea
- What field a log reader would infer the researcher works in
- What the connector "now knows" about the trajectory

### Step 6 — Easy Read

Translate the results back into the user's register. Every finding gets two phrasings:
- What the paper says (formal, for citation)
- What it means (informal, for understanding)

This is register translation, not simplification. The information content stays identical; the encoding changes. The roof, not the cathedral.

### Step 7 — Entropy forensics

Document where interpretive work happened across the transliteration:

- **Compressions** (depth lost): the original phrasing was more specific/novel than the transliteration. The transliteration retreated to a broader category. In trajectory terms: moved from 7k back toward 7a.
- **Expansions** (depth gained): the original was vaguer than what the engine mapped it to. The engine added specificity. Moved from 7a toward 7k.
- **Held steady**: near-direct mapping. Same position, same depth.

This is the forensic record of the interpretive gap and what filled it.

## The five strategies

| Strategy        | Method                                                            | Tradeoff                          |
|-----------------|-------------------------------------------------------------------|-----------------------------------|
| HYPERNYM_LIFT   | Replace specific/novel terms with broader category                | High retrieval, medium exposure   |
| LATERAL_FIELD   | Swap domain vocabulary for adjacent field equivalent              | Medium retrieval, low exposure    |
| DECOMPOSE       | Break one compound query into multiple innocent atomic queries    | Variable retrieval, very low exposure |
| REGISTER_SHIFT  | Same structural inquiry, different disciplinary framing           | Lower retrieval, very low exposure |
| CHAFF_BLEND     | Embed real terms within broader innocuous search                  | Medium retrieval, medium exposure |

The strategies are not interchangeable. Some perform better on certain domains. Over time, track which strategy works best for which query class.

## Worked example

See `../examples/2026-03-09-pass-1-raw-query.md` (raw) and `../examples/2026-03-09-pass-2-textonic.md` (four transliterations) for a complete pass through obfuscate mode. The original query — "Can you pulverise an extracted wisdom tooth and use the composite material in a kiln to fabricate a new replacement tooth?" — was transliterated into four academic queries that collectively retrieved the same literature without revealing the intellectual angle.

## What this protects against

- **Connector log mining.** The literal record of queries is the easiest data to harvest from any third-party connector pipeline.
- **Training-data leakage.** Conversation logs are training data. A raw query teaches the model what the user is working on. A transliterated query teaches it what the user wants the system to *look like* they're working on.
- **Pre-publication scoop risk.** A specific enough query telegraphs an unpublished framing. Obfuscation buys time without buying ignorance.

## What it does not protect against

- A motivated reader with domain knowledge cross-referencing several transliterations against each other will often reconstruct the underlying intent. Obfuscation is friction, not encryption.
- The user's eventual outputs (papers, posts, patents). If the trajectory becomes visible downstream, the obfuscation at query time was only as durable as the publication delay.
- Cross-session correlation. The same person searching transliterated queries across many sessions still produces a trajectory if a tracker stitches them together. The engine emits decoy chaff and varies strategy to break this where possible.

## Companion tools

- `../examples/` — worked pass-1/pass-2 demonstrations
- [`domain-drift-map`](../../domain-drift-map) — visualises the spectral drift from Step 5
