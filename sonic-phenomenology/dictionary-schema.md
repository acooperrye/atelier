# DICTIONARY SCHEMA
## Rhythm Dictionary â€” Living Reference
## 2026-02-08

---

## PURPOSE

The Dictionary is NOT part of the versioning system. It is a continuously growing body of analyzed songs that all components read from. Adding a new entry never requires any component to update â€” each component simply has a larger pool of reference data available.

The Dictionary is the only thing that permanently grows. It grows through The Conversation.

---

## ENTRY STRUCTURE

```
DictionaryEntry {
  song_id:          string
  artist:           string
  title:            string
  
  fingerprint: {
    // 15-element conversational ground truth
    cv:         float
    grid:       float
    corr:       float
    attack:     float
    ad:         float
    flatMin:    float
    flatMax:    float
    hnr:        float
    silence:    float
    dynRange:   float
    sym:        float
    chromatic:  float
    sim:        float
    gallop:     float
    trail:      float
  }
  
  zones:            object          // categorical zone assignments
  engine_match:     float           // % self-match score
  genre:            string          // confirmed genre
  bridge_type:      string          // Concealment | Compensation | Contradiction | Refusal | Conceit
  bridge_span:      string          // short | medium | long
  somatic_report:   string          // Alex's documented somatic response
  validated:        bool
  
  // Cached engine outputs (for testing without re-running)
  cached_structural: StructuralDescriptor | null
  cached_context:    ContextDescriptor | null
  cached_activated:  ActivatedAxes | null
}
```

---

## CURRENT ENTRIES

| Song | Artist | Genre | Engine Match | Bridge Type | Validated |
|------|--------|-------|-------------|-------------|-----------|
| Black and Gold | Sam Sparro | Electronic/Synth-pop | 94% | Short span, high coherence | Yes |
| Only Human | Tides of Man | Post-rock | 73% | TBD | Partial |
| No Tears Left to Cry | Ariana Grande | Pop/Dance-pop | 52% | TBD | Partial |
| Music | underscores | Hyperpop | 68% | TBD | Partial |
| Everybody Wants to Rule the World | Tears for Fears | Synth-pop | Uncalibrated | Concealment | Yes |
| Von Dutch | Charli XCX | Hyperpop | TBD | TBD | No |
| Virtual Insanity | Jamiroquai | Acid jazz/Funk | TBD | TBD | No |
| Portrait of Tracy | Jaco Pastorius | Jazz | TBD | TBD | No |
| Phoneline | Pola & Bryson & Emily Makis | Liquid DnB | Uncalibrated | TBD (Conceit?) | Partial (re-entry complete, shape-first validated) |

### Ground truth fingerprints (conversational â€” DO NOT REPLACE with engine values):

```
Black and Gold:  cv:0.190 grid:0.52 corr:0.929 attack:226 ad:0.343 flatMin:0.023 flatMax:0.058 hnr:4.43 silence:0.018 dynRange:6.95 sym:5 chromatic:5.7 sim:0.79 gallop:0.95 trail:8377
Only Human:      cv:0.364 grid:0.13 corr:0.751 attack:697 ad:1.938 flatMin:0.045 flatMax:0.212 hnr:2.51 silence:0 dynRange:5.17 sym:1 chromatic:6.4 sim:0.77 gallop:0.44 trail:908
NTLTC:           cv:0.008 grid:0.11 corr:0.686 attack:68 ad:0.5 flatMin:0.0001 flatMax:0.14 hnr:9.38 silence:0.11 dynRange:13.76 sym:89 chromatic:11.4 sim:0.857 gallop:1.0 trail:9885
underscores:     cv:0.115 grid:0.81 corr:0.633 attack:300 ad:0.5 flatMin:0.0001 flatMax:0.069 hnr:8.82 silence:0.115 dynRange:31.4 sym:35 chromatic:11.3 sim:0.874 gallop:0.95 trail:4323
```

---

## HOW EACH COMPONENT USES THE DICTIONARY

### Binary Engine
- Reads fingerprints for **zone-based matching** and **novelty detection**
- "Is this value inside any known zone?" â€” more entries = more zones = better novelty sensitivity
- No recalibration needed when entries are added
- The engine just has a larger body of "known" to compare against

### Web Engine
- Reads existing analyses for **reference** when encountering similar songs
- Can use cached ContextDescriptors as **templates** for similar genre/era songs
- Bridge types inform what kind of context to prioritize in searches

### Activation Module
- Reads activation patterns to **calibrate expectations**
- "For synth-pop songs, we typically see 8-12 primary findings"
- This comes from the dictionary, not from hardcoded thresholds
- More entries per genre = better calibration of what's normal

### Bridge Module
- Reads bridge types and somatic reports for **pattern matching**
- "For Concealment bridges in electronic genres, the somatic prediction typically involves..."
- The bridge taxonomy grows here â€” new types emerge from new analyses
- Genre-calibrated bridge predictions improve as genre coverage grows

---

## GROWTH PRINCIPLES

1. **Entries are added through The Conversation.** Not through automated processes. Every entry represents a song that has been analyzed with human somatic feedback.

2. **Conversational ground truth takes precedence.** Engine fingerprints are calibration data. The values in the dictionary are from deep conversational analysis and are more accurate than any single engine pass.

3. **Adding an entry never breaks anything.** No component needs to recalibrate, re-version, or acknowledge the new entry. They just have more data to read.

4. **The dictionary doesn't interpret.** It stores facts: what was measured, what was found, what it felt like. Interpretation happens in the components that read it.

5. **Cached outputs enable testing.** When a component is updated, it can be tested against cached dictionary data without re-running other components.
