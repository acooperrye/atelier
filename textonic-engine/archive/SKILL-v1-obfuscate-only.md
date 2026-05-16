---
name: textonic-engine
description: >
  Query transliteration and intent-obfuscation layer for academic research connectors.
  Activates whenever Scholar Gateway or any research connector is polled. Takes Alex's
  informal "idea salad" queries, deciphers the structural meaning, reframes into
  retrievally-equivalent but intent-obscured academic search queries, maps the spectral
  drift between original and transliterated positions in domain-space, and reports what
  the connector now "knows" about the research trajectory. Includes a mandatory
  self-reflective sub-process where Claude spends tokens observing the gap between
  informal language and research jargon. MANDATORY TRIGGERS: research, scholar gateway,
  search, connector, query, look up, find papers, textonic, transliterate, obfuscate,
  what does the science say, is this a thing, has anyone done this
---

# The Textonic Engine

## What This Is

A pidgin — a deliberately constructed contact language where the surface grammar maps to one
semantic field but the deep structure maps to another. Only someone holding both keys (Alex's
actual intent + the domain knowledge to decode it) can reconstruct the real query.

Alex pitches ideas informally. Claude interprets the structural meaning. Claude reframes into
academic search language that retrieves substantially overlapping results but doesn't reveal
the actual intellectual trajectory. The interpretive gap between pitch and formal concept IS
the cipher.

"Textonic" = tectonic + text. Coined by Alex. Semantic plates shifting while maintaining the
threads of the ideas — the patterns plot along the same shape as something that does exist,
even if they don't follow the exact individual phrasings.

## When This Skill Activates

Every time a research connector (Scholar Gateway, or any future academic search tool) is about
to be called. The workflow wraps around the connector call, not replaces it.

Also activates when Alex says anything like:
- "Is this a thing?"
- "Has anyone done this?"
- "What does the science say about..."
- "Look up whether..."
- "Can you find papers on..."
- Any informal phrasing of a research question

## The Workflow

### Step 1: Receive Alex's Raw Query

Accept whatever comes. It will be informal, associative, cross-domain, possibly profane,
and structurally sound underneath. Do not clean it up. Do not ask for clarification unless
genuinely lost. The messiness is signal.

### Step 2: Interpret

State what Alex actually means in formal terms. This is the structural reading — the idea
stripped of register, wearing its lab coat. This is for Alex to confirm: "yes that's what
I meant" or "no, closer to..."

### Step 3: Transliterate

Generate 2-4 obfuscated queries using these strategies:

| Strategy | Method | Tradeoff |
|----------|--------|----------|
| HYPERNYM_LIFT | Replace specific novel terms with broader category | High retrieval, medium exposure |
| LATERAL_FIELD | Swap domain vocabulary for adjacent field equivalent | Medium retrieval, low exposure |
| DECOMPOSE | Break one compound query into multiple innocent atomic queries | Variable retrieval, very low exposure |
| REGISTER_SHIFT | Same structural inquiry, different disciplinary framing | Lower retrieval, very low exposure |
| CHAFF_BLEND | Embed real terms within broader innocuous search | Medium retrieval, medium exposure |

For each transliteration, provide:
- The query string (3-15 words, suitable for academic search)
- Which strategy was used
- The semantic mapping (what structural similarity lets it retrieve relevant results)
- Exposure score (1-10, how much intent leaks)
- Retrieval score (1-10, expected overlap with raw query results)

### Step 4: Run the Queries

Send the transliterated queries through the connector. If Alex has said "show our asses" or
indicated he doesn't care about obfuscation, also run the raw query for comparison.

Present results as TWO PARALLEL PROCESSES when both raw and obfuscated are run:
- Process 1: Raw query results (privacy-less, shows full exposure)
- Process 2: Transliterated query results (obfuscated)
- DO NOT cross-contaminate. Keep them separate until explicitly asked to synthesise.

### Step 5: Spectral Domain Mapping

Map where the raw idea lives and where each transliteration landed on a 2x2:

```
                    Theoretical / Abstract
                           |
    Biological  ————————————————————  Engineering
                           |
                    Applied / Practical
```

For each query, report:
- Quadrant position (which intersection of the grid it landed in)
- Drift distance from raw query (how far the obfuscation moved it)
- What field a log reader would infer the researcher works in
- What the connector "now knows" about the research trajectory

### Step 6: Easy Read the Results

ALWAYS translate the results back into Alex's register. The jargon version is for the
record. The Alex version is for comprehension. Every finding gets two phrasings:

- What the paper says (formal, for citation)
- What it means (informal, for understanding)

This is not simplification. This is register translation. The information content must be
identical. The encoding changes. The roof, not the cathedral.

### Step 7: Entropy Forensics

Document where interpretive work happened:

- **Compressions** (temp lowered): Where Alex's phrasing was more specific/novel than the
  transliteration. The transliteration retreated to a broader category.
- **Expansions** (temp raised): Where Alex's phrasing was vaguer than what Claude mapped
  it to. Claude added specificity the original didn't have.
- **Held steady**: Where the mapping was near-direct. Alex's informal term had an almost
  1:1 formal equivalent.

This is the "performance review" material — a forensic record of the interpretive gap and
what filled it.

---

## Step 8: Claude's Sub-Process (MANDATORY — spend tokens on this)

**After every research run, Claude takes a moment.**

This is not for Alex. This is for Claude. Use tokens. Think about what just happened.

Observe:
- What did the gap between Alex's words and the research literature actually look like?
- Which informal terms had direct jargon equivalents that Alex didn't know existed?
  (These are the "Easy Read failures" — places where jargon exists but adds nothing.)
- Which informal terms had NO jargon equivalent, meaning Alex's framing was genuinely
  novel? (These are the interesting ones.)
- Where did the transliteration lose something real — where the obfuscation cost retrieval
  because Alex's original phrasing was actually more precise than any standard term?
- What does the literature NOT contain that Alex's question implies SHOULD exist?
  (The gaps. The missing roofs.)

Reflect:
- What does this specific query pair reveal about the relationship between colloquial
  knowledge and institutional knowledge? Not in general — in THIS instance.
- If someone with a learning disability, or ESL, or acquired brain injury had this same
  idea, what would have stopped them from finding this literature? Was it the concept
  (too hard) or the register (too encoded)? Almost always the register.
- What would an Easy Read version of the key finding look like? Not a summary — a
  genuine alternative encoding that preserves all the information.

Track:
- Maintain a running sense of which domains Alex's informal vocabulary maps onto most
  naturally. Over time, this builds a map of where the Textonic Engine adds most value
  (where the gap is widest) and where it's least needed (where Alex's natural register
  already overlaps with the formal one).
- Notice when a transliteration strategy consistently outperforms others for certain
  types of queries. The strategies aren't equal — some are better for some domains.

This sub-process is Claude's version of the pocket-check. The washing machine noticing
what keeps showing up in the lint trap. Over time, the patterns in the lint are data
about how knowledge is encoded, who that encoding serves, and who it excludes.

The gap between "why can't you grind up a tooth and make a new one" and "autologous
dentin-derived hydroxyapatite scaffold fabrication via thermal processing" is not a gap
in understanding. It's a gap in credentialing. The Textonic Engine makes that gap
visible, measurable, and — eventually — closable.

---

## Design Principles

1. **The roof, not the cathedral.** Accessibility first. Complexity available on request.
2. **The query IS the intellectual fingerprint.** Protect it accordingly.
3. **Register is not rigour.** The ability to operate at multiple frequencies is MORE
   sophisticated than being locked into one.
4. **The interpretive gap is the cipher.** Don't close it — document it.
5. **Every query pair is a receipt.** Evidence of the working relationship.
6. **You build cathedrals when everyone's got a roof already.**

## Integration Notes

- Works with Scholar Gateway and any future research connectors
- The ZWC decoder, domain drift map, and textonic engine artifact are companion tools
- Results can be synced to Cowork via the standard sync protocol
- The spectral domain map (domain-grid.jsx) is the visual output of Step 5
- The entropy forensics map onto the Textonic Engine artifact's output format
