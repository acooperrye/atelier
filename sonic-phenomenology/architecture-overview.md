# ARCHITECTURE OVERVIEW
## Rhythm Dictionary — Two-Engine Architecture
## 2026-02-08

---

## Component Map

```
┌─────────────────────────────────────────────────────────────┐
│                   SHARED PROTOCOL LAYER                      │
│  Element Registry · Genre Baselines · Meta-Dimensions        │
│  Co-Production Cluster Defs · Weight/Status Table            │
└──────────┬──────────────────────────────────┬────────────────┘
           │                                  │
     ┌─────▼──────┐                    ┌──────▼─────┐
     │   BINARY   │                    │    WEB     │
     │   ENGINE   │                    │   ENGINE   │
     │            │                    │            │
     │  audio in  │                    │ artist +   │
     │  struct out │                    │ title in   │
     │            │                    │ context out│
     └─────┬──────┘                    └──────┬─────┘
           │                                  │
           │    StructuralDescriptor          │    ContextDescriptor
           │                                  │
     ┌─────▼──────────────────────────────────▼────────────────┐
     │                  ACTIVATION LAYER                        │
     │  Three-filter scoring: genre × thematic × production     │
     │  Output: weighted, signed axis scores + tension markers  │
     └─────────────────────────┬───────────────────────────────┘
                               │
                               │    ActivatedAxes
                               │
     ┌─────────────────────────▼───────────────────────────────┐
     │                   BRIDGE ENGINE                          │
     │  Passes 3-5: Somatic inference → Hypothesis → Confirm   │
     │  Can call Binary Engine again at higher resolution       │
     └─────────────────────────┬───────────────────────────────┘
                               │
                               │    BridgeFindings
                               │
     ┌─────────────────────────▼───────────────────────────────┐
     │                  THE CONVERSATION                        │
     │  Passes 6-8: Convergence · Naming · Diagnosis            │
     │  Human somatic data enters here                          │
     └─────────────────────────────────────────────────────────┘
```

---

## File Index

| File | Contains | Load when... |
|------|----------|-------------|
| `engine-binary.md` | Binary Engine spec, I/O contracts, re-entry interface | Workshopping audio extraction |
| `engine-web.md` | Web Engine spec, I/O contracts, search targets | Workshopping context retrieval |
| `module-activation.md` | Activation Module spec, three-filter process, tier thresholds | Tuning filter weights or scoring |
| `module-bridge.md` | Bridge Module spec, Passes 3-5, re-entry logic, bridge types | Workshopping somatic inference |
| `shared-protocol.md` | Element Registry, Genre Baselines, Meta-Dimensions, Co-Production Templates | Cross-cutting changes (co-load with target file) |
| `dictionary-schema.md` | Dictionary entry structure, how each component reads it | Schema changes or entry validation |

---

## Phase Flow

**Phase A — Parallel Extraction** (no dependencies between engines)
- Binary Engine: audio → `StructuralDescriptor`
- Web Engine: artist + title → `ContextDescriptor`
- Optional handoff: Binary's `genre_hypothesis` can seed Web's genre confirmation (but Web can run without it)

**Phase B — Sequential Interpretation** (each step feeds the next)
1. Activation Module: `StructuralDescriptor` + `ContextDescriptor` → `ActivatedAxes`
2. Bridge Module: `ActivatedAxes` → somatic hypothesis → re-entry request → `BridgeFindings`
3. The Conversation: `BridgePresentation` + human somatic data → convergence assessment

---

## Versioning Contract

```
SystemVersion {
  protocol_version:     string      // changes here require both engines to acknowledge
  binary_engine_version: string     // independent
  web_engine_version:   string      // independent
  activation_version:   string      // tied to protocol version
  bridge_version:       string      // independent
  
  // Compatibility matrix
  // Binary Engine vX.Y works with Protocol vA.B+
  // Web Engine vX.Y works with Protocol vA.B+
  // If Protocol changes, both engines must update to acknowledge new fields
  // but can ignore new fields gracefully (additive changes don't break old engines)
}
```

### Breaking changes (require protocol version bump):
- Adding/removing/renaming an element in the Element Registry
- Changing axis pole definitions
- Adding/removing a meta-dimension
- Changing the ActivatedAxes output schema

### Non-breaking changes (engine-internal, no protocol bump):
- Binary Engine: fixing measurements, improving accuracy, adding resolution modes
- Web Engine: adding sources, refining thematic extraction, expanding genre set
- Activation Layer: tuning filter weights (0.2/2.0 thresholds)
- Bridge Engine: improving hypothesis generation, adding bridge types

---

## Testing Contracts

Each engine can be tested independently against the dictionary songs.

### Binary Engine test:
- Input: audio file for BG/OH/NTLTC/USC/EWTRTW
- Expected: fingerprint values within calibrated zones
- Score: self-match % against dictionary ground truth
- No web data needed

### Web Engine test:
- Input: artist + title for any dictionary song
- Expected: correct genre, thematic vector consistent with bridge analysis, production method matches known credits
- No audio data needed

### Activation Layer test:
- Input: pre-computed StructuralDescriptor + ContextDescriptor for a dictionary song
- Expected: primary findings match the documented bridge tensions for that song
- Both engines' cached outputs needed, but neither engine runs live

### Bridge Engine test:
- Input: pre-computed ActivatedAxes for a dictionary song
- Expected: somatic prediction aligns with Alex's documented somatic reports
- Hardest to automate — somatic ground truth is conversational

---

## Open Questions

1. **Parallel vs sequential?** Binary and Web can run simultaneously (web doesn't need audio data, binary doesn't need web data). The only dependency is the genre hypothesis handoff — binary can give web a head start on which genre to confirm. Worth running parallel?

2. **Activation Layer ownership.** It's currently defined as separate from both engines. Should it be a thin function that both engines know about, or a third module with its own version?

3. **Bridge Engine re-entry depth.** Currently allows one re-entry to Binary at higher resolution. Should it be allowed to loop (predict → check → revise → check again)? If so, what's the termination condition?

4. **Dictionary as shared state.** The dictionary entries are currently read-only reference for engines. When a new song is fully analyzed and added, should both engines auto-recalibrate, or is that a manual step?

5. **Web Engine caching.** For the same song, web results don't change. Should the Web Engine cache its ContextDescriptor so repeat analyses (e.g., after Binary Engine improvements) skip the web scrape?
