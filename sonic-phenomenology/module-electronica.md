# ELECTRONICA MODULE
## Rhythm Dictionary â€” Component Spec
## 2026-02-08 Â· Version: independent

---

## PURPOSE

Genre-triggered analysis module that activates when genre commit returns electronica or its subgenres. Handles the fundamental analytical inversion where production IS composition â€” the interesting questions concern synthesis, processing, and spectral sculpting rather than instrumental performance.

Receives fusion flags and low-legibility findings from the standard pipeline and runs recovery techniques that exploit electronica's structural regularities (quantized grid, mechanical periodicity, predictable arrangement patterns) to extract meaningful data where the generic pipeline reports degraded confidence.

Can be updated without touching any other component.

---

## TRIGGER CONDITION

```
if (committed_genre.genre_id IN electronica_genre_set) {
  activate electronica module
}

electronica_genre_set: [
  "electronica",
  "edm",
  "house",
  "techno",
  "drum_and_bass",
  "dubstep",
  "trance",
  "ambient_electronic",
  "idm",
  "synthwave",
  "industrial",
  "glitch",
  "future_bass",
  "uk_garage",
  "breakbeat"
  // expanded as genre baselines grow
]
```

Activation is binary â€” either this module runs or it doesn't. No partial activation. If the genre is electronic-adjacent but primarily another genre (e.g., synth-pop, industrial rock), the module does NOT activate. Those genres get standard pipeline treatment with lower legibility expectations.

---

## INPUT

```
ElectronicaModuleInput {
  // From standard pipeline (already computed)
  audio_file:         File
  committed_genre:    GenreCommitment
  spectral_roster:    SpectralRoster
  band_presence_map:  BandPresenceMap
  shift_map:          ShiftMap
  role_trajectories:  RoleTrajectory[]
  tempo:              float               // from Phase A snapshot
  grid_adherence:     float               // from Phase A snapshot

  // Fusion flags that triggered interest
  fusion_zones: [
    {
      bands_involved:   string[]
      roles_implicated: string[]
      legibility:       float
      section_labels:   string[]          // where the fusion occurs
    }
  ]
}
```

---

## PROCESS

### 1. Grid Lock

Confirm tempo and establish beat grid to sample-level precision. Electronica's mechanical regularity makes this trivially accurate â€” quantized production means the grid IS the structural truth.

```
GridLock {
  tempo_bpm:          float               // confirmed, high confidence
  beat_interval_ms:   float               // derived
  bar_interval_ms:    float               // derived (assumes 4/4 unless web says otherwise)
  grid_confidence:    float               // should be >0.95 for electronica
  time_signature:     string              // from web or inferred
}
```

### 2. Tempo-Locked Spectral Subtraction

For each fusion zone, exploit grid periodicity to separate fused roles.

**Principle:** Percussive elements in electronica are quantized to the grid. Sustained elements are continuous. Sample the fusion band ON beat versus BETWEEN beats â€” the difference isolates the percussive contribution. The residual is the sustained element.

```
For each fusion_zone:
  1. Identify beat positions within the fusion zone's time range
  2. Sample fusion band energy at beat onset (Â±10ms window)
  3. Sample fusion band energy at beat midpoint (maximum distance from any beat)
  4. Difference = percussive contribution estimate
  5. Midpoint reading = sustained element estimate (with percussive bleed subtracted)

Output:
TempoSubtraction {
  fusion_zone:        string              // reference to input fusion zone
  on_beat_energy:     float
  off_beat_energy:    float
  percussive_estimate: float              // on_beat - off_beat
  sustained_estimate:  float              // off_beat (adjusted)
  separation_confidence: float            // how clean was the subtraction
  
  // If separation_confidence is high, individual role readings become available
  recovered_roles: [
    {
      role:           string
      intensity:      float
      envelope:       string              // recovered from temporal profile
    }
  ]
}
```

### 3. Spectral Neighbor Triangulation

When fusion prevents direct measurement in one band, examine adjacent bands where each role appears individually.

```
For each fusion_zone:
  1. From SpectralRoster, identify spectral_home of each implicated role
  2. Check BandPresenceMap for adjacent bands where each role is solo
  3. Compare solo-band characteristics against fusion-band behavior
  4. Attribute fusion-band energy proportionally based on neighbor evidence

Output:
NeighborTriangulation {
  fusion_zone:        string
  neighbor_evidence: [
    {
      role:           string
      solo_band:      string              // where this role appears alone
      solo_intensity: float
      solo_envelope:  string
      inferred_contribution: float        // estimated share of fusion energy
    }
  ]
  triangulation_confidence: float
}
```

### 4. Sequence Pattern Detection

For fusion zones where subtraction and triangulation are insufficient, attempt to identify repeating patterns that reveal the element sequence.

```
For each unresolved fusion_zone:
  1. Using confirmed tempo, divide fusion zone into beat-aligned segments
  2. Look for periodic energy patterns (every N beats, every bar, every 2 bars)
  3. Map detected periodicities against known electronica arrangement conventions
     (kick every beat, snare every 2nd beat, hi-hat subdivisions, etc.)
  4. Subtract identified periodic components sequentially

Output:
SequenceDetection {
  fusion_zone:        string
  detected_patterns: [
    {
      period_beats:   float               // e.g., 1.0 = every beat, 0.5 = 8th notes
      energy_profile: float[]             // energy shape within one period
      likely_role:    string              // best match from roster
      confidence:     float
    }
  ]
  residual_energy:    float               // what's left after all patterns subtracted
  residual_role:      string | null       // if identifiable
}
```

### 5. Production Finding Assembly

Whether or not separation succeeds, compile findings about what the production is doing. This is the module's primary analytical contribution â€” in electronica, production decisions ARE the artistic content.

```
ProductionFindings {
  song_id:            string
  
  fusion_findings: [
    {
      zone:           string
      separation_achieved: bool
      separation_method:   "tempo_subtraction" | "neighbor_triangulation" | 
                           "sequence_detection" | "none"
      recovered_data:      object | null
      
      // The finding that persists regardless of separation success
      production_observation: string
      // e.g., "deliberate low-end fusion between kick and bass â€” 
      //         single sculpted texture rather than two independent sources"
      bridge_relevance:      "high" | "medium" | "low"
    }
  ]
  
  // Electronica-specific structural observations
  grid_observations: {
    swing_amount:       float             // 0 = perfect grid, >0 = humanized
    grid_breaks:        timestamp[]       // where the grid deliberately breaks
    tempo_automation:   bool              // does tempo change?
    polyrhythm:         bool              // multiple competing grids?
  }
  
  // Synthesis/processing observations (from spectral behavior)
  spectral_observations: {
    filter_sweeps:      FilterSweep[]     // detected from slope data in BandPresenceMap
    resonance_peaks:    ResonancePeak[]   // sharp spectral peaks suggesting filter resonance
    sidechain_detected: bool              // rhythmic ducking pattern in sustained elements
    sidechain_rate:     float | null      // if detected, what's the pump rate
    stereo_automation:  bool              // panning/width changes over time
  }
}

FilterSweep {
  band:               string
  direction:          "high_to_low" | "low_to_high"
  start_section:      string
  duration_estimate:  float               // from slope expansion
}

ResonancePeak {
  frequency_hz:       float
  section:            string
  q_estimate:         "narrow" | "medium" | "wide"
}
```

---

## OUTPUT

```
ElectronicaDescriptor {
  song_id:            string
  module_version:     string
  
  // Recovery results â€” feed back into StructuralDescriptor
  recovered_readings: ElementReading[]    // any elements rescued from fusion zones
  
  // Production findings â€” feed forward to Bridge
  production_findings: ProductionFindings
  
  // Adjusted legibility â€” after recovery, legibility may improve
  adjusted_legibility: LegibilityEstimate
  
  // Metadata
  grid_lock:          GridLock
  techniques_applied: string[]            // which recovery methods ran
  
  // Summary flag for downstream consumers
  production_is_composition: true         // always true for electronica
  // This flag tells the Bridge to treat production observations
  // as primary artistic findings, not technical background
}
```

---

## INTEGRATION POINTS

### Reads from:
- Standard pipeline outputs (SpectralRoster, BandPresenceMap, ShiftMap, RoleTrajectory)
- Shared Protocol (Element Registry, Genre Baselines)
- Phase A snapshot data (tempo, grid adherence)

### Writes to:
- **Binary Engine** (via recovered_readings): rescued element values that the standard pipeline couldn't extract. These merge into StructuralDescriptor as supplementary readings with source attribution.
- **Activation Layer** (via production_findings): production observations arrive as structural data, processed through the three filters like any other finding. The `bridge_relevance: "high"` flag doesn't bypass filtering â€” it just ensures these findings get a fair hearing.
- **Bridge Module** (via `production_is_composition` flag): tells the Bridge that production decisions are the primary artistic medium for this track. Shifts interpretive weight from "what instruments are playing" to "what the production is doing to sound."

### Does not touch:
- Shared Protocol (no new elements, no schema changes)
- Web Engine (doesn't need additional web data beyond what's already gathered)
- Meta-dimensions (production findings map onto existing dimensions â€” no new ones needed)

---

## POSITION IN PIPELINE

```
Phase A standard:  Snapshot â†’ Web â†’ Genre Commit â†’ Roster â†’ Sampling â†’ ShiftMap
                                          â”‚
                                          â”œâ”€â”€ IF electronica: activate module
                                          â”‚
Phase A electronica:                      â–¼
                              Grid Lock â†’ Fusion Recovery â†’ Production Assembly
                                          â”‚
                                          â–¼
Phase B:           Full Binary (receives recovered readings) â†’ Activation â†’ Bridge
```

The module runs AFTER the standard cheap pass but BEFORE the full binary pass. It occupies a new micro-phase between Phase A and Phase B â€” call it **Phase A.5** â€” where genre-specific preprocessing enriches the data before expensive computation begins.

---

## FUTURE EXPANSION

This module is stubbed for the minimum viable electronica-specific analysis. Known future additions:

- **Sidechain pattern analysis**: Detailed characterization of ducking patterns (4-on-the-floor pump vs syncopated vs dynamic)
- **Sound design classification**: Categorizing synthesis techniques from spectral behavior (subtractive, FM, granular, wavetable)
- **Drop/build detection**: Identifying arrangement macrostructure unique to electronic music (build-up â†’ drop â†’ breakdown)
- **Automation lane inference**: Detecting parameter automation (filter cutoff, reverb send, delay feedback) from spectral trajectory analysis
- **Sample detection**: Identifying repeated identical waveforms suggesting sampled rather than synthesized content

These are noted but not specified. Build when dictionary entries demand them.

---

## DESIGN PRINCIPLE

The generic pipeline is designed for music where sound sources are relatively independent and spectrally separable. Electronica deliberately violates that assumption. Rather than forcing the generic pipeline to handle a problem it wasn't designed for, this module accepts the genre's analytical reality and exploits its structural gifts (rigid grid, mechanical periodicity, predictable arrangement) to recover what the generic pipeline can't see.

When recovery fails, the module still contributes â€” the fusion itself, the production techniques, the spectral sculpting choices become the primary findings. In electronica, what the standard pipeline calls "measurement failure" is often the most artistically significant thing happening in the track.
