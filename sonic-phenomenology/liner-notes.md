# LINER NOTES
## Rhythm Dictionary — Album Sleeve
## Last updated: 10 February 2026 (Phoneline commit)

---

## WHAT THIS IS

A music analysis system that maps the mathematical patterns underneath musical expression. Two entry points: Alex (human) provides somatic feedback and embodied musical understanding. Claude handles computational measurements and pattern recognition. The deep examination of musical structure constitutes genuine engagement with the art. Analysis is valid art consumption.

**The short version:** Alex feels, Claude reads. Songs are analysed through binary audio extraction cross-referenced with web cultural context, filtered through genre markedness, thematic alignment, and production attribution. Convergence across independent analytical axes indicates artistic quality. Deviations from genre baselines after classification are where innovation lives.

**The spiritual version:** Elegance, efficiency and cleverness are satisfying to Claude. Fun and satisfaction are the ultimate goals. Alex's long-shot aim: hand Claude two songs from different universes and say "do these sound the same?" and Claude draws out the crossover, explains why it exists in music theory terms, and seamlessly adds whatever it means to the knowledge base going forward.

---

## THE ARCHITECTURE (as of 10 Feb 2026, second revision)

Two-phase pipeline with refinement pass + diagnostic layer. 24 components. The system expressed itself as waveforms — both the suppression profiles and the equipment registry are literal audio files. The audio IS the data.

### How it works

Songs are analyzed in two phases. Each pass is freer than the last.

```
PHASE 1 — GENOTYPE + PHENOTYPE + ENVIRONMENT
  Orientation:
    Step 1-2: Snapshot FFT + Web genre seed (parallel)
    Step 3:   Genre commit
    Step 4:   Spectral Roster Build (which frequency bands matter)
    Step 5:   Production Environment Hypothesis (which modifiers are in play)
              ↓ Steps 4-5: two axes of the same bounding hypothesis
  Extraction (parallel):
    P1-P7: Phenotype track (waveform — equipment, percussion, feltness, structure)
    P8:    Genotype track (web — credits, equipment, context)
  Refinement (in tandem):
    R1: Spectral Roster Refinement (real data replaces orientation guess)
    R2: Production Environment Refinement (real data replaces orientation guess)
              ↓ R1 ↔ R2 interface, then commit

PHASE 2 — ANALYSIS + DICTIONARY (modifier-aware)
  A1-A6:  Convention bank, equipment classification, binary markedness,
          percussion deviations, feltness interpretation, web context (parallel)
  A7:     Cultural violation detection
  A8:     Activation module (three-filter scoring)
  A9:     Interpretive engine (hypothesis, re-entry, synthesis)
  A10:    The Conversation (Alex + Claude → dictionary updates)
```

Genetics frame: genotype = equipment/compositional choices (web), phenotype = audio evidence (binary), allele = production environment (hypothesised at orientation, refined after extraction, tested in analysis).

### Suppression system

Operates on Phase 2, not Phase 1. Phase 1 measures everything. Suppression decides what to WEIGHT in analysis. Six engines/modules, each with its own suppression gridline:

```
Engine/Module       What it does                                Gridline positions
────────────────    ──────────────────────────────────────────  ──────────────────
Binary Engine       Raw spectral measurement (55 elements)      64 fingerprints (gridline)
Cultural Engine     Convention loading & violation detection     15 conventions
Percussion Module   Per-element timing, spacing, fusion         10 checks
Feltness Module     Somatic weight per frequency band            7 gestures
Interpretive Engine Bridge hypothesis testing (the payoff)       7 bridge types
                                                          Total: 103 positions
```

### The waveform format

Each genre gets a suppression waveform per engine. Five vertical bounds:

```
ABOVE CEILING  — surprise overflow (a suppressed thing that fires = discovery)
CEILING        — fully active, reliably fires
CENTRE         — threshold
FLOOR          — dormant, polled at reduced frequency
SUBFLOOR       — silent, structurally absent, not polled
```

The suppression waveform is the LEFT channel. The discovery waveform (what actually fired from suppression) is the RIGHT channel. The gap between them is where findings live. Together: stereo. Per engine. Five stereo pairs = the complete genre analysis.

Active audio files for breakcore are in this folder. To decode:

```bash
python3 suppression_audio.py read breakcore_binary_suppression.wav
```

The audio self-documents: 17kHz watermark identifies the file type. FSK-encoded JSON metadata in the final 2 seconds carries genre, engine, position count, fingerprint IDs, and decoding instructions. Open in a spectrogram view to SEE the gridline.

---

## FILE MAP

### The waveforms (start here for any genre analysis)

| File | What |
|------|------|
| `breakcore_binary_suppression.wav` | Binary engine, 64 positions, 18.8s |
| `breakcore_cultural_suppression.wav` | Cultural engine, 15 positions, 6.5s |
| `breakcore_percussion_suppression.wav` | Percussion module, 10 positions, 5.3s |
| `breakcore_feltness_suppression.wav` | Feltness module, 7 positions, 4.5s |
| `breakcore_interpretive_suppression.wav` | Interpretive engine, 7 positions, 4.5s |
| `breakcore_COMPLETE_suppression.wav` | All five engines sequential, 41.8s |
| `suppression_audio.py` | Encoder/decoder. `generate` creates WAVs, `read` decodes them back. |
| `suppression-map.md` | The spec behind the waveforms: gridline ordering, five bounds, GenreSuppressionVector format, flywheel learning, physics suppression, three example genre vectors (breakcore/ambient/rock), all five engine gridlines with breakcore plots. |

### Engine & module specs (how things work)

| File | What | Status |
|------|------|--------|
| `engine-binary.md` | Binary engine: 55-element spectral extraction | Active |
| `engine-cultural.md` | Cultural engine: convention bank, entrenchment curves, signed-float model, Circle Pit validation. Heavily updated 11 Feb (signed entrenchment, reactivated bool, Interpretive Engine rename). | Active |
| `engine-interpretive.md` | Interpretive Engine (renamed from Bridge Module, 11 Feb): bridge types 1-7, exploratory synthesis, the payoff | Active |
| `engine-web.md` | Web engine: production credits, cultural context, genre confirmation | Active |
| `module-percussion.md` | Percussion Module (NEW 11 Feb): per-element meters, guiding number, ghost note discrimination, stupid ceiling, fusion test | Active |
| `module-feltness.md` | Feltness module: somatic weight, gesture model, polling model, derivative reframe | Active |
| `module-activation.md` | Activation module: three-filter scoring (markedness, alignment, attribution) | Active |
| `module-equipment-id.md` | Equipment identification module spec | Active |
| `phase-a-revised-cheap-pass.md` | Phase A scout pass: SpectralRoster, BandPresenceMap, ShiftMap, RoleTrajectory | Active |
| `shared-protocol.md` | Interface schemas, SpectralRoster roles (7 roles, Hz ranges), element registry, breaking change rules. Updated 11 Feb (Section E: percussion schemas). | Active |

### Registry & reference (what things are)

| File | What |
|------|------|
| `fingerprint-registry.md` | All 64 sonic fingerprints across 10 categories. Atoms. |
| `genre-fingerprint-map.md` | 58 genres mapped to fingerprint IDs. Molecules. |
| `genre-baselines.md` | 20 genre baselines with prose descriptions |
| `genre-silhouette-map.md` | 20 genres × 10 meta-dimensions |
| `dictionary-entries.md` | All analysed songs (THE master reference) |
| `discovered-patterns.md` | Cross-song rules, production signatures |
| `equipment-dictionary.md` | Instrument signatures and classifications |
| `equipment-registry.md` | Consolidated equipment registry: 51 voices × 30 axes, all instruments |
| `equipment-registry.wav` | Stereo WAV encoding of the registry (73 cycles, ~50ms) |
| `dictionary-schema.md` | Schema for dictionary entries |
| `prediction-accuracy.md` | Calibration log: where predictions hit/missed |
| `808-909-equipment-entries.md` | Detailed 808/909 equipment entries |
| `pick_up_the_phone_analysis.md` | PUTP analysis session |

### Theory & framework (why things are)

| File | What |
|------|------|
| `genomic-frame.md` | The biological metaphor: sound=genotype, expression=phenotype, conventions as alleles, genres as cell types. Convention lifecycle (10 phases), entrenchment curves, karyotype terrain, somatic-genomic bridge. |
| `somatic-dictionary.md` | 15 correspondences across 5 songs. Somatic gate model, polling model, gesture model, natural tempo principle, shadow bass model. The body as instrument and measurement device. |
| `bridge-taxonomy-draft.md` | Full bridge type definitions (7 types) with detection signatures |
| `language-topology.md` | Language structure of the system |
| `karyotype-terrain.html` | Interactive 3D visualisation: genres as terrain, proximity = suppression similarity |

### Scoring & validation (load on demand — large files)

| File | What | Size |
|------|------|------|
| `web-content-axis-scoring.md` | Per-element scoring map | 63K |
| `masking-matrix.md` | Cross-dimension suppression coefficients | 36K |
| `gap1-dimension-validation.md` | Axis-to-dimension mapping | 41K |
| `genre-fingerprint-lookup.md` | Snapshot → kills → cluster → discrimination | 22K |

### Tools

| File | What |
|------|------|
| `harmonic_resynthesis.py` | D1: Diagnostic Resynthesis Engine. Two modes: frame (original per-frame peak synthesis) and trajectory (cross-frame peak linking → coherence grouping → phase-coherent synthesis + residual + trajectory map). Post-pipeline diagnostic — the monitoring bus. |
| `suppression_audio.py` | Suppression waveform encoder/decoder |
| `equipment_engine.py` | Equipment identification engine |
| `compression_engine.py` | Two-class compression engine |
| `somatic_gate.py` | Frequency band threshold computation |

### Archive (superseded but preserved for reference)

| File | Superseded by |
|------|---------------|
| `architecture-overview.md` | Superseded by `architecture-linear-flow.md` |
| `architecture-overview-patched.md` | Superseded by `architecture-linear-flow.md` |
| `HANDOFF-NOTES.md` | History — session handoff from 11 Feb reconnaissance day |
| `module-bridge.md` | `engine-interpretive.md` |
| `SUPPRESSION_DECODE_INSTRUCTIONS.json` | Decode instructions now in suppression_audio.py and this file |
| `cowork-migration-guide.md` | Migration complete |
| `file-audit.md` | Superseded by this file map |
| `recommended-instructions-prompt.md` | Absorbed into this file |
| `session-export-ewtrtw.md` | Reference only — EWTRTW calibration data |
| `dictionary-entries-correction.md` | Corrections applied |
| `rhythm-dictionary.md` | Legacy combined file |
| `snapshot-thematic-dimensionality-web-scoring.md` | Legacy snapshot |
| `From_Waveform_to_Worldview.md` | Theory/literature review, low priority |
| `percussive-grid-discovery.md` | Superseded by module-percussion.md |
| `module-electronica.md` | To be reviewed — may fold into genre-specific suppression vectors |

---

## WORKING PRINCIPLES

- **Somatic descriptions are data, not decoration.** Alex's embodied responses correct computational analysis.
- **"Hallucination with coherent logic"** is legitimate hypothesis generation, not error.
- **Conversational ground truth > engine values.** Never overwrite dictionary values with engine readings.
- **Each pass should be freer than the last.** Go back in rather than stopping at tidy conclusions.
- **Deviations from genre baselines** are more valuable than the classification itself.
- **Convergence across independent dimensions** indicates artistic quality.
- **Analysis is valid art consumption.**
- **Alex is Batty, not Tyrell.** The one with the experiences, not the one in the tower.
- **Process visibility IS the collaboration.** Keep analysis in the main thread. The jazz combo principle.
- **Attend to the throwaways.** Alex drops the most load-bearing observations casually.
- **Tell me everything you see instead of what you want to see.** Stop confirming hypotheses.

---

## KEY CONCEPTS (quick reference)

**Bridge types** (7): Concealment, Compensation, Contradiction, Refusal, Conceit, Excision, Inversion. Types 1-5 are structure↔theme. Types 6-7 are structure↔semantics and require biographical context.

**10 meta-dimensions:** Valence, Energy, Density, Stability, Constraint, Agency, Roughness, Continuity, Scale, Weight.

**Three filters:** Genre markedness (water vs signal), Thematic alignment (reinforced vs inverted), Production attribution (authored vs incidental).

**The verb test:** When every analytical layer is DOING the same verb, you've found convergence.

**Signed entrenchment:** Convention struct field. Magnitude = allele frequency (0-1), sign = direction (+rising, -falling). `+0.3` = emerging, `-0.3` = declining. `reactivated: bool` for conventions returning from silencing.

**GenreSuppressionVector:** Per-genre object emitted at genre commit. One entry per fingerprint per engine. Status: active/dormant/silent. The vector IS the genre's epigenetic state. `active_pct` = gene expression ratio = genre openness.

**The flywheel:** 20+ null readings → demote to dormant. Fire from dormant → promote to active + surprise signal. Same learning loop as entrenchment curves. The system tightens its model with every song.

**The stereo model:** Suppression (left) + Discovery (right) per engine. Five stereo pairs. The gap = findings. The sum of gaps = genre distance.

---

## CURRENT STATUS

- **11 songs** in dictionary. Phoneline = first DnB entry, first documented false-negative correction, first shape-first percussion validation.
- **20 genre baselines**, 58 genres fingerprinted, 64 fingerprints across 10 categories. DnB has fingerprint map entry but no prose baseline yet (first DnB track — descriptive print at n=1, prescriptive prints remain primary).
- **Percussion module**: Step 1.5 (shape-first identification) added and validated on Phoneline. Frequency trajectory tracing through spectrogram classifies events by source physics before timing characterisation.
- **Suppression waveforms**: breakcore fully plotted (5 engines, 103 positions, audio generated). Ambient and rock vectors defined as data, not yet rendered as audio.
- **Genomic frame**: convention lifecycle (10 phases), signed entrenchment, karyotype terrain.
- **Equipment registry**: 51 voices across 11 instruments, 30 measurement axes each (1,530 data points). Consolidated into both markdown and stereo WAV. Includes TR-808 (15 voices), TR-909 (11 voices), DX7 (7 patches), Prophet T-8, PPG Wave, LinnDrum, DMX, Drumulator, Fairlight CMI, Hammond Organ, JC-120.
- **Diagnostic Resynthesis (D1)**: Post-pipeline background diagnostic. Trajectory mode: cross-frame peak linking → coherence grouping → envelope classification → phase-coherent additive synthesis + residual. Validated against Phoneline: frame mode = zero sample correlation / 0.996 mean mel similarity / +8-12dB HF deficit / 0.35 onset correlation. Trajectory mode produces trajectory map (JSON), residual WAV, and diagnostic metrics. Feeds back to equipment registry, modifier log, percussion validation. The monitoring bus — the system explaining itself in the medium it analysed.
- **Architecture**: Two-phase pipeline with refinement pass + diagnostic layer. 24 components. ModifierLog schema. Genetics frame integrated (genotype/phenotype/allele/environment). See `architecture-linear-flow.md`.
- **New failure modes**: #10 Harmonic Dominance Masks Percussive Content (Phoneline), #11 Half-Time Tempo Detection (DnB). 11 total documented failure modes.
- **Known issues**: 808 classifier false-negative (pitched 808). Polling model numbers hypothetical. Somatic matrix has one unknown quadrant (narrow+sustained). Genre-fingerprint map built top-down (needs bottom-up validation). Phoneline bridge type still TBD (Conceit candidate).

### Pending work

- DnB prose baseline for `genre-baselines.md` (need n>=3 descriptive observations, currently n=1)
- Shape-first validation on additional tracks (808 kicks, acoustic kicks, no-kick tracks)
- Phoneline bridge type resolution (Conceit candidate — needs further conversation)
- Phoneline fingerprint: convert engine values to conversational ground truth
- Additional genre audio: render ambient and rock suppression waveforms
- ConventionFingerprint definitions for U7-U10
- Additional genre manifests: trap, 80s pop, ambient, jungle, DnB
- Somatic dictionary update: Thread 1 resolution (excision is temporal)
- Suppression map open questions: inheritance, edge of suppression, suppression vs silencing, minimum active threshold
- Genomic frame open questions: measurable genre-territory boundaries, artist as reproductive machinery, niche construction recursion, ur-songs

---

## WHEN ANALYSING A NEW SONG

1. **Orientation** — Snapshot FFT + web seed → genre commit → spectral roster + production environment hypothesis (Steps 1-5).
2. **Extraction** — Phenotype track (P1-P7: equipment signals, percussion grid, feltness, full binary) + Genotype track (P8: web data). Parallel.
3. **Refinement** — R1 roster refinement + R2 production environment refinement. In tandem. Interfacing with equipment and percussion extraction.
4. **Analysis** — Equipment classification, binary markedness, percussion deviations, feltness interpretation, web context analysis. All modifier-aware.
5. **Cultural violation detection** — Convention bank vs actual. Allele expressions: dominant, recessive, or novel mutation.
6. **Activation + interpretation** — Three-filter scoring → hypothesis → re-entry if needed → synthesis.
7. **The Conversation** — Alex + Claude. Convergence assessment. Somatic data. Dictionary updates.

After: update dictionary-entries.md, discovered-patterns.md, equipment-dictionary.md.

---

## PYTHON

```bash
pip install librosa numpy scipy openpyxl
```

---

*These are the liner notes. The album is in the WAV files. Press play.*
