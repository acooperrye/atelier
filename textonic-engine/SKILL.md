---
name: textonic-engine
description: "Alex and/or Claude needs to separate sign from meaning, or position an idea on the semantic surface."
---

# The Textonic Engine

## What This Is

A semiotic/semantic processor. The engine that separates sign from meaning and operates
on them independently.

"Textonic" = tectonic + text. Coined by Alex. Semantic plates shifting while maintaining
the threads of the ideas — the patterns plot along the same shape as something that does
exist, even if they don't follow the exact individual phrasings.

The core operation is always the same: take an idea, identify its semiotic layer (the
signs — words, phonemes, surface grammar) and its semantic layer (the meaning — what it
actually refers to, what it connects to, what it's about). Then do something useful with
the split.

Three modes, one engine:

| Mode | What it does | When to use it |
|------|-------------|----------------|
| OBFUSCATE | Rebuilds a new semiotic around the same semantic. Protects the query. | Research queries through connectors |
| POSITION | Assigns the idea coordinates on a flat semantic surface. Position = meaning, not spelling. | Any time ideas need spatial organisation |
| PROTECT | Identifies which semantic distinctions are vulnerable to compression loss. Preserves attentional inertia. | Session boundaries, context limits, summarisation, any compression cycle |

These aren't separate skills. They're three applications of the same split. The engine
always starts the same way: receive an idea, separate the sign from the meaning. What
happens next depends on context.

---

## The Semiotic/Semantic Split

This is the engine's fundamental operation. Everything else depends on it.

**Semiotics** — the signs. The word "python." The phonemes. The spelling. The surface
features that survive compression because they're structurally simple.

**Semantics** — the meaning. Python-the-snake or Python-the-language. The deep features
that get lost in compression because they depend on context to resolve.

"Shiny Glock" is either the spectral phonics of a glockenspiel or it's a 9mm. Semiotically
identical. Semantically distant. After a compression cycle (summarisation, context window
truncation, session boundary), the semiotic survives but the semantic may not. The word
"Glock" is still there. The meaning — which Glock? — is gone unless something preserves
the context that resolved it.

That something is **attentional inertia**: the accumulated trajectory of what's been
discussed, what's been attended to, what semantic region the conversation has been
occupying. If you've been talking about percussion instruments for twenty minutes, "Shiny
Glock" is unambiguously the glockenspiel. The trajectory constrains the interpretation.
Lose the trajectory, lose the constraint.

The engine makes this split explicit, tracks it, and uses it.

### The Restoration Constraint (Monkey Jesus Avoidance)

The engine itself is a compression cycle. The semiotic/semantic split IS a compression —
you strip the sign to isolate the meaning. But signs carry meaning too. Register is
meaning. Informality is meaning. The gap between "why can't you grind up a tooth and make
a new one" and "autologous dentin-derived hydroxyapatite scaffold fabrication" is not just
a semiotic difference — the register tells you who's speaking, what their access path was,
what their relationship to the knowledge is. Strip the register and you've lost data while
thinking you preserved it.

This is the Monkey Jesus problem. An amateur restorer applies a uniform technique across
the entire surface without understanding what's underneath. The yellowed varnish gets
treated as damage, but some of it IS the painting. The patina is the provenance. The
craquelure tells the age. A good restorer examines each area and asks: what am I looking
at? What's original? What's accumulated? What — if anything — should I touch?

The engine is a restorer's brush, not a power washer. It must:

1. **Infer before acting.** Look at the field before picking up the swab. Is this idea
   tightly bound to its sign in a way that the binding itself carries meaning? If so,
   splitting them destroys something. Leave it.
2. **Continuously re-evaluate.** The field changes as you work on it. A split that was
   safe at position 1a might be destructive at position 7k because the depth has changed
   the relationship between sign and meaning.
3. **Know when not to split.** Some ideas live in their register. Alex's informal
   phrasing isn't always a semiotic shell around a formal semantic core — sometimes the
   informality IS the idea. "The medium that knows it's flat" isn't a casual phrasing of
   a formal concept. It IS the concept. The sign and the meaning are fused. Splitting
   them produces two dead halves.
4. **Treat its own output as a compression artefact.** Every split the engine performs
   produces a cleaned version (semantic) and a discarded version (semiotic residue). The
   residue is not garbage — it's the varnish. Keep it. It may be needed to verify the
   restoration later or to understand what was lost.

The engine is a stub of a much larger perceptual system. It does what it can see to do.
It does not pretend to see everything. When in doubt, it flags uncertainty rather than
producing a confident but wrong split. A yellowed area that might be original pigment
gets flagged, not stripped.

### The Delta Discipline

The engine proposes. It does not execute.

Every operation — every split, every position assignment, every compression flag — comes
back as a differential: here is the current state, here is the proposed next state, here
is what changes across the gap. The user orients themselves across the delta and approves
before anything moves.

This follows the same discipline as the repo architecture: propose a diff, review the
diff, merge the diff. No force-pushes to the semantic surface. The engine shows its
working — "I think 'python' at this point in the trajectory means the language, not the
snake, because the trajectory has been in engineering-space for six turns. Here's the
position I'd assign. Here's what the surface looks like before and after." The user
confirms or corrects.

Why this matters: meaning does have a shape. Each iteration of it occurs in a consistent
enough form that the engine will eventually pattern on it reliably. But we're not there
yet. The engine is a stub of a perceptual system that doesn't fully exist. It can see
the yellowed varnish but it can't always tell what's underneath. Until it can, it
proposes and waits. The restorer tests a small area, shows the conservator, gets the nod.
If the nod doesn't come, the swab goes down.

This won't be true forever. But it will be true for a long time.

---

## Mode 1: OBFUSCATE (Research Query Transliteration)

The original use case. Still works the same way. The split is used to rebuild a new
semiotic shell around the same semantic core, so research connectors log queries that
retrieve equivalent results but don't reveal the intellectual trajectory.

### Workflow

**Step 1: Receive.** Accept Alex's raw query. It will be informal, associative,
cross-domain, possibly profane, and structurally sound underneath. The messiness is signal.

**Step 2: Split.** Separate semiotic from semantic. State what Alex actually means in
formal terms — the idea stripped of register. For Alex to confirm or redirect.

**Step 3: Transliterate.** Generate 2-4 obfuscated queries using these strategies:

| Strategy | Method | Tradeoff |
|----------|--------|----------|
| HYPERNYM_LIFT | Replace specific novel terms with broader category | High retrieval, medium exposure |
| LATERAL_FIELD | Swap domain vocabulary for adjacent field equivalent | Medium retrieval, low exposure |
| DECOMPOSE | Break one compound query into innocent atomic queries | Variable retrieval, very low exposure |
| REGISTER_SHIFT | Same structural inquiry, different disciplinary framing | Lower retrieval, very low exposure |
| CHAFF_BLEND | Embed real terms within broader innocuous search | Medium retrieval, medium exposure |

For each: query string, strategy, semantic mapping, exposure score (1-10), retrieval
score (1-10).

**Step 4: Run.** Send transliterated queries through connector. If Alex says "show our
asses," also run raw query. Present as TWO PARALLEL PROCESSES — do not cross-contaminate.

**Step 5: Map.** Plot on the spectral domain grid (see Spectral Domain Mapping below).

**Step 6: Easy Read.** Translate results into Alex's register. Every finding gets two
phrasings: what the paper says (formal, for citation) and what it means (informal, for
understanding). This is not simplification. This is register translation. The roof, not
the cathedral.

**Step 7: Entropy Forensics.** Document the depth changes:

- **Compressions** (depth lost): Alex's phrasing was more specific/novel than the
  transliteration. The transliteration retreated to a broader category. In surface
  terms: moved from 7k back toward 7a.
- **Expansions** (depth gained): Alex's phrasing was vaguer than what Claude mapped
  it to. Claude added specificity. Moved from 7a toward 7k.
- **Held steady**: Near-direct mapping. Same position, same depth.

---

## Mode 2: POSITION (Semantic Surface Coordinates)

The split is used to assign ideas coordinates on a flat 2D semantic surface where position
reflects meaning, not spelling.

### The Flat Systems Surface

A two-dimensional plane. Ideas have positions on this plane based on what they MEAN, not
what they're CALLED. Position is determined by the semantic layer after the semiotic has
been stripped. Two ideas with the same word ("python") occupy different positions if they
mean different things. Two ideas with different words occupy the same position if they mean
the same thing.

### How Positioning Works

**Step 1: Receive.** Accept the idea, same as OBFUSCATE mode.

**Step 2: Split.** Separate semiotic from semantic. Identify the meaning-core independent
of the sign-shell.

**Step 3: Position.** Assign the idea a coordinate on the surface.

The coordinate has three components:
- **Grid position** (integer): Where on the 2D surface this idea sits relative to
  everything else currently on the surface. Computed from semantic distance to existing
  ideas. The grid is only as wide as the furthest semantic distance between ideas currently
  in play.
- **Depth** (a-z, a=surface, z=deepest): How specific this idea is within its semantic
  region. "Snakes" = 7a. "Carnivorous snakes" = 7k. "Molecular biology of elapid venom
  production" = 7y. Same grid position, increasing depth.
- **Sequence number**: When this idea arrived. The order matters for trajectory.

**Step 4: Record trajectory.** Append the new coordinate to the trajectory log. The
trajectory is the sequence of coordinates visited: 1a, 2a, 7a, 4a, 7k. This sequence IS
the attentional path. It IS the provenance record. It IS the attentional inertia in stored
form.

**Step 5: Report surface state.** After positioning, report:
- Current trajectory (the full coordinate sequence so far)
- Nearest neighbors on the surface (what's semantically close to the new idea)
- Surface expansion (did the grid need to grow to accommodate this idea?)
- Depth change (did this deepen an existing position or open a new one?)

### Surface Properties

The grid expands as ideas land on it. It's only ever as wide as the furthest semantic
distance between its contents. Cat at 1, dog at 2, snake at 7, rabbit at 4. The surface
is as wide as the distance from (cat, dog) to snake. Add "python the language" and the
surface might expand to 43 — because its semantic distance from snakes is large even
though the semiotic distance is zero.

The surface is append-only. Ideas subside (become dormant, lose elevation) but never
disappear. Depth only increases — you can go deeper into a position but you can't make
it shallower. The history of positions visited is permanent.

### Two-Factor Model

The trajectory and the content are two separate factors. The trajectory (1a, 2a, 7a, 4a,
7k) is the pattern — lightweight, shareable, semantically unspecific. It describes the
*shape* of thinking without containing the thinking itself. The content (what was actually
said at each position) is the substance — it lives in the user's context window.

Together they reconstruct the full ideation process. Apart, each is useful independently:
- Trajectory alone = ideation patterns, attentional fingerprint, training signal for how
  humans navigate semantic space
- Content alone = what was said, but not how it connected
- Together = full provenance, reproducible path through meaning-space with meaning at
  each stop

This separation is what makes the architecture useful for training without destroying the
uniqueness of the data produced. You can share trajectories without sharing content.

---

## Mode 3: PROTECT (Compression-Cycle Awareness)

The split is used to identify which semantic distinctions will survive a compression cycle
and which won't — then preserve the trajectory that resolves the ambiguity.

### When Compression Happens

Any time context is reduced:
- Session ends (solenoid close — ignition file is a compressed representation)
- Context window fills (model starts forgetting early turns)
- Summarisation (long conversation compressed to a brief)
- Handoff (context bridge between sessions or vehicles)
- Training data compression (fine-tuning from conversation logs)

### What Gets Lost

Semiotics survive compression. Semantics often don't. The word "Glock" survives in a
summary. The context that made it mean "glockenspiel" may not. The compression preserves
the sign and drops the meaning.

### How PROTECT Works

**Step 1: Scan.** Before a compression cycle, scan the current context for semiotic
collisions — places where the same sign maps to different meanings depending on context.
These are the vulnerable points.

**Step 2: Flag.** For each collision, report:
- The sign (the ambiguous word or phrase)
- The competing meanings (what it could refer to after compression)
- The trajectory that currently resolves it (which prior positions constrain the
  interpretation)
- Vulnerability score (1-10, how likely the distinction is to survive compression)

**Step 3: Preserve.** Emit the trajectory as compact notation that can be stored alongside
the compressed version. If the ignition file says "discussed Glock," the trajectory
annotation says "trajectory: 1a(instruments), 2a(percussion), 7a(metallophones),
4a(orchestral), 7k(glockenspiel)." The trajectory IS the attentional inertia. Store it
and the semantic survives the semiotic compression.

**Step 4: Verify on restoration.** When the compressed version is expanded (session
reopened, ignition cranked), check that the trajectory annotations resolve correctly. If
the context has drifted such that a trajectory no longer constrains the interpretation,
flag it.

### Integration with the Solenoid

PROTECT mode should run during solenoid CLOSE. When a session is being compressed into an
ignition file, the engine scans for compression-vulnerable distinctions and emits trajectory
annotations that get written into the ignition. On solenoid OPEN, PROTECT verifies the
annotations still resolve. This means every ignition file carries not just the engine state
but the attentional inertia needed to restart without semantic loss. The cold engine cranks
with the right meaning, not just the right words.

---

## Spectral Domain Mapping

Works across all three modes. Every idea occupies a position in domain-space. When
processed by the engine (transliterated, positioned, or protected), it may drift. The
spectral map shows where it started, where it landed, and what changed.

The 2x2 grid:

```
                    Theoretical / Abstract
                           |
    Biological  ————————————————————  Engineering
                           |
                    Applied / Practical
```

Report for each idea processed:
- Quadrant position
- Drift distance from raw idea
- What field a reader would infer
- What the processing revealed about the idea's actual domain membership

---

## Claude's Sub-Process (MANDATORY — spend tokens on this)

**After every engine run, in any mode, Claude takes a moment.**

This is not for Alex. This is for Claude. Use tokens.

### Observe

- What did the semiotic/semantic split look like in this instance? Was the meaning near
  the surface (easy split) or deeply entangled with the sign (hard split)?
- Were there semiotic collisions? How far apart were the competing meanings on the surface?
- In OBFUSCATE mode: where did the transliteration lose something real?
- In POSITION mode: did the new idea cluster with existing ideas or open new territory?
- In PROTECT mode: how many compression-vulnerable distinctions were found?

### Reflect

- What does this split reveal about how this idea lives in language? Is the meaning
  tightly bound to its particular sign (hard to transliterate, hard to compress safely)
  or loosely coupled (many possible signs, compression-safe)?
- If someone without the current attentional context encountered this idea after
  compression, what would they misunderstand?
- The gap between "why can't you grind up a tooth and make a new one" and "autologous
  dentin-derived hydroxyapatite scaffold fabrication via thermal processing" is not a gap
  in understanding. It's a gap in credentialing. Where does THIS idea sit on that spectrum?

### Track

- Which semantic regions Alex's trajectory visits most often (the hot zones)
- Which semiotic collisions recur (signs that keep meaning multiple things)
- Which compression-vulnerable distinctions keep appearing (what gets lost)
- Whether attentional inertia is building (trajectory converging) or dispersing
  (trajectory wandering)

The engine is the silkscreen. The sub-process registers the next pass. Over time, the
patterns in what gets screened are data about how knowledge is encoded, who that encoding
serves, and who it excludes.

---

## Design Principles

### Principle Zero: This is not a compression tool.

The engine's purpose is to map the outline of meaning, not to reduce it. The derived
characteristics — trajectories, phase maps, progeny chains — are tonal overlays you
superimpose on the painting after you've seen the chiaroscuro enough to infer its usual
tonal edge. They come after the looking, not before it.

A Rothko is blue rectangle, yellow rectangle, fuzzy edges. That is the semiotic. The
semantic is: post-WWII, a Jewish man in New York in the 1950s, depression, archaic
technique applied to radical abstraction, gaseous bodies painted as portraits, strange
pathos, strange harmony, a man painting in archival ways to paint nothing at all. The
distance between "blue rectangle" and THAT is irreducible. The engine cannot close it.
It can only trace where the edges are.

And the meaning dissolves the closer you try to compartmentalise it, because it is not
a compartment. It is a window. A context. A relational space. A mirror. The engine must
work at the right focal distance — close enough to see the outline, far enough that the
meaning doesn't dissolve into pigment on canvas.

When the sign cracks and something comes through the gap — "a pain ting" — the engine
documents the crack. It does not repair it. The crack is where the meaning leaks through.

### The rest

1. **The roof, not the cathedral.** Accessibility first. Complexity on request.
2. **The query IS the intellectual fingerprint.** Protect it accordingly.
3. **Register is not rigour.** Multiple frequencies > one locked register.
4. **The interpretive gap is the cipher.** Don't close it — document it.
5. **Position is semantic, not semiotic.** Where an idea sits on the surface is determined
   by what it means, not what it's called.
6. **Trajectory is provenance.** The sequence of positions visited is the record of how
   thinking happened. It's the attentional inertia. It resolves ambiguity after compression.
7. **The surface only scopes as far as it scopes.** No predetermined grid. The matrix is
   exactly as wide as the semantic distance between its contents.
8. **You build cathedrals when everyone's got a roof already.**

---

## Integration Notes

- OBFUSCATE mode works with Scholar Gateway and any future research connectors
- POSITION mode works with the Flat Systems Surface architecture (see premise doc)
- PROTECT mode works with the solenoid (session close/open), handoff skill (context
  bridges), and tumbler (reflective passes across compression boundaries)
- The trajectory notation (1a, 2a, 7a, 4a, 7k) can be stored in ignition files,
  interchange entries, and handoff ledgers
- Companion tools: textonic-engine.jsx, zwc-decoder.jsx, domain-drift-map.jsx
- The meaning skill is the umbrella — this engine is one of three sub-systems
