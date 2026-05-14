# SUPPRESSION MAP
## Rhythm Dictionary — Signal Hygiene
## 2026-02-11 · Version: draft

---

## THE IDEA

Every engine in this system asks questions. Onset ratio? HPSS balance? Band energy? Convention violated? Each question costs cycles. Most of the time, most of the questions return answers. But for any given genre, band, or analysis phase, some questions are structurally guaranteed to return nothing — and the system asks them anyway.

The suppression map is the negative image of the fingerprint registry. Where the registry says "look for this shape," the suppression map says "this shape's expected value is zero here — don't look." The fingerprint and its suppression are two views of the same curve.

**The biological parallel (from genomic-frame.md):** The cell doesn't waste ribosomes translating non-coding regions. The regulatory machinery has a "don't bother" list — not because those regions are useless, but because *right now, in this cell type, in this context,* they are silent. If they fire anyway, the cell notices precisely because the region was suppressed. An unexpected signal from a suppressed region is louder than a normal signal from an active one.

**The musical parallel:** You don't check for bass notes at 15kHz. You don't check for gated reverb in ambient drone. You don't look for vocal address in instrumental breakcore. These aren't errors — they're prior knowledge. The suppression map formalises what every experienced listener already knows: where not to look.

**What this buys us:**
1. Fewer wasted cycles per analysis pass
2. Higher signal-to-noise on the findings that do emerge
3. A built-in anomaly detector: when a suppressed region fires, it's automatically a finding
4. Progressive learning: the more songs analysed, the tighter the suppression gets

---

## THE FORMAT: ALGEBRAIC FINGERPRINTS

Each fingerprint in the registry (FP-E01, FP-S03, etc.) currently expresses a threshold — a pass/fail gate. But the real fingerprint is a **distribution**: for a given genre and band, what values does this measurement typically take?

### From threshold to curve

**Current (threshold):**
```
FP-H01: hpss_balance(hi_mid) > 0.5 → percussive dominant
```

**Algebraic (distribution):**
```
FP-H01.distribution(genre, band) → expected_value ± spread

  rock:       μ = 0.65, σ = 0.10   // solidly percussive, narrow spread
  breakcore:  μ = 0.55, σ = 0.15   // percussive but variable (can fuse)
  ambient:    μ = 0.25, σ = 0.10   // harmonic dominant — FP-H01 is suppressed
  noise:      μ = 0.50, σ = 0.20   // right on the boundary, wide spread — ambiguous
```

When the expected distribution sits entirely below the threshold, the fingerprint is in suppression territory. Don't poll it. Or rather: poll it at low priority, and if it fires, amplify the finding.

### The suppression function

For any fingerprint F, genre G, band B, and phase P:

```
suppression(F, G, B, P) = {
  active:     μ + 2σ > threshold          // expected range crosses the threshold
  dormant:    μ + 2σ < threshold           // expected range below threshold (95% confidence)
                AND μ > noise_floor         // but the measurement isn't zero
  silent:     μ < noise_floor              // measurement is structurally absent
}
```

**Active** = poll normally. The distribution predicts the fingerprint might fire.
**Dormant** = poll at reduced frequency (every Nth song, or on re-entry only). The distribution predicts the fingerprint won't fire, but the measurement exists.
**Silent** = don't poll. The measurement is structurally impossible in this context (bass content at 15kHz, vocal presence in instrumental music, etc.).

### When a suppressed region fires

This is the immune response. A dormant or silent fingerprint that returns a value above threshold is automatically escalated:

```
SurpriseSignal {
  fingerprint:    string          // which fingerprint fired
  expected:       "dormant" | "silent"
  measured:       float           // actual value
  deviation:      float           // how many σ from expected μ
  escalation:     float           // deviation × suppression_weight
                                  // (higher suppression = louder alarm)

  // A 3σ event from a dormant fingerprint is worth more than
  // a 1σ event from an active fingerprint. The surprise IS the signal.
}
```

---

## LAYER 0: PHYSICS SUPPRESSION (genre-independent, always applied)

Before any genre commits, physics constrains what's possible in each band. These suppressions are permanent and universal — they apply to every song regardless of genre.

```
PhysicsSuppression {
  // These are not conventions. They are laws.
  // No genre can override physics. No learning can change them.
  // They form the floor of every GenreSuppressionVector.

  always_silent: [
    { fingerprint: "onset_ratio",     band: "sub_bass (20-80Hz)",
      engines: ["binary", "percussion"],
      reason: "sub-bass cannot produce sharp transients. A 40Hz wave needs 25ms
               per cycle. Onset ratio in this band is always low (<3).
               Checking for onset_ratio > 10 here is checking for something
               physics forbids." },

    { fingerprint: "stereo_width",    band: "sub_bass (20-80Hz)",
      engines: ["binary"],
      reason: "sub-bass wavelengths at 40Hz are ~8.5 metres. Panning is inaudible.
               Physics enforces mono. M/S ratio in sub-bass is always near-zero." },

    { fingerprint: "hpss_harmonic",   band: "high (8-20kHz)",
      engines: ["binary", "cultural"],
      reason: "above 8kHz, content is almost entirely inharmonic — noise, air,
               sibilance, cymbal ring. Checking for harmonic dominance here wastes
               cycles. Exception: specific synth overtones (recheck on re-entry if
               equipment engine identifies strong upper partials)." },

    { fingerprint: "pitch_hz",        band: "sub_bass (20-80Hz)",
      engines: ["binary"],
      reason: "pitch detection at sub-bass requires long FFT windows (>50ms for
               2 cycles at 40Hz). Standard window may not resolve. Defer to feltness
               module envelope analysis or equipment engine 808 bloom detection." },
  ]
}
```

---

## LAYER 1: THE GENRE SUPPRESSION VECTOR

When genre commits, the system emits a `GenreSuppressionVector` — a single object that tells every engine what to check and what to skip. This is the genre's negative fingerprint. The shape of what you don't check is as diagnostic as the shape of what you do.

### The format

```
GenreSuppressionVector {
  genre_id:         string
  version:          string
  last_updated:     ISO datetime
  songs_analysed:   int             // how many songs have contributed to this vector
  confidence:       float           // higher with more songs

  // THE VECTOR: one entry per fingerprint, per engine that polls it
  // This is the core data structure. Everything else derives from it.
  entries: [
    {
      fingerprint_id:   string      // e.g. "FP-H01"
      engine:           string      // which engine polls this: "binary" | "cultural" |
                                    // "percussion" | "feltness" | "activation" | "interpretive"
      band:             string      // which band this check targets (if applicable)
      status:           "active" | "dormant" | "silent"

      // The algebraic curve: expected distribution for this fingerprint in this genre
      distribution: {
        μ:              float       // expected mean value
        σ:              float       // expected spread
        threshold:      float       // the fingerprint's activation threshold
        // Suppression test: if μ + 2σ < threshold → dormant
        //                   if μ < noise_floor → silent
      }

      // Learning data
      null_count:       int         // consecutive songs where this returned nothing
      surprise_count:   int         // times this fired from dormant/silent
      last_fired:       ISO datetime | null

      // What to do if it fires from suppression
      recheck_trigger:  string | null   // condition that would promote this back to active
    }
  ]

  // CONVENTION SUPPRESSION (Cultural Engine specific)
  // Conventions with entrenchment below this floor are not loaded
  cultural_suppression_floor: 0.15

  // Conventions whose violations are EXPECTED for this genre
  // These are the false positive suppressors — see below
  expected_violations: string[]     // convention IDs that this genre violates by definition

  // PERCUSSION MODULE FLAGS
  percussion_active:    bool        // does this genre expect percussive elements?
  ghost_note_prior:     float       // 0-1, web-derived prior for ghost note testing

  // INTERPRETIVE ENGINE PRUNING
  // Bridge types that are structurally impossible given this genre's suppression
  suppressed_bridge_types: int[]    // e.g. [6, 7] if no excision/inversion conventions loaded

  // THE COMPOSITE SHAPE
  // Summary stats derived from the entries array
  total_fingerprints:   int         // 64 (from registry)
  total_active:         int
  total_dormant:        int
  total_silent:         int
  active_pct:           float       // the genre's "openness" — how much of the spectrum it uses
  suppression_pct:      float       // 1 - active_pct — how much it ignores
}
```

### The false positive problem (why this matters beyond efficiency)

A convention that is violated BY CONVENTION in a genre should not be loaded as a convention to check. Otherwise every noise track triggers Type 6 (Excision) on `bass_provides_foundation`, every ambient track triggers Type 7 (Inversion) on `drums_are_rhythmic`, and the Interpretive Engine drowns in false bridge signals.

The `expected_violations` field handles this. If a genre's definition includes violating a convention, that violation is not a finding — it's genre compliance. The suppression vector strips it out so that only UNEXPECTED violations reach the Interpretive Engine. This isn't just efficiency. It's signal hygiene.

---

## EXAMPLE GENRE VECTORS

### Breakcore

```
GenreSuppressionVector {
  genre_id: "breakcore"
  songs_analysed: 1               // Circle Pit only — initial calibration
  confidence: 0.3                 // low — needs more data

  entries: [
    // === BINARY ENGINE ===
    // Envelope
    { fp: "FP-E01", engine: "binary", status: "active",  μ: 12, σ: 4,   threshold: 10  },  // sharp attack — yes, breaks
    { fp: "FP-E02", engine: "binary", status: "dormant", μ: 2,  σ: 3,   threshold: 15  },  // gated decay — not a breakcore thing
    { fp: "FP-E03", engine: "binary", status: "dormant", μ: 500, σ: 800, threshold: 2000 }, // slow onset/sustain — rare
    { fp: "FP-E04", engine: "binary", status: "active",  μ: 1.2, σ: 0.2, threshold: 1.2 },  // bloom — 808 sub-bass bloom present
    { fp: "FP-E05", engine: "binary", status: "dormant", μ: 1,  σ: 0.3, threshold: 2   },  // two-stage — unusual in breakcore
    { fp: "FP-E06", engine: "binary", status: "dormant", μ: 0.8, σ: 0.3, threshold: 1.0 },  // reversed — occasionally
    { fp: "FP-E07", engine: "binary", status: "silent",  μ: 0,  σ: 0,   threshold: 3   },  // sidechain pump — not a breakcore technique
    { fp: "FP-E08", engine: "binary", status: "dormant", μ: 0.3, σ: 0.5, threshold: 0.5 },  // sustained micro-variation — rare

    // Dynamics
    { fp: "FP-D01", engine: "binary", status: "dormant", μ: 5,  σ: 3,   threshold: 15  },  // high crest — brick-wall limited
    { fp: "FP-D02", engine: "binary", status: "dormant", μ: 6,  σ: 2,   threshold: 8   },  // moderate crest — unlikely
    { fp: "FP-D03", engine: "binary", status: "active",  μ: 5,  σ: 1.5, threshold: 4   },  // low crest — yes, expected
    { fp: "FP-D04", engine: "binary", status: "active",  μ: 3.5, σ: 0.5, threshold: 4  },  // brick-wall — Circle Pit 3.1
    { fp: "FP-D05", engine: "binary", status: "dormant", μ: 3,  σ: 2,   threshold: 6   },  // section contrast — relentless
    { fp: "FP-D06", engine: "binary", status: "active",  μ: 2.5, σ: 0.5, threshold: 2.0 },  // relentless escalation — defining

    // HPSS
    { fp: "FP-H01", engine: "binary", status: "active",  μ: 0.55, σ: 0.15, threshold: 0.5 }, // hi-mid percussive — yes but variable!
    { fp: "FP-H02", engine: "binary", status: "active",  μ: 0.45, σ: 0.15, threshold: 0.6 }, // hi-mid harmonic — Circle Pit violation zone
    { fp: "FP-H03", engine: "binary", status: "active",  μ: 0.7, σ: 0.1,  threshold: 0.6 },  // sub-bass harmonic — yes, pitched bass
    { fp: "FP-H04", engine: "binary", status: "dormant", μ: 0.3, σ: 0.1,  threshold: 0.5 },  // sub-bass percussive — rare
    { fp: "FP-H05", engine: "binary", status: "dormant", μ: 0.45, σ: 0.05, threshold: 0.4 }, // HPSS ambiguous — possible at fusion

    // Vocal
    { fp: "FP-V01", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 0.5   },  // vocal foreground — instrumental genre
    { fp: "FP-V02", engine: "binary", status: "dormant", μ: 0.1, σ: 0.2, threshold: 0.3 }, // vocal as texture — sometimes sampled
    { fp: "FP-V03", engine: "binary", status: "active",  μ: 0.9, σ: 0.1, threshold: 0.5 },  // no vocal — yes, typically instrumental
    { fp: "FP-V04", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 0.3   },  // vocal non-address — no vocal to not-address

    // Temporal
    { fp: "FP-T01", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 80   },  // slow tempo — never
    { fp: "FP-T02", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 140  },  // standard tempo — never
    { fp: "FP-T03", engine: "binary", status: "active",  μ: 165, σ: 10, threshold: 140 }, // fast tempo — yes, lower breakcore range
    { fp: "FP-T04", engine: "binary", status: "active",  μ: 185, σ: 15, threshold: 180 }, // extreme tempo — yes, defining
    { fp: "FP-T05", engine: "binary", status: "active",  μ: 0.85, σ: 0.1, threshold: 0.8 }, // regular grid — yes, locked
    { fp: "FP-T07", engine: "binary", status: "active",  μ: 0.6, σ: 0.3, threshold: 0.3 },  // irregular meter — Venetian Snares 7/4
    { fp: "FP-T09", engine: "binary", status: "active",  μ: 6, σ: 2, threshold: 4     },  // high onset density — yes
    { fp: "FP-T10", engine: "binary", status: "active",  μ: 7, σ: 3, threshold: 8     },  // extreme density — Circle Pit zone

    // (remaining fingerprints follow same pattern — abbreviated here)

    // === CULTURAL ENGINE ===
    // Convention loading: entrenchment below 0.15 = suppressed
    // All 10 universals load (lowest is vocals_are_foreground at +0.2)
    // Expected violations: none for standard breakcore
    //   (Circle Pit's violations are UNEXPECTED — that's why they're findings)

    // === PERCUSSION MODULE ===
    { fp: "percussion_active",  engine: "percussion", status: "active"  },  // yes, breaks
    { fp: "ghost_note_test",    engine: "percussion", status: "dormant" },  // prior low for breakcore
    { fp: "pairwise_ratios",    engine: "percussion", status: "active"  },  // yes, multiple elements

    // === FELTNESS MODULE ===
    { fp: "gesture_sub_bass",   engine: "feltness",   status: "active"  },  // sub-bass shadow
    { fp: "gesture_hi_mid",     engine: "feltness",   status: "active"  },  // break transients
    { fp: "gesture_high",       engine: "feltness",   status: "dormant" },  // high band less relevant
    { fp: "polling_rate",       engine: "feltness",   status: "active",
      note: "1Hz standard — breakcore events are fast enough to sustain continuous diff" },

    // === INTERPRETIVE ENGINE ===
    { fp: "bridge_type_1",      engine: "interpretive", status: "active"  },  // concealment possible
    { fp: "bridge_type_2",      engine: "interpretive", status: "dormant" },  // compensation unlikely
    { fp: "bridge_type_3",      engine: "interpretive", status: "dormant" },  // contradiction — needs theme
    { fp: "bridge_type_6",      engine: "interpretive", status: "active"  },  // excision possible
    { fp: "bridge_type_7",      engine: "interpretive", status: "active"  },  // inversion — Circle Pit
  ]

  cultural_suppression_floor: 0.15
  expected_violations: []         // breakcore doesn't DEFINE itself by violating universals
                                  // (individual tracks might, but the genre doesn't)
  percussion_active: true
  ghost_note_prior: 0.1           // low — chopped breaks, not played drums

  suppressed_bridge_types: []     // all types remain possible

  total_fingerprints: 64
  total_active: 38
  total_dormant: 17
  total_silent: 9
  active_pct: 0.59
  suppression_pct: 0.41
}
```

### Ambient

```
GenreSuppressionVector {
  genre_id: "ambient"
  songs_analysed: 0               // no dictionary songs yet — pure prior
  confidence: 0.2

  entries: [
    // === BINARY ENGINE ===
    { fp: "FP-E01", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 10  },  // sharp attack — no percussion
    { fp: "FP-E02", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 15  },  // gated decay — no
    { fp: "FP-E03", engine: "binary", status: "active",  μ: 4000, σ: 2000, threshold: 2000 }, // slow onset/sustain — defining
    { fp: "FP-E07", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 3   },  // sidechain — no
    { fp: "FP-E08", engine: "binary", status: "active",  μ: 1.5, σ: 0.8, threshold: 0.5 },  // sustained micro-variation — yes

    { fp: "FP-D01", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 15  },  // high crest — no transients
    { fp: "FP-D04", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 4   },  // brick-wall — no
    { fp: "FP-D06", engine: "binary", status: "dormant", μ: 1.2, σ: 0.3, threshold: 2.0 }, // escalation — occasionally

    { fp: "FP-H01", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 0.5 },  // hi-mid percussive — no drums
    { fp: "FP-H03", engine: "binary", status: "active",  μ: 0.75, σ: 0.1, threshold: 0.6 }, // sub-bass harmonic — drones

    { fp: "FP-V01", engine: "binary", status: "dormant", μ: 0.15, σ: 0.2, threshold: 0.5 }, // vocal — sometimes
    { fp: "FP-V03", engine: "binary", status: "active",  μ: 0.8, σ: 0.15, threshold: 0.5 }, // no vocal — usually

    { fp: "FP-T01", engine: "binary", status: "active",  μ: 60, σ: 15, threshold: 80  },  // slow tempo — if any
    { fp: "FP-T05", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 0.8 },  // regular grid — no beat
    { fp: "FP-T08", engine: "binary", status: "active",  μ: 0.2, σ: 0.1, threshold: 0.4 }, // free time — yes
    { fp: "FP-T09", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 4   },  // high density — no
    { fp: "FP-T10", engine: "binary", status: "silent",  μ: 0, σ: 0, threshold: 8   },  // extreme density — no

    { fp: "FP-R03", engine: "binary", status: "active",  μ: 0.8, σ: 0.1, threshold: 0.5 }, // through-composed — yes

    // === CULTURAL ENGINE ===
    // Most universals suppressed via expected_violations

    // === PERCUSSION MODULE ===
    { fp: "percussion_active",  engine: "percussion", status: "silent"  },  // no drums — module off

    // === FELTNESS MODULE ===
    { fp: "gesture_sub_bass",   engine: "feltness",   status: "active"  },  // drones are felt
    { fp: "gesture_hi_mid",     engine: "feltness",   status: "silent"  },  // no transients to feel
    { fp: "polling_rate",       engine: "feltness",   status: "active",
      note: "reduce to 0.1Hz after first 10s — acclimatisation is fast in ambient" },

    // === INTERPRETIVE ENGINE ===
    { fp: "bridge_type_6",      engine: "interpretive", status: "dormant" },  // excision unlikely
    { fp: "bridge_type_7",      engine: "interpretive", status: "dormant" },  // inversion unlikely
  ]

  cultural_suppression_floor: 0.15
  expected_violations: [
    "universal.drums_are_rhythmic",
    "universal.temporal_regularity",
    "universal.dynamic_emphasis",
    "universal.structure_has_sections"
  ]
  percussion_active: false
  ghost_note_prior: 0.0

  suppressed_bridge_types: [6, 7]   // no conventions to violate after expected_violations removed

  total_fingerprints: 64
  total_active: 18
  total_dormant: 12
  total_silent: 34
  active_pct: 0.28
  suppression_pct: 0.72            // ambient suppresses 72% of fingerprints — that IS ambient
}
```

### Rock (baseline — minimal suppression)

```
GenreSuppressionVector {
  genre_id: "rock"
  songs_analysed: 0
  confidence: 0.2

  // Rock is the baseline genre — it uses almost everything.
  // Most fingerprints are active because rock encompasses the standard
  // Western popular music conventions that the universals are built from.

  // Abbreviated — only showing suppressions, everything else is active:
  entries: [
    { fp: "FP-E07", engine: "binary", status: "dormant" },  // sidechain — not standard rock
    { fp: "FP-D04", engine: "binary", status: "dormant" },  // brick-wall — less extreme mastering
    { fp: "FP-D06", engine: "binary", status: "dormant" },  // relentless escalation — sections exist
    { fp: "FP-T04", engine: "binary", status: "silent"  },  // extreme tempo — rock caps ~180
    { fp: "FP-T10", engine: "binary", status: "silent"  },  // extreme density — no
    { fp: "FP-P08", engine: "binary", status: "silent"  },  // tracker precision — not rock production
  ]

  cultural_suppression_floor: 0.15
  expected_violations: []           // rock defines the conventions, it doesn't violate them
  percussion_active: true
  ghost_note_prior: 0.5             // moderate — live drummers use ghost notes

  suppressed_bridge_types: []

  total_fingerprints: 64
  total_active: 55
  total_dormant: 5
  total_silent: 4
  active_pct: 0.86
  suppression_pct: 0.14             // rock suppresses only 14% — it's the broadest genre
}
```

---

## THE SUPPRESSION VECTOR IS A GENRE SIGNATURE

Look at the `active_pct` across genres:

```
rock:       0.86  — broadest. Uses almost everything. The baseline.
breakcore:  0.59  — selective. Heavy temporal and dynamic use, suppresses vocal/subtle.
ambient:    0.28  — narrowest. Most of the spectrum is irrelevant. The genre IS suppression.
```

This number — the fraction of fingerprints a genre actively checks — is itself a genre descriptor. It measures how much of Music's total vocabulary a genre uses. Broad genres (rock, pop, R&B) have high `active_pct` because they inherit most conventions. Narrow genres (ambient, drone, noise) have low `active_pct` because they define themselves by what they exclude.

In genomic terms: `active_pct` is the gene expression ratio. Same genome (64 fingerprints), different expression profile. Genre as cell type. The suppression vector IS the epigenetic state.

And when two genres have similar suppression vectors — similar shapes of what they ignore — they are sonically proximate on the karyotype terrain, regardless of their cultural lineage. Ambient and drone might have unrelated ancestry but nearly identical suppression shapes. That proximity IS the terrain.

---

## THE FLYWHEEL: SUPPRESSION LEARNS

The suppression map starts from priors (genre conventions, physics constraints) but improves with data. Every analysis contributes:

```
SuppressionLearning {
  // After each song analysis:
  for each fingerprint F in suppression profile:
    if F.status == "active" AND F.measured_value < noise_floor:
      F.null_count += 1
      if F.null_count > N (e.g. 20 songs in this genre):
        F.status = "dormant"  // promote to suppression
        log: "FP-{id} demoted to dormant for {genre} after {N} null readings"

    if F.status == "dormant" AND F.measured_value > threshold:
      F.status = "active"     // demote from suppression
      F.null_count = 0
      emit SurpriseSignal     // the finding is amplified
      log: "FP-{id} REACTIVATED in {genre} — surprise signal"

    if F.status == "silent" AND F.measured_value > noise_floor:
      // This shouldn't happen. Something is wrong.
      // Either the genre classification is wrong, or the physics model is wrong,
      // or there's an anomaly in the audio.
      emit AnomalyAlert
      log: "FP-{id} fired from SILENT in {genre} — anomaly"

  // The suppression map converges over time:
  // More songs → tighter distributions → more confident suppression.
  // This is the same flywheel as the entrenchment curves in genomic-frame.md.
  // Every analysis tightens the system's model of what's normal.
}
```

---

## RELATIONSHIP TO EXISTING ARCHITECTURE

### The suppression map reads from:
- **Fingerprint Registry** — the 64 fingerprints that can be suppressed
- **Genre-Fingerprint Map** — which fingerprints are expected per genre (●/○/△/✱ markers already imply suppression: a fingerprint not assigned to a genre is a suppression candidate)
- **Shared Protocol** — SpectralRoster roles (determines which bands have content)
- **Web Engine** — genre confirmation, production credits (vocal presence, instrument inventory)
- **Genomic Frame** — entrenchment values (low entrenchment → suppression candidate)

### The suppression map feeds into:
- **Binary Engine** — skip silent/dormant measurements
- **Cultural Engine** — skip low-entrenchment conventions
- **Percussion Module** — skip elements with no onsets
- **Feltness Module** — skip bands below somatic weight threshold
- **Activation Module** — additional dampening on deep-water readings
- **Interpretive Engine** — prune impossible bridge hypotheses

### The suppression map does NOT replace:
- The fingerprint registry (which defines what to look for)
- The genre-fingerprint map (which assigns fingerprints to genres)
- The convention bank (which defines what to check for violations)
- Any engine's core measurement logic

It sits alongside these as a filter: "before you ask this question, check whether the answer is structurally possible."

---

## OPEN QUESTIONS

1. ~~**Suppression granularity.**~~ **RESOLVED (11 Feb 2026).** Per-genre. Each genre emits a `GenreSuppressionVector` that tells every engine what to check. The vector is the genre's negative fingerprint — its epigenetic state. Per-song refinement happens via the flywheel (learning from null readings within the genre).

2. **Suppression inheritance.** If breakcore inherits from jungle inherits from rave, does the suppression map inherit too? A convention suppressed in rave might be active in breakcore (which violates rave conventions deliberately). Inheritance should be additive for *active* fingerprints but not for *suppression* — each genre's suppression is its own.

3. **The edge of suppression.** The ✱ (violation) marker in genre-fingerprint-map.md means a fingerprint is notable for its *absence* in a genre. Is "notable absence" the same as "suppressed"? Not quite — a notable absence is a finding ("this genre lacks X"). A suppression is an efficiency choice ("don't check for X"). The difference: notable absences should still be checked once (to confirm the absence), then suppressed for subsequent songs in the same genre.

4. **Suppression vs the Genomic Frame's silenced genes.** Epigenetic silencing (Phase 8 in the convention lifecycle) and suppression are related but distinct. A silenced convention is one that WAS active and has been culturally muted. A suppressed fingerprint is one that the system has learned not to poll. They overlap when a culturally silenced convention is also suppressed in the polling map — but a fingerprint can be suppressed without having been culturally active (physics constraints), and a convention can be silenced without being suppressed (the system might still check, hoping for reactivation).

5. **Minimum active threshold.** Is there a floor below which too much suppression makes the analysis unreliable? If 60% of fingerprints are suppressed for a genre, the analysis is fast but blind. Proposal: minimum 40% of fingerprints must remain active for any genre. Below that, the genre classification may be too narrow.

---

---

## THE SUPPRESSION GRIDLINE

The gridline is the x-axis schema for the suppression waveform. It fixes the order of fingerprints so that every genre plots on the same axis. The ordering principle: **most genre-differentiating fingerprints first, least last.** A fingerprint that swings between active and silent across genres carries more information than one that's always active everywhere.

This ordering is draft — it can and will be rearranged as more genre vectors are plotted. The positions are not sacred. The principle is.

### Five vertical bounds

```
─ ─ ─ ─ ─ ─ ─ ─ ─  ABOVE CEILING  (surprise overflow — discovery zone)
═══════════════════  CEILING
                     active zone (fingerprint fires reliably)
───────────────────  CENTRE (threshold)
                     sub-threshold zone (fingerprint exists but doesn't fire)
═══════════════════  FLOOR
                     dormant zone (fingerprint rarely appears, polled at low freq)
═══════════════════  SUBFLOOR (silent — structurally absent, not polled)
```

Position on the y-axis IS status. No labels needed. Where the dot sits tells you what it is.

### The 64 positions

```
SUPPRESSION GRIDLINE v0.1 — ordered by genre-differentiation power (rough)

Pos  FP-ID    Name                     Category    Why it's here (front = high differentiation)
───  ───────  ───────────────────────   ─────────   ──────────────────────────────────────────────
 1   FP-T04   extreme tempo            Temporal    S in rock, S in ambient, A in breakcore. Maximum split.
 2   FP-V01   vocal foreground         Vocal       S in breakcore, A in rock, D in ambient. Instrumental vs vocal.
 3   FP-T08   free time                Temporal    A in ambient, S in breakcore, S in rock. Grid vs free.
 4   FP-E03   slow onset               Envelope    A in ambient, D in breakcore, D in rock. Percussive vs sustained.
 5   FP-D06   relentless escalation    Dynamics    A in breakcore, D in ambient, D in rock. Breakcore marker.
 6   FP-T10   extreme density          Temporal    A in breakcore, S in ambient, S in rock. Tonal threshold.
 7   FP-D04   brick-wall               Dynamics    A in breakcore, S in ambient, D in rock. Loudness war.
 8   FP-T01   slow tempo               Temporal    S in breakcore, A in ambient, D in rock. Tempo family.
 9   FP-H02   hi-mid harmonic          HPSS        A in breakcore (fusion!), S in ambient, A in rock (differently).
10   FP-E07   sidechain pump           Envelope    S in breakcore, S in ambient, D in rock. EDM-specific.
11   FP-T09   high onset density       Temporal    A in breakcore, S in ambient, A in rock (lower).
12   FP-D05   section contrast         Dynamics    D in breakcore, D in ambient, A in rock. Structural.
13   FP-R03   through-composed         Structure   A in breakcore, A in ambient, D in rock. Linear vs sectional.
14   FP-R04   sample-based             Structure   A in breakcore, S in ambient, D in rock. Material source.
15   FP-V02   vocal texture            Vocal       D in breakcore, D in ambient, D in rock. But swings wildly in electronic.
16   FP-E04   bloom                    Envelope    A in breakcore, D in ambient, D in rock. 808 marker.
17   FP-X04   independent layers       Cross-band  D in breakcore, S in ambient, D in rock. Jungle/DnB.
18   FP-X02   shadow bass              Cross-band  A in breakcore, D in ambient, D in rock. Tethered bass.
19   FP-P08   tracker precision        Production  D in breakcore, S in ambient, S in rock. Electronic subgenre.
20   FP-R02   build-drop               Structure   D in breakcore, S in ambient, D in rock. EDM architecture.
21   FP-T03   fast tempo               Temporal    A in breakcore, S in ambient, A in rock (some).
22   FP-T07   irregular meter          Temporal    A in breakcore, S in ambient, D in rock. Odd meters.
23   FP-H01   hi-mid percussive        HPSS        A in breakcore (variable!), S in ambient, A in rock.
24   FP-D03   low crest                Dynamics    A in breakcore, S in ambient, D in rock. Compression.
25   FP-E01   sharp attack             Envelope    A in breakcore, S in ambient, A in rock. Percussive default.
26   FP-E02   gated decay              Envelope    D in breakcore, S in ambient, D in rock. 80s marker.
27   FP-S01   sub-bass dominant        Spectral    A in breakcore, A in ambient (drones), D in rock.
28   FP-P06   intentional distortion   Production  A in breakcore, S in ambient, D in rock. Aesthetic choice.
29   FP-R01   verse-chorus             Structure   S in breakcore, S in ambient, A in rock. Pop form.
30   FP-V04   vocal non-address        Vocal       S in breakcore, D in ambient, D in rock. SOPHIE territory.
31   FP-W01   mono                     Stereo      D in breakcore, D in ambient, D in rock. Varies per track.
32   FP-W03   wide stereo              Stereo      D in breakcore, A in ambient, D in rock. Spatial.
33   FP-R06   additive layering        Structure   D in breakcore, D in ambient, D in rock. Post-rock.
34   FP-E05   two-stage                Envelope    D in breakcore, S in ambient, D in rock. SOPHIE.
35   FP-E06   reversed                 Envelope    D in breakcore, D in ambient, D in rock. Transitional.
36   FP-H04   sub-bass percussive      HPSS        D in breakcore, S in ambient, S in rock. Noise-bass.
37   FP-H05   HPSS ambiguous           HPSS        D in breakcore, D in ambient, D in rock. Granular.
38   FP-P03   gated reverb             Production  D in breakcore, S in ambient, D in rock (80s: A).
39   FP-S06   spectral scoop           Spectral    D in breakcore, D in ambient, D in rock. Anti-voice.
40   FP-E08   sustained micro-var      Envelope    D in breakcore, A in ambient, D in rock. Analog drift.
41   FP-R05   loop-based               Structure   D in breakcore, A in ambient, D in rock. Repetitive.
42   FP-X03   envelope staging         Cross-band  D in breakcore, D in ambient, D in rock. Band timing.
43   FP-V03   no vocal                 Vocal       A in breakcore, A in ambient, D in rock. Instrumental.
44   FP-S07   sub/upper coupling       Spectral    A in breakcore, D in ambient, D in rock. Bass physics.
45   FP-T05   regular grid             Temporal    A in breakcore, S in ambient, A in rock. Quantized.
46   FP-T06   human feel               Temporal    S in breakcore, D in ambient, A in rock. Live feel.
47   FP-W05   hard-panned              Stereo      D in breakcore, S in ambient, D in rock. Spatial drama.
48   FP-X01   rhythm-heard-bass-felt   Cross-band  D in breakcore, S in ambient, A in rock. Default hierarchy.
49   FP-P07   detuned oscillators      Production  D in breakcore, A in ambient, D in rock. CS-80.
50   FP-S04   treble-bright            Spectral    D in breakcore, D in ambient, D in rock. Shimmer.
51   FP-T02   standard tempo           Temporal    S in breakcore, S in ambient, A in rock. The default.
52   FP-D01   high crest               Dynamics    D in breakcore, S in ambient, D in rock. Dynamic range.
53   FP-D02   moderate crest           Dynamics    D in breakcore, D in ambient, A in rock. The middle.
54   FP-H03   sub-bass harmonic        HPSS        A in breakcore, A in ambient, A in rock. Nearly universal.
55   FP-S02   bass-heavy               Spectral    D in breakcore, D in ambient, A in rock. Warm mixes.
56   FP-S03   mid-heavy                Spectral    D in breakcore, D in ambient, A in rock. Presence.
57   FP-S05   full-band even           Spectral    D in breakcore, D in ambient, D in rock. Flat spectrum.
58   FP-P01   natural room             Production  D in breakcore, D in ambient, A in rock. Space.
59   FP-P02   dry                      Production  A in breakcore, D in ambient, D in rock. Close.
60   FP-P04   analog warmth            Production  D in breakcore, D in ambient, D in rock. Vintage.
61   FP-P05   digital precision        Production  A in breakcore, D in ambient, D in rock. Clean.
62   FP-W02   moderate stereo          Stereo      D in breakcore, D in ambient, A in rock. Standard.
63   FP-W04   center-priority          Stereo      D in breakcore, D in ambient, A in rock. Mix convention.
64   FP-X05   frequency roles std      Cross-band  D in breakcore, D in ambient, A in rock. Everything normal.
```

---

## BREAKCORE — BINARY ENGINE — SUPPRESSION WAVEFORM

The first waveform plotted on the gridline. Breakcore's binary engine, after 5 songs (Circle Pit, Szamar Madar, Rossz, gabber-adjacent, Shitmat). Y-level indicates status + strength. Direction arrow shows trajectory after 5 tracks.

```
Legend:  ■ = position   ↑ = rising   ↓ = sinking   → = stable   ⚡ = was surprised
        ABOVE = surprise overflow   CEIL-CNTR = active   CNTR-FLOOR = sub-threshold
        FLOOR-SUBFL = dormant   SUBFL = silent

Pos  FP-ID    Y-Level         Dir  Note
───  ───────  ──────────────  ───  ─────────────────────────────────────────
 1   FP-T04   CEILING         ⚡↑  was demoted, surprised back. bimodal. wide σ.
 2   FP-V01   SUBFLOOR        →    silent. instrumental genre. flatline.
 3   FP-T08   SUBFLOOR        →    silent. breakcore has grid. flatline.
 4   FP-E03   FLOOR           →    dormant. slow onset rare. occasional pad.
 5   FP-D06   CEILING         ↑    defining. escalation IS breakcore. stable high.
 6   FP-T10   CEILING         ⚡↑  was demoted, surprised back. twin of pos 1.
 7   FP-D04   mid-ACTIVE      →    brick-wall present but not every track.
 8   FP-T01   SUBFLOOR        →    silent. never slow. flatline.
 9   FP-H02   mid-ACTIVE      ↓    the fusion line. Circle Pit pushed it high, others lower.
10   FP-E07   SUBFLOOR        →    silent. no sidechain in breakcore.
11   FP-T09   CEILING         →    high density. reliable. stable.
12   FP-D05   FLOOR           ↓    dormant. no sections. approaching silent.
13   FP-R03   upper-ACTIVE    →    through-composed. yes. breakcore is linear.
14   FP-R04   CEILING         →    sample-based. amen chops. always fires.
15   FP-V02   low-ACTIVE      ⚡↑  was dormant, Shitmat surprised it. newly promoted.
16   FP-E04   mid-ACTIVE      →    bloom present. 808-dependent. variable.
17   FP-X04   FLOOR           →    dormant. breakcore tethers bass, doesn't free it.
18   FP-X02   upper-ACTIVE    →    shadow bass confirmed. Circle Pit 0.481 correlation.
19   FP-P08   FLOOR           →    dormant. tracker precision possible but not confirmed.
20   FP-R02   FLOOR           →    dormant. no build-drop. relentless instead.
21   FP-T03   CEILING         →    fast tempo. always. stable.
22   FP-T07   mid-ACTIVE      →    irregular meter. Szamar 7/4 pushed it up. variable.
23   FP-H01   sub-CENTRE      ↑    hi-mid percussive — below threshold (fusion zone).
                                    mean climbing as non-Circle-Pit tracks enter.
24   FP-D03   mid-ACTIVE      →    low crest. compressed. consistent.
25   FP-E01   CEILING         →    sharp attack. every track. boring reliable.
26   FP-E02   FLOOR           →    dormant. gated decay not a breakcore move.
27   FP-S01   mid-ACTIVE      →    sub-bass dominant. present but varies per track.
28   FP-P06   upper-ACTIVE    →    distortion as aesthetic. clipping is texture.
29   FP-R01   SUBFLOOR        →    silent. no verse-chorus. flatline.
30   FP-V04   SUBFLOOR        →    silent. no vocals to non-address.
31   FP-W01   FLOOR           →    dormant. not characteristically mono.
32   FP-W03   FLOOR           →    dormant. not characteristically wide.
33   FP-R06   FLOOR           →    dormant. not additive — relentless.
34   FP-E05   FLOOR           →    dormant. two-stage rare.
35   FP-E06   FLOOR           →    dormant. reversed envelopes occasional.
36   FP-H04   FLOOR           →    dormant. sub-bass percussive rare.
37   FP-H05   FLOOR           →    dormant. HPSS ambiguous at fusion edges.
38   FP-P03   FLOOR           →    dormant. no gated reverb.
39   FP-S06   FLOOR           →    dormant. spectral scoop not characteristic.
40   FP-E08   FLOOR           →    dormant. sustained micro-var not breakcore.
41   FP-R05   FLOOR           →    dormant. not loop-based.
42   FP-X03   FLOOR           →    dormant. envelope staging not prominent.
43   FP-V03   CEILING         →    no vocal. instrumental. always fires.
44   FP-S07   mid-ACTIVE      →    sub/upper coupling. bass physics present.
45   FP-T05   upper-ACTIVE    →    regular grid. quantised. locked.
46   FP-T06   SUBFLOOR        →    silent. no human feel. machine-played.
47   FP-W05   FLOOR           →    dormant. not hard-panned.
48   FP-X01   FLOOR           ↓    rhythm-heard-bass-felt hierarchy disrupted. approaching silent.
49   FP-P07   FLOOR           →    dormant. no detuned oscillators.
50   FP-S04   FLOOR           →    dormant. not treble-bright.
51   FP-T02   SUBFLOOR        →    silent. never standard tempo.
52   FP-D01   FLOOR           →    dormant. high crest absent (too compressed).
53   FP-D02   FLOOR           →    dormant. moderate crest absent.
54   FP-H03   upper-ACTIVE    →    sub-bass harmonic. pitched bass. universal.
55   FP-S02   FLOOR           →    dormant. not bass-heavy (sub-bass dominant instead).
56   FP-S03   FLOOR           →    dormant. not mid-heavy.
57   FP-S05   FLOOR           →    dormant. not evenly distributed.
58   FP-P01   FLOOR           →    dormant. no natural room.
59   FP-P02   upper-ACTIVE    →    dry. close. tracker production.
60   FP-P04   FLOOR           →    dormant. not analog warm.
61   FP-P05   upper-ACTIVE    →    digital precision. yes.
62   FP-W02   FLOOR           →    dormant. not moderate stereo.
63   FP-W04   FLOOR           →    dormant. not center-priority (no vocals to center).
64   FP-X05   FLOOR           →    dormant. frequency roles not standard. breakcore violates this.
```

### The waveform drawn

```
                  GENRE: BREAKCORE — BINARY ENGINE — AFTER 5 TRACKS

ABOVE   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

         ⚡        ⚡
CEIL    ═■═══════■══■═════■══■═══════════■═════════════════■════════════════════════
         │     ↑  │  │  ■  │  │     ■     │  ■  ■  ⚡      │                  ■ ■ ■
         │     │  │  │  │  │  │     │     │  │  │  │       │                  │ │ │
CENTRE  ─│──■──│──│──│──│──│──│──■──│──■──│──│──│──│──■──■─│──────────────────│─│─│─
         │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │                  │ │ │
         │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │ ■■■■■■■■■■■■■■■ │ │ │
FLOOR   ═│══│══│══■══│══│══│══│══│══│══│══│══│══│══│══│══│═│═■■■■■■■■■■■■■■■═│═│═│═
         │  │  │     │  │  │  │  │  │  │  │  │  │  │  │  │ │                  │ │ │
SUBFL   ═│══■══■═════│══│══■══│══│══│══│══│══│══│══│══│══│═■═══════════■══════│═│═│═
         1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17    ...           54 59 61
        T04 V01T08E03D06T10D04T01H02E07T09D05R03R04V02E04X04              H03P02P05

         ←── genre splitters ──→←── differentiators ──→←── mid ──→←── baseline ──→
```

The shape: two spikes at positions 1 and 6 (the tempo/density twins, both surprised), a dip to subfloor at 2-3 (vocal and free time — structurally absent), back up to ceiling at 5 (escalation), then the active zone rides between centre and ceiling through the mid-positions with a long flat dormant stretch through positions 31-42, punctuated by a few active pops at 43 (no vocal), 54 (sub-bass harmonic), 59 (dry), 61 (digital precision).

The long flat section in the middle-right IS breakcore's suppression signature. That's the dormant zone — the stuff breakcore doesn't need. A rock waveform would ride high through that same stretch. An ambient waveform would flatline at the LEFT (where breakcore peaks) and ride high at positions like 3, 4, 40, 41 (free time, slow onset, micro-variation, loop-based).

Overlay them and you see the genre distance as vertical gap at every position.

---

## CULTURAL ENGINE GRIDLINE (15 positions)

The cultural engine doesn't measure fingerprints — it loads conventions and checks for violations. Its y-axis is entrenchment magnitude: CEILING = deeply entrenched (+0.8-1.0), CENTRE = moderate (+0.4-0.8), FLOOR = barely loaded (+0.15-0.4), SUBFLOOR = not loaded (<0.15 or doesn't exist for this genre). ABOVE CEILING = convention violated (the discovery signal).

Ordering: universals with the biggest cross-genre entrenchment swing first, then genre-specific conventions (maximally differentiating by definition), then stable universals.

```
CULTURAL ENGINE GRIDLINE v0.1

Pos  Convention                    Why it's here
───  ────────────────────────────  ─────────────────────────────────────────────
 1   U8:  vocals_are_foreground    +0.85 in rock → +0.2 in breakcore. Δ0.65. Biggest swing.
 2   U6:  dynamic_emphasis         +0.75 → +0.3 in breakcore. Δ0.45.
 3   U4:  sounds_decay_naturally   +0.85 → +0.4 in breakcore. Δ0.45.
 4   U10: structure_has_sections   +0.7 → +0.4 in breakcore. Δ0.3.
 5   G:   extreme_tempo            genre-specific. +0.9 in breakcore. absent elsewhere.
 6   G:   sample_atomization       genre-specific. +0.9 in breakcore. absent elsewhere.
 7   G:   relentless_escalation    genre-specific. +0.6 in breakcore. absent elsewhere.
 8   G:   no_address               genre-specific. +0.7 in breakcore. absent elsewhere.
 9   G:   sub_bass_shadow          genre-specific. +0.4 in breakcore. low confidence.
10   U1:  drums_are_rhythmic       +1.0 everywhere. threshold modified per genre.
11   U5:  frequency_roles_fixed    +0.85 everywhere. breakcore violates it (fusion).
12   U7:  temporal_regularity      +0.8 everywhere. breakcore: meter override.
13   U2:  rhythm_heard_bass_felt   +0.95 everywhere. softened in breakcore.
14   U3:  bass_provides_foundation +0.9 everywhere. rarely changes.
15   U9:  stereo_center_priority   +0.7 everywhere. least changed across genres.
```

### Breakcore — Cultural Engine Waveform

```
Pos  Convention               Y-Level         Dir  Note
───  ────────────────────────  ──────────────  ───  ────────────────────────────────
 1   U8:  vocals_foreground    FLOOR           ↓    +0.2 in breakcore. barely loaded. near suppression.
 2   U6:  dynamic_emphasis     FLOOR           →    +0.3. brick-wall is normal. barely checked.
 3   U4:  sounds_decay         mid-ACTIVE      →    +0.4. unnatural decay expected but still loaded.
 4   U10: structure_sections   mid-ACTIVE      →    +0.4. sections rare but convention still present.
 5   G:   extreme_tempo        CEILING         →    +0.9. genre-defining. stable.
 6   G:   sample_atomization   CEILING         →    +0.9. amen chops. stable.
 7   G:   relentless_escal     upper-ACTIVE    →    +0.6. present but not every track.
 8   G:   no_address           upper-ACTIVE    →    +0.7. characteristic but not absolute.
 9   G:   sub_bass_shadow      mid-ACTIVE      ↓    +0.4. might be artist-specific. watching.
10   U1:  drums_rhythmic       CEILING         →    +1.0. loaded at full. threshold raised to 12/sec.
11   U5:  freq_roles_fixed     CEILING         →    +0.85. loaded. and VIOLATED (fusion = discovery).
12   U7:  temporal_regularity  CEILING         →    +0.8. loaded. meter override active.
13   U2:  rhythm/bass_felt     CEILING         →    +0.95. loaded. softened threshold.
14   U3:  bass_foundation      CEILING         →    +0.9. loaded. bass is there.
15   U9:  stereo_center        upper-ACTIVE    →    +0.7. loaded. not much to check (no vocals).
```

The shape: positions 1-2 sit near the FLOOR (barely loaded — vocals and dynamics are suppressed in breakcore), a step up at 3-4 (moderate), then a spike to CEILING at 5-6 (genre-specific conventions are the strongest), a dip through 7-9, then the universals ride CEILING from 10-14 with a slight dip at 15.

The discovery channel (violations found) would spike ABOVE CEILING at position 11 (frequency_roles_fixed is loaded AND violated — the hi-mid fusion in Circle Pit). That's the interpretive engine's raw material.

---

## PERCUSSION MODULE GRIDLINE (10 positions)

The percussion module checks per-element timing, spacing, deviation patterns, and fusion thresholds. Its y-axis: CEILING = element present and actively analysed, CENTRE = element present but unremarkable, FLOOR = element absent or test returns null, SUBFLOOR = module off (no percussion detected).

```
PERCUSSION MODULE GRIDLINE v0.1

Pos  Check                    Why it's here
───  ───────────────────────  ─────────────────────────────────────────────
 1   fusion_test              S in rock, S in ambient, A in breakcore. Maximum split.
 2   ghost_note_discrimin     D in breakcore, S in ambient, A in rock. Different reasons.
 3   crash_ride_detection     D in breakcore, S in ambient, A in rock.
 4   percussion_active        S in ambient, A in breakcore/rock. On/off switch.
 5   hat_open_detection       varies. less prominent in breakcore.
 6   deviation_log_density    A in breakcore (deviations ARE content), D in rock.
 7   kick_detection           A everywhere with percussion.
 8   snare_detection          A everywhere with percussion.
 9   hat_closed_detection     A everywhere with percussion.
10   pairwise_ratios          A whenever percussion active.
```

### Breakcore — Percussion Module Waveform

```
Pos  Check                Y-Level         Dir  Note
───  ────────────────────  ──────────────  ───  ────────────────────────────────
 1   fusion_test           CEILING         →    5.7/sec snare. at fusion threshold. defining.
 2   ghost_note            FLOOR           →    dormant. chopped breaks have no ghost notes.
 3   crash_ride            FLOOR           →    dormant. not characteristic of breakcore.
 4   percussion_active     CEILING         →    yes. breaks everywhere.
 5   hat_open              mid-ACTIVE      →    present but less prominent than snare/kick.
 6   deviation_density     CEILING         →    deviations are high. fills, displacements, fusions.
 7   kick                  CEILING         →    present. sub-bass shadow anchor.
 8   snare                 CEILING         →    present. the main event. rapid fire.
 9   hat_closed            CEILING         →    present. thirtysecond positions.
10   pairwise_ratios       CEILING         →    complex timing. non-integer ratios (Szamar 7/4).
```

The shape: spike at position 1 (fusion — breakcore's signature), drop to FLOOR at 2-3 (ghost notes and crashes absent), back to CEILING at 4, dip at 5 (hat open), then solid CEILING from 6-10. An ambient waveform would be SUBFLOOR across all 10 positions (module off). A rock waveform would ride CEILING across most but drop at position 1 (no fusion) and spike at 2 (ghost notes present from live drumming).

---

## FELTNESS MODULE GRIDLINE (7 positions)

The feltness module measures somatic weight — what the body FEELS per frequency band. Its y-axis: CEILING = band is somatically dominant (the body locks onto this), CENTRE = band is present but not felt strongly, FLOOR = band is dormant (body doesn't register it), SUBFLOOR = band is structurally absent (nothing to feel).

```
FELTNESS MODULE GRIDLINE v0.1

Pos  Check                 Why it's here
───  ────────────────────  ──────────────────────────────────────────────
 1   gesture_hi_mid        A in breakcore/rock, S in ambient. Percussive feel.
 2   gesture_high          D in breakcore, S in ambient, D in rock. Least felt.
 3   polling_rate           1Hz breakcore, 0.1Hz ambient, 0.5Hz rock. Varies hugely.
 4   acclimatisation_rate  fast in ambient (constant), slow in breakcore (always new).
 5   gesture_sub_bass      A in breakcore, A in ambient, A in rock. Nearly universal.
 6   gesture_bass          A in most. mid range.
 7   gesture_mid           D in most. least somatic.
```

### Breakcore — Feltness Module Waveform

```
Pos  Check               Y-Level         Dir  Note
───  ───────────────────  ──────────────  ───  ────────────────────────────────
 1   gesture_hi_mid       CEILING         →    break transients. main somatic event.
 2   gesture_high         FLOOR           →    dormant. high band not somatically relevant.
 3   polling_rate         CEILING         →    1Hz. breakcore events sustain continuous diff.
 4   acclimatisation      FLOOR           ↓    slow. too much variation to acclimatise. never settles.
 5   gesture_sub_bass     CEILING         →    808 bloom. shadow bass. the body feels this.
 6   gesture_bass         mid-ACTIVE      →    present but sub-bass dominant.
 7   gesture_mid          FLOOR           →    dormant. mid band not prominent.
```

The shape: spike at 1 (hi-mid transients), drop at 2 (high band), spike at 3 (polling rate high), drop at 4 (no acclimatisation — breakcore keeps surprising), spike at 5 (sub-bass), then trailing down through 6-7. Zigzag pattern. An ambient waveform would be the inverse: low at 1, low at 2, low at 3 (reduced polling), spike at 4 (fast acclimatisation — drones settle in), spike at 5, trailing.

---

## INTERPRETIVE ENGINE GRIDLINE (7 positions)

The interpretive engine evaluates bridge hypotheses — what KIND of relationship exists between a convention and its violation. Its y-axis: CEILING = bridge type actively tested and expected to fire, CENTRE = bridge type possible but not likely, FLOOR = bridge type dormant (no evidence yet), SUBFLOOR = bridge type structurally impossible given genre's suppression profile.

```
INTERPRETIVE ENGINE GRIDLINE v0.1

Pos  Bridge Type               Why it's here
───  ────────────────────────  ────────────────────────────────────────────
 1   Type 7: Inversion         A in breakcore (fusion), D in ambient/rock. The big one.
 2   Type 6: Excision          A in breakcore, D in ambient, D in rock. Absent conventions.
 3   Type 5: Mutation          mid-A in breakcore, D elsewhere. Convention shape-shifting.
 4   Type 4: Displacement      mid-A in breakcore, D elsewhere. Temporal displacement.
 5   Type 1: Concealment       D in breakcore (demoted after 5 nulls), D elsewhere.
 6   Type 3: Contradiction     D everywhere. Rare. Requires thematic context.
 7   Type 2: Compensation      D everywhere. Rare. Requires multiple conventions.
```

### Breakcore — Interpretive Engine Waveform

```
Pos  Bridge Type          Y-Level         Dir  Note
───  ────────────────────  ──────────────  ───  ────────────────────────────────
 1   Type 7: Inversion    CEILING         →    Circle Pit's hi-mid fusion. defining finding.
 2   Type 6: Excision     CEILING         →    conventions absent (vocals, sections, decay).
 3   Type 5: Mutation     mid-ACTIVE      →    conventions mutated (decay → bloom, emphasis → wall).
 4   Type 4: Displacement mid-ACTIVE      →    temporal displacement of percussive elements.
 5   Type 1: Concealment  FLOOR           ↓    demoted. 5 nulls. breakcore doesn't conceal.
 6   Type 3: Contradiction FLOOR          →    dormant. needs thematic setup breakcore lacks.
 7   Type 2: Compensation FLOOR           →    dormant. needs multiple interacting conventions.
```

The shape: two peaks at 1-2 (inversion and excision — the active bridge types for breakcore), a step down at 3-4 (possible but not dominant), then a cliff to FLOOR at 5-6-7 (dormant, the subtle bridge types that breakcore has no use for). A jazz waveform might spike at positions 3-5 (mutation, displacement, concealment are jazz's bread and butter) while dropping at 1 (no inversion — jazz doesn't fuse percussion into tone the way breakcore does).

---

## THE COMPLETE STACK: BREAKCORE AS FIVE WAVEFORMS

```
Engine          Positions   Shape summary
──────────────  ─────────   ────────────────────────────────────────────
Binary          64          Jagged. High peaks at genre splitters, long dormant plateau
                            mid-right, surprise spikes from flywheel learning.
Cultural        15          U-shape. Low at front (suppressed universals), high at genre-
                            specific, high again at stable universals.
Percussion      10          Spike-dip-plateau. Fusion spike, ghost/crash dip, then solid
                            ceiling across elements.
Feltness         7          Zigzag. Hi-mid and sub-bass peak, everything else dormant.
                            High polling rate, no acclimatisation.
Interpretive     7          Cliff. Inversion and excision peak, mutation/displacement mid,
                            then cliff to dormant for subtle bridge types.
Vocal            7          NOT YET PLOTTED. 7 positions for FP-V05-V11 (Vocal Silhouette
                            Engine outputs). Separate from FP-V01-V04 which remain in the
                            binary 64. See module-vocal.md.

Total positions: 110 (binary 64 + cultural 15 + percussion 10 + feltness 7 + vocal 7 + interpretive 7)
```

Each engine's waveform is a left channel (suppression). Each gets a right channel (discovery) plotted on the same gridline. The stereo pair per engine, stacked six high, IS the complete genre analysis. 12 waveforms total. 110 positions per channel. 220 data points per genre.

Same schema, any genre. Overlay to compare. The vertical gap between two genres at any position on any engine IS the genre distance at that measurement. The sum of all gaps IS the total genre distance — and it decomposes into per-engine contributions, so you can say "these genres differ mostly in their percussion profile" or "the cultural suppression is identical but the feltness diverges."

---

## VOCAL ENGINE GRIDLINE (7 positions) — STUB

The vocal silhouette engine measures horizontal patterns in the vocal band: formant contours, phrase envelopes, sibilance coupling, pitch continuity, vibrato, formant movement, and vocal-percussion independence. Its y-axis: CEILING = measure strongly indicates human voice, CENTRE = measure inconclusive, FLOOR = measure absent or at noise level, SUBFLOOR = measure structurally impossible (instrumental genre, or physics prevents).

```
VOCAL ENGINE GRIDLINE v0.1

Pos  FP-ID    Name                     Why it's here
───  ───────  ───────────────────────   ─────────────────────────────────────────
 1   FP-V06   sibilance coupling       S in breakcore, A in rock/pop, D in ambient. Maximum genre split.
                                        Most voice-specific measure — no instrument produces this pattern.
 2   FP-V05   vocal phrase contour     S in breakcore, A in rock/pop, D in ambient. Breath-scale phrasing.
 3   FP-V09   formant movement         S in breakcore, A in rock/pop, D in ambient. Moving resonances.
 4   FP-V07   vocal pitch continuity   S in breakcore, A in rock/pop, D in ambient. Glide vs step.
 5   FP-V08   vocal vibrato            D everywhere. Most genre-dependent in depth, not presence.
 6   FP-V10   vocal-perc independence  S in breakcore/ambient, A in rock/pop. Bio clock vs beat grid.
 7   FP-V11   vocal continuity         D in breakcore, A in DnB/pop, D in rock. Coverage pattern.
```

### Liquid DnB — Vocal Engine Waveform (n=1, Phoneline only)

```
Pos  FP-ID    Y-Level         Dir  Note
───  ───────  ──────────────  ───  ────────────────────────────────────────
 1   FP-V06   mid-ACTIVE      →    sibilance coupling 0.320, lag +23ms. Consonant-vowel present.
 2   FP-V05   CEILING         →    26 phrases, 6.1s mean. Textbook breath phrasing.
 3   FP-V09   mid-ACTIVE      →    F1 continuity 0.715 (strong), mean 0.516 (breaks contaminate F2/F3).
 4   FP-V07   sub-CENTRE      →    glide ratio 2.1 — below voice threshold, contaminated by breaks.
 5   FP-V08   FLOOR           →    vibrato 5.8Hz peak but ratio 0.338 — subtle, DnB vocal style.
 6   FP-V10   CEILING         →    voice enters at 30s, persists continuously. Independent of DnB energy.
 7   FP-V11   CEILING         →    86% coverage, continuous shape. Voice IS the structural spine.
```

The shape: sibilance coupling and formant movement at mid-active (voice present but contaminated by dense production), phrase contour and vocal-percussion independence at ceiling (the horizontal features that survive the mix), vibrato at floor (DnB vocal style suppresses it), pitch continuity below centre (breaks drag it down). The pattern: the longer-timescale measures (phrases, independence, coverage) read clearly; the shorter-timescale measures (formants, pitch, vibrato) are degraded by production density.

A breakcore waveform would flatline at SUBFLOOR across all 7 positions (no vocal). A pop waveform would ride CEILING across most positions (voice dominates). An ambient-with-vocal waveform might show strong formant and vibrato (clean production) but weak phrase contour (ambient vocals are often textural, not phrase-structured).

**Pending:** Genre suppression vector entries for FP-V05-V11 in breakcore, ambient, and rock example vectors. Need vocal-present and vocal-absent tracks in each genre for calibration.

---

*Suppression map created: 11 February 2026*
*Restructured: 11 February 2026 — genre-keyed vectors replacing per-engine profiles. GenreSuppressionVector format defined. Three example vectors (breakcore, ambient, rock).*
*Gridline added: 11 February 2026 — 64-position universal fingerprint ordering. Five vertical bounds defined (above ceiling, ceiling, centre, floor, subfloor). Breakcore binary engine waveform plotted.*
*Vocal engine gridline added: 11 February 2026 — 7-position vocal fingerprint ordering. Liquid DnB waveform plotted (n=1, Phoneline). FP-V05-V11 entries pending for breakcore/ambient/rock suppression vectors.*
*Cross-references: fingerprint-registry.md, genre-fingerprint-map.md, genomic-frame.md, engine-cultural.md, module-vocal.md*
*Status: Draft. Gridline ordering is v0.1 — will be rearranged as more genre waveforms are plotted. Breakcore waveform based on 5 imaginary tracks (Circle Pit + 4 hypothetical). Vocal gridline based on 1 track (Phoneline).*
