# BINARY ENGINE
## Rhythm Dictionary â€” Component Spec
## 2026-02-08 Â· Version: independent

---

## PURPOSE

Extracts structural measurements from raw audio. Produces inert descriptors â€” numbers without interpretation. After Phase A genre commitment, it knows what's water and can flag markedness internally, but does NOT interpret.

Can be updated without touching any other component.

---

## INPUT

```
BinaryEngineInput {
  audio_file:       File (WAV or MP3)
  mode:             "snapshot" | "full" | "reentry"
  
  // Available for "full" and "reentry" modes (from Phase A)
  committed_genre:  GenreCommitment | null
  
  // Re-entry params (Bridge Module calling back)
  reentry_params:   BinaryReEntryRequest | null
}

GenreCommitment {
  genre_id:         string          // confirmed genre from Phase A
  baseline:         GenreBaseline   // loaded from Shared Protocol
  confidence:       float           // how sure are we
  source:           "binary_only" | "web_confirmed" | "web_corrected"
}
```

---

## OUTPUT

### Phase A output (snapshot mode):

```
GenreHypothesis {
  top_matches:      GenreMatch[]    // ranked by confidence
  confidence:       float
  discriminators:   string[]        // which measurements drove the guess
  snapshot_data:    object          // raw 10-sec readings (retained for reference)
}
```

### Phase B output (full mode):

```
StructuralDescriptor {
  song_id:          string
  duration_sec:     float
  sample_rate:      int
  committed_genre:  GenreCommitment // carried through from Phase A
  
  elements:         ElementReading[]
  co_production:    CoProductionCluster[]   // candidate clusters (unconfirmed)
  
  // Internal markedness flags (binary knows what's unusual for genre)
  markedness_flags: [
    {
      element_id:   int
      flag:         "within_baseline" | "outside_baseline" | "novelty"
      distance:     float           // how far outside baseline (0 = within)
    }
  ]
  
  metadata: {
    resolution:     string
    sections:       int
    engine_version: string
    timestamp:      ISO datetime
  }
}
```

### Shared types:

```
ElementReading {
  element_id:       int             // 1-55, canonical
  name:             string
  category:         string          // Dynamics | Spectral | Rhythm | Timbre | Stereo | Structure
  engine_status:    "active" | "degraded" | "broken"
  engine_weight:    float           // from Shared Protocol: 0.0, 0.3, 0.5, or 1.0
  
  value_summary:    float | string
  value_trajectory: float[]         // per-section values
  trajectory_tag:   "STATIC" | "TRAJECTORY-REQUIRED" | "TRAJECTORY-ENHANCED"
  
  axes: [
    {
      axis_id:      string          // A1-A4
      pole_low:     string
      pole_high:    string
      position:     float           // -1.0 to +1.0
      sign:         +1              // ALWAYS +1 (inert)
      weight:       1.0             // ALWAYS 1.0 (inert)
    }
  ]
}

GenreMatch {
  genre:            string
  confidence:       float
  discriminators:   string[]
  baseline_id:      string
}

CoProductionCluster {
  cluster_id:       string
  element_ids:      int[]
  correlation:      float
  confirmed:        false           // always false â€” web confirms
  lead_element:     null            // assigned after web confirmation
}
```

---

## RE-ENTRY INTERFACE (called by Bridge Module)

```
BinaryReEntryRequest {
  song_id:          string          // same audio, already loaded
  target_elements:  int[]           // specific elements to re-examine
  resolution:       "high"          // 16-32 sections minimum
  target_sections:  [float, float][] // specific time ranges
  hypothesis_tag:   string          // for logging only
}
```

Returns `ElementReading[]` at higher resolution. Binary doesn't know why it's being asked.

---

## READS FROM SHARED PROTOCOL
- Element Registry (IDs, names, categories, weight overrides, status flags)
- Genre Fingerprint Table (fingerprints with discriminator thresholds)
- Co-Production Cluster Templates (known patterns to detect)

## READS FROM DICTIONARY
- All existing fingerprint values (for zone-based matching, novelty detection)
- More entries = better novelty sensitivity, no recalibration needed

## DOES NOT KNOW
- Thematic content, lyrics, cultural context
- Production credits or methods
- Whether any measurement is artistically significant
- What any measurement means

---

## KNOWN ISSUES (current version)

### Broken elements (engine weight 0.0):
| # | Element | Issue |
|---|---------|-------|
| 25 | Beat micro-peaks | Suspect measurements â€” discard |
| 49 | Vocal presence | Returns 0% for all tracks â€” needs ML replacement |
| 52 | Reverb estimation | Impossibly dry readings â€” needs isolated transient analysis |

### Degraded elements (reduced weight):
| # | Element | Weight | Issue |
|---|---------|--------|-------|
| 27 | Decay time | 0.3 | Physically impossible readings |
| 28 | A/D ratio | 0.3 | Dependent on broken #27 |
| 30 | F0 (>200Hz) | 0.5 | Fails for polyphonic mid/high |
| 40 | Chromatic density | 0.5 | Low discrimination (all songs 5.7-6.9) |
| 44 | HNR | 0.5 | Systematically 3-6dB low |
| 47 | F0 trajectory (>200Hz) | 0.5 | Same as #30 |

### Systematic biases:
- A/D ratio wildly unreliable (BG reads 24.649 vs dictionary 0.343)
- HNR systematically 3-6dB low across all songs
- Production transparency correlates with engine accuracy:
  - BG (94%): transparent production, waveform IS the song
  - OH (73%): organic but layered
  - USC (68%): extreme dynamics challenge engine
  - NTLTC (52%): heavily constructed, waveform obscures layer architecture

---

## IMPROVEMENT ROADMAP (internal, no protocol changes needed)
- Fix HNR computation (systematic bias correction)
- Replace vocal presence with ML-based detection
- Improve reverb estimation (isolated transient analysis)
- Increase default resolution from 8 to 16 sections
- Improve genre fingerprint confidence for Tier 2/3 genres
