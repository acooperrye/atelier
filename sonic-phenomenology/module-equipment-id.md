# MODULE: EQUIPMENT IDENTIFICATION ENGINE
## Rhythm Dictionary â€” Phase A Component
## 2026-02-09 Â· Version: 0.1

---

## PURPOSE

Identifies what MADE each sound in an audio file. Complements the role taxonomy (which identifies what each sound DOES) with production archaeology (which identifies what PRODUCED it).

Sits in Phase A after the spectral roster is built and before full binary extraction. Its output feeds into:
- **Production attribution filter** (third filter in Activation Module) â€” authored vs incidental decisions
- **Equipment Dictionary** cross-referencing â€” matching detected signatures to known gear
- **Composite source detection** â€” evidence for Concealment bridge type

---

## POSITION IN PIPELINE

```
Phase A: Parallel Extraction
â”‚
â”œâ”€ Binary Engine (snapshot) â†’ GenreHypothesis
â”œâ”€ Web Engine â†’ ContextDescriptor (includes instrument roster from credits)
â”‚
â”œâ”€ Genre commit
â”œâ”€ Spectral Roster build â†’ SpectralRoster (8 roles)
â”‚
â”œâ”€ â˜… EQUIPMENT ID ENGINE â˜…          â† NEW: runs here
â”‚   Input:  audio + SpectralRoster
â”‚   Output: EquipmentReport
â”‚   - Per-role synthesis classification
â”‚   - Drum machine vs live drums
â”‚   - Composite source evidence
â”‚   - Overall programmed/organic score
â”‚
â”œâ”€ Structural sampling â†’ BandPresenceMap
â”œâ”€ Shift point identification â†’ ShiftMap
â””â”€ Role trajectory â†’ RoleTrajectory
```

### Why this position?

1. **After spectral roster**: we need to know the roles before classifying what fills them
2. **Before full extraction**: equipment ID informs what measurements matter
   - If drums are programmed â†’ onset CV measurements are water (expected to be near-zero)
   - If bass is FM synthesis â†’ spectral flatness readings have different interpretation
   - If composite sources detected â†’ stereo analysis needs band-separated treatment
3. **Parallel with web engine**: web provides production credits (what gear was used). Equipment ID provides spectral evidence (what gear sounds like it was used). Convergence = high confidence.

---

## INPUT / OUTPUT CONTRACT

### Input

```
EquipmentEngineInput {
  audio:           ndarray         // raw audio (mono or stereo)
  sr:              int             // sample rate
  spectral_roster: SpectralRoster  // from Phase A (which roles are present)
  genre_hypothesis: GenreHypothesis | null  // optional genre context
}
```

### Output

```
EquipmentReport {
  source_type:              "programmed" | "organic" | "hybrid"
  source_confidence:        float
  overall_programmed_score: float     // 0.0â€“1.0

  synthesis_classifications: [        // one per detected role
    {
      role:                 string    // from 8-role taxonomy
      family:               "fm" | "analog_subtractive" | "sample_based" | "wavetable" | "acoustic"
      confidence:           float
      evidence:             string[]
      harmonic_analysis: {
        fundamental_hz:     float
        n_partials:         int
        integer_ratio_score: float    // 1.0 = all integer (acoustic/analog)
        sideband_energy:    float     // high = FM
        odd_harmonic_bias:  float     // high = pulse/square wave
        rolloff_slope:      float     // steep = filtered (analog)
        aliasing_score:     float     // high = low-bitrate sampler
        drift_hz:           float     // high = analog oscillator
      }
    }
  ]
  
  drum_classification: {
    type:                   "drum_machine" | "live_drums" | "hybrid"
    confidence:             float
    per_band_analysis: {
      kick:  RepetitionAnalysis | null
      snare: RepetitionAnalysis | null
      hihat: RepetitionAnalysis | null
    }
  }
  
  composite_evidence: [               // one per analyzed role
    {
      role:                 string
      is_composite:         bool
      confidence:           float
      estimated_sources:    int
      evidence:             string[]
    }
  ]
}
```

---

## FOUR DETECTORS

### 1. Too Clean Detector (runs first, cheapest)

**Question**: Is this sound programmed or organic?

**Method**: Extract transient profiles from repeated events in each spectral region. Measure coefficient of variation across hits for:
- Spectral centroid (shape consistency)
- Peak amplitude (velocity consistency)
- Attack time (onset consistency)
- Decay time (release consistency)

**Thresholds** (v0.1, needs calibration against dictionary):
- Centroid CV < 0.03 â†’ programmed
- Amplitude CV < 0.05 â†’ programmed
- Attack CV < 0.08 â†’ programmed
- 2/3 indicators positive â†’ classified as programmed

**Key insight from Alex**: When synths/drums replicate natural instruments, they betray themselves through mathematically clean velocities and exposures. A real guitarist's palm mutes vary slightly every time. A Fairlight-triggered palm mute sample is identical every time. The variation IS the fingerprint.

**What this gates**: If a region is classified as organic with high confidence, skip synthesis family classification (it's not a synth). This saves compute.

### 2. Drum Classifier

**Question**: Drum machine or live drums?

**Method**: Band-split the audio into kick (30-200Hz), snare (200-3kHz), and hihat (3-16kHz) regions. Run Too Clean detector on each band independently. Aggregate:
- 2/3 bands programmed â†’ drum machine
- 2/3 bands organic â†’ live drums
- Mixed â†’ hybrid (e.g., programmed kick + live cymbals)

**Why drums first**: Drums are the rhythmic foundation. Their programmed/organic classification cascades into interpretation of every temporal measurement in the binary engine. If drums are programmed, grid adherence and onset CV are WATER â€” they tell you about the sequencer, not the music.

### 3. Synthesis Family Classifier

**Question**: FM, analog subtractive, sample-based, wavetable, or acoustic?

**Method**: Harmonic analysis of sustained tones in each spectral role:

| Indicator | FM | Analog Sub | Sample-based | Wavetable | Acoustic |
|-----------|------|-----------|-------------|-----------|----------|
| Sideband energy | HIGH | LOW | varies | MODERATE | LOW |
| Integer ratio | LOW | HIGH | HIGH (inherited) | MODERATE | HIGH |
| Aliasing | LOW | LOW | HIGH (8-bit) | MODERATE (12-bit PPG) | NONE |
| Pitch drift | NONE | PRESENT | NONE | NONE | PRESENT |
| Odd harmonic bias | varies | HIGH (pulse/sq) | varies | varies | LOW (strings) |
| Spectral rolloff | shallow | steep (filter) | varies | varies | natural |

**Current accuracy estimate**: Level 1 (synthesis family) achievable at MEDIUM-HIGH confidence for prominent, relatively isolated sounds. Drops to LOW in dense mixes where multiple synths occupy the same frequency range. This is acceptable â€” web context typically confirms what the binary suggests.

### 4. Composite Source Detector

**Question**: Is this audible element actually multiple blended sources?

**Method**: Three tests on each spectral region:

1. **Cross-band envelope correlation**: Split the region into 8 mel bands. Correlate their amplitude envelopes. Single source â†’ high correlation (same ADSR everywhere). Composite â†’ low correlation (different layers have different envelopes).

2. **Spectral discontinuities**: Analyze the mean spectrum for abrupt slope changes. Where one source "hands off" to another (e.g., DX7 bass body hands off to PPG click at ~500Hz), the spectral slope changes abruptly.

3. **Attack onset spread**: Measure when each frequency band reaches its peak. Single source â†’ all bands peak together. Composite â†’ different bands peak at different times (fast-attack click layer vs slow-attack body layer).

**EWTRTW prediction**: The bass region should show composite evidence (DX7 body + PPG click). The mid region should show composite evidence (Prophet chords + DX7 pianos). The overall composite count should be HIGH.

**Bridge connection**: High composite source count is production-level evidence for Concealment. When nothing has a single identifiable source, the production prevents analytical decomposition â€” which IS concealment.

---

## CALIBRATION PLAN

### Phase 1: EWTRTW validation (immediate)
- Upload EWTRTW audio
- Run engine
- Compare drum classification against known: should detect DRUM_MACHINE
- Compare synthesis classifications against known: should detect FM (DX7 regions) and analog (Prophet regions)
- Compare composite evidence against known: should detect composite bass, composite chords
- Document hits and misses

### Phase 2: Dictionary expansion
- Run on each dictionary song as uploaded
- Cross-reference against web-sourced production credits
- Adjust thresholds based on hit/miss rates
- Build calibration table:

```
| Song | Drums | Expected | Got | Bass Synth | Expected | Got | Composite | Expected | Got |
|------|-------|----------|-----|-----------|----------|-----|-----------|----------|-----|
| EWTRTW | DM | machine | ? | FM+WT | fm+wavetable | ? | HIGH | composite | ? |
| BG | ? | ? | ? | ? | ? | ? | ? | ? | ? |
```

### Phase 3: Reference library
- Each confirmed equipment identification adds to Equipment Dictionary
- Equipment Dictionary becomes a lookup table for future identifications
- Over time: hear DX7 â†’ recognize DX7 â†’ confirm DX7 â†’ know DX7 better

---

## INTERACTION WITH OTHER MODULES

### â†’ Binary Engine
Equipment report informs interpretation of binary measurements:
- `source_type: programmed` â†’ grid adherence, onset CV are WATER
- `drum_type: drum_machine` â†’ timing measurements describe sequencer, not performer
- `synthesis_family: FM` â†’ spectral flatness has different meaning (FM is bright by nature)

### â†’ Activation Module (Production Filter)
Equipment report feeds the third filter directly:
- `source_type: programmed` + production credits say "programmed" â†’ production attribution CONFIRMED (high weight)
- Synthesis family matches credited instruments â†’ AUTHORED (not incidental)
- Composite sources detected â†’ production technique is AUTHORED (deliberate blending)

### â†’ Bridge Module
Equipment report provides evidence for bridge type classification:
- High composite source count â†’ evidence for Concealment
- Programmed sources performing organic roles â†’ evidence for Concealment (machines pretending to be human)
- Live sources in mechanical context â†’ evidence for Contradiction

### â† Web Engine
Web provides the ground truth that calibrates equipment identification:
- Production credits list specific instruments â†’ compare against spectral detection
- When they converge: high confidence
- When they diverge: either the detection is wrong OR the credits are incomplete (common in liner notes)

---

## OPEN QUESTIONS

1. **Stem separation**: Would pre-processing with Demucs or similar improve per-role classification? Probably yes, but adds significant compute cost. Worth testing.

2. **Era priors**: Should genre/era hypothesis influence classification? A 1985 synth-pop track is MORE LIKELY to contain DX7 than a 2024 track. But priors can also blind us. Current approach: classify blind, then check against era expectations.

3. **Velocity curve analysis**: The Prophet T-8's weighted keyboard creates a specific velocity distribution. Could we detect specific instruments from their velocity curves (as recorded via MIDI and rendered through the synth's velocity response)? Theoretical â€” needs investigation.

4. **Multi-instrument separation in dense mixes**: Current approach uses broad frequency bands. A more sophisticated approach would use NMF (non-negative matrix factorization) to separate spectral components before classifying each. This is a known technique in MIR. Worth implementing if band-based analysis proves insufficient.
