# ACTIVATION MODULE
## Rhythm Dictionary â€” Component Spec
## 2026-02-08 Â· Version: independent

---

## PURPOSE

Applies the three-filter scoring system where Binary and Web outputs meet. This is where inert structural measurements become meaningful findings. Its own versioned module so filter logic, weights, and thresholds can be tuned independently of either engine.

Can be updated without touching any other component.

---

## INPUT

```
ActivationInput {
  structural:       StructuralDescriptor    // from Binary Engine (Phase B)
  context:          ContextDescriptor       // from Web Engine (Phase B)
}
```

---

## PROCESS

For each element (1-54 active):

### 1. Engine Status Check
- Read `engine_status` and `engine_weight` from Element Registry
- If broken: substitute `web_only_elements` data from Web Engine (if available)
- If degraded: blend binary reading with web validation (web weight = 1 - engine_weight)

### 2. Genre Markedness Filter
**Question: Is this measurement notable for this genre, or is it the water?**
- Compare element reading against committed genre baseline ranges
- Within range â†’ weight Ã— 0.2 (water â€” suppress)
- Outside range â†’ weight Ã— 2.0 (signal â€” amplify)
- No genre data â†’ weight Ã— 1.0 (unchanged)
- Binary's own `markedness_flags` are a cross-check, not the authority
  (Activation Module applies genre markedness independently using the protocol)

### 3. Thematic Alignment Filter
**Question: Does the meaning reinforce or contradict this structural reading?**
- For each axis, compare pole direction against `thematic_vector`
- Reinforced: thematic content agrees â†’ sign = +1
- Inverted: thematic content contradicts â†’ sign = -1 (bridge tension marker)
- Neutral: thematic content unrelated â†’ sign = +1, weight Ã— 0.5

### 4. Production Attribution Filter
**Question: Is this an artistic choice or a technical artifact?**
- Cross-reference against `production.notable_techniques` and `production.era_conventions`
- Authored â†’ weight Ã— 1.0
- Incidental â†’ weight Ã— 0.1
- Unknown â†’ weight Ã— 0.7

### 5. Co-Production Clustering
- For confirmed clusters: lead element weight Ã— 2.0, subordinate weight Ã— 0.3
- For unconfirmed candidates: no modification (leave independent)

### 6. Final Score
```
axis_score = position Ã— sign Ã— (genre_w Ã— thematic_w Ã— production_w Ã— cluster_w Ã— engine_w)
```

---

## OUTPUT

```
ActivatedAxes {
  song_id:          string
  genre_confirmed:  string
  
  axes: [
    {
      element_id:   int
      axis_id:      string
      position:     float           // raw measurement (-1 to +1)
      final_score:  float           // after all filters
      sign:         +1 | -1
      weight:       float           // composite
      tier:         "primary" | "supporting" | "suppressed"
                    // |score| > 1.5 = primary
                    // 0.15 < |score| < 1.5 = supporting
                    // |score| < 0.15 = suppressed
      tension:      bool            // true if sign is negative
      cluster_id:   string | null
      
      filters: {
        genre_weight:      float
        thematic_weight:   float
        production_weight: float
        cluster_weight:    float
        engine_weight:     float
      }
    }
  ]
  
  primary_findings: AxisResult[]    // sorted by |final_score| desc
  tension_markers:  AxisResult[]    // all axes with sign = -1
  clusters:         ConfirmedCluster[]
  
  dimension_summary: [
    {
      dimension:    string          // one of 10 meta-dimensions
      score:        float           // -1 to +1
      contributing_axes: string[]
      tension_present: bool
    }
  ]
}
```

---

## READS FROM SHARED PROTOCOL
- Element Registry (weight overrides, status)
- Genre Baselines (markedness ranges)
- Meta-Dimension Definitions (how to aggregate axes into dimensions)
- Co-Production Cluster Templates (scoring rules for confirmed clusters)

## READS FROM DICTIONARY
- Existing songs' activation patterns (for calibrating what "typical" primary finding counts look like)

---

## TUNABLE PARAMETERS

All independent of engine versions. These are the knobs this module owns:

| Parameter | Current Value | Description |
|-----------|--------------|-------------|
| Water threshold | 0.2 | Multiplier for within-baseline readings |
| Signal threshold | 2.0 | Multiplier for outside-baseline readings |
| Primary tier threshold | 1.5 | \|score\| above this = primary finding |
| Suppression threshold | 0.15 | \|score\| below this = suppressed |
| Authored weight | 1.0 | Production attribution: intentional choice |
| Incidental weight | 0.1 | Production attribution: technical artifact |
| Unknown weight | 0.7 | Production attribution: no data |
| Co-prod lead multiplier | 2.0 | Cluster lead element amplification |
| Co-prod subordinate multiplier | 0.3 | Cluster subordinate element suppression |
| Thematic neutral discount | 0.5 | Weight multiplier when theme is unrelated |

### Future: per-genre tuning

Different genres may need different activation sensitivity. A heavily produced pop song may have more "authored" elements than a lo-fi recording. The Activation Module can develop genre-specific parameter sets as the dictionary grows, without requiring changes to either engine.

---

## THE KEY INSIGHT

This module exists because neither engine interprets. The Binary Engine measures bridge cables. The Web Engine tells you which direction they pull. This module applies the tension.

Without activation, the engine produces 216 unweighted, unsigned axis readings â€” a cloud of potential meanings with no way to select which ones are real for this song. The three filters are the selection mechanism.
