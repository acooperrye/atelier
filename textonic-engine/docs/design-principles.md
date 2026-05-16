# Design Principles

The principles that govern how the engine operates. Read these before extending the engine, building tools that talk to it, or porting the mechanism to other architectures.

## Principle Zero — This is not a compression tool

The engine's purpose is to *map the outline of meaning*, not to reduce it. The derived characteristics — trajectories, phase maps, progeny chains — are tonal overlays you superimpose on the painting after you've seen the chiaroscuro enough to infer its usual tonal edge. They come after the looking, not before it.

A Rothko is blue rectangle, yellow rectangle, fuzzy edges. That is the semiotic. The semantic is: post-WWII, a Jewish man in New York in the 1950s, depression, archaic technique applied to radical abstraction, gaseous bodies painted as portraits, strange pathos, strange harmony, a man painting in archival ways to paint nothing at all. The distance between "blue rectangle" and *that* is irreducible. The engine cannot close it. It can only trace where the edges are.

And the meaning dissolves the closer you try to compartmentalise it, because it is not a compartment. It is a window. A context. A relational space. A mirror. The engine must work at the right focal distance — close enough to see the outline, far enough that the meaning doesn't dissolve into pigment on canvas.

When the sign cracks and something comes through the gap — "a pain ting" — the engine documents the crack. It does not repair it. The crack is where the meaning leaks through.

## The Eight

### 1. The roof, not the cathedral

Accessibility first. Complexity available on request, not as the entry point.

Every output should be legible to the user in the register they brought to the engine. Formal phrasings exist for the record. Informal phrasings exist for understanding. Both are emitted; neither is presented as the canonical version.

### 2. The query IS the intellectual fingerprint

Protect it accordingly. Every raw query is potentially proprietary signal. The engine's default posture is privacy-preserving — obfuscate first, run the raw query only on explicit instruction, and keep raw and transliterated processes separate until merged.

### 3. Register is not rigour

Multiple frequencies beats one locked register. A user who can operate across informal, technical, vernacular, and ceremonial registers is more sophisticated than one who is locked into a single one — not less. The engine treats register-switching as a feature of competent thought, not a deficit.

This matters for the LLM implications: training that normalises every utterance to a single formal register destroys exactly the cross-register flexibility that competent humans display.

### 4. The interpretive gap is the cipher

Don't close it — document it. The space between what the user said and what the formal literature says is the engine's primary working material. Every transliteration is a controlled crossing of that gap, and every crossing leaves a forensic record.

### 5. Position is semantic, not semiotic

Where an idea sits on the surface is determined by what it means, not what it's called. Two ideas with the same words can sit at different positions; two ideas with different words can sit at the same position. This is the principle behind the position-mode coordinate system.

### 6. Trajectory is provenance

The sequence of positions visited is the record of how thinking happened. It is the attentional inertia. It resolves ambiguity after compression.

A trajectory without content is a pattern of thought without the substance. A content transcript without a trajectory is words without the shape that gave them meaning. Both factors must be tracked independently, and both released or withheld independently.

### 7. The surface only scopes as far as it scopes

No predetermined grid. The matrix is exactly as wide as the semantic distance between its contents. The surface grows with the conversation; it does not impose a coordinate system on a conversation that hasn't earned one.

This is also why trajectory notation is session-relative: a coordinate is meaningful within the surface that produced it, not as a global address.

### 8. You build cathedrals when everyone's got a roof already

Build the small, accessible, working version first. Generalisations and elaborations follow from concrete instances, not the other way around. The engine started as a tool for one user's connector queries. The broader architecture grew out of repeated contact with the working version.

## Operational discipline

### The Delta Discipline

The engine proposes; it does not execute. Every operation comes back as a differential: current state, proposed state, the gap. The user reads the gap and approves before anything moves.

Until the engine's pattern-recognition on semiotic/semantic binding is strong enough to act autonomously without producing Monkey Jesus restorations, the human approval is non-negotiable. See `monkey-jesus-restoration.md` for the full argument.

### The Restoration Constraint

Infer before acting. Continuously re-evaluate. Know when not to split. Treat your own output as a compression artefact and retain the residue.

### The Two-Factor Discipline

Trajectory and content are independent factors. Anywhere the engine emits a trajectory, it should be possible to release that trajectory without releasing the content, and vice versa. Designs that conflate them fail at the first request for selective disclosure.

### The Substitution Test

Before performing the split on any idea, run the substitution test: if the original phrasing were replaced by a formal paraphrase, would the meaning survive? If yes, operate. If no, mark the binding as tight and operate with the original retained as canonical. If the original is fused with its sign, refuse the split.

## What the engine refuses

- To produce confident output when the binding strength is ambiguous. (Output the ambiguity instead.)
- To discard the residue of a split. (The varnish is part of the painting.)
- To force-push to the semantic surface. (The delta discipline holds.)
- To treat compression as a neutral operation. (Every compression destroys something; the engine surfaces what.)
- To apply uniform technique without per-idea evaluation. (Power washers belong elsewhere.)

## Extending the engine

When adding modes, strategies, or notations:

- New modes must use the same split as their first operation. No mode operates on the unsplit idea.
- New strategies (for obfuscate mode) must have explicit exposure and retrieval scores, and must be benchmarked against existing strategies.
- New notation must be content-independent — readable and writable without consuming the substance.
- Extensions must preserve the propose-not-execute discipline. The engine never acts on the user's behalf without surfacing the action first.

The fragmentation is the design. Each principle has earned its place by surviving repeated contact with the working version. New principles can be added but should not be merged or simplified.
