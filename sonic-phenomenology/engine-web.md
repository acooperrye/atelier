# WEB ENGINE
## Rhythm Dictionary â€” Component Spec
## 2026-02-08 Â· Version: independent

---

## PURPOSE

Retrieves and structures cultural context for a song. Produces inert descriptors â€” facts without structural grounding. Operates in two phases: genre confirmation (Phase A) and full context retrieval (Phase B).

Can be updated without touching any other component.

---

## INPUT

### Phase A (genre confirmation only):

```
WebGenreConfirmInput {
  artist:           string
  title:            string
  genre_hypothesis: GenreMatch[]    // from Binary Engine snapshot
}
```

### Phase B (full context):

```
WebFullInput {
  artist:           string
  title:            string
  committed_genre:  GenreCommitment // from Phase A
  binary_clusters:  CoProductionCluster[] | null  // candidate clusters to confirm
  broken_elements:  int[]           // element IDs that need web population
}
```

---

## OUTPUT

### Phase A output:

```
GenreConfirmation {
  confirmed:        bool
  corrected_genre:  string | null   // if binary was wrong
  confidence:       float
  source:           string          // URL/reference
}
```

### Phase B output:

```
ContextDescriptor {
  song_id:          string
  
  genre: {
    primary:        string          // committed in Phase A, carried through
    subgenre:       string | null
    era:            string
    baseline_id:    string
    sources:        string[]
  }
  
  thematic_vector: {
    dimensions: [
      {
        dimension:  string          // one of 10 meta-dimensions
        score:      float           // -1.0 to +1.0
        evidence:   string
        confidence: float
      }
    ]
    raw_themes:     string[]
    lyrical_summary: string
    sources:        string[]
  }
  
  production: {
    method:         "electronic" | "live" | "sample-based" | "hybrid" | "unknown"
    producer:       string | null
    studio:         string | null
    era_conventions: string[]
    notable_techniques: string[]
    credits:        object
    sources:        string[]
  }
  
  co_production_confirmations: [
    {
      cluster_id:   string
      confirmed:    bool
      evidence:     string
      lead_element: int
    }
  ]
  
  web_only_elements: [
    {
      element_id:   int             // 25, 49, 50, 52
      web_value:    string | float
      web_axes:     AxisReading[]
      sources:      string[]
    }
  ]
  
  cached:           bool
  cache_timestamp:  ISO datetime | null
  
  metadata: {
    engine_version: string
    timestamp:      ISO datetime
    source_count:   int
  }
}
```

---

## RE-ENTRY INTERFACE (called by Bridge Module)

The Bridge Module can request deeper contextual investigation when the somatic hypothesis needs cultural/sentiment grounding that the initial web pass didn't capture.

```
WebReEntryRequest {
  song_id:          string
  query_type:       "sentiment" | "context" | "production_detail" | "cultural"
  specific_query:   string          // what the Bridge needs to know
                                    // e.g. "what was the artist's personal context during recording?"
                                    // e.g. "how was this song received critically vs commercially?"
                                    // e.g. "what specific reverb/compression chain was used?"
  hypothesis_tag:   string          // what Bridge is trying to confirm
}

WebReEntryResponse {
  query_type:       string
  findings:         string          // structured response
  thematic_update:  DimensionScore[] | null  // updated scores if sentiment query
  production_update: object | null  // updated production data if detail query
  sources:          string[]
  confidence:       float
}
```

---

## READS FROM SHARED PROTOCOL
- Element Registry (which elements are broken/degraded and need web population)
- Genre Baseline Table (to confirm/correct binary hypothesis)
- Meta-Dimension Definitions (dimensions to score thematic content against)
- Co-Production Cluster Templates (what to look for in production credits)

## READS FROM DICTIONARY
- Existing analyses for reference (if analyzing a song similar to a dictionary entry)
- Bridge types and tension patterns (to know what kind of context matters)

## DOES NOT KNOW
- Any audio measurements
- What the waveform looks like
- Which axes are marked or unmarked

---

## SEARCH TARGETS

### Phase A (genre only):
- Wikipedia (genre classification)
- RateYourMusic, AllMusic, Discogs (genre tags)

### Phase B (full context):

**Genre** (already committed â€” carried through for reference):
- Wikipedia, RateYourMusic, AllMusic, Discogs

**Thematic content:**
- Genius (lyrics + annotations)
- Wikipedia (song background, album context)
- Critical reviews (Pitchfork, NME, etc.)
- Artist interviews mentioning the song

**Production method:**
- Wikipedia, AllMusic credits
- Discogs (detailed credits, formats)
- Producer interviews
- Studio databases
- Era-specific production convention references

### Re-entry (Bridge-directed):

**Sentiment queries:**
- Critical reception analysis
- Fan community responses
- Commercial vs critical reception gap

**Cultural context queries:**
- Artist biographical context during recording
- Historical/cultural moment
- Genre scene context

**Production detail queries:**
- Specific equipment/technique documentation
- Studio session reports
- Engineer/mixer interviews

---

## CACHING

Web results for the same artist+title don't change. The Web Engine caches its ContextDescriptor after Phase B. Benefits:
- If Binary Engine is updated and the same song is re-analyzed, cached ContextDescriptor reused â€” no repeat web scrape
- Cache can be manually invalidated if new web sources become available
- Re-entry responses are NOT cached (they're hypothesis-specific)

---

## WEB-ONLY ELEMENTS (Binary Engine can't measure these)

| # | Element | Web Source |
|---|---------|------------|
| 25 | Beat micro-peaks | N/A â€” discard entirely |
| 49 | Vocal presence | Track listing, credits, reviews |
| 50 | Instrument ID | Production credits, liner notes, interviews |
| 52 | Reverb estimation | Studio notes, era conventions, producer interviews |

---

## IMPROVEMENT ROADMAP (internal, no protocol changes needed)
- Write structured thematic extraction prompt ("Score lyrical content -1 to +1 on each of 10 dimensions, with evidence")
- Expand genre baseline set beyond 20 genres
- Improve production attribution logic (authored vs incidental detection)
- Add cultural context sources (scene databases, era timelines)
- Refine co-production confirmation logic (currently relies on finding specific production terms)
