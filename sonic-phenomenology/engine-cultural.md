# CULTURAL CONTEXT ENGINE
## Rhythm Dictionary — Component Spec
## 2026-02-10 · Version: independent

---

## PURPOSE

Maps the cultural tension field surrounding a song. Produces a structured account of what conventions the song inherits, which it obeys, and which it subverts — the prerequisite context without which bridge Types 6 (Excision) and 7 (Inversion) cannot be identified.

Runs parallel to the Web Engine in Phase B (receives the same artist/title/genre input). Can also be invoked as a subordinate pass after the Web Engine has committed genre, if the cultural context depends on genre-specific knowledge.

Produces inert descriptors — contextual facts without interpretation. The Interpretive Engine decides what's artistically significant.

Can be updated without touching any other component.

**Cross-references:**
- **fingerprint-registry.md** — universal catalogue of 64 sonic fingerprints (the atoms). Each convention in this engine references fingerprint IDs.
- **genre-fingerprint-map.md** — 58 genres mapped to fingerprint IDs (the molecules). Once genre is committed, this is the lookup table for expected fingerprints.

---

## THE PROBLEM THIS ENGINE SOLVES

Bridge Types 1-5 (Structure ↔ Theme) can be identified from audio + lyrics + thematic context. The Binary Engine measures structure. The Web Engine retrieves theme. Tension between them is computationally detectable.

Bridge Types 6-7 (Musical structure ↔ Musical semantics) CANNOT be identified from the song alone. They require knowledge of what the song is subverting — conventions that exist outside the audio file, in the accumulated history of the genre, the era, and the listener's biographical exposure. The Binary Engine can detect that a snare has become tonal (Circle Pit). It cannot detect that this is a violation of the convention that snares are rhythmic. That convention lives in cultural context, not in the waveform.

**Without this engine, the Interpretive Engine can only identify Types 1-5.**

---

## CORE CONCEPT: THE CONVENTION BANK

Every genre/era/scene establishes a set of conventions — default expectations about what music does structurally, who it addresses, what roles instruments play, how production relates to content. These conventions form a **tension bank**: accumulated structural norms that are available for violation.

The Cultural Context Engine's primary output is a structured Convention Bank for the song under analysis. This is what Types 6 and 7 subvert.

---

## INPUT

```
CulturalEngineInput {
  artist:           string
  title:            string
  album:            string | null
  year:             int | null
  committed_genre:  GenreCommitment     // from Phase A
  web_context:      ContextDescriptor   // from Web Engine Phase B (if available)
}
```

---

## OUTPUT

```
CulturalDescriptor {
  song_id:          string

  // 1. LINEAGE — where does this song come from?
  lineage: {
    genre_ancestry:   GenreNode[]       // chain: breakcore ← jungle ← rave ← acid house ← disco
    direct_influences: ArtistInfluence[] // documented influences on this artist
    scene_context:    SceneContext       // the specific scene/moment this emerged from
    era_placement:    EraPlacement       // modernist / postmodern / post-postmodern / other
  }

  // 2. CONVENTION BANK — what norms does this genre/era establish?
  convention_bank: {
    structural:       Convention[]       // how songs in this genre are typically built
    semantic:         Convention[]       // what instruments/sounds typically mean
    hierarchical:     Convention[]       // what the expected perceptual hierarchy is
    address:          Convention[]       // how the music relates to the listener
    production:       Convention[]       // how the music is expected to sound/be made
  }

  // 3. VIOLATION MAP — which conventions does THIS song violate?
  violations: Violation[]               // populated after binary+web data available

  // 4. PRIOR REQUIREMENTS — what must the listener know for each violation to register?
  prior_requirements: PriorRequirement[]

  metadata: {
    engine_version:   string
    timestamp:        ISO datetime
    source_count:     int
    confidence:       float             // overall confidence in convention bank completeness
  }
}
```

### Convention (the unit of the convention bank)

**DESIGN PRINCIPLE (Alex, 10 Feb 2026):** A convention is not a prose description that gets translated into a binary search instruction. The convention IS the binary fingerprint. The cultural engine doesn't tell the binary engine what to look for in natural language — it hands it fingerprint patterns ranked by likelihood for this genre. The convention and the detection instruction are the same object.

This means: Web Engine commits genre → Cultural Engine receives genre → genre maps to an ordered set of fingerprint references → each fingerprint defines both the convention (what's expected) and the detection shape (what to measure), with pass level, zoom level, and masking/subtractive analysis parameters.

```
Convention {
  id:               string              // e.g. "breakcore.snare_is_rhythmic"
  category:         "structural" | "semantic" | "hierarchical" | "address" | "production"
  domain:           string              // which genre/era established this

  statement:        string              // human-readable: "snare drums provide rhythmic structure"
                                        // (for logging/debugging only — NOT the detection instruction)

  entrenchment:     float               // SIGNED. Magnitude = allele frequency (0.0–1.0),
                                        // sign = direction of travel. +0.3 = emerging convention,
                                        // -0.3 = declining convention. +1.0 = deeply entrenched, stable.
                                        // Algebraic precision available: e(t) = ±f(t) for lifecycle curves
                                        // (e.g. e(t) = e^(-0.4(t-1986)²) for gated reverb's Gaussian rise/fall).
                                        // See genomic-frame.md § Convention Lifecycle for the 9-phase model.
  reactivated:      bool                // true if convention was epigenetically silenced and has returned.
                                        // Reactivated conventions carry different meaning (ironic, quotational,
                                        // nostalgic) than their original occurrence. The magnitude may be
                                        // identical to an earlier phase but the semantic weight differs.
  scope:            "universal" | "genre" | "era" | "scene" | "artist"

  // THE FINGERPRINT — this IS the convention expressed as a binary measurement instruction
  fingerprint: ConventionFingerprint

  // Likelihood ranking for this genre (lower = more likely to be present)
  genre_rank:       int                 // 1 = most expected convention for this genre

  sources:          string[]
}
```

### ConventionFingerprint (the binary shape of a convention)

```
ConventionFingerprint {
  // What to measure
  target_band:      string | string[]   // "hi_mid" | ["sub_bass", "bass"] | "full"
  target_role:      string | null       // SpectralRoster role if applicable: "percussive-high"

  // What the convention predicts (the "normal" shape)
  expected_shape: {
    onset_ratio:    { op: string, val: float } | null   // e.g. { op: ">", val: 10 }
    decay_type:     string | null       // "natural" | "hard_gate" | "sustained" | "reversed"
    decay_time_ms:  { op: string, val: float } | null   // e.g. { op: "<", val: 50 }
    hpss_balance:   { op: string, val: float } | null   // e.g. { op: ">", val: 0.6 } (percussive fraction)
    crest_factor_db: { op: string, val: float } | null
    ms_ratio:       { op: string, val: float } | null   // stereo width
    band_energy_pct: { op: string, val: float } | null  // % of total energy in target band
    onset_rate_hz:  { op: string, val: float } | null   // events per second
    pitch_range_hz: [float, float] | null
    envelope_stages: int | null         // expected number of envelope stages (1, 2, etc.)
    stage_delay_ms: { op: string, val: float } | null   // delay between stages
  }

  // How to detect it
  detection: {
    pass_level:     "snapshot" | "cheap" | "full" | "reentry"
                                        // when in the analysis pipeline to check
    zoom_level:     "song" | "section" | "bar" | "hit"
                                        // temporal resolution needed
    masking:        string | null       // subtractive analysis instruction:
                                        // "isolate_band" | "hpss_percussive" | "hpss_harmonic"
                                        // "subtract_sub_bass" | "envelope_only" | null
    min_section_duration_ms: int | null // minimum analysis window
    requires_roster: bool               // does detection need SpectralRoster context?
  }

  // What violation looks like (the "not normal" shape)
  violation_signature: {
    // If these measurements are found INSTEAD of expected_shape, flag as violation
    // Uses same fields as expected_shape but with inverted/different values
    // null fields = don't check (violation could manifest in any unmeasured dimension)
    onset_ratio:    { op: string, val: float } | null
    decay_type:     string | null
    hpss_balance:   { op: string, val: float } | null
    onset_rate_hz:  { op: string, val: float } | null
    // etc. — same fields as expected_shape
  }

  // What type of violation this would be
  violation_type_if_found: "excision" | "inversion" | "mutation" | null
  bridge_type_if_found:    6 | 7 | null
}
```

### Example: Convention fingerprint for "drums are rhythmic"

```
{
  id: "universal.drums_are_rhythmic",
  category: "hierarchical",
  domain: "universal",
  statement: "percussion provides rhythmic structure, not tonal/harmonic content",
  entrenchment: +1.0,      // POSITIVE: stable, deeply entrenched, no decline trajectory
  reactivated: false,
  scope: "universal",
  genre_rank: 1,

  fingerprint: {
    target_band: "hi_mid",
    target_role: "percussive-high",

    expected_shape: {
      hpss_balance: { op: ">", val: 0.5 },    // more percussive than harmonic in this band
      onset_rate_hz: { op: "<", val: 8 },       // below ~480 BPM = individual events legible
      crest_factor_db: { op: ">", val: 15 }     // sharp transients (discrete hits)
    },

    detection: {
      pass_level: "full",
      zoom_level: "section",
      masking: "isolate_band",
      requires_roster: true
    },

    violation_signature: {
      hpss_balance: { op: "<", val: 0.4 },     // more harmonic than percussive = drums became tonal
      onset_rate_hz: { op: ">", val: 5 },       // >5/sec = repetition entering tonal territory
    },

    violation_type_if_found: "inversion",
    bridge_type_if_found: 7
  }
}
```

### Example: Convention fingerprint for "gated snare"

```
{
  id: "era.80s_gated_snare",
  category: "production",
  domain: "1980s pop/rock",
  statement: "gated reverb on snare with hard cutoff",
  entrenchment: +0.15,     // POSITIVE but low: reactivating. Original lifecycle peaked at
                            // ~+0.9 in 1985, genericized by ~1992, silenced by ~1998.
                            // Currently rising again in synthwave/retrowave contexts (2015+)
                            // but at much lower amplitude than original peak.
                            // Sign = current direction of travel = rising (reactivation).
                            // Algebraic (original): e(t) ≈ 0.9·e^(-0.3(t-1986)²)
                            // Algebraic (reactivation): e(t) ≈ 0.15·(1 - e^(-0.2(t-2015)))
  reactivated: true,        // reappears in synthwave (2015+) but as quotation, not convention.
                            // Semantic weight differs from original — ironic/nostalgic, not default.
  scope: "era",
  genre_rank: 4,           // 4th most expected convention for 80s pop

  fingerprint: {
    target_band: ["mid", "hi_mid"],
    target_role: "percussive-mid",

    expected_shape: {
      onset_ratio: { op: ">", val: 15 },
      decay_type: "hard_gate",
      decay_time_ms: { op: "<", val: 80 },
      crest_factor_db: { op: ">", val: 18 }
    },

    detection: {
      pass_level: "full",
      zoom_level: "hit",
      masking: "hpss_percussive",
      min_section_duration_ms: 100,
      requires_roster: false            // gated snare is detectable without knowing context
    },

    violation_signature: null,          // gated snare isn't typically violated — it's a convention
                                        // that's either present or absent. Its absence from an 80s
                                        // track might be notable but isn't a bridge-type violation.
    violation_type_if_found: null,
    bridge_type_if_found: null
  }
}
```

### Genre → Convention ordering

The genre fingerprint in Shared Protocol gains an associated convention manifest:

```
GenreConventionManifest {
  genre_id:         string
  conventions:      ConventionRef[]     // ordered by likelihood

  // Each ref points to a convention + specifies genre-specific overrides
  ConventionRef {
    convention_id:  string              // "universal.drums_are_rhythmic"
    genre_rank:     int                 // position in the ordered list for this genre
    genre_override: object | null       // genre-specific parameter adjustments
                                        // e.g. breakcore might override onset_rate_hz threshold
                                        // because extreme onset rates ARE expected in breakcore
  }
}
```

This is the key mechanism: the same convention ("drums are rhythmic") can appear in multiple genre manifests with different rankings and overrides. In rock, it's rank 1 with standard thresholds. In breakcore, it's rank 1 but with the `onset_rate_hz` threshold raised — because breakcore expects extreme onset rates as a genre convention. Circle Pit violates it by pushing PAST even breakcore's raised threshold. The violation is measured relative to the genre's own adjusted expectations, not relative to universal defaults.

---

## UNIVERSAL CONVENTION BANK

The minimum set of conventions loaded for EVERY analysis, regardless of genre. These represent expectations so deeply internalized that virtually all music listeners hold them. All 10 are checked on every pass. Genre manifests override thresholds but never remove a universal convention — the convention is still present, just with adjusted parameters.

Conventions are numbered U1-U10. The first 6 have full fingerprint definitions (these are the ones most likely to trigger Type 6/7 bridge signals). U7-U10 have reference definitions and are pending full fingerprint specification.

### U1: universal.drums_are_rhythmic

*(Full fingerprint defined above as worked example. Reproduced here by reference.)*

Category: hierarchical. Entrenchment: 1.0. Scope: universal.
Detection: hi_mid band, HPSS balance, onset rate, crest factor.
Violation: HPSS inverts (drums become tonal through density). Bridge type 7 (Inversion).

### U2: universal.rhythm_heard_bass_felt

```
{
  id: "universal.rhythm_heard_bass_felt",
  category: "hierarchical",
  domain: "universal",
  statement: "percussion provides the consciously tracked beat; bass/sub-bass provides felt weight",
  entrenchment: +0.95,     // stable
  reactivated: false,
  scope: "universal",
  genre_rank: 2,

  fingerprint: {
    target_band: ["hi_mid", "sub_bass"],
    target_role: null,

    expected_shape: {
      // Hi-mid: the rhythmic reference. Discrete hits, consciously countable.
      onset_ratio: { op: ">", val: 4, band: "hi_mid" },
      hpss_balance: { op: ">", val: 0.5, band: "hi_mid" },
      crest_factor_db: { op: ">", val: 10, band: "hi_mid" },

      // Sub-bass: the weight system. Present, felt, but not the beat grid.
      onset_ratio: { op: "<", val: 25, band: "sub_bass" },
      band_energy_pct: { op: ">", val: 10, band: "sub_bass" },

      // CROSS-BAND: hi-mid onset ratio > sub-bass onset ratio
      // (the sharpest transients are in the "heard" band, not the "felt" band)
      cross_band: {
        comparison: "onset_ratio",
        rule: "hi_mid > sub_bass",
        description: "percussion attacks are sharper than bass attacks"
      }
    },

    detection: {
      pass_level: "full",
      zoom_level: "section",
      masking: "isolate_band",
      min_section_duration_ms: 2000,
      requires_roster: false
    },

    violation_signature: {
      // Sub-bass becomes the primary rhythmic reference
      // Hi-mid loses discrete transient character
      cross_band: {
        comparison: "onset_ratio",
        rule: "sub_bass > hi_mid",
        description: "bass hits are sharper than drum hits — felt band carries the beat"
      },
      hpss_balance: { op: "<", val: 0.4, band: "hi_mid" },
    },

    violation_type_if_found: "inversion",
    bridge_type_if_found: 7
  }
}
```

Note on `cross_band`: Extension to the ConventionFingerprint struct for hierarchical conventions. These conventions are ABOUT relationships between frequency bands, not properties of a single band. The `cross_band` field specifies which measurement to compare across which bands. This is what makes Types 6 and 7 detectable — they are relational violations, not absolute ones. Circle Pit's sub-bass onset ratio (1.1x) is unremarkable on its own. It only becomes a violation when compared to the hi-mid onset character (which has become tonal).

### U3: universal.bass_provides_foundation

```
{
  id: "universal.bass_provides_foundation",
  category: "semantic",
  domain: "universal",
  statement: "bass/sub-bass provides harmonic foundation and felt weight beneath other elements",
  entrenchment: +0.9,      // stable
  reactivated: false,
  scope: "universal",
  genre_rank: 3,

  fingerprint: {
    target_band: ["sub_bass", "bass"],
    target_role: null,

    expected_shape: {
      band_energy_pct: { op: ">", val: 15 },     // sub+bass combined > 15% of total energy
      hpss_balance: { op: ">", val: 0.5 },        // mostly harmonic (pitched bass notes, not noise)
      pitch_range_hz: [20, 250],                    // bass content lives in the low end
      onset_ratio: { op: ">", val: 1.5 },          // has SOME attack (not pure drone)
    },

    detection: {
      pass_level: "full",
      zoom_level: "song",
      masking: null,                                // measurable from full mix
      requires_roster: false
    },

    violation_signature: {
      band_energy_pct: { op: "<", val: 5 },        // bass essentially absent
      // OR: bass present but not harmonic (noise-bass, distortion-bass)
      hpss_balance: { op: "<", val: 0.3 },
    },

    violation_type_if_found: "excision",            // removing bass entirely = semantic excision
    bridge_type_if_found: 6
  }
}
```

Dictionary reference: PUTP sub+bass = 74%, Blade Runner = 76%, Circle Pit = 54%, Shout ~55%. All well above the 15% floor. A track with <5% combined bass would be violating a near-universal convention.

### U4: universal.sounds_decay_naturally

```
{
  id: "universal.sounds_decay_naturally",
  category: "structural",
  domain: "universal",
  statement: "sounds begin with attack and decay over time, following acoustic physics",
  entrenchment: +0.85,     // stable (physics-grounded, not culturally contingent)
  reactivated: false,
  scope: "universal",
  genre_rank: 4,

  fingerprint: {
    target_band: "full",
    target_role: null,

    expected_shape: {
      onset_ratio: { op: ">", val: 1.5 },          // attacks exist (energy arrives faster than it leaves)
      decay_type: "natural",                         // exponential decay, not hard gate or reverse
      envelope_stages: 1,                            // single attack-decay per event (not multi-stage)
    },

    detection: {
      pass_level: "full",
      zoom_level: "hit",
      masking: "hpss_percussive",                   // check transients specifically
      min_section_duration_ms: 50,
      requires_roster: false
    },

    violation_signature: {
      onset_ratio: { op: "<", val: 1.0 },           // reversed sound (energy grows instead of decaying)
      decay_type: "reversed",
      // OR: multi-stage envelope that no acoustic object produces
      envelope_stages: { op: ">", val: 1 },
    },

    // Not necessarily a bridge — could just be production technique
    violation_type_if_found: "mutation",
    bridge_type_if_found: null                      // reversed sounds aren't automatically a bridge
  }
}
```

Note: This convention is weaker than U1-U3. Electronic music routinely violates natural decay (gated reverb, reversed cymbals, sidechain pumping). The entrenchment is lower (0.85) and violations don't signal bridge types on their own. BUT: this convention becomes structurally important in combination with others — SOPHIE's two-stage envelope (sub-bass snap + mid rubber bloom at +93ms) violates U4 in a way that's not just a production technique but a material statement. The multi-stage envelope is what makes the rubber texture. The violation is the material.

### U5: universal.frequency_roles_fixed

```
{
  id: "universal.frequency_roles_fixed",
  category: "hierarchical",
  domain: "universal",
  statement: "each frequency band has a conventional role: bass = foundation, mid = melody/harmony, hi-mid = percussion/definition, high = air/sparkle",
  entrenchment: +0.85,     // stable
  reactivated: false,
  scope: "universal",
  genre_rank: 5,

  fingerprint: {
    target_band: "full",
    target_role: null,

    expected_shape: {
      // Sub-bass/bass: predominantly harmonic (pitched content)
      hpss_balance: { op: ">", val: 0.6, band: "sub_bass" },
      hpss_balance: { op: ">", val: 0.5, band: "bass" },

      // Hi-mid: predominantly percussive (transients, definition)
      hpss_balance: { op: ">", val: 0.4, band: "hi_mid" },

      // High: percussive or noise (cymbals, air, sibilance)
      hpss_balance: { op: "<", val: 0.5, band: "high" },

      // Cross-band: energy distribution follows standard spectral shape
      // (not a single number — this is the spectral centroid being in a "normal" range)
    },

    detection: {
      pass_level: "full",
      zoom_level: "song",
      masking: "isolate_band",
      requires_roster: true                         // needs role assignment to detect role-swaps
    },

    violation_signature: {
      // Role swap: bass band becomes percussive, hi-mid becomes harmonic
      hpss_balance: { op: "<", val: 0.3, band: "sub_bass" },  // bass has become noise
      hpss_balance: { op: ">", val: 0.7, band: "hi_mid" },    // percussion has become tonal
    },

    violation_type_if_found: "inversion",
    bridge_type_if_found: 7
  }
}
```

Dictionary reference: Circle Pit shows exactly this violation — hi_mid HPSS reads 70.8% harmonic (percussion has become tonal). The sub-bass remains harmonic (35-40Hz pitch center) so the violation is one-sided: hi-mid role has flipped, sub-bass role has held.

### U6: universal.dynamic_emphasis

```
{
  id: "universal.dynamic_emphasis",
  category: "structural",
  domain: "universal",
  statement: "louder moments carry structural emphasis; dynamics signal hierarchy",
  entrenchment: +0.75,     // stable but weakening slightly (loudness wars erode this)
  reactivated: false,
  scope: "universal",
  genre_rank: 6,

  fingerprint: {
    target_band: "full",
    target_role: null,

    expected_shape: {
      crest_factor_db: { op: ">", val: 6 },        // meaningful dynamic range exists
      // Spectral flux trajectory has peaks and valleys (section-level dynamics)
      // This is harder to express as a single operator — may need custom measurement
    },

    detection: {
      pass_level: "full",
      zoom_level: "song",
      masking: null,
      requires_roster: false
    },

    violation_signature: {
      crest_factor_db: { op: "<", val: 4 },         // brick-wall limited, no dynamic variation
      // Note: low crest factor is common in modern mastering (loudness wars)
      // and in genres like breakcore, noise, industrial.
      // This violation is NOT automatically a bridge — it's often just a production norm.
    },

    violation_type_if_found: null,                   // too common to be a bridge signal on its own
    bridge_type_if_found: null
  }
}
```

Dictionary reference: Circle Pit crest factor 3.1 (extreme limiting). Shout crest factor 16.1. PUTP somewhere between. Low crest factor is a genre convention for breakcore, not a violation — the breakcore manifest overrides this threshold.

### U7-U10 (reference definitions, pending full fingerprints)

```
U7: universal.temporal_regularity
  category: "structural"
  statement: "music has a detectable, stable pulse or beat grid"
  entrenchment: +0.8, reactivated: false
  detection: autocorrelation peak at a single tempo, stable across sections
  violation: arrhythmic, tempo unstable, no detectable pulse
  bridge_type_if_found: null (free time is a production choice, not typically a bridge)

U8: universal.vocals_are_foreground
  category: "hierarchical"
  statement: "when vocals are present, they occupy the lead/foreground position"
  entrenchment: +0.85 (conditional — only applies when vocals detected), reactivated: false
  detection: vocal band (200-4000Hz) harmonic content centered, higher relative energy
  violation: vocal pushed to background, treated as texture, spatially distant
  bridge_type_if_found: 6 (Excision — vocal's semantic role removed while voice persists)
  NOTE: SOPHIE's Lemonade shows partial violation — vocal recognized as human but NOT
  mapped to self, spatially above/away rather than foreground. Not full excision but
  partial. The vocal is present but doesn't address the listener.

U9: universal.stereo_center_priority
  category: "production"
  statement: "primary elements (vocal, kick, bass) are centered; support elements are wider"
  entrenchment: +0.7, reactivated: false
  detection: primary band M/S ratio low (<2), support band M/S ratio higher
  violation: center empty, primary elements pushed to extremes
  bridge_type_if_found: null (stereo experimentation is common, rarely a bridge)

U10: universal.structure_has_sections
  category: "structural"
  statement: "songs have identifiable sections with transitions between them"
  entrenchment: +0.7, reactivated: false
  detection: spectral flux shows section-level changes, energy trajectory has peaks/valleys
  violation: completely uniform texture, no section boundaries, relentless consistency
  bridge_type_if_found: null (drone, ambient, and noise genres routinely omit sections)
```

---

## BREAKCORE CONVENTION MANIFEST

The first complete GenreConventionManifest. Validates against Circle Pit analysis data.

```
GenreConventionManifest {
  genre_id: "breakcore",

  conventions: [

    // === UNIVERSAL CONVENTIONS WITH OVERRIDES ===

    {
      convention_id: "universal.drums_are_rhythmic",
      genre_rank: 1,
      genre_override: {
        // Breakcore expects EXTREME onset rates as standard. The universal threshold
        // (onset_rate_hz < 8) is far too low. Breakcore raises it.
        expected_shape: {
          onset_rate_hz: { op: "<", val: 12 }
          // Was: < 8. Breakcore routinely hits 8-10 events/sec and they're
          // still rhythmic (just very fast). Circle Pit pushes past 12 to ~5.7/sec
          // on individual snare hits but the COMPOSITE rate is higher.
          // The threshold for "drum events are individually legible" is raised
          // but not eliminated. Even breakcore assumes you can hear individual hits.
        },
        violation_signature: {
          onset_rate_hz: { op: ">", val: 12 }
          // Above 12/sec, even breakcore-literate listeners lose individual hit
          // tracking. This is where percussion crosses into texture/tone.
        }
      }
    },

    {
      convention_id: "universal.rhythm_heard_bass_felt",
      genre_rank: 2,
      genre_override: {
        // Jungle lineage: breaks and bass are a DUAL SYSTEM, not a simple hierarchy.
        // Both are rhythmic, both are felt. The hierarchy is flatter.
        expected_shape: {
          cross_band: {
            comparison: "onset_ratio",
            rule: "hi_mid >= sub_bass",
            // Softened from "hi_mid > sub_bass" — in breakcore, sub-bass can be nearly
            // as sharp as percussion. The convention just requires percussion is AT LEAST
            // as sharp as bass, not necessarily sharper.
            description: "percussion attacks at least as sharp as bass attacks"
          }
        }
      }
    },

    {
      convention_id: "universal.bass_provides_foundation",
      genre_rank: 3,
      genre_override: null
      // No override needed. Breakcore inherits sub-bass from jungle.
      // Circle Pit: sub+bass = 54%, well above the 15% floor.
    },

    {
      convention_id: "universal.sounds_decay_naturally",
      genre_rank: 7,
      genre_override: {
        // Lower rank: breakcore EXPECTS unnatural decay. Sample chopping means
        // sounds are routinely truncated, reversed, or interrupted.
        entrenchment: 0.4,
        // Dropped from +0.85 to +0.4. Hard edits and unnatural envelopes are the norm.
        // This convention is barely operative in breakcore — it's almost expected to be violated.
        reactivated: false,
      }
    },

    {
      convention_id: "universal.frequency_roles_fixed",
      genre_rank: 4,
      genre_override: null
      // Standard thresholds. Even in breakcore, bass is bass and drums are drums.
      // Circle Pit violates this despite breakcore's raised tolerance for other conventions.
    },

    {
      convention_id: "universal.dynamic_emphasis",
      genre_rank: 9,
      genre_override: {
        // Breakcore is typically brick-wall limited. Low crest factor is EXPECTED.
        expected_shape: {
          crest_factor_db: { op: ">", val: 3 }
          // Dropped from >6 to >3. Circle Pit is 3.1 — right at the floor.
        },
        // This convention is almost irrelevant in breakcore.
        entrenchment: +0.3,   // low but stable within breakcore
        reactivated: false,
      }
    },

    {
      convention_id: "universal.temporal_regularity",
      genre_rank: 5,
      genre_override: {
        // Breakcore DOES have a regular tempo — typically very fast (160-200+ BPM).
        // But metric regularity (time signature, bar structure) is experimental.
        // The pulse exists. The meter doesn't.
        expected_shape: {
          // Tempo detectable but time signature may be non-4/4
          // This override is more about WHAT is regular (tempo) vs what isn't (meter)
        }
      }
    },

    {
      convention_id: "universal.vocals_are_foreground",
      genre_rank: 10,
      genre_override: {
        // Most breakcore is instrumental. When vocals appear, they're usually
        // sampled, chopped, treated as material — not as foreground address.
        entrenchment: 0.2,
        // Nearly irrelevant. If vocals are present, they're likely cut up.
        reactivated: false,
      }
    },

    {
      convention_id: "universal.stereo_center_priority",
      genre_rank: 8,
      genre_override: null
      // Physics dictates sub-bass centering regardless of genre.
    },

    {
      convention_id: "universal.structure_has_sections",
      genre_rank: 6,
      genre_override: {
        // Some breakcore tracks have sections. Many don't.
        // Relentless escalation (no plateau, continuous increase) is more
        // typical than section-based structure.
        entrenchment: 0.4,
      }
    },

    // === GENRE-SPECIFIC CONVENTIONS (not universal) ===

    {
      convention_id: "breakcore.extreme_tempo",
      genre_rank: 1,          // MOST expected convention for breakcore (tied with U1)
      genre_override: null,

      // Inline convention definition (not in universal bank):
      convention: {
        id: "breakcore.extreme_tempo",
        category: "structural",
        domain: "breakcore",
        statement: "tempo is 160-200+ BPM",
        entrenchment: +0.9,   // stable within genre
        reactivated: false,
        scope: "genre",

        fingerprint: {
          target_band: "full",
          target_role: null,

          expected_shape: {
            onset_rate_hz: null,                 // measured at song level
            // BPM measured via autocorrelation
            // Expected: 160-220 BPM
          },

          detection: {
            pass_level: "snapshot",               // detectable in first 10 seconds
            zoom_level: "song",
            masking: null,
            requires_roster: false
          },

          violation_signature: null,              // slow breakcore isn't really a bridge
          violation_type_if_found: null,
          bridge_type_if_found: null
        }
      }
    },

    {
      convention_id: "breakcore.sample_atomization",
      genre_rank: 2,

      convention: {
        id: "breakcore.sample_atomization",
        category: "production",
        domain: "breakcore",
        statement: "drum breaks (typically amen) are chopped to individual hits and reassembled",
        entrenchment: +0.9,   // stable within genre
        reactivated: false,
        scope: "genre",

        fingerprint: {
          target_band: "hi_mid",
          target_role: "percussive-high",

          expected_shape: {
            onset_rate_hz: { op: ">", val: 4 },  // >4 hits/sec = chopped material, not played
            crest_factor_db: { op: ">", val: 10 },
            // Each chop has its own spectral character (varying slightly because
            // slices come from different parts of the source break)
          },

          detection: {
            pass_level: "full",
            zoom_level: "bar",
            masking: "hpss_percussive",
            requires_roster: false
          },

          violation_signature: null,
          violation_type_if_found: null,
          bridge_type_if_found: null
        }
      }
    },

    {
      convention_id: "breakcore.no_address",
      genre_rank: 3,

      convention: {
        id: "breakcore.no_address",
        category: "address",
        domain: "breakcore",
        statement: "music does not accommodate the listener — listener must orient themselves",
        entrenchment: +0.7,   // stable within genre
        reactivated: false,
        scope: "genre",

        fingerprint: {
          target_band: "full",
          target_role: null,

          expected_shape: {
            // No vocal address (instrumental or vocals-as-material)
            // No build-drop structure guiding the listener
            // High information density (many events, little repetition)
            onset_rate_hz: { op: ">", val: 4 },
            crest_factor_db: { op: "<", val: 8 },  // limited = relentless, no breathing room
          },

          detection: {
            pass_level: "full",
            zoom_level: "song",
            masking: null,
            requires_roster: false
          },

          violation_signature: null,
          violation_type_if_found: null,
          bridge_type_if_found: null
        }
      }
    },

    {
      convention_id: "breakcore.relentless_escalation",
      genre_rank: 4,

      convention: {
        id: "breakcore.relentless_escalation",
        category: "structural",
        domain: "breakcore",
        statement: "spectral flux increases throughout the track with no plateau or release",
        entrenchment: +0.6,   // stable within genre
        reactivated: false,
        scope: "genre",

        fingerprint: {
          target_band: "full",
          target_role: null,

          expected_shape: {
            // Spectral flux trajectory: monotonically increasing or at least never
            // returning to opening levels. No "verse-chorus" dynamics.
            // Circle Pit: spectral flux triples across the track (78→237)
          },

          detection: {
            pass_level: "full",
            zoom_level: "song",
            masking: null,
            requires_roster: false
          },

          violation_signature: null,
          violation_type_if_found: null,
          bridge_type_if_found: null
        }
      }
    },

    {
      convention_id: "breakcore.sub_bass_shadow",
      genre_rank: 5,

      convention: {
        id: "breakcore.sub_bass_shadow",
        category: "production",
        domain: "breakcore",
        statement: "sub-bass is tethered directly underneath break hits as a shadow layer",
        entrenchment: +0.4,   // low — possibly artist-specific rather than genre-wide
        reactivated: false,
        scope: "genre",
        // NOTE: Low entrenchment. This may be a Venetian Snares-specific technique
        // rather than a breakcore convention. Not documented in breakcore production
        // literature. Needs more data from other breakcore artists to confirm scope.

        fingerprint: {
          target_band: ["sub_bass", "hi_mid"],
          target_role: null,

          expected_shape: {
            // Sub-bass envelope correlated with hi-mid onsets
            // Sub-bass onset ratio low (1-3x) — doesn't need its own attack
            // because the hi-mid transient IS the onset event
            onset_ratio: { op: "<", val: 3, band: "sub_bass" },
            // Cross-correlation between sub-bass envelope and hi-mid onsets: moderate
            cross_band: {
              comparison: "envelope_correlation",
              rule: "sub_bass correlates hi_mid onsets > 0.3",
              description: "sub-bass rises on break hits"
            },
            // Sub-bass begins rising BEFORE hi-mid peak
            stage_delay_ms: { op: "<", val: 5 },
          },

          detection: {
            pass_level: "reentry",                  // needs high-resolution envelope analysis
            zoom_level: "hit",
            masking: "isolate_band",
            min_section_duration_ms: 50,
            requires_roster: false
          },

          violation_signature: null,
          violation_type_if_found: null,
          bridge_type_if_found: null
        }
      }
    }
  ]
}
```

---

### Violation (the unit of subversion)

```
Violation {
  convention_id:    string              // which convention is being violated
  violation_type:   "excision" | "inversion" | "mutation" | "compression" | "expansion"

  description:      string              // "snare repetition rate crosses from rhythmic to tonal"

  // What bridge type does this support?
  bridge_type_signal: 6 | 7 | null      // Excision or Inversion, or neither (just unusual)

  // How detectable is this violation?
  detectability: {
    from_audio:     bool                // can Binary Engine see this?
    from_web:       bool                // can Web Engine context reveal this?
    requires_cultural: bool             // does it NEED convention bank to interpret?
  }

  // Evidence
  binary_evidence:  string | null       // what the Binary Engine measurement shows
  cultural_evidence: string | null      // what the convention bank comparison reveals

  confidence:       float
}
```

### PriorRequirement (what the listener needs to know)

```
PriorRequirement {
  violation_id:     string              // which violation this applies to

  requirement:      string              // "listener must have internalized that drums provide rhythm"

  // How common is this prior?
  population_coverage: float            // 0-1: what % of music listeners have this prior?
                                        // 1.0 = "rhythm comes from percussion" (everyone)
                                        // 0.5 = "808 patterns define trap" (genre listeners)
                                        // 0.1 = "amen break is the canonical breakcore source" (scene)

  // Biographical bridge requirement
  minimum_exposure: string              // "any popular music" | "electronic music" | "breakcore specifically"

  // Does this violation work without the prior?
  degrades_without_prior: bool          // true = violation is invisible without prior
                                        // false = violation is still unusual, just not meaningful
}
```

---

## SUPPORTING STRUCTURES

### GenreNode (ancestry chain)

```
GenreNode {
  genre:            string
  era:              string              // "1988-1992"
  key_conventions:  string[]            // what this genre ADDED to the lineage
  key_subversions:  string[]            // what this genre broke from its parent
  relationship:     "evolved_from" | "reacted_against" | "fused_with" | "specialized_from"
}
```

Example for Circle Pit:
```
[
  { genre: "breakcore", era: "1995-present",
    key_conventions: ["extreme tempo", "sample atomization", "time signature experimentation"],
    key_subversions: ["breaks no longer provide danceable rhythm", "song structure abandoned"],
    relationship: "reacted_against" },
  { genre: "jungle/drum_and_bass", era: "1991-1997",
    key_conventions: ["chopped amen break", "sub-bass as independent layer", "160-180 BPM"],
    key_subversions: ["breakbeat freed from hip-hop tempo", "bass and breaks as dual system"],
    relationship: "evolved_from" },
  { genre: "rave/hardcore", era: "1989-1993",
    key_conventions: ["sampled breakbeats", "sustained sub-bass", "ecstatic build-drop"],
    key_subversions: ["electronic production as primary, not accompaniment"],
    relationship: "evolved_from" },
  { genre: "acid_house", era: "1986-1989",
    key_conventions: ["4/4 kick", "303 bassline", "repetitive structure"],
    key_subversions: ["synthesizer as lead voice replacing vocalist"],
    relationship: "evolved_from" }
]
```

### SceneContext

```
SceneContext {
  scene:            string              // "Winnipeg breakcore / Planet Mu"
  active_period:    string              // "2000-2012"
  key_figures:      string[]            // artists, labels, venues
  aesthetic_values: string[]            // what this scene prizes
  tools:            string[]            // "Renoise tracker", "hardware samplers"
  relationship_to_mainstream: string    // "deliberately antagonistic", "parallel", "emergent"
  sources:          string[]
}
```

### EraPlacement

```
EraPlacement {
  primary:          string              // "post-postmodern" | "postmodern" | "modernist" | "other"

  justification:    string              // why this placement

  // What kind of relationship does the work have to convention?
  convention_stance: "operates_within" | "extends" | "subverts" | "deconstructs" | "ignores"

  // Artistic context
  parallel_movements: string[]          // non-musical art movements with similar stance
                                        // e.g. ["fluxus", "noise art", "glitch aesthetics"]
  sources:          string[]
}
```

---

## CONVENTION BANK CATEGORIES (DETAILED)

### 1. Structural conventions
What songs in this genre typically do architecturally.

Examples:
- "Songs have verse-chorus-verse-chorus-bridge-chorus structure"
- "Tracks build via additive layering toward a peak/drop"
- "Songs are typically 3-5 minutes long"
- "Tempo is typically 120-140 BPM"
- "Time signature is 4/4"

### 2. Semantic conventions
What instruments/sounds/techniques typically MEAN in this genre.

Examples:
- "Drums provide rhythmic structure"
- "Bass provides harmonic foundation and felt weight"
- "Vocal carries melody and lyrical content"
- "A drop signifies release of built tension"
- "Gated reverb signifies 1980s production"

### 3. Hierarchical conventions
What the expected perceptual hierarchy is — what you hear vs feel, what's foreground vs background.

Examples:
- "Percussion is rhythmic, bass is felt, melody is heard"
- "Vocal is foreground, instruments are accompaniment"
- "Sub-bass is felt, not consciously tracked"
- "Hi-hats provide subdivisions, not melodic content"

**THIS IS WHERE TYPES 6 AND 7 OPERATE.** Excision removes a semantic layer. Inversion flips a hierarchical relationship. Both require this category to be populated for detection.

### 4. Address conventions
How the music relates to the listener.

Examples:
- "Pop music addresses the listener through vocal performance"
- "Dance music addresses the listener through bodily rhythm"
- "Ambient music creates an environment the listener inhabits"
- "Breakcore does not address the listener — listener must orient themselves"

### 5. Production conventions
How the music is expected to sound and be made.

Examples:
- "Electronic music uses synthesized rather than recorded sound sources"
- "Lo-fi production signifies authenticity"
- "Mastering loudness is maximized in this genre"
- "Breakcore uses sample-based production with heavy editing"

---

## WORKFLOW

### Phase B (parallel with Web Engine):

```
Step 1: LINEAGE RETRIEVAL
  Input: artist, genre, year
  Action: Web search for genre ancestry, artist influences, scene context
  Output: lineage, scene_context, era_placement
  Sources: Wikipedia, RYM, AllMusic, academic genre studies, artist interviews

Step 2: CONVENTION BANK ASSEMBLY
  Input: committed genre, lineage, era
  Action: Build convention bank from:
    a) Universal conventions (always present, scope: "universal")
    b) Genre-specific conventions (from genre ancestry chain)
    c) Era-specific conventions (from era placement)
    d) Scene-specific conventions (from scene context, if available)
  Output: convention_bank (all five categories populated)
  Sources: Genre studies, production manuals, critical discourse

Step 3: CONVENTION CONFIDENCE CHECK
  Input: convention_bank, web_context (from Web Engine)
  Action: Cross-reference conventions against known production/arrangement data
  Output: convention_bank with confidence scores
  Note: Some conventions may be uncertain until Binary Engine data arrives
```

### Post-Binary (after full analysis available):

```
Step 4: VIOLATION DETECTION
  Input: convention_bank, binary structural descriptor, web context
  Action: Compare each convention's structural_prediction against actual measurements
  Output: violations[] — which conventions are being violated, how, and to what degree

Step 5: PRIOR REQUIREMENT MAPPING
  Input: violations[]
  Action: For each violation, determine what the listener needs to know for it to register
  Output: prior_requirements[] — biographical bridge requirements

Step 6: BRIDGE TYPE SIGNALING
  Input: violations[], prior_requirements[]
  Action: Flag violations that signal Type 6 (Excision) or Type 7 (Inversion)
  Output: Updated violations with bridge_type_signal
  Note: Does NOT determine bridge type — passes signals to Interpretive Engine
```

---

## RE-ENTRY INTERFACE (called by Interpretive Engine)

```
CulturalReEntryRequest {
  song_id:          string
  query_type:       "deepen_lineage" | "convention_specificity" | "violation_context" | "prior_assessment"
  specific_query:   string
  hypothesis_tag:   string
}

CulturalReEntryResponse {
  query_type:       string
  findings:         string
  convention_updates: Convention[] | null
  violation_updates: Violation[] | null
  sources:          string[]
  confidence:       float
}
```

---

## RELATIONSHIP TO EXISTING ENGINES

### Reads from:
- **Web Engine**: genre commitment, thematic vector, production method, credits
- **Binary Engine**: structural descriptor (post-full-pass, for violation detection)
- **Shared Protocol**: genre baselines, element registry

### Produces for:
- **Interpretive Engine**: convention bank, violations, prior requirements, bridge type signals
- **Activation Layer**: convention context for interpreting roster deviations
  - A roster deviation (from Binary Engine) + convention context (from Cultural Engine) = meaningful finding
  - Example: Binary flags "percussive-high role has become harmonic" (roster deviation: spectral_fusion). Cultural Engine provides convention "snare drums are rhythmic" (entrenchment: 1.0). Together: this is a hierarchical inversion with near-universal prior requirement.

### Does NOT know:
- Raw audio measurements (only receives structured Binary Engine output)
- How to interpret violations artistically (that's the Interpretive Engine's job)

---

## EXAMPLE: CIRCLE PIT (full fingerprint pass)

**Song**: Venetian Snares — Circle Pit (Detrimentalist, 2008)
**Genre committed**: breakcore (Phase A)
**Manifest loaded**: breakcore GenreConventionManifest (above)

### Step 1: Convention bank assembly

Breakcore manifest loads 10 universal conventions (with overrides) and 5 genre-specific conventions. Ordered by genre_rank:

```
Rank  Convention ID                              Source       Category        Entrenchment (signed)
──────────────────────────────────────────────────────────────────────────────────────────────
 1    universal.drums_are_rhythmic               universal    hierarchical    +1.0
 1    breakcore.extreme_tempo                    genre        structural      +0.9
 2    universal.rhythm_heard_bass_felt           universal    hierarchical    +0.95
 2    breakcore.sample_atomization               genre        production      +0.9
 3    universal.bass_provides_foundation         universal    semantic        +0.9
 3    breakcore.no_address                       genre        address         +0.7
 4    universal.frequency_roles_fixed            universal    hierarchical    +0.85
 4    breakcore.relentless_escalation            genre        structural      +0.6
 5    universal.temporal_regularity              universal    structural      +0.8
 5    breakcore.sub_bass_shadow                  genre        production      +0.4
 6    universal.structure_has_sections           universal    structural      +0.4 (overridden)
 7    universal.sounds_decay_naturally           universal    structural      +0.4 (overridden)
 8    universal.stereo_center_priority           universal    production      +0.7
 9    universal.dynamic_emphasis                 universal    structural      +0.3 (overridden)
10    universal.vocals_are_foreground            universal    hierarchical    +0.2 (overridden)
```

### Step 2: Binary data (from full analysis)

```
Measurement                  Value            Convention(s) this informs
──────────────────────────────────────────────────────────────────────────
BPM (autocorrelation)        172              breakcore.extreme_tempo ✓ (within 160-220)
Hi-mid HPSS balance          0.292 percussive universal.drums_are_rhythmic → CHECK
Hi-mid onset rate            ~5.7/sec (snare) universal.drums_are_rhythmic → CHECK
Hi-mid crest factor          ~11 dB           (within expected range)
Sub-bass onset ratio         1.1x             universal.rhythm_heard_bass_felt → CHECK
Sub-bass band energy         25.3%            universal.bass_provides_foundation ✓ (>15%)
Sub-bass + bass combined     54.1%            universal.bass_provides_foundation ✓
Sub-bass HPSS balance        >0.6 harmonic    universal.frequency_roles_fixed ✓ (bass is harmonic)
Sub-bass M/S ratio           18.9             universal.stereo_center_priority ✓
Overall crest factor         3.1 dB           universal.dynamic_emphasis → CHECK
Spectral flux trajectory     78→237 (3x)      breakcore.relentless_escalation ✓
Sub-bass/hi-mid correlation  0.481            breakcore.sub_bass_shadow → partial match
Envelope staging             hi-mid -7.4ms, sub +2.3ms   breakcore.sub_bass_shadow ✓
Section boundaries           minimal          universal.structure_has_sections ✓ (expected absent)
Vocal content                none detected    universal.vocals_are_foreground → N/A
```

### Step 3: Violation detection (fingerprint comparison)

```
VIOLATION 1: universal.drums_are_rhythmic
─────────────────────────────────────────
  Convention fingerprint (breakcore-adjusted):
    expected:   hpss_balance > 0.5, onset_rate_hz < 12, crest_factor > 15
    measured:   hpss_balance = 0.292, onset_rate ~5.7/sec (individual), crest ~11
    violation:  hpss_balance < 0.4 → TRIGGERED (0.292 < 0.4)
               onset_rate_hz > 12 → NOT triggered for individual hits
               BUT composite percussion rate pushes into quasi-harmonic territory
               HPSS inversion is the definitive signal: drums are 70.8% HARMONIC

  Fingerprint match: violation_signature.hpss_balance < 0.4 → TRUE
  Violation type: inversion
  Bridge type signal: 7

  Binary evidence: HPSS reads 70.8% harmonic in hi-mid band. Amen snare hits at
    ~5.7/sec individually, but composite break density (all percussion) crosses the
    threshold where repetition rate enters tonal territory. The percussion has BECOME
    a harmonic texture — a "single somewhat detuned keyboard note" (Alex).

  Cultural evidence: Violates most deeply entrenched musical convention (entrenchment 1.0).
    Even the breakcore-adjusted threshold (onset_rate < 12) is designed to accommodate
    extreme speed — this track still violates via the HPSS route rather than the pure
    rate route. The drums didn't just get fast. They changed state.

  Confidence: 0.95


VIOLATION 2: universal.rhythm_heard_bass_felt
─────────────────────────────────────────────
  Convention fingerprint (breakcore-adjusted):
    expected:   cross_band.rule = "hi_mid onset_ratio >= sub_bass onset_ratio"
                hi_mid band = percussive primary, sub_bass band = felt weight
    measured:   hi_mid has LOST percussive identity (see Violation 1)
                sub_bass onset_ratio = 1.1x (low, not sharp)
                BUT sub-bass is the ONLY remaining legible rhythmic structure
    violation:  cross_band rule INVERTED: sub-bass carries the beat, hi-mid is texture

  Fingerprint match: violation_signature.cross_band.rule = "sub_bass > hi_mid" → TRUE
    (sub-bass is the rhythmic reference because hi-mid has fused into drone)
  Violation type: inversion
  Bridge type signal: 7

  Binary evidence: Sub-bass onset correlation with hi-mid = 0.481 (partially aligned).
    Sub-bass envelope begins rising before hi-mid peak. Sub-bass peak at +2.3ms after
    hi-mid transient. Sub-bass provides the only felt beat grid at 172 BPM (~2.9Hz).
    Onset ratio 1.1x means the sub-bass doesn't hit hard — it SWAYS. But it's the only
    thing swaying at a trackable rate. Everything else is drone.

  Cultural evidence: Violates near-universal hierarchical convention (entrenchment 0.95).
    "You hear the beat and feel the bass" becomes "you hear the drone and feel the beat."
    The breakcore manifest's softened cross_band rule (>= rather than >) makes no
    difference here — the inversion is total, not marginal.

  Confidence: 0.90


VIOLATION 3: universal.frequency_roles_fixed
────────────────────────────────────────────
  Convention fingerprint:
    expected:   hi-mid hpss_balance > 0.4 (percussive character)
    measured:   hi-mid hpss_balance = 0.292
    violation:  hi-mid HPSS < 0.3 → approaching violation threshold

  This is CORRELATED with Violation 1 but distinct: Violation 1 says "drums aren't
  rhythmic." Violation 3 says "the hi-mid frequency band has changed its role."
  The convention being violated is about frequency assignment, not instrument function.

  Fingerprint match: violation_signature.hpss_balance > 0.7 (band: hi_mid) → PARTIAL
    (0.708 harmonic, just above the 0.7 threshold)
  Violation type: inversion
  Bridge type signal: 7 (correlated with Violation 1)

  Confidence: 0.85 (partially redundant with V1)


NO VIOLATION: breakcore.sub_bass_shadow
───────────────────────────────────────
  Convention fingerprint:
    expected:   sub-bass onset_ratio < 3, correlation > 0.3, delay < 5ms
    measured:   onset_ratio 1.1x ✓, correlation 0.481 ✓, delay ~2.3ms ✓
    result:     CONVENTION MET — the shadow bass IS a breakcore production technique.
                It's not a violation. It's the mechanism by which Violations 1 and 2 work.
                The shadow provides the rhythmic replacement that lets percussion become drone.

  This is significant: the shadow bass is the ENABLER of the inversions, not itself a
  violation. Without it, Circle Pit would be noise (no rhythmic reference at all).
  With it, Circle Pit is a hierarchical inversion (the rhythm is felt, not heard).
```

### Step 4: Prior requirements

```
Violation 1 priors:
  requirement: "listener must know that drums provide rhythmic structure"
  population_coverage: 0.95
  minimum_exposure: "any popular music"
  degrades_without_prior: true
  // Without this prior, the 70.8% harmonic HPSS is just "a sound."
  // With it, it's "drums doing something drums don't do."

Violation 2 priors:
  requirement: "listener must know that you hear beats and feel bass"
  population_coverage: 0.90
  minimum_exposure: "any bass-heavy music (hip-hop, electronic, club)"
  degrades_without_prior: true
  // Without bass-heavy music experience, the sub-bass shadow as rhythmic
  // reference is invisible — the listener has no expectation to invert.

Violation 3 priors:
  requirement: "listener must know that high frequencies carry percussion"
  population_coverage: 0.85
  minimum_exposure: "any produced music"
  degrades_without_prior: true
  // Correlated with Violation 1 — same biographical bridge, different angle.
```

### Step 5: Bridge type signaling

```
BRIDGE SIGNAL: TYPE 7 (INVERSION) — HIGH CONFIDENCE

Three correlated violations all signaling Type 7:
  - V1: drums → tonal (instrument function swap)
  - V2: heard/felt hierarchy → felt/heard (perceptual hierarchy swap)
  - V3: hi-mid role → harmonic (frequency assignment swap)

All three require near-universal priors (population coverage 0.85-0.95).
All three degrade without prior (biographical bridges).

COMPOUND EFFECT: These violations are not independent — they are three faces
of one structural inversion. V1 causes V3 (drums becoming tonal changes the
hi-mid band's role). V1+V3 cause V2 (if percussion is no longer rhythmic,
something else must be, and the sub-bass shadow is the only candidate).
The Interpretive Engine should interpret these as a single compound inversion,
not three separate violations.

ENABLER: breakcore.sub_bass_shadow (convention MET) provides the structural
mechanism that makes the inversion listenable rather than chaotic. Without the
shadow, the inversions would produce formless noise. With it, they produce a
track where the beat has merely moved — from ears to chest, from hi-mid to
sub-bass, from heard to felt.

SOMATIC CONFIRMATION (from dictionary, correspondence #15):
  - Fever dream → rollercoaster cognitive flip
  - Sub-bass at 172 BPM ≈ elevated heartbeat → internal misattribution
  - "Bit like a circle pit" — continuous rotation, individual become collective
  → Interpretive Engine receives these as Tier 1 (somatic) evidence for Type 7
```

---

## OPEN QUESTIONS

1. ~~**Convention bank completeness.** How many conventions constitute a "complete enough" bank for a given genre? Is there a minimum set of universal conventions that every analysis starts with?~~ **ANSWERED (10 Feb 2026):** 10 universal conventions (U1-U10) form the minimum set. 6 have full fingerprint definitions; 4 have reference definitions. Every analysis loads all 10. Genre manifests add genre-specific conventions and override universal thresholds. The breakcore manifest adds 5 genre-specific conventions on top of the 10 universals, for 15 total. This appears sufficient for Type 6/7 detection based on the Circle Pit validation.

2. **Convention discovery.** Some conventions are obvious (drums = rhythm). Others are subtle (gated reverb = 80s). How does the engine discover genre-specific conventions it doesn't already know? Web search for "conventions of [genre]" is unreliable. Academic genre studies are better but sparse.

3. **Entrenchment measurement.** How to quantify how deeply a convention is held? Population surveys don't exist. Proxy: how many genres share this convention? If it appears in the ancestry chain of 5+ genres, entrenchment is high.

4. **Cross-cultural conventions.** The current model assumes Western popular music conventions. Non-Western music has different hierarchical, semantic, and structural conventions. The engine needs to be aware of which conventions are culturally bounded. "Drums = rhythm" is probably near-universal. "Verse-chorus structure" is not.

5. ~~**Convention evolution.** Conventions change over time. The 808 was once unusual; now it's a convention. Autotune was once a violation; now it's expected. The convention bank needs to be era-aware — what was a violation in 2005 may be a convention by 2025. Timestamp all conventions.~~ **PARTIALLY RESOLVED (11 Feb 2026):** The Genomic Frame (`genomic-frame.md`) provides the formal model for convention evolution — a 9-phase lifecycle mapped from population genetics (Mutation → Transposition → Polymorphism → Fixation → Selective Sweep → Genericization → Negative Selection → Epigenetic Silencing → Reactivation). The `entrenchment` field is now a signed float: magnitude = allele frequency, sign = direction of travel (+rising, -falling). Algebraic lifecycle curves (e.g. `e(t) = 0.9·e^(-0.3(t-1986)²)` for gated reverb) are available for precision. The `reactivated` boolean flags conventions that have returned from silencing (carrying different semantic weight). **Remaining:** curve parameterization sources need documenting (Web Engine retrieval as flywheel data), and era-awareness needs formalizing as a lookup function that evaluates `e(t)` at the song's release year.

6. **Interaction with somatic dictionary.** The somatic dictionary contains correspondences that are essentially felt conventions — "sub-bass at this onset ratio = punch," "sustained sub-bass = atmosphere." These are calibrated to Alex, not universal. Should the Cultural Engine have access to the somatic dictionary as a source of listener-specific conventions?

7. **Multiple simultaneous violations.** Circle Pit violates at least two conventions simultaneously (drums→tonal, heard/felt inversion). Does the interaction between violations compound the bridge effect, or does each operate independently? SOPHIE similarly has multiple simultaneous operations (referent excision + vocal non-address + synthetic materiality). The Interpretive Engine probably handles this, but the Cultural Engine should flag when multiple violations interact.

---

## RELATIONSHIP TO BRIDGE TAXONOMY

| Bridge type | Tension source | Engine that detects it |
|-------------|---------------|----------------------|
| 1. Concealment | Structure ↔ Theme | Binary + Web |
| 2. Compensation | Structure ↔ Theme | Binary + Web |
| 3. Contradiction | Structure ↔ Theme | Binary + Web |
| 4. Refusal | Structure ↔ Theme | Binary + Web |
| 5. Conceit | Structure ↔ Theme | Binary + Web |
| 6. Excision | Musical structure ↔ Musical semantics | Binary + Web + **Cultural** |
| 7. Inversion | Musical structure ↔ Musical semantics | Binary + Web + **Cultural** |

Types 1-5: Binary measures structure, Web provides theme. Tension is between them.
Types 6-7: Binary measures structure, Cultural provides the conventions being violated. Tension is between what IS and what the listener EXPECTS.

**The Cultural Engine is the reason the bridge taxonomy can grow past five.**

---

*Engine spec created: 10 February 2026*
*Updated: 11 February 2026 — entrenchment field converted to signed float (magnitude + direction), reactivated boolean added. Convention lifecycle model formalized in genomic-frame.md. Open Question 5 partially resolved.*
*Status: Architecture draft. Universal convention bank populated (10 conventions, 6 with full fingerprints). Breakcore manifest complete (15 conventions). Circle Pit validated against fingerprint system — 3 violations detected, all signaling Type 7 (Inversion). Next: additional genre manifests (trap, 80s pop, ambient, jungle) and ConventionFingerprint definitions for U7-U10.*
