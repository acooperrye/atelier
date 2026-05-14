# DISCOVERED PATTERNS
## Cross-Song Rules, Generalizations, and Emerging Heuristics
## Last updated: 2026-02-10

---

## PRODUCTION METHOD DETECTION

| Method | Signature | Source songs |
|--------|-----------|-------------|
| Electronic/sequenced | grid>40% + CV<0.25 + corr>0.9 + flat<0.06 | BG |
| Live band | grid<20% + CV>0.25 + corr<0.8 + flat range>0.15 | OH |
| Sample-based | grid<15% + CV<0.02 + attack<100ms | NTLTC |
| Bedroom-electronic/hyperpop | grid>70% + high contrast all bands + sub>40% | USC |
| Hybrid-era (machine+organic samples) | timing CV ~2% + random deviation autocorrelation + engine misclassifies source | SHOUT |
| Trap/808-melodic | sub-bass >40% + pitched bass (pitch CV >0.3) + blooming decay (energy grows post-onset) + M/S ratio <0.2 | PUTP |
| DnB/liquid | grid>90% + sub-bass melodic (hpss_harmonic>95%, onset_ratio>15x) + dual-system percussion (bass leads hi-mid) + kick embedded in bass synth (~7% energy) + M/S<0.1 | PL |

## PHYSICAL CHARACTER

| Character | Signature | Source |
|-----------|-----------|--------|
| Percussive | A/D<0.5, attack<300ms | BG |
| Swelling | A/D>1.5, attack>500ms | OH |
| Sampled-sharp | attack<100ms with off-grid IOI | NTLTC |
| Textural | attack~300ms with high grid + high density | USC |

## ARRANGEMENT ARCHITECTURE

| Architecture | Signature | Source |
|-------------|-----------|--------|
| Continuous-fed | silence<2%, density floor>1.0 | BG |
| Continuous-sustained | silence=0%, density floor<0.5 | OH |
| ON/OFF alternating | silence>10%, density range>10 | NTLTC |
| WALLâ†'COLLAPSEâ†'REBUILDâ†'DEATH | silence>10%, dynRange>25dB, MFCC shift>300 | USC |
| Overture→Drop→Breakdown→Drop→Outro | silence~24%, bass-first intro (overture teaches gestural vocabulary), sectional plateau (not linear escalation), spectral flux stable Q2-Q4 | PL |

## HARMONIC PURITY ZONES

| Zone | Signature | Source |
|------|-----------|--------|
| Noise-dominant/percussive | HNR<0, overall noise-heavy (breaks pull it down), but sub-bands split: sub-bass 99% harmonic, hi-mid 81% percussive | PL |
| Rough/noisy | HNR<3.0, flat max>0.15 | OH |
| Clean/electronic | HNR 3-6, flat max<0.06 | BG |
| Vocal-dominant | HNR>9.0, flat floor<0.001 | NTLTC |
| Vocal-stacked | HNR avg>8.0, HNR peak>15, flat floor<0.001 | USC |

## SPATIAL DESIGN

| Design | Signature | Source |
|--------|-----------|--------|
| Mono | corr>0.9, M/S<0.05 | BG |
| Near-mono/stacked | corr>0.8, M/S<0.1, everything co-located center | PL |
| Wide-static | corr 0.7-0.8, M/S 0.1-0.2 | OH |
| Narrative-convergent | corr range>0.5, trending upward | NTLTC |
| Two-act | corr>0.9 then crashes to <0.1, including negative | USC |

## TEMPO ZONES

| Zone | Range | Genre association |
|------|-------|-------------------|
| ~85 BPM | 80-90 | Indie/post-rock |
| ~99 BPM | 96-102 | Synth-pop (slow end) |
| ~112 BPM | 108-116 | Synth-pop |
| ~122 BPM | 118-126 | Dance-pop/UK garage |
| ~137 BPM | 130-140 | R&B-electronic |
| ~152 BPM | 148-156 | Hyperpop/high-energy electronic/trap |
| ~174 BPM | 170-180 | DnB/liquid DnB (often detected as half-time ~87 BPM) |

## DYNAMIC RANGE ZONES

| Zone | Range | Character |
|------|-------|-----------|
| <7 dB | Modern compressed | BG, OH |
| 10-14 dB | ON/OFF with deliberate contrast | NTLTC, EWTRTW, PL |
| 15-22 dB | Breathing/dynamic, preserved transients | SHOUT |
| >25 dB | Wallâ†'collapse, extreme structural dynamics | USC |

## FORMAL STRUCTURE

| Structure | Signature | Source |
|-----------|-----------|--------|
| Repetitive-pop | sym>4, sim>0.8 | BG |
| Developmental | sym<2, sim<0.78, MFCC multi-shift | OH |
| Maximally-repetitive | sym>50, sim>0.85, single-texture | NTLTC |
| Wall-then-collapse | sym>30 in first half, MFCC mega-shift mid-song | USC |

---

## BRIDGE TYPE CORRELATIONS (EMERGING)

| Bridge type | Dimensional pattern | Detection hint | Prototype |
|------------|-------------------|----------------|-----------|
| Concealment | Cross-dimensional. High-VALENCE/DENSITY structure + Low-VALENCE theme | Bright/stable structure vs dark meaning | EWTRTW |
| Compensation | Cross-dimensional. High-DENSITY structure + Low-DENSITY theme | Full sound around empty subject | NTLTC |
| Contradiction | Within-dimensional. Both structural and thematic strong, opposite signs | Neither side wins. Vertigo | BG |
| Refusal | Within-dimensional. Structure static despite thematic escalation | Structure won't respond. Withholding | EWTRTW (dynamics) |
| Conceit | Cross-dimensional via metaphor. Convergence verb reveals it | Process analogy, not surface match | No prototype yet |
| Alignment | Structure and meaning agree internally. Significance is relational/contextual | Song's meaning depends on contrast with what surrounds it, or on somatic memory | SHOUT, PUTP |

**Distinguishing CONTRADICTION from REFUSAL:** Both within-dimensional. In contradiction, structure actively participates in opposition (vertigo). In refusal, structure remains static while content moves (frustrationâ†’recognition). Diagnostic: does the structure MOVE or STAY?

**Distinguishing ALIGNMENT from CONCEIT:** Both involve structure agreeing with meaning. In Conceit, the agreement is an authored metaphor (knowing, designed). In Alignment, the agreement is earnest and the significance comes from the song's CONTEXT rather than internal tension. Diagnostic: is the meaning self-contained, or does it require contrast with something external? Two subtypes emerging: (1) contextual alignment (Shout — meaning requires contrast with restraint/silence around it), (2) somatic alignment (PUTP — meaning requires the listener's body memory, e.g. the 808 envelope reproducing the physical sensation of a phone vibrating).

**Distinguishing CONCEALMENT from COMPENSATION:** Both cross-dimensional. Concealment hides (bright over dark). Compensation fills (full around empty). Diagnostic: is the structure masking something or surrounding something?

---

## ENGINE RELIABILITY CORRELATIONS

Production transparency predicts engine accuracy:
- BG (94%): transparent production, waveform IS the song
- OH (73%): organic but layered
- USC (68%): extreme dynamics challenge engine
- NTLTC (52%): heavily constructed, waveform obscures layer architecture

**Rule of thumb:** More production layers = lower engine match % = greater web engine reliance.

---

## BROKEN ELEMENTS (consistent across all songs)

| # | Element | Status | Notes |
|---|---------|--------|-------|
| 25 | Beat micro-peaks | DISCARD | Suspect measurements |
| 27 | Decay time | DEGRADED (0.3) | Physically impossible readings |
| 28 | A/D ratio | DEGRADED (0.3) | Depends on broken #27. BG engine reads 24.649 vs dictionary 0.343 |
| 30 | F0 (>200Hz) | DEGRADED (0.5) | Fails for polyphonic mid/high |
| 40 | Chromatic density | DEGRADED (0.5) | Low discrimination (all 5.7-6.9) |
| 44 | HNR | DEGRADED (0.5) | Systematically 3-6dB low |
| 47 | F0 trajectory | DEGRADED (0.5) | Same issue as #30 |
| 49 | Vocal presence | BROKEN | Returns 0% for all tracks |
| 52 | Reverb estimation | BROKEN | Impossibly dry readings |

---

## FIVE FAILURE MODES

1. **Axis Selection Error** â€" right number, wrong axis leads interpretation
2. **Co-Production Blindness** â€" individual elements correct but experience lives in their interaction
3. **Averaging Destroys Trajectory** â€" summary hides the shape (NTLTC stereo: avg 0.686 hides 0.02â†'0.89)
4. **Genre Frame Reversal** â€" measurement correct but genre convention reverses markedness
5. **Bridge Problem** â€" structurally correct but misleading about the SONG because meaning side not accounted for
5b. **Premature Collapse** — treating an unresolved observation as a resolved one. "I can't see X" becomes "X is absent" and downstream analysis builds on the absence. The correct stance is Schrodinger's: every element is in superposition until there exists a method to collapse it. If the observation doesn't settle (e.g. 399 unexplained fast-attack events), hold it open. The gnaw is the data. (Phoneline kick drum, 10 Feb 2026.)
6. **Ghost Source Confusion** — machine triggering organic samples (Drumulator + Bonham) defeats source classification. Engine reads the sample, not the machine. Timing analysis required to unmask.
7. **Dominant Bass Key Swamp** — strong bass note on non-tonic degree swamps chroma analysis. Engine reports key of bass note rather than harmonic center (Shout: G bass in C major → engine reports F minor; PUTP: D bass dominant in G minor → engine reports D)
8. **Pitched 808 Repetition Defeat** — drum classifier uses spectral repetition consistency to identify machines. Pitched 808 bass has different spectral content on every hit (31 unique pitches, CV 0.6678 in PUTP). Classifier reads this as "organic variation" when it's the same instrument playing different notes. Two alternative detection angles: (a) decay envelope shape — 808's blooming resonance grows to 2.36x at 200ms, unique among all instruments; (b) attack-body spectral ratio — 2kHz trigger click is pitch-independent, present on every hit regardless of tuning.
9. **808 Sustain Defeats Synth Subtraction** — two-axis subtraction works when the drum transient is separate from the sustained content (Shout: Drumulator fires, synths sustain). Fails when the drum IS the sustain (PUTP: 808 bass tail fills the pre-onset window at 100-114% energy). Subtraction only works above 1kHz where the attack transient separates from the body.
10. **Harmonic Dominance Masks Percussive Content** — when a sustained harmonic element (bass synth) and a transient percussive element (kick) share the same frequency band, time-averaged analysis only sees the dominant harmonic content. Phoneline: 30-150 Hz reads 96% harmonic because the bass synth's sustained energy dwarfs the kick's transient energy in any averaging window. Five extraction methods failed: (a) time-domain amplitude, (b) HPSS ratio, (c) bandpass energy, (d) onset detection phase maps, (e) energy deposit/withdrawal ratios. All measure MAGNITUDE, not shape. Solution: HPSS separation (extract percussive component), then frequency trajectory tracing through spectrogram. Kick identified by downward frequency sweep shape. The shape persists regardless of amplitude ratio — a kick sweeps downward whether it's 7% or 70% of total energy.
11. **Half-Time Tempo Detection** — DnB at ~174 BPM consistently detected as ~87-119 BPM by standard autocorrelation-based tempo estimators. The syncopated kick pattern (beats 1 and 3, not every beat) and the two-bar phrase structure cause the estimator to lock onto the half-time pulse. Web-sourced BPM is essential to disambiguate (GuidingPrior from percussion module).

---

## SHAPE-FIRST PERCUSSION IDENTIFICATION (NEW — Phoneline, 10 Feb 2026)

### The Problem

Magnitude-based percussion identification fails when multiple elements share a frequency band at different energy levels. In Phoneline, five independent extraction methods failed to isolate the kick drum from the bass synth and snare bleed in the 30-150 Hz band: time-domain amplitude, HPSS ratio, bandpass energy, onset detection phase maps, and energy deposit/withdrawal ratios. All measure HOW MUCH energy, not WHAT KIND.

### The Insight (Alex Cooper-Rye)

"You need to plot where it comes on and plot where it leaves off in the 2D space of the actual wave. It's a parabola from the spike in the spectrogram where it onsets to the point in the spectrogram where it is gone again."

"You don't see a speaker making the kick drum noises but you hear them clear as crystal." — The shape of the sound persists through the medium. A kick drum's frequency trajectory is the same whether it's 7% or 70% of the mix energy.

### The Method

1. Detect onset events via standard onset detection (spectral flux, peak picking)
2. For each event, extract the spectrogram window (onset → onset+decay)
3. Track the PEAK FREQUENCY through that window frame by frame
4. Classify by trajectory shape:
   - **Downward sweep** (high → low, fast): KICK. Starts 129-194 Hz, ends 32-86 Hz. The drum head's resonant frequency drops as the initial impact energy dissipates.
   - **Broadband spread** (no directional trajectory): SNARE BLEED / noise burst. Energy distributed across band without coherent frequency movement.
   - **Static or upward** (frequency holds or rises): BASS NOTE onset. Pitched content establishing and sustaining.
   - **Rapid oscillation** (frequency jumps between harmonics): 808-TYPE pitched decay. The harmonic series of the tuned drum.

5. After classification: characterize timing, grid position, deviation pattern

### Why Shape Works When Magnitude Fails

Magnitude is relative — it depends on the mix balance, the production processing, the mastering chain. Shape is intrinsic — it depends on the physics of the sound source. A kick drum sweeps downward because the drum head's tension dissipates after impact. That's physics, not mixing. No amount of compression, EQ, or layering changes the direction of the sweep. It may change the amplitude, the bandwidth, the duration — but the trajectory through frequency-time space is a signature of the source.

### Implications for the Percussion Module

Shape-first identification should precede timing characterization. The current Step 1 (find the hits) finds events. A new Step 1.5 (trace shapes) identifies WHAT each event is. Step 2 (derive intervals) then operates on classified events, not raw onsets. This reordering means the percussion module can distinguish kick from snare bleed before trying to build per-element meters, avoiding the flat-phase-map problem where unclassified events smear the timing distribution.

### Validation Status

Validated on one song (Phoneline). Downward sweeps clustered at beats 1 and 3 (68.5%) matching Alex's somatic description exactly. Needs validation on additional tracks, especially: (a) songs with pitched 808 kicks (different sweep shape expected), (b) songs with acoustic kicks (similar downward sweep expected but different bandwidth), (c) songs with no kick (should find zero downward sweeps in the low band).

---

## COMPRESSION ARTIFACT PROFILE (MP3, 320kbps vs 120kbps)

Source: Variance analysis on "Shout" — Tears for Fears. Same master, two bitrates.

### Metric Reliability by Bitrate

| Tier | Metrics | Max drift at 120kbps | Recommendation |
|------|---------|---------------------|----------------|
| 1 — Bitrate-immune | tempo, beat_cv, key, onset timing, dynamic range, bass/mid/treble %, stereo corr, M/S ratio, self-similarity, MFCCs 0–3 | <2% | Use at any quality |
| 2 — Bitrate-sensitive | side centroid, treble %, HNR, ZCR, onset envelope peaks, crest factor | 2–5% | Flag below 256kbps |
| 3 — Bitrate-dependent | MFCCs 4–12, flatness_min, MFCC shift calculations, fine timbral fingerprinting | 10–55% | Require ≥256kbps |

### Frequency Band Survival

| Band | 120kbps energy vs 320kbps | Notes |
|------|--------------------------|-------|
| 0–8 kHz | ~100–106% (stable or slightly inflated) | Safe zone. Artifacts ADD energy to 4–8kHz |
| 8–12 kHz | ~100% | Borderline safe |
| 12–16 kHz | ~91% | Air/shimmer begins to thin |
| 16–20 kHz | ~3% (97% loss) | Effectively amputated at 120kbps |
| Effective ceiling | 17.5 kHz (320) vs 15.5 kHz (120) | 2kHz band of information lost |

### Implications for Analysis

- **Percussion timing analysis**: IMMUNE. Grid precision, IOI measurements, onset detection all survive.
- **Equipment engine (source classification)**: Mostly robust for band-isolated features. FM sideband detection may lose sensitivity if sidebands are above 15kHz.
- **MFCC-based timbral comparisons**: UNRELIABLE below 256kbps. MFCC shift calculations (used for COLLAPSE detection in USC) should not be trusted at low bitrate.
- **Stereo field analysis**: Robust for correlation/M/S. Side brightness (centroid) shifts ~3.4% downward — edges get slightly darker.
- **The 4–8kHz artifact inflation**: Compression ADDS ~6% energy to presence range. This can cause false brightness readings or inflate treble percentage.

### Detection Heuristic

To estimate source bitrate from audio:
- Energy above 16kHz < 0.1% → likely ≤128kbps
- Energy above 16kHz 0.1–1.0% → likely 128–256kbps
- Energy above 16kHz > 1.0% → likely ≥256kbps or lossless
- Sharp spectral cliff at 15–16kHz with flat noise floor below → MP3 encoding signature

---

## MULTI-RESOLUTION EXTRACTION ARCHITECTURE

Source: Bitrate ladder + sample rate comparison on "Shout." Validated against 320kbps ground truth.

### Three-Pass Extraction Strategy

| Pass | Sample Rate | Time | Purpose | Metrics Available |
|------|-------------|------|---------|-------------------|
| Scout | sr=11025 | ~8s | Structural skeleton | tempo, key, self-similarity, stereo corr, dynamic range, RMS, crest factor |
| Standard | sr=22050 | ~17s | Detailed anatomy | + band balance, onset detection, centroid, HNR, percussion timing, MFCCs 0–3 |
| Timbral | sr=44100 | ~35s | Fine spectral detail | + MFCCs 4–12, equipment identification, synthesis family, section-level timbral comparison |

### When to Use Each Pass

- **Scout only**: Quick song comparison, playlist-level analysis, structural landmark mapping. Gives you the skeleton in 8 seconds.
- **Scout + Standard**: Normal song analysis (passes 1–5). Covers everything except fine timbral fingerprinting.
- **All three**: Equipment identification, MFCC shift detection (COLLAPSE-type events), synthesis family classification.

### Sample Rate vs Compression: Different Blindness

| Distortion source | Direction | Mechanism | Shared immune metrics |
|-------------------|-----------|-----------|----------------------|
| Low sample rate (sr=11025) | Reads DARKER, BASSIER | Clean removal of HF content | tempo, key, self-sim, stereo corr, crest |
| MP3 compression (120kbps) | Reads SLIGHTLY BRIGHTER | Codec adds artifacts in 4–8kHz | tempo, key, self-sim, stereo corr, crest |

These are OPPOSITE distortions. Cannot use one correction factor for the other.

### Bitrate Survival Ladder

| Metric | Floor (>5% = broken) |
|--------|---------------------|
| tempo, self_similarity, key, stereo_corr, crest | 16kbps (indestructible) |
| rms_mean, key_confidence | 32kbps |
| dynamic_range | 48kbps |
| onset_count, beat_cv, bass/mid/treble %, zcr | 64kbps |
| centroid, hnr, treble_pct | 96kbps |
| MFCCs 0–3, flatness_mean | 120kbps |
| MFCCs 4–12, flatness_min | 256kbps+ |

---

## INSTRUMENT COMPRESSION FINGERPRINT METHODOLOGY (VALIDATED)

### Core Insight

1980s samplers and synthesizers imposed their own lossy compression on source material:

| Machine | Bit Depth | Sample Rate | Nyquist Ceiling | Quantization Levels |
|---------|-----------|-------------|-----------------|---------------------|
| E-mu Drumulator | 8-bit | ~28kHz | ~14kHz | 256 |
| LinnDrum LM-2 | 8-bit | ~28kHz | ~14kHz | 256 |
| Fairlight CMI (I/II) | 8-bit | ~16kHz | ~8kHz | 256 |
| Oberheim DMX | 8-bit | varies | varies | 256 |
| Yamaha DX7 (DAC) | 12-bit | 49.1kHz | ~24.5kHz | 4096 |
| PPG Wave 2.3 (DAC) | 12-bit | varies | varies | 4096 |
| E-mu Emulator | 8-bit | ~28kHz | ~14kHz | 256 |

These specifications create FIXED, PREDICTABLE artifact signatures:
- **Aliasing**: energy above the Nyquist ceiling folds back, creating phantom harmonics at specific frequencies
- **Quantization noise**: bit-depth-dependent noise floor with specific spectral characteristics
- **Spectral ceiling**: hard cutoff above Nyquist, analogous to MP3’s frequency ceiling

### Detection Approach (derived from MP3 variance analysis)

The same methodology used for bitrate detection can identify instrument-era compression:

1. **Spectral ceiling detection**: Look for the frequency above which energy drops sharply.
   - Ceiling at ~8kHz → likely Fairlight CMI (Series I/II)
   - Ceiling at ~14kHz → likely 8-bit/28kHz class (Drumulator, LinnDrum, Emulator)
   - No ceiling below 20kHz → 12-bit or higher (DX7, PPG, modern)

2. **Quantization noise profile**: 8-bit quantization creates specific noise floor characteristics.
   - 8-bit: noise floor at approximately -48dB (6dB per bit)
   - 12-bit: noise floor at approximately -72dB
   - 16-bit: noise floor at approximately -96dB

3. **Aliasing artifact detection**: Energy at frequencies above the machine’s Nyquist that fold back into the audible range.
   - 28kHz sample rate: aliasing mirrors around 14kHz
   - 16kHz sample rate: aliasing mirrors around 8kHz
   - The folded-back energy creates phantom harmonics at predictable positions

### Why This Solves Ghost Source Confusion

The Drumulator’s Bonham samples SOUND organic (because the source IS organic). But they CARRY:
- 8-bit quantization noise (256 levels of amplitude resolution)
- Spectral ceiling at ~14kHz (energy above this is aliasing, not source)
- Identical artifact signature on every hit (because it’s the same compressed sample replayed)

These artifacts persist through mixing, EQ, gating, and layering. They are the machine’s fingerprint imposed on the organic source. Detecting them allows identification of the MACHINE even when the SAMPLE sounds human.

### Relationship to MP3 Variance Analysis

| What we measure | MP3 compression | Instrument compression |
|----------------|-----------------|----------------------|
| Frequency ceiling | 15.5kHz at 120kbps | ~14kHz (8-bit/28kHz), ~8kHz (Fairlight) |
| Artifact inflation | +6% in 4–8kHz | Aliasing energy below Nyquist |
| Noise floor | Codec quantization | Bit-depth quantization |
| Detection method | Compare bitrate ladder | Compare spectral ceiling + noise floor |

### Status

VALIDATED (2026-02-09). Spectral ceiling detection works in full mixes after two-axis subtraction.

**The problem:** Raw spectral analysis of full mix cannot see the Drumulator's 14kHz ceiling. Sustained synths (Prophet-5, DX7, Hammond) provide 120-125% energy cloaking below 14kHz, thinning to 54% at 15kHz and 19% at 16kHz. The synths paper over the ceiling.

**The solution — two-axis subtraction:**

1. **Vertical axis (spatial):** MID channel isolates center-panned kick/snare from edge-panned percussion (hi-hats, LinnDrum bell, cowbell). Removes instruments that naturally extend above 14kHz.

2. **Horizontal axis (temporal):** Synths sustain across the bar — their spectral contribution doesn't change much within a 4/4 period. Sample the synth bed from 180ms BEFORE each beat hit (where synths are present but the drum transient isn't). Subtract that from the beat window. What remains is the drum machine's transient contribution alone.

**Result after subtraction (309 snare hits averaged):**
- Residual shows -3.8dB dip at 14kHz (normalized to 12kHz)
- Steepest gradient drop: -69.9 dB/kHz at 14,812 Hz (sharper than the MP3 ceiling at -51.3 dB/kHz)
- Above 16kHz: 94% of remaining energy is transient, only 6% synth leakage
- The Drumulator's ceiling is visible as a cliff, not just a dent

**Generalizability:** This method works whenever: (a) the drum machine is center-panned (nearly always true), (b) the sustained harmonic content is predictable within a bar (true of most synths and pitched instruments), and (c) beat positions can be tracked (trivial at any tempo). Implemented as `SpectralCeilingDetector.analyze_in_mix()` in `compression_engine.py`.

---

## COMPRESSION VECTOR FRAMEWORK (VALIDATED)

### Core Insight (Alex Cooper-Rye, 2026-02-09)

Compression floors from the bitrate ladder ARE vectors for analysis. A dictionary of sounds needs only:
1. The PURE endpoint (highest quality)
2. The MOST DISTORTED endpoint (lowest quality)
3. The understanding that any variant falls somewhere on the vector between them

### Validation: Shout Full Mix

Bitrate ladder (320/120/96/64/48/32/16 kbps) extracted across 20 metrics. Key findings:

**The compression transfer function is approximately LINEAR in aggregate.**
Intermediate bitrates project onto the pure→distorted line with residuals:
- 120kbps: 0.6% off line
- 96kbps: 0.5% off line
- 64kbps: 2.4% off line
- 48kbps: 6.5% off line
- 32kbps: 3.5% off line

**Five behavioral families** govern how metrics respond to compression:

| Family | Behavior | Members |
|--------|----------|---------|
| IMMUNE | <2% change across all bitrates | tempo, crest_factor |
| GRADUAL_DEFLATION | Monotone decrease | flatness_min, onset_count, rms_mean |
| ARTIFACT_INFLATION | Monotone increase (codec adds energy) | mfcc_0, mfcc_2 |
| INFLECT_THEN_COLLAPSE | Rise at 120kbps (artifact inflation), collapse below 64kbps | centroid, treble_pct, zcr, flatness_mean, mfcc_3-12 |
| NON-MONOTONIC | Rise then collapse then rise again | mfcc_7, mfcc_8, mfcc_9 (chaotic below 48kbps) |

**The inflection at 120kbps** in centroid and treble_pct confirms the +6% artifact inflation in 4-8kHz documented in the Compression Artifact Profile. The codec ADDS brightness before the bandwidth ceiling kills it.

**Most discriminative dimensions** (ranked by total change):
1. mfcc_4: 3210% change (from -1.31 to +40.77)
2. mfcc_12: 2109% change
3. mfcc_11: 1325% change
4. mfcc_5: 691% change
5. treble_pct: 100% (vanishes at 16kbps)

### Why Different Sounds Trace Different Vectors

Different spectral content interacts with lossy encoding differently:
- Bass-heavy sounds (808 kick) lose different information than treble-heavy sounds (hi-hat)
- Transient-rich sounds lose different information than sustained tones
- Harmonically-rich FM sounds lose different information than noise-based sounds

The SHAPE of the transfer function is the fingerprint. Not a single metric, but the 20-dimensional trajectory.

### Implementation

`compression_engine.py` — `CompressionVectorEngine` class.
- `add_reference_from_ladder()` — build a reference vector from a bitrate ladder
- `identify()` — project unknown metrics onto reference vectors
- `compare_transfer_functions()` — compare transfer function shapes between references

### Next Steps

1. Build reference vectors for isolated instruments (808 kick, DX7 bell, Drumulator snare, etc.)
2. Test cross-instrument discrimination (can the vector engine tell an 808 kick from a Drumulator kick?)
3. Test in-mix identification (can a reference built from isolated samples identify the same instrument in a full mix?)

---

## CO-PRODUCTION CLUSTERS (confirmed)

| Cluster | Elements | Lead | Known in |
|---------|----------|------|----------|
| Gated drums | attack + dyn range + silence + crest | attack | EWTRTW |
| Bedroom production | grid + stereo corr + M/S + flatness range | grid | BG |
| Sample-locked | grid + CV + attack | grid | NTLTC |
| Wallâ†’collapse | dyn range + MFCC shift + stereo corr + loudness | dyn range | USC |
| Sustain-fills-gaps | silence + density floor + attack | attack | OH |
| Polymetric percussion | on-grid machine + off-grid asymmetric element + clock-shaker | timing CV | SHOUT |
| Ghost samples | machine-triggered organic samples + machine timing precision | onset CV + chroma confusion | SHOUT |
| Kick embeddedness | kick ~7% total energy, masked by sustained bass synth in same band (96% harmonic), separable only via HPSS + shape tracing | HPSS percussive extraction + frequency trajectory classification | PL |
| Bass-kick layering | bass synth (slow attack, harmonic) and kick (fast attack, percussive) co-located in 30-150 Hz, distinguished by attack slope (fast=kick, slow=bass) and frequency sweep direction (downward=kick, static/upward=bass note) | attack classification + spectrogram shape | PL |
