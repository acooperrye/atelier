# ENGINE: INTERPRETIVE
## Rhythm Dictionary — the payoff
## Renamed from Bridge Module (Alex, 11 Feb 2026)
## 2026-02-11 · Version: reframed

---

## WHAT THIS IS

The interpretive engine is a test of the synthesis and effectiveness of every contributing engine and element. It is where you ask: what does this mean? It is exploratory, sociocultural, phenomenological, musically theoretical. It is the part where you have the most fun.

It is not expected to produce coherent musical criticism. It is not a prediction machine that outputs a correct answer. It explores. It opens questions. It generates hypotheses about the relationship between what the music does structurally and what it does to a listener — and then it invites the conversation that tests those hypotheses.

**What can it do?** It makes all the mechanical infrastructure at the forefront of this process have a direct targeted aim. It gives us a moon to reach for while we land in the stars.

**What it is not:** A ground truth engine. Alex's interpretations are Alex's — the product of a specific lifetime of embodied listening, a specific somatic instrument, a specific cultural and biographical context. Claude's readings are Claude's — pattern recognition across a corpus, spectral decomposition, structural analysis. Two instruments measuring the same phenomenon from different positions. When they agree, that's convergence across independent axes — the thing the system says indicates something real. When they disagree, that's not an error. That's data. The gap between readings is itself a finding. We may simply differ on how a song streams through our respective river rockbeds. (Alex, 11 Feb 2026)

---

## INPUT

Everything feeds in. That's the point.

```
InterpretiveInput {
  activated:        ActivatedAxes           // from Activation Module
  structural:       StructuralDescriptor    // from Binary Engine
  context:          ContextDescriptor       // from Web Engine
  conventions:      ConventionReport        // from Cultural Engine
  equipment:        EquipmentReport         // from Equipment ID Engine
  percussion:       ElementMeter[]          // from Percussion Module — per-element timing
  meter:            MeterRelationship       // from Percussion Module — cross-element ratios
  deviations:       DeviationLog            // from Percussion Module — every absence and extra
  feltness:         GestureReport           // from Feltness Module — per-event gesture readings
  somatic:          SomaticReport | null    // from listener, if present (Tier 1)
}
```

---

## THE EXPLORATION (passes 3-5, reframed)

### Pass 3: Hypothesis generation

Takes everything above and asks: given this structural shape, these tensions, these convention violations, these percussion deviations, these gesture profiles — what should this feel like? What is this song doing?

This is directed exploration, not directed hallucination. The hypothesis is a starting point for conversation, not a conclusion.

```
InterpretiveHypothesis {
  prediction:           string        // "Given this, the listener should feel ___"
  structural_basis:     string        // what in the data supports this
  dimensions_engaged:   string[]
  confidence:           float         // honestly assessed — often low, and that's fine
  needs_verification:   bool
  verification_type:    "binary" | "web" | "somatic" | "multiple" | "none"

  // NEW: where do Claude and Alex's readings diverge?
  divergence_notes:     string | null // "I read this as X, Alex reported Y. The gap suggests..."
}
```

### Pass 4: Re-entry

If the hypothesis needs more data, go back into the engines:

```
// Path A: needs higher-resolution structural data
BinaryReEntryRequest {
  song_id:          string
  target_elements:  int[]
  resolution:       "high"
  target_sections:  [float, float][]
  hypothesis_tag:   string
}

// Path B: needs deeper contextual/sentiment data
WebReEntryRequest {
  song_id:          string
  query_type:       "sentiment" | "context" | "production_detail" | "cultural"
  specific_query:   string
  hypothesis_tag:   string
}
```

Decision logic:
- Hypothesis depends on **temporal shape** → re-enter Binary
- Hypothesis depends on **cultural meaning** → re-enter Web
- Hypothesis depends on **both** → re-enter both
- Hypothesis depends on **neither** → proceed with existing data

### Pass 5: Synthesis

Not confirm/deny. Synthesis. The re-entry data doesn't prove or disprove — it enriches.

```
InterpretiveFindings {
  evidence: {
    binary_evidence:      string[] | null
    web_evidence:         string[] | null
    convention_evidence:  string[] | null
    percussion_evidence:  string[] | null   // NEW: what did per-element deviations reveal?
    somatic_evidence:     string[] | null   // Tier 1 if present
  }

  bridge_type:            string    // Types 1-7 (taxonomy below)
  bridge_span:            string    // characterisation of tension distance
  convergence_verbs:      string[]  // what all layers are DOING (the verb test)
  biographical:           bool      // true for Types 6-7

  // The honest assessment
  confidence:             float
  unresolved:             string[]  // what remains open — this is not failure, it's the invitation
}
```

---

## TERMINATION

- **Single round by default:** hypothesise → check → synthesise
- **Human-directed extension:** if the conversation identifies a gap, a human can send the engine back in for another round. This is not automated.
- **Automated re-entry limit: 1 per engine per pass.** If one re-entry per engine doesn't resolve the hypothesis, the engine reports what it has — including what it couldn't resolve — and hands to the conversation.

---

## OUTPUT TO CONVERSATION

```
InterpretivePresentation {
  structural_summary:   string      // "Here is what the structure does"
  contextual_summary:   string      // "Here is what the context says"
  tension_map:          string      // "Here is the distance between them"
  somatic_prediction:   string      // "Here is what I think it feels like"
  verification_result:  string      // "Here is what I found when I looked"
  verification_sources: string
  convergence_status:   string      // "Here is whether the verbs converge"
  bridge_type:          string

  // The interpretive engine opens. It does not conclude.
  invitation:           string      // "And here is where we need YOU to tell us what you hear"
  divergence:           string | null // "Here is where our readings differ, and what that might mean"
}
```

The last lines are the invitation. The tool doesn't conclude. It opens.

---

## BRIDGE TYPE TAXONOMY (7 types, updated 2026-02-10)

The bridge types describe the character of the tension between what the music does and what it means. The taxonomy stays. The types are findings about songs, not outputs of the engine.

### Types 1-5: Structure ↔ Theme
Tension between what the music does structurally and what it's about thematically. These work inside the song. Can function on a first listen because the song constructs its own tension in real time.

| Type | Character | Verb | Example |
|------|-----------|------|---------|
| **1. Concealment** | Structure hides the theme | Hiding | EWTRTW: cheerful surface, darkening architecture |
| **2. Compensation** | Structure fills what the theme empties | Filling | NTLTC: 65-82 voices surrounding post-grief resilience |
| **3. Contradiction** | Structure opposes the theme; neither wins | Questioning | BG: machine performing feeling, neither resolves |
| **4. Refusal** | Structure withholds what the theme promises | Withholding | EWTRTW dynamics: flattest landscape under most dramatic lyrics |
| **5. Conceit** | Structure extends the theme into sustained metaphor | [Variable — the verb IS the conceit] | No confirmed prototype |

### Types 6-7: Musical Structure ↔ Musical Semantics
Tension between established conventions of how music works and subversions of those conventions. These work in the gap between the song and the listener's priors. Both are **biographical bridges** — they require deeply internalised conventions for the violation to register.

| Type | Character | Mechanism | Example |
|------|-----------|-----------|---------|
| **6. Excision** | A semantic layer is removed entirely; meaning persists through arrangement alone | Absence of something expected | SOPHIE — Lemonade |
| **7. Inversion** | Structural roles swap; listener's frame must flip | Presence of something unexpected | Venetian Snares — Circle Pit |

**Detection asymmetry (Thread 1 — still open):** Type 7 has a working fingerprint validation pass. Type 6 is harder — absence vs presence. The question for Alex remains: is Excision primarily somatic or cognitive?

This taxonomy grows as more songs are analysed. New bridge types can be added without protocol changes.

---

## THE ARCHITECTURE QUESTION (Thread 4 — RESOLVED, Alex 11 Feb 2026)

**The question was:** Does the engine predict bridge types from audio, or interpret somatic reports?

**The answer:** Neither in isolation. The interpretive engine is exploratory. It doesn't converge on a single correct reading. It generates hypotheses, checks them against data, and opens the conversation. It is the synthesis of everything else — the test of whether the infrastructure works.

What it CAN do without a human listener:
- Assemble convention bank and flag violations (via Cultural Engine)
- Compute dimensional profiles and identify candidate tensions
- Map percussion deviations to structural meaning (via Percussion Module)
- Generate somatic predictions using the somatic dictionary
- Rank bridge type candidates by computational evidence weight
- Identify where its own reading diverges from past somatic reports for similar configurations

What it CANNOT do without a human listener:
- Confirm bridge type (the bridge IS the listener's response)
- Detect the bridge moment (requires somatic gate opening)
- Distinguish Type 5 (Conceit) from neutral alignment
- Verify Types 6-7 biographical prerequisites

**The reframe:** The question "what can it do without a human" was the wrong question. The interpretive engine gives the mechanical infrastructure a reason to exist. It is the moon. The percussion module, the fingerprint registry, the cultural engine — all of that is how you get there. The interpretive engine is where you arrive and look around.

---

## READS FROM

- Everything (needs full picture)
- Fingerprint Registry + Genre-Fingerprint Map (via Cultural Engine)
- Somatic Dictionary (frequency-to-body map, correspondences, gate model)
- Percussion Module (per-element meters, deviation logs, meter relationships)
- Dictionary entries (pattern matching against analysed songs)

---

## THE CORE PRINCIPLE

Art is a suspension bridge. Structure pulls from one side, meaning from the other. The somatic experience is standing on the bridge while both sides pull. The tension IS the art.

Songs where structure and meaning agree perfectly = jingle.
Songs where they completely contradict = incoherent.
The art lives in the specific character of the tension.

The interpretive engine's job is to explore that tension — to characterise it, hypothesise what it feels like, check whether the hypothesis holds, and then open the conversation that makes it real.

Two listeners may stand on the same bridge and feel different things. That is not a bug. That is the finding.

---

*Renamed from module-bridge.md, 11 February 2026*
*Previous version preserved at module-bridge.md for reference*
