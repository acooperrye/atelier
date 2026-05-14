# MODULE: PERCUSSION
## Status: DRAFT — Step 1.5 (shape-first) partially validated against Phoneline (10 Feb 2026). Full pipeline not yet validated end-to-end.
## Origin: Alex's observation that tempo is the most algorithmic axis once resolved

---

## WHAT THIS MODULE DOES

Discovers a song's own percussive timing grid from spectral evidence, generates an expectation map of where specific percussive elements should land, and logs every deviation. The deviations are the data — they're what the Cultural Engine checks for convention violations and what the Interpretive Engine reads for structural meaning.

**This is not a metronome.** The grid is not imposed — it's derived from cross-sectional spectral observation within the song itself. Reverb tails, echoes, chorus effects, fade-ins, swing, humanisation, and deliberate drift all exist in real audio. The grid must be found phenotypically (from what the audio actually shows) before any mathematical model is applied.

**Principle:** Do not use pure maths until you know the math of the song is right. Always look for cross-sectionally spectrally-evidenced intervals that correlate with web content production data.

---

## PERCUSSION IS TONAL

This module isolates percussive events by band and onset, but **percussive elements are not non-tonal**. Every percussive element has pitch content:

- A kick drum has a fundamental pitch. An 808 kick is explicitly tuned — its sub-bass body sits at a specific note. An acoustic kick resonates at a frequency determined by shell diameter and head tension. The pitch of the kick matters harmonically. A kick tuned to the root of the song reinforces the key. A kick tuned to a dissonant interval creates tension whether or not anyone consciously hears the pitch.

- A snare has a resonant body frequency (150-300Hz) that contributes to the tonal character of the midrange. A deep, loose snare colours the 200Hz range differently than a tight, high-pitched one. Snare wires add broadband noise, but the shell tone is a note.

- Hi-hats and cymbals are pitched, just inharmonically. Different alloys, sizes, and profiles produce different spectral peaks. A dark ride cymbal and a bright splash occupy the same "percussive-high" band but sound nothing alike because their spectral peaks are in different places.

- Toms are explicitly pitched and often tuned to intervals across the kit.

**What this means for the module:** The percussion module's onset detection and grid-building work happens in parallel with — not instead of — the tonal analysis happening in the binary engine and feltness module. When this module finds a kick onset at a grid position, the binary engine simultaneously has spectral data about what pitch that kick is at, what its harmonic content looks like, how it relates to the bass line underneath. The percussion module contributes WHERE and WHEN. The other engines contribute WHAT and HOW. Neither is complete alone.

---

## THIS MODULE RUNS IN PARALLEL

The percussion module does not run distinct from any other engine. It runs alongside them, and its outputs cross-reference with theirs. This is especially critical in the bass band.

### The bass-band overlap problem

The kick lives at 30-150Hz. The bass line lives at 30-250Hz. They share the same spectral territory. In the audio, they are superimposed — the bandpass filter that isolates kick energy also captures bass energy, and vice versa.

This means:
- **The percussion module's kick onsets must be cross-referenced against the binary engine's sustained-low (bass) readings.** A sudden energy spike in 30-150Hz could be a kick hit OR a bass note onset. The percussion module flags it as a percussive onset candidate; the binary engine checks if there's sustain after it (bass note) or rapid decay (kick). Together they disambiguate.

- **The feltness module's gesture analysis applies to both.** A kick and a bass note at the same grid position create a compound gesture — the kick's transient attack primes the bass note's sustain (this is the bass-subbass coupling from the feltness module). The percussion module sees the onset; the feltness module reads the full gesture; the binary engine identifies which sources are contributing.

- **808 kicks are both percussive and tonal simultaneously.** An 808 hit has a transient attack (percussive) that blooms into a pitched sub-bass sustain (tonal). The percussion module should log the onset and grid position. The binary engine should log the pitch and sustain duration. The feltness module should read the complete gesture. No single module owns the 808 — it exists at the intersection of all three.

- **Sidechain compression links kick and bass causally.** In many genres, the bass signal is ducked by the kick's onset — the kick's percussive event directly modulates the bass's tonal content. The percussion module sees the kick onset; the binary engine sees the bass amplitude dip; together they identify the sidechain relationship and its depth/release parameters.

### Parallel operation protocol

```
When the percussion module detects an onset in the 30-150Hz band:
  1. Log it as a kick_candidate
  2. Pass the timestamp to the binary engine
  3. Binary engine checks:
     - Is there sustained-low energy AFTER the transient? → bass note co-present
     - Does the transient have a pitched tail (808 bloom)? → hybrid percussive-tonal
     - Is there an amplitude dip in sustained-low at this timestamp? → sidechain
  4. Feltness module receives the onset timestamp and computes the full gesture
     (onset slope, sustain, offset, silence) for the compound kick+bass event
  5. Results recombine: percussion module logs the grid position and deviation status,
     annotated with binary engine's source attribution and feltness module's gesture reading
```

This is not sequential — it's concurrent. The modules share timestamps and pass annotations. The percussion module is the clock; the other engines are the instruments reading from it.

### Beyond bass: other parallel concerns

- **Snare and vocal consonants** share the 2-4kHz range. A hard "T" or "K" in a vocal line can look like a snare transient. Cross-reference with the vocal role from SpectralRoster — if a vocal is expected in this section, check whether the percussive-mid onset aligns with a formant structure (vocal) or a noise burst (snare).

- **Crash cymbals and synth pads** can overlap in the 3-8kHz range. A synth swell and a crash both produce broadband energy in that band. The percussion module flags the onset; the binary engine checks for sustain character (cymbal ring vs pad sustain).

- **Hi-hats and sibilance** ('s' and 'sh' sounds) overlap at 5-12kHz. Same cross-referencing logic applies.

---

## TEMPORAL PRIMACY: WHY THIS MODULE EXISTS

Tempo is the last musical parameter to resolve (requires minimum two beats — one event carries zero tempo information) but the first to become predictive once resolved. This asymmetry is why percussion gets its own module:

- **Pitch** can be extracted from a single event (given sufficient duration).
- **Timbre** can be characterised from a single event.
- **Loudness** can be measured from a single event.
- **Tempo** cannot be extracted from a single event. Period. It requires minimum two events.

But once tempo is established, it generates the strongest expectations of any musical parameter. A listener who knows the BPM and genre can predict the next kick within milliseconds. That prediction — and its confirmation or violation — is the most algorithmic axis in the entire system. The grid is a machine for generating expectations. This module builds the machine, runs the predictions, and logs the results.

---

## DISCOVERY METHOD

### Step 0: The guiding number (Alex, 11 Feb 2026)

Before any audio processing, you already have a tempo and a meter. The BPM is on the Spotify page, the Beatport listing, the production notes, the DJ database. The time signature is overwhelmingly 4/4 in western music — it's at the front of every bar of notation for a reason. This is your first phenotypic data point, and it arrives from the web engine before a single sample is processed.

**The frame is not purely cultural convention.** (Alex, 11 Feb 2026.) The mechanical properties of sound waves constrain what temporal structures are viable. The reason 120 BPM clusters as the most common tempo isn't arbitrary — it's near resting heart rate, near walking cadence, and it's where sub-bass has enough headroom to complete cycles while repeating fast enough to be rhythmic (see feltness module headroom analysis). The reason the 8-bar phrase is the chunking unit isn't arbitrary — at 120 BPM it's ~16 seconds, roughly the window of short-term musical memory and comfortable breath cycle. The guiding number has two legs: cultural convention (BPM from Spotify, genre norms) and acoustic physics (propagation, resonance, physiological coupling). The convention grew around the physics. What humans experience as "this tempo feels right" is the integrated readout of those physical constraints. What the system can see is each constraint individually — spectral flux, IOI distributions, envelope shapes, phase relationships. The vibes are the physics, decomposed.

```
GuidingPrior {
  bpm:              float      // from web context (Spotify, Beatport, production notes, etc.)
  bpm_source:       string     // where it came from
  time_signature:   string     // "4/4" by default for western music, web-confirmed if available
  quarter_note_ms:  float      // 60000 / bpm — the base unit everything ratios back to
  bar_ms:           float      // quarter_note_ms × beats per bar (e.g. 2000ms at 120bpm 4/4)
  phrase_bars:      int        // default 8 — the structural chunking unit
  phrase_ms:        float      // bar_ms × phrase_bars (e.g. 16000ms = 16s at 120bpm)

  // This is the frame — like the grand staff. Treble clef, bass clef,
  // five lines each, a brace. The staff isn't decoration you skip past
  // to get to the notes. The staff is what makes the notes legible.
  // One number, one meter, one frame — and from that, every subsequent
  // relationship becomes parseable. Without it, per-element meters
  // float free with no anchor. With it, every element's IOI is
  // immediately relational: ratio to the quarter note = position
  // on the staff.
  //
  // The per-element meter model doesn't replace this — it refines it.
  // The guiding number is the handle the brain grabs first.
  // It cognitively lowers the barrier of entry so that all further
  // relational information has one thing to hold onto.
  // Agreement between elements and this frame is the schematic backbone.
  // Disagreement is where the findings live.
}
```

The guiding number grounds every subsequent step. When Step 2 derives a kick IOI of 500ms and the guiding number says 120 BPM (quarter = 500ms), that's confirmation — schematic, structural, load-bearing. When Step 4 computes cross-element ratios, they feed back to this number first. The per-element model handles the edge cases (polyrhythm, drift, non-4/4), but the standard metering dominates, and the architecture should reflect that dominance.

### Step 1: Find the hits

For each percussive band (see Element Profiles below), run onset detection within that band only. Do not detect onsets across the full spectrum — that conflates kick transients with hi-hat transients with vocal consonants.

```
Per-band onset detection:
  1. Bandpass filter to element's spectral home
  2. Compute spectral flux within that band
  3. Apply adaptive threshold (local median + k * local std)
  4. Peak-pick above threshold → onset timestamps

Output: raw onset list per band
  e.g. kick_onsets: [0.375, 0.875, 1.375, 1.876, 2.375, ...]
  e.g. hat_onsets:  [0.125, 0.250, 0.376, 0.500, 0.624, ...]
```

**Critical:** These are the measured reality. They will not be perfectly equidistant. They will have jitter from swing, humanisation, audio encoding artefacts, reverb pre-ringing, ghost transients from bleed, etc. That's fine. That's the data.

### Step 1.5: Trace shapes — identify WHAT each event is (NEW — Phoneline, 10 Feb 2026)

Before deriving intervals, classify each onset event by tracing its frequency trajectory through the spectrogram. This step identifies WHAT produced the sound before Step 2 characterises WHEN it occurs.

**Why this step exists:** Step 1 finds events. But in shared frequency bands (especially 30-150 Hz where kick and bass coexist), the onset list contains multiple source types mixed together. If you derive intervals from an unclassified list, different sources smear each other's timing distributions, producing flat phase maps where no pattern emerges. Phoneline demonstrated this failure: 1,434 transient events in the low band included kick, bass synth onsets, snare bleed, and hi-hat leakage. Five magnitude-based methods failed to separate them. Shape-first classification solved it.

**The principle:** Magnitude is relative (depends on mix balance). Shape is intrinsic (depends on source physics). A kick drum sweeps downward because the drum head's tension dissipates after impact. That trajectory persists regardless of amplitude, compression, EQ, or layering. "You don't see a speaker making the kick drum noises but you hear them clear as crystal" — the shape persists through the medium. (Alex Cooper-Rye, 10 Feb 2026.)

```
Per-event shape classification:
  For each onset detected in Step 1:
    1. Extract spectrogram window: onset timestamp → onset + estimated decay
    2. Track peak frequency frame-by-frame through the window
    3. Compute trajectory: direction (up/down/static), speed, bandwidth
    4. Classify:

ShapeClassification {
  onset_timestamp:    float
  band:               string     // which percussive band this was detected in

  trajectory: {
    start_freq_hz:    float      // peak frequency at onset
    end_freq_hz:      float      // peak frequency at decay
    direction:        "downward" | "upward" | "static" | "oscillating" | "broadband"
    sweep_speed_hz_per_ms: float // rate of frequency change
    bandwidth_hz:     float      // spectral width of the event
  }

  classification:     "kick"              // downward sweep, 129-194 Hz → 32-86 Hz
                    | "bass_note"         // static or upward, pitched sustain follows
                    | "snare_bleed"       // broadband spread, no directional trajectory
                    | "808_pitched"       // rapid oscillation between harmonics
                    | "hat_leakage"       // very high start frequency, fast decay
                    | "unclassified"      // doesn't match known shapes

  confidence:         float      // how cleanly the trajectory matches the template
}
```

**Shape templates by source (validated/hypothesised):**

| Source | Direction | Start Hz | End Hz | Speed | Status |
|--------|-----------|----------|--------|-------|--------|
| Kick (electronic) | Downward | 129-194 | 32-86 | Fast (>1 Hz/ms) | VALIDATED (Phoneline) |
| Bass synth onset | Static/upward | Varies | Varies | Slow (<0.5 Hz/ms) | Validated (Phoneline, attack slope classification) |
| Snare bleed (low band) | Broadband | N/A | N/A | N/A | Validated (Phoneline, no directional trajectory) |
| 808 kick (pitched) | Oscillating | Tuned note | Tuned note ± harmonics | Medium | HYPOTHESISED (needs PUTP validation) |
| Acoustic kick | Downward | Higher start (~200+) | Lower end (~40-60) | Medium | HYPOTHESISED (needs live drum validation) |

**After classification:** Pass the classified onset list (with source labels) to Step 2. Per-element intervals are now computed on events of the SAME TYPE, not on a mixed pile.

### Step 2: Derive intervals from the hits (not the other way around)

From each onset list, compute inter-onset intervals (IOIs):

```
kick_iois: [0.500, 0.500, 0.501, 0.499, 0.500, ...]
hat_iois:  [0.125, 0.126, 0.124, 0.125, 0.124, ...]
```

Then find the **modal interval** — the most common IOI (within a tolerance window of +/- 5%). This is the element's own pulse, as evidenced by the audio. Don't convert it to BPM yet. Don't name it "quarter note" or "sixteenth." It's just an interval in milliseconds.

```
kick_modal_ioi: 500ms
hat_modal_ioi:  125ms
snare_modal_ioi: 1000ms
```

Each element now has its own meter. That's the unit of analysis. Not a shared grid — a per-element interval.

### Step 3: Build per-element meters

Each element gets its own complete meter description derived from its own IOIs:

```
ElementMeter {
  element:          string     // "kick", "snare", "hat_closed", etc.
  band:             [float, float]  // Hz range where it was detected

  // Core timing — derived from audio, not assumed
  modal_ioi_ms:     float      // most common interval between this element's onsets
  ioi_confidence:   float      // how tight the IOI distribution is (low variance = high confidence)
  anchor:           float      // timestamp of this element's first confirmed onset
                               // (not t=0, not a shared downbeat — THIS element's first hit)

  // The element's own cycle
  // The bar is the byte. The 8-bar phrase is the word. (Alex, 11 Feb 2026)
  // A kick doesn't just repeat every bar — its structural variation
  // (where it doubles, where it drops, where the fill lands) repeats
  // over 8 bars. The 8-bar phrase is the default cycle_length hypothesis
  // for the same reason 4/4 is the default meter: it's the schematic
  // chunking unit of western music. The brain holds one 8-bar phrase
  // and diffs against it.
  //
  // cycle_length is measured in modal_ioi positions, not bars.
  // So a kick hitting on quarter notes at 120 BPM in an 8-bar phrase:
  //   modal_ioi = 500ms, 4 beats per bar, 8 bars = 32 positions.
  //   cycle_length = 32
  //   cycle_ms = 16000ms = 16s
  //
  // Discover the actual cycle by autocorrelating the onset pattern
  // against itself at multiples of the bar length. The highest
  // autocorrelation peak is the true cycle. Default hypothesis: 8 bars.

  cycle_length:     int        // how many modal_ioi positions before the pattern repeats
                               // default hypothesis: 8 bars worth of positions
                               // (confirmed by onset pattern autocorrelation)
  cycle_ms:         float      // cycle_length * modal_ioi_ms

  // The element's onsets as positions within its own cycle
  // Position 0 = anchor, position 1 = anchor + modal_ioi_ms, etc.
  cycle_pattern: [
    {
      position:     int        // 0-indexed within cycle
      timestamp:    float      // actual measured onset time (first occurrence)
      status:       "confirmed"          // onset detected here
                  | "expected_absent"    // gap that's part of the pattern
                  | "ghost"             // low-amplitude, on-meter, band-clean (three-part test)
                  | "echo_candidate"    // low-amplitude, off-meter

      amplitude:    float      // relative to this element's peak
      jitter_ms:    float      // deviation from ideal position (per-instance avg)

      // Parallel engine annotations (filled by binary/feltness, not this module)
      tonal_annotation: {
        pitch_hz:       float | null  // if binary engine detected pitch
        bass_copresent: bool          // is sustained-low also active?
        sidechain:      bool          // did sustained-low duck?
        gesture:        string | null // feltness module's gesture classification
      }
    }
  ]

  // Deviations from the cycle across the song's duration
  // (positions where the actual audio breaks from the established pattern)
  deviations: [
    {
      occurrence:   int        // which repetition of the cycle (0-indexed)
      position:     int        // which position within the cycle
      type:         "unexpected_absent"  // pattern says hit, audio says no
                  | "unexpected_present" // pattern says gap, audio says hit
                  | "displaced"         // hit present but >20ms off expected time
                  | "fused"            // merged with adjacent (spacing < min viable)
                  | "fill"             // transition zone, pattern break expected
                  | "amplitude_shift"  // hit present but notably louder/quieter than pattern

      amplitude:    float
      jitter_ms:    float
      section:      string     // structural section (from BandPresenceMap)
    }
  ]

  // Summary stats
  pattern_regularity: float    // 0-1, how consistent the cycle is across repetitions
  swing_ms:           float    // systematic jitter bias on specific positions
  structural_variation: {
    per_section: [{ label: string, fill: float, regularity: float }]
  }
}
```

**Why per-element meters instead of a shared grid:** Not "instead of" — "underneath." The standard metering (4/4, web-sourced BPM) dominates in western music and is the guiding prior from Step 0. Per-element meters give you precision and handle edge cases, but for 95% of the catalogue, every element's modal_ioi will ratio cleanly back to the guiding number. That agreement is the boring, load-bearing backbone. The per-element model ensures you can still process the other 5% without the architecture breaking.

For downstream processing, the per-element representation is also computationally tight. To reproduce a track, you replay each ElementMeter at its own interval with its own deviations applied. To compare elements, you compute ratios. To detect polyrhythm, you look for non-integer ratios. All of it feeds back to the guiding number.

### Step 4: Cross-reference element meters against each other and the guiding number

Once every element has its own meter, compute the relationships — first against the guiding prior, then pairwise:

```
MeterRelationship {
  song_id:          string

  // Step 0's guiding number — the gravity well
  guiding_bpm:      float      // from web context
  guiding_quarter_ms: float    // 60000 / guiding_bpm

  // Each element's ratio to the guiding number
  // This is the FIRST comparison — before pairwise ratios
  guiding_ratios: [
    {
      element:      string     // e.g. "kick"
      modal_ioi_ms: float      // e.g. 500ms
      ratio_to_quarter: float  // modal_ioi / guiding_quarter_ms
                               // e.g. 1.0 = quarter, 0.5 = eighth, 0.25 = sixteenth
      ratio_clean:  bool       // does it snap to a standard subdivision?
                               // (1, 1/2, 1/3, 1/4, 1/6, 1/8, 2, 3, 4, etc.)
      subdivision_name: string | null  // if ratio_clean: "quarter", "eighth", etc.
                                        // if not clean: null (non-standard)
    }
  ]

  // Pairwise ratios between elements
  pairwise_ratios: [
    {
      element_a:    string
      element_b:    string
      ioi_ratio:    float      // e.g. 4.0 (kick IOI is 4x hat IOI)
      ratio_clean:  bool       // integer or simple fraction?
      anchor_offset_ms: float  // time difference between anchors
    }
  ]

  // Derived: do all elements agree with each other AND with the guiding number?
  common_pulse_ms:   float | null   // GCD of all modal IOIs, if one exists
  common_pulse_confidence: float
  guiding_agreement: bool           // does common_pulse ratio cleanly to guiding BPM?

  // The three possible outcomes:
  // 1. guiding_agreement = true, all ratio_clean = true
  //    → Standard metering. The schematic frame holds. 95% of songs.
  //    → Every element is on a standard subdivision of the web-sourced BPM.
  //
  // 2. guiding_agreement = true, some ratio_clean = false
  //    → Mostly standard but one or more elements are doing something unusual.
  //    → The unusual elements are the findings.
  //
  // 3. guiding_agreement = false
  //    → Either the web BPM is wrong, the song is polymetric,
  //      or there's a tempo change. Per-element meters still work.
  //      The guiding number needs revision or the song is genuinely
  //      outside standard metering.
}
```

All ratios and intervals feed back to the original guiding number first and foremost. The per-element model is the fine structure; the web-sourced BPM and time signature are the frame it hangs on.

---

## ELEMENT PROFILES

Each profile defines what the system looks for, where, and what's realistic.

### Physical constraints (from feltness module headroom analysis)

The minimum viable event spacing is the point below which the sound can no longer function as a discrete percussive event — it either fuses into a tone/drone (high end) or can't complete enough cycles to be identifiable (low end).

| Element | Min viable spacing | Reasoning |
|---------|--------------------|-----------|
| Kick (sub-bass component) | ~100ms | Needs 2-3 cycles at 30-50Hz to register as pitched thump |
| Kick (attack component) | ~30ms | Attack transient is broadband, resolves fast |
| Snare | ~50ms | Body resonance at 150-300Hz needs a few cycles |
| Clap | ~40ms | Layered micro-transients, but composite resolves fast |
| Hi-hat closed | ~15ms | High frequency, minimal sustain needed |
| Hi-hat open | ~80ms | Needs sustain/decay tail to read as "open" |
| Crash/ride | ~100ms | Needs ring to distinguish from hat |
| Rim shot | ~30ms | Pure transient, minimal sustain |

Below these spacings, elements fuse. This is the physics floor.

### The Stupid Ceiling

At the other end: at what point does the fill density become perceptually absurd?

```
StupidCeiling {
  // Genre that deliberately maxes out: breakcore
  // Breakcore parameters represent the practical upper bound
  // of what is still intentional rhythm (vs noise/texture)

  // In per-element meter terms: these are the minimum modal_ioi_ms
  // values before the element stops functioning as percussion
  breakcore_reference: {
    kick_min_ioi:   117ms   // at 170 BPM, 75% of sixteenth positions filled
                            // → avg 117ms between hits
                            // → right at the sub-bass min viable spacing (100ms)
                            // i.e. breakcore kick is operating AT the physics floor

    snare_min_ioi:  147ms   // 60% of sixteenth positions at 170 BPM

    hat_min_ioi:    49ms    // 90% of thirtysecond positions at 170 BPM
                            // → still above hat min viable (15ms) but dense

    // When an element's modal_ioi_ms drops below its min viable spacing,
    // or its cycle has so few gaps that adjacent hits overlap,
    // the element has fused — it's now tonal/textural, not rhythmic.
    // Above breakcore rates, you're not doing rhythm anymore.
    // That's a different analysis mode.

    // Fusion test: if modal_ioi_ms < (2 × min_viable_spacing),
    // flag as "percussive fusion"
    // (see: Circle Pit amen snares at 5.7 hits/sec → 175ms IOI
    //  → HPSS reads 70.8% harmonic. Percussion became drone.)
  }
}
```

### Element profiles by genre

These are **expected ranges**, not rules. They narrow the search space and define what "unexpected" means.

```
ElementProfile {
  element:            string
  spectral_home:      [float, float]   // Hz — where to look
  envelope_signature: string           // what the onset shape looks like

  genre_expectations: {
    [genre_id]: {
      typical_subdivision: string      // what grid level it usually lands on
      fill_range:         [float, float]  // min-max % of those positions filled
      structural_notes:   string       // how it varies across song sections
    }
  }
}
```

#### KICK

```
spectral_home: [30, 150]   // sub-bass body + low-mid attack
envelope: transient with variable sustain (808 bloom = long, acoustic = short)
tonal_note: kick pitch matters — 808s are tuned, acoustic kicks resonate.
            Pitch data comes from binary engine, not this module.

genre_expectations:
  four_on_floor (house/techno/disco):
    subdivision: quarter
    fill: [0.95, 1.00]     // it's literally every beat, that's the genre
    structural: "drops out in breakdowns, returns at drops"

  dnb:
    subdivision: eighth
    fill: [0.25, 0.50]     // syncopated, not on every beat
    structural: "pattern mutates across 4-8 bar phrases"

  hip_hop:
    subdivision: eighth
    fill: [0.30, 0.60]     // boom-bap patterns, often swung
    structural: "consistent pattern, may simplify in verse"

  trap:
    subdivision: sixteenth (808 rolls) / quarter (single hits)
    fill: [0.15, 0.70]     // huge range — sparse single hits to 808 rolls
    structural: "rolls in hooks/drops, sparse in verses"

  breakcore:
    subdivision: sixteenth
    fill: [0.40, 0.75]     // dense, often mangled break samples
    structural: "pattern may change every bar or half-bar"

  rock:
    subdivision: quarter / eighth
    fill: [0.25, 0.50]     // standard kick patterns
    structural: "doubles up in choruses, sparse in verses"
```

#### SNARE / CLAP

```
spectral_home: [150, 4000]  // body at 150-400, crack/wire at 2k-4k
envelope: sharp transient + short noise tail (snare) or layered transients (clap)
tonal_note: snare body resonance at 150-300Hz is pitched. Deep vs tight snare
            changes the tonal character of the midrange.

genre_expectations:
  most_genres:
    subdivision: quarter (on 2 and 4)
    fill: [0.20, 0.30]     // typically 2 hits per bar in 4/4
    structural: "rolls or fills at section boundaries"

  dnb:
    subdivision: eighth / sixteenth
    fill: [0.25, 0.60]     // breakbeat patterns, heavy snare use
    structural: "snare carries the break rhythm"

  trap:
    subdivision: quarter (main) + sixteenth (rolls at phrase ends)
    fill: [0.15, 0.50]     // sparse main hits with occasional rolls
    structural: "triplet rolls in transitions"

  breakcore:
    subdivision: sixteenth / thirtysecond
    fill: [0.30, 0.60]     // can approach tonal fusion (Circle Pit)
    structural: "may be continuous or absent — rarely steady"
```

#### HI-HAT (CLOSED)

```
spectral_home: [5000, 16000]
envelope: very short transient, minimal sustain
tonal_note: inharmonic pitch from alloy/size. Dark vs bright hats are
            spectrally distinct despite both being "percussive-high."

genre_expectations:
  house_techno:
    subdivision: eighth / sixteenth
    fill: [0.50, 1.00]     // driving hats, often every offbeat eighth
    structural: "consistent, may filter or open in builds"

  trap:
    subdivision: thirtysecond (rolls) / sixteenth (standard)
    fill: [0.30, 0.90]     // signature trap hat rolls
    structural: "rolls accelerate toward section climaxes"

  hip_hop:
    subdivision: sixteenth
    fill: [0.40, 0.75]     // swung, velocity-varied
    structural: "consistent groove pattern"

  dnb:
    subdivision: sixteenth / thirtysecond
    fill: [0.50, 0.85]     // fast, driving
    structural: "may thin out in half-time sections"

  rock:
    subdivision: eighth
    fill: [0.80, 1.00]     // steady eighth note pulse
    structural: "opens to ride in choruses"

  breakcore:
    subdivision: thirtysecond
    fill: [0.50, 0.90]     // dense, often pitched or filtered
    structural: "may be absent or continuous — binary"
```

#### HI-HAT (OPEN)

```
spectral_home: [3000, 14000]  // broader, more sustain than closed
envelope: transient + 80-200ms decay tail
tonal_note: longer sustain means more perceptible pitch character than closed hat.

genre_expectations:
  most_genres:
    subdivision: eighth (offbeats)
    fill: [0.05, 0.25]     // punctuation, not continuous
    structural: "more frequent in choruses/high-energy sections"

  disco_funk:
    subdivision: eighth (every offbeat)
    fill: [0.40, 0.50]     // the disco offbeat hat IS the groove
    structural: "relentless, defines the genre"
```

---

## DEALING WITH REAL AUDIO (things that will mess you up)

### Reverb tails and room sound
A snare with 200ms of reverb tail will produce spectral energy well past its grid position. The onset detector should be looking at the **attack**, not the sustain. Spectral flux (rate of change) catches the transient; raw energy level catches the tail. Use flux for onset detection, not energy.

### Echo and delay effects
A single snare hit through a dotted-eighth delay will produce onsets at the original position AND at positions that are NOT on the grid (dotted eighth = 0.75 beats, which doesn't land on any standard subdivision). The echoed hits will typically be lower amplitude. The amplitude gate (e.g. 40% of peak) flags low-amplitude onsets as candidates for further discrimination — but the gate alone does not determine whether a quiet hit is an echo or a ghost note. See Ghost Note Discrimination below.

### Ghost note discrimination (Alex, 11 Feb 2026)

Ghost notes are quiet, deliberate hits that are part of the groove. Echoes are artefacts of delay processing. Both are low-amplitude. The amplitude gate catches both. Telling them apart requires a three-part test, applied in order:

**Part 1: Web engine prior.** Before touching the audio, check whether ghost notes are expected for this genre and production context. If the web engine returns genre=hip-hop and production credits mention a live drummer or a producer known for ghost note programming (Dilla, Questlove, 9th Wonder, etc.), the prior is high. If it's quantised four-on-the-floor techno with a drum machine credit, the prior is near-zero. The prior determines whether to run parts 2-3 at all — don't go looking for ghost notes in music that doesn't use them.

**Part 2: Grid-locked gate lowering.** Lower the amplitude gate, but ONLY on grid positions that the module has already confirmed exist. The grid is already built by this point — Step 5 has mapped the element's confirmed onsets to grid positions. Now re-scan the same band at a lower amplitude threshold (e.g. 15-40% of peak instead of 40%), but only at the specific subdivision positions that fall ON the established grid. This is the critical distinction: ghost notes land on grid positions (sixteenths, thirty-seconds between the main hits). Echoes land at delay-time offsets from source hits, which are almost never clean grid positions (dotted eighths, ping-pong intervals, feedback decay — all off-grid). If a low-amplitude onset is found precisely at a grid subdivision, it's a ghost candidate. If it's between grid positions, it's an echo candidate.

**Part 3: Spectral isolation confirmation.** For each ghost candidate found in Part 2, check whether the element's band is spectrally clean at that timestamp. If the ONLY energy in the snare band (150-4000Hz) at that grid position is the quiet hit — nothing else bleeding in from adjacent elements, no sustained energy from a pad or vocal, no reverb tail from a previous louder hit still ringing — then confirm it as a ghost note. The logic: a ghost note is a deliberate sound placed at a deliberate time. At the moment it occurs, it should be the only thing happening in its band, because the producer put it there in a space where it can be heard (even quietly). An artefact, by contrast, tends to arrive on top of other energy — reverb tails overlap with subsequent sounds, delay echoes stack on top of ongoing signal.

```
GhostNoteTest {
  // Applied to each low-amplitude onset candidate after grid is built

  web_prior:        float    // 0-1, from genre + production context
                             // 0 = ghost notes not expected
                             // 1 = ghost notes are defining feature of this style
  prior_threshold:  0.3      // below this, don't bother with parts 2-3

  grid_locked:      bool     // is this candidate at a confirmed grid position?
                             // true → ghost candidate
                             // false → echo candidate

  band_clean:       bool     // is the element's spectral band clean at this timestamp?
                             // true → nothing else present, confirms deliberate placement
                             // false → bleed/overlap present, likely artefact

  verdict:          "ghost"          // prior > threshold, grid_locked, band_clean
                  | "echo_candidate" // not grid_locked
                  | "bleed"          // grid_locked but band not clean
                  | "ambiguous"      // mixed signals, flag for manual inspection
}
```

### Chorus/flanger/phaser on percussion
These modulate the spectral content cyclically, which can produce phantom flux peaks that look like onsets. Cross-reference against other bands — a real percussive onset will produce correlated energy changes across its full spectral home. A chorus artefact will modulate within a narrow sub-band.

### Swing and humanisation
Systematic offset from the grid on specific beats (usually offbeats). This is not error — it's feel. The `snap_error` field in the ElementGridMap captures this. If offbeat positions consistently show +10-30ms late arrival, that's swing. Report it as `swing_amount`, don't try to correct for it.

### Tempo drift
Live recordings and some deliberate electronic production drift in tempo across the song. The grid should not be one fixed BPM applied to the whole track. Re-derive the local IOI modal interval per section (or per 8-16 bars) and allow the grid to flex. Flag the drift rate.

```
TempoDrift {
  method: "fixed" | "per_section" | "continuous"
  // fixed: one BPM for whole song (most electronic music)
  // per_section: recalculated per structural section
  // continuous: sliding window IOI estimation (live recordings)

  drift_rate: float  // BPM change per minute (0 for fixed)
  confidence: float
}
```

### Transition fills
Drum fills at section boundaries deliberately break the element's established cycle — that's the point. Expect pattern_regularity to drop and deviation count to spike in the 1-2 cycles before a section change. Use the ShiftMap from Phase A to anticipate where these will be and don't flag deviations in those zones as errors.

---

## DEVIATION LOG

The output of the full grid comparison. Every position on the grid, for every element, gets a status. The deviations are the data.

```
DeviationLog {
  song_id:    string
  bpm:        float

  deviations: [
    {
      element:        string
      bar:            int
      beat:           float
      subdivision:    string
      type:           "unexpected_absent"    // should be there, isn't
                    | "unexpected_present"   // shouldn't be there, is
                    | "ghost"               // present but at <40% peak amplitude
                    | "displaced"           // present but >20ms off grid
                    | "fused"              // element at this position has merged with adjacent
                    | "echo_candidate"     // likely delay/echo artefact
                    | "fill"               // in a transition zone, pattern breaks expected

      amplitude:      float    // 0-1 relative to element peak
      snap_error_ms:  float    // how far off grid
      section:        string   // which structural section this falls in
      context:        string   // adjacent positions' statuses for pattern inference
    }
  ]

  // Aggregated per element
  element_summaries: [
    {
      element:               string
      total_expected:        int      // grid positions where genre says it should appear
      total_confirmed:       int      // actually present
      total_unexpected_absent: int    // missing
      total_unexpected_present: int   // extra
      fill_vs_expected:      string   // "within_range" | "sparse" | "dense" | "fused"
      regularity_score:      float    // 0-1, how close to a repeating pattern
      swing_amount_ms:       float    // systematic offset

      // The money question: WHY is it deviating?
      deviation_hypothesis:  "genre_convention"  // this is normal for the genre
                           | "structural_variation" // section-dependent (e.g. chorus doubles)
                           | "artistic_choice"  // deliberate pattern break
                           | "production_artefact" // echo, bleed, processing
                           | "possible_error"  // unclear intent
                           | "fusion_event"    // element has crossed stupid ceiling
      // Note: hypothesis is generated, not ground truth. Requires web/somatic validation.
    }
  ]
}
```

---

## INTEGRATION WITH EXISTING ARCHITECTURE

### Feeds from:
- **Phase A scout pass** — initial tempo estimate
- **SpectralRoster** — which percussive roles to look for and where
- **BandPresenceMap / ShiftMap** — section boundaries, where to expect fills/transitions
- **Genre fingerprint** — expected fill ranges, subdivisions, structural variation
- **Web engine** — production credits, confirmed instrumentation, BPM confirmation

### Feeds into:
- **Binary engine** — onset timestamps, per-band IOIs, grid-aligned element positions
- **Cultural engine** — deviation log for convention violation detection
- **Feltness module** — gesture analysis (onset slope, sustain, offset per element per hit)
- **Interpretive Engine** — pattern deviations as potential bridge-type signals
- **Activation layer** — fill percentages and deviation types as scorable axes

### Receives from (parallel operation):
- **Binary engine** — pitch data at percussion onsets, sustained-low presence, source attribution
- **Feltness module** — gesture classification for each percussive event
- **Equipment engine** — machine identification (is this a 909 hat? an 808 kick? a live kit?)

### Relationship to SpectralRoster roles:
The three percussive roles in SpectralRoster (percussive-low, percussive-mid, percussive-high) map to element profiles here:

```
percussive-low  → kick
percussive-mid  → snare, clap, rim
percussive-high → hat_closed, hat_open, crash, ride, shaker
```

This module refines what SpectralRoster can say about percussive roles by adding temporal structure. SpectralRoster says "there is a percussive-low element at 30-150Hz." This module says "it hits at positions 1, 3, 5, 7 of every bar at eighth-note resolution, with 43% fill, 12ms swing, it drops out in the bridge, the kick is pitched at E1, and the bass ducks 6dB at every onset."

---

## OPEN QUESTIONS

1. ~~**Polyrhythm.**~~ **RESOLVED (Alex, 11 Feb 2026).** Per-element meters handle this natively. Each element has its own IOI. If two elements have a non-integer ratio (e.g. 3:4), that's polyrhythm — visible directly in the MeterRelationship ratios. No special handling needed because the model never assumed a shared grid in the first place. The `ratio_clean` flag in MeterRelationship marks whether each pair shares a simple integer ratio or not.

2. ~~**Non-4/4 time.**~~ **RESOLVED (Alex, 11 Feb 2026).** Per-element meters eliminate the problem entirely. Each element has its own IOI in milliseconds, its own cycle length, its own anchor. No subdivision names needed. Cross-element relationships are expressed as ratios, not as positions within a shared bar. Time signatures are derived bottom-up as the GCD of element IOIs (if one exists), not assumed top-down. Waltz, 6/8, 5/4, 7/8, polymetric — all handled natively because the model never assumes a meter in the first place.

3. **Sample-chopped breaks.** Breakcore and jungle chop and rearrange breakbeats. The original break has a grid; the chopped version may not. Individual hits land at positions that reference the original break's feel while violating the song's own grid. This may look like "unexpected_present" everywhere when it's actually a deliberate resequencing.

4. ~~**Ghost notes and velocity layers.**~~ **RESOLVED (Alex, 11 Feb 2026).** Three-part test: (1) web engine prior — is this genre/production context known for ghost notes? (2) grid-locked gate lowering — only look for quiet hits at confirmed grid positions, not between them (echoes are off-grid, ghosts are on-grid), (3) spectral isolation — confirm the band is clean at that timestamp, nothing else bleeding in. See "Ghost Note Discrimination" section above.

5. **Continuous percussion (shakers, tambourines, maracas).** These don't have discrete onsets in the same way — they're textural, filling space between beats. They may register as 100% fill at very high subdivisions, which is normal, not fused. Need a "continuous_texture" element type distinct from discrete hits.

6. **Tonal interaction between kick and key.** When the kick is pitched (808, tuned acoustic), does its pitch relationship to the song's key affect the deviation log? A kick tuned to the root on beat 1 is different from a kick tuned to the root on every beat — the latter reinforces, the former punctuates. This is tonal data from the binary engine annotating temporal data from this module. The question is where that annotation lives and who reads it.

---

*Module created: 11 February 2026*
*Step 1.5 (shape-first identification) added: 10 February 2026, validated on Phoneline.*
*Status: Draft spec. Step 1.5 partially validated. Full pipeline not yet validated end-to-end.*
*Separated from percussive-grid-discovery.md (working draft) for independent development.*
