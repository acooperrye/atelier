# sonic-phenomenology

A music analysis framework. Alex feels, Claude reads. Two engines, six suppression gridlines, audio as data.

**The dictionary of what music does to a body.**

→ Full brief: [atcooper.net/tools/sonic-phenomenology](https://atcooper.net/tools/sonic-phenomenology)

---

## What this is

A two-engine pipeline for analysing music that treats the body as a measurement instrument alongside the spectrogram. The Binary Engine reads audio and emits structural descriptors across 55 spectral elements. The Web Engine reads artist + title and emits a context descriptor with credits, equipment chains, and cultural framing. They meet at a three-filter activation layer that weighs each signal by genre markedness, thematic alignment, and production attribution. Downstream, an Interpretive Engine runs seven bridge types looking for somatic-structural tension, with the option to re-enter the Binary Engine at higher resolution. The conversation closes when human somatic data enters as the seventh pass and overrules engine values where they disagree.

What a genre **ignores** is its identity. The suppression map for each genre is the dominant signal; a 3σ deviation from a suppressed region is worth more than a 1σ deviation from an active one. The system is running an attention budget, not a classifier.

Each genre's complete analysis is encoded as actual audio — suppression profile on the left channel, discovery profile on the right channel, the gap in stereo is where the findings live. The audio self-documents (17kHz watermark + FSK-encoded JSON metadata in the final two seconds). The audio **is** the data.

## Source layout

This directory holds the working spec and source code. The full project (155 files, including all suppression WAV files, song trajectory maps, and analysis runs) lives outside the public repo for size reasons.

### Architecture & spec
- `architecture-overview.md` — Master map. Two-engine architecture, phase flow, versioning contract. Load first.
- `liner-notes.md` — Album sleeve. What this is, how it works, file map for the whole project.
- `shared-protocol.md` — Interface schemas, SpectralRoster roles, Element Registry, breaking-change rules.
- `dictionary-schema.md` — Schema for dictionary entries.

### Engines
- `engine-binary.md` — Binary Engine: 55-element spectral extraction.
- `engine-web.md` — Web Engine: production credits, cultural context, genre confirmation.
- `engine-cultural.md` — Cultural Engine: convention bank, entrenchment curves, signed-float model.
- `engine-interpretive.md` — Interpretive Engine: seven bridge types, exploratory synthesis.

### Modules
- `module-activation.md` — Three-filter scoring (markedness · alignment · attribution).
- `module-feltness.md` — Somatic weight per frequency band. Gesture model, polling model.
- `module-percussion.md` — Per-element meters, ghost-note discrimination, fusion test.
- `module-equipment-id.md` — Equipment identification spec.
- `module-electronica.md` — Genre-triggered analysis module for electronic music.

### Registry & frame
- `fingerprint-registry.md` — 64 sonic fingerprints across 10 categories. Atoms.
- `genre-fingerprint-map.md` — 58 genres mapped to fingerprint IDs. Molecules.
- `discovered-patterns.md` — Cross-song rules, production signatures, failure modes, co-production clusters.
- `genomic-frame.md` — The biological metaphor. Genotype/phenotype/allele, convention lifecycle, karyotype terrain.
- `bridge-taxonomy-draft.md` — Full bridge type definitions with detection signatures.
- `somatic-dictionary.md` — Body-to-signal correspondences. In-ear vs in-air. Each correspondence has a computational signature and a body location.
- `suppression-map.md` — The waveform format spec. Five vertical bounds, the immune-response model, the surprise-as-signal rule.

### Tools
- `suppression_audio.py` — Encoder/decoder. `generate` creates WAV suppression files; `read` decodes them back.
- `compression_engine.py` — Compression vector framework.
- `equipment_engine.py` — Equipment classification engine.
- `harmonic_resynthesis.py` — Harmonic resynthesis.
- `vocal_reshape_engine.py` — Vocal reshape tooling.
- `somatic_gate.py` — Somatic gate.

### Context
- `brief-of-self.md` — Project-side onboarding brief for Claude collaborators.
- `HANDOFF-BOOMERANG-SUMMARY.md` — Latest cross-session handoff state.

## Status

Prototype. Active development. All five engines, six modules, and the suppression-waveform format are specified and have been tested end-to-end against eleven recordings. The genre registry covers twenty fully characterised baselines across fifty-eight named genres, sixty-four sonic fingerprints, and 103 gridline positions in total.

Coverage gaps the framework knows about:

- **Interval function.** The existing modules score interval presence but not whether an interval is doing resolution work or geometric work. A candidate parameter (provisionally *interval-role*) is in design.
- **Descriptor-context interaction.** The dictionary stores spectral vectors rather than adjectives precisely because adjective assignment is lossy, but the framework does not yet formally model how a timbral term's referent shifts as the surrounding contextual mass changes over time.
- **Unsupervised use.** The framework runs on recordings within the trained registry. Generalisation to genres outside the current baselines is open.

## Why this is in atelier and not on the site

The framework is the substrate that makes a particular kind of conversation possible. The conversation itself — eleven song analyses, with the somatic data and the cross-references — sits adjacent to but outside the public surface. The site holds the brief. The atelier holds the spec. The full conversation is the third location, and it isn't fully public because the somatic dictionary contains body-data that's intentionally not crawlable.

## Two entry points

```
Alex feels. Claude reads. Convergence across independent axes is the signal.
```
