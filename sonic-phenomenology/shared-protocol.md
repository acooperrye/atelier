# SHARED PROTOCOL LAYER
## Rhythm Dictionary Ã¢â‚¬â€ Cross-Component Definitions
## 2026-02-08 Ã‚Â· Version: requires coordination

---

## PURPOSE

The canonical definitions that all four components read from. Changes here are the ONLY changes that require cross-component coordination. Everything else is component-internal.

**Rule:** If you're changing something here, both engines and both modules need to know about it. If you're NOT changing something here, you can update any component independently.

---

## A. ELEMENT REGISTRY

The canonical list of 55 measurement elements. Immutable IDs Ã¢â‚¬â€ elements can be deprecated but not renumbered.

```
ElementRegistry {
  version:          string
  elements: [
    {
      id:           int             // 1-55, canonical, immutable
      name:         string
      category:     "Dynamics" | "Spectral" | "Rhythm" | "Timbre" | "Stereo" | "Structure"
      engine_status: "active" | "degraded" | "broken"
      engine_weight: float          // 0.0 | 0.3 | 0.5 | 1.0
      trajectory_tag: "STATIC" | "TRAJECTORY-REQUIRED" | "TRAJECTORY-ENHANCED"
      axes: [
        {
          axis_id:   string         // A1-A4
          pole_low:  string
          pole_high: string
          trajectory_tag_override: string | null  // if axis-level differs from element
        }
      ]
      web_fallback:  bool           // true if web engine should try to populate
      web_sources:   string[]       // suggested source types for web fallback
      notes:         string         // known issues, calibration notes
    }
  ]
}
```

### Current status summary:

**Broken (weight 0.0, web-only):** #25, #49, #52
**Degraded (reduced weight):** #27 (0.3), #28 (0.3), #30 (0.5), #40 (0.5), #44 (0.5), #47 (0.5)
**Active (weight 1.0):** all others

Full element-by-element axis definitions are in `web-content-axis-scoring.md` (the operational reference for how each element's 4 axes are scored).

---

## B. PRESCRIPTIVE GENRE PRINTS

Hand-written genre fingerprints â€” a theory of what genres look like. The bootstrap. These are necessary because with zero empirical data, the engine needs something to match against. They define what genre *should* look like based on knowledge and inference.

Genre is not set with intention to reproduce a convention. Certain conventions become conventional, and then a genre is derived or established. The prescriptive prints are an approximation of that derivation, written from theory. They are the scaffold â€” permanent as cold-start fallback and sanity check, but their authority diminishes proportionally as descriptive data accumulates.

```
PrescriptiveGenrePrints {
  version:          string
  genres: [
    {
      genre_id:     string
      name:         string
      tier:         1 | 2 | 3      // fingerprint confidence tier
      fingerprint: {
        tempo:          [float, float]  // [min, max] BPM
        grid:           [float, float]  // adherence range
        rms:            [float, float]
        dyn_range:      [float, float]
        centroid:       [float, float]
        band_ratios:    object
        onset_density:  [float, float]
        flatness:       [float, float]
        zcr:            [float, float]
        silence:        [float, float]
        ioi_shape:      string          // categorical
        poly_density:   [float, float]
        stereo:         [float, float]
        crest:          [float, float]
        duration:       [float, float]
      }
      dimension_baselines: {
        valence:    [float, float]      // expected range per dimension
        energy:     [float, float]
        density:    [float, float]
        stability:  [float, float]
        constraint: [float, float]
        agency:     [float, float]
        roughness:  [float, float]
        continuity: [float, float]
        scale:      [float, float]
        weight:     [float, float]
      }
    }
  ]
}
```

### Current coverage:
- 20 genres defined in `genre-fingerprint-lookup.md`
- Tier 1 (tight fingerprints): Ambient, Noise, Classical, Jazz, Metal, Punk, EDM/House, Hip-Hop/Trap
- Tier 2 (moderate): Indie Rock, R&B, Country, Folk, Reggae, Funk/Soul
- Tier 3 (loose): Pop, Singer-Songwriter, World, Experimental, Shoegaze, Post-Rock

### Expansion needed:
- Gap 5 in `instructions-gap-closure.md`: prescriptive prints need expansion beyond 20

---

## B2. DESCRIPTIVE GENRE PRINTS

Empirical genre data â€” what genres *actually* look like, built from real Resolution 1 snapshots of analyzed songs tagged with web-confirmed genre. Where prescriptive prints encode theory, descriptive prints encode observation.

Genre is not set with intention to reproduce a convention. Certain conventions become conventional, and then a genre is derived or established. The descriptive prints capture that derivation from observed reality. Every song that completes Phase A (Resolution 1 snapshot + web genre confirmation) commits its snapshot here. Over time, the descriptive cluster becomes more trustworthy than the prescriptive fingerprint because it is built from actual observations.

```
DescriptiveGenrePrints {
  version:          string
  genres: [
    {
      genre_id:         string
      observations:     GenreObservation[]
      derived_center:   object | null       // computed when n >= 3
      derived_variance: object | null       // computed when n >= 3
      n:                int                 // count of observations
    }
  ]
}

GenreObservation {
  song_id:            string
  snapshot_data: {                          // the 15 Resolution 1 discriminators, raw values
    tempo:            float
    grid:             float
    rms:              float
    dyn_range:        float
    centroid:         float
    band_ratios:      object
    onset_density:    float
    flatness:         float
    zcr:              float
    silence:          float
    ioi_shape:        string
    poly_density:     float
    stereo_width:     float
    stereo_corr:      float
    crest:            float
    duration:         float
  }
  genre_source:       "web_confirmed" | "web_corrected"
  timestamp:          ISO datetime
}
```

### Matching priority:
- If `n < 3` for a genre -> prescriptive prints are primary, descriptive is supplementary
- If `n >= 3` -> descriptive cluster center becomes primary, prescriptive prints become fallback/sanity check
- If descriptive cluster and prescriptive prints *disagree* on a match -> flag as genre boundary question, do not auto-resolve

### Resolution constraint:
Observations are committed at Resolution 1 only (the 15-discriminator snapshot). Genre lives at body-type level. Storing finer detail would contaminate the genre memory with song-specific information that has nothing to do with the genre cluster.

### Current observations:
| Genre | n | Songs |
|-------|---|-------|
| Synth-pop | 1 | EWTRTW |
| Dance-pop | 1 | NTLTC |
| Electropop/Hyperpop | 1 | Music (underscores) |
| Post-rock | 1 | Only Human |
| Electro-pop/Synth-soul | 1 | Black and Gold |

All genres at n=1. Prescriptive prints remain primary for all. Descriptive authority begins at n=3.


---

## C. META-DIMENSION DEFINITIONS

The 10 perceptual dimensions that bridge structural measurement and thematic meaning. Both engines and both modules score into these.

```
MetaDimensions {
  version:          string
  dimensions: [
    {
      id:           string
      name:         string
      pole_low:     string
      pole_high:    string
      description:  string
      structural_contributors: int[]    // which element IDs feed in
      thematic_contributors: string[]   // which thematic keywords map here
      scoring_notes: string
    }
  ]
}
```

### The 10 dimensions:

| ID | Name | Low Pole | High Pole |
|----|------|----------|-----------|
| valence | Valence | Dark | Bright |
| energy | Energy | Still | Kinetic |
| density | Density | Sparse | Dense |
| stability | Stability | Unstable | Anchored |
| constraint | Constraint | Free | Contained |
| agency | Agency | Mechanical | Human |
| roughness | Roughness | Smooth | Rough |
| continuity | Continuity | Fragmented | Continuous |
| scale | Scale | Intimate | Vast |
| weight | Weight | Light | Heavy |

### Validation status:
- Gap 1 in `instructions-gap-closure.md`: these 10 dimensions need formal validation against dictionary songs
- Structural contributors and thematic contributors not yet fully mapped

---

## D. CO-PRODUCTION CLUSTER TEMPLATES

Known patterns where multiple elements are symptoms of the same physical phenomenon.

```
CoProductionTemplates {
  version:          string
  known_clusters: [
    {
      template_id:  string
      name:         string
      element_ids:  int[]           // elements involved
      lead_element: int             // the "cause"
      detection: {
        correlation_threshold: float
        temporal_alignment: bool    // must move together?
        required_elements: int[]    // minimum subset to trigger
      }
      web_confirmers: string[]      // production terms that confirm
      scoring: {
        lead_weight: float          // typically 2.0
        subordinate_weight: float   // typically 0.3
      }
      known_instances: [
        { song: string, evidence: string }
      ]
    }
  ]
}
```

### Known clusters (from dictionary songs):

| Cluster | Elements | Lead | Known In |
|---------|----------|------|----------|
| Gated drums | #26 attack + #11 dyn range + #12 silence + #10 crest | #26 | EWTRTW |
| Bedroom production | grid + stereo corr + M/S + flatness range | grid | BG |
| Sample-locked | grid + CV + attack | grid | NTLTC |
| WallÃ¢â€ â€™collapse | dyn range + MFCC shift + stereo corr + loudness | dyn range | underscores |
| Sustain-fills-gaps | silence + density floor + attack | attack | OH |

### Formalization status:
- Gap 3 in `instructions-gap-closure.md`: co-production detection mechanism not yet fully formalized
- Correlation thresholds and temporal alignment rules need calibration

---

## E. SPECTRAL ROSTER ROLES

The canonical role assignments used by SpectralRoster and consumed by multiple components. Roles are frequency-band-based groupings that identify what audible function a spectral region is performing. Defined in `phase-a-revised-cheap-pass.md`, referenced by Percussion Module, Cultural Engine, and Binary Engine.

```
SpectralRoles {
  version:          string

  roles: [
    // Percussive roles — consumed by Percussion Module for per-element timing
    { role: "percussive-low",   band_hz: [30, 150],    maps_to: "kick" }
    { role: "percussive-mid",   band_hz: [150, 4000],  maps_to: "snare, clap, rim" }
    { role: "percussive-high",  band_hz: [5000, 16000], maps_to: "hat, crash, ride, shaker" }

    // Sustained roles — consumed by Binary Engine for tonal analysis
    { role: "sustained-low",    band_hz: [30, 250],    maps_to: "bass, sub-bass" }
    { role: "sustained-mid",    band_hz: [250, 4000],  maps_to: "melody, harmony, pads" }
    { role: "sustained-high",   band_hz: [4000, 16000], maps_to: "air, sparkle, texture" }

    // Special roles
    { role: "vocal",            band_hz: [200, 4000],  maps_to: "lead/backing vocal" }
  ]
}
```

### Percussion Module interface schemas (cross-component):

These structs are defined in `module-percussion.md` and consumed by multiple engines. Registered here by reference — full definitions live in the percussion module spec.

| Schema | Defined in | Consumed by | Purpose |
|--------|-----------|-------------|---------|
| `GuidingPrior` | module-percussion.md | Percussion, Binary | Web-sourced BPM + time signature — the frame |
| `ElementMeter` | module-percussion.md | Binary, Cultural, Feltness, Interpretive | Per-element timing grid + deviations |
| `MeterRelationship` | module-percussion.md | Interpretive, Cultural | Cross-element timing ratios |
| `DeviationLog` | module-percussion.md | Cultural, Interpretive | Every absence/extra vs expected grid |

### Breaking change note:
Changing SpectralRoster role names or band boundaries is a breaking change (requires all consumers to update). Adding new roles is non-breaking (additive).

---

## VERSIONING RULES

### Breaking changes (require version bump here + all components acknowledge):
- Adding/removing/renaming an element in Element Registry
- Changing axis pole definitions
- Adding/removing a meta-dimension
- Changing interface schemas (StructuralDescriptor, ContextDescriptor, ActivatedAxes, ElementMeter, MeterRelationship, DeviationLog)
- Changing SpectralRoster role names or band boundaries

### Non-breaking changes to protocol tables:
- Expanding Prescriptive Genre Prints (adding new genres) â€” non-breaking, components just have more fingerprints available
- Committing new observations to Descriptive Genre Prints â€” non-breaking, empirical clusters grow automatically
- Adding new co-production cluster templates Ã¢â‚¬â€ non-breaking, detection is additive
- Updating element notes/status Ã¢â‚¬â€ non-breaking, components read current status dynamically

### The distinction:
If the SHAPE of a table changes (new columns, renamed fields) Ã¢â€ â€™ breaking.
If the CONTENTS of a table change (new rows, updated values) Ã¢â€ â€™ non-breaking.
