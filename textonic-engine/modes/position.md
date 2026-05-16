# Mode II — POSITION

## What it does

Assigns ideas coordinates on a flat 2D semantic surface. Position is determined by what an idea means, not what it's called. Two ideas with the same word can occupy different positions; two ideas with different words can occupy the same position.

## Why

Meaning has a shape. Spelling does not. Standard taxonomies organise by sign — alphabetical, hierarchical by surface category. That organisation is useful for retrieval but lossy for reasoning. The semantic surface organises by content: ideas land near each other when they're about the same thing, regardless of how they're phrased.

The surface is also the substrate for the engine's other two modes. Obfuscate mode reports drift on the surface. Protect mode tracks attentional inertia on the surface. Without a stable coordinate system, "the trajectory" is just a metaphor.

## The coordinate system

Each idea is assigned a position with three components:

- **Grid position** (integer): where this idea sits relative to everything else currently in play. Computed from semantic distance to existing ideas. The grid is only as wide as the furthest semantic distance between its contents.
- **Depth** (a–z, a=surface, z=deepest): how specific this idea is within its semantic region. "Snakes" = 7a. "Carnivorous snakes" = 7k. "Molecular biology of elapid venom production" = 7y. Same grid position, increasing depth.
- **Sequence number**: when this idea arrived. Sequence preserves order, which preserves the trajectory.

A full coordinate looks like `(7k, #14)` — grid position 7, depth k, the 14th idea to land on the surface.

## How positioning works

### Step 1 — Receive

Accept the idea, same as obfuscate mode.

### Step 2 — Split

Separate semiotic from semantic. Identify the meaning-core independent of the sign-shell. This is the same operation as obfuscate Step 2.

### Step 3 — Position

Assign the coordinate:

- Find nearest neighbours on the surface (which existing positions does this idea cluster with?)
- Compute grid position from semantic distance to those neighbours
- Compute depth from specificity within the grid neighbourhood
- Assign the next sequence number

If the new idea is far from everything already on the surface, the grid expands to accommodate. The surface is only ever as wide as it needs to be.

### Step 4 — Record trajectory

Append the new coordinate to the trajectory log. Over a conversation, the trajectory becomes a sequence: `1a, 2a, 7a, 4a, 7k, ...`. This sequence is the attentional path. It is the provenance record. It is the attentional inertia in stored form.

### Step 5 — Report surface state

After positioning, report:
- Current trajectory (the full coordinate sequence so far)
- Nearest neighbours on the surface
- Did the grid expand to accommodate this idea?
- Did this deepen an existing position or open a new one?

## Surface properties

**Append-only.** Ideas never disappear from the surface. They can subside (become dormant, lose elevation) but the position remains as a record that the conversation visited there.

**Depth only increases.** You can go deeper at an existing grid position. You cannot make it shallower. "Snakes" (7a) → "carnivorous snakes" (7k) is a legal move. "Carnivorous snakes" (7k) → "snakes" (7a) is treated as a *return* to a known position, not a regression of depth.

**Grid expansion is bounded.** The grid is exactly as wide as the furthest semantic distance between its contents. Cat at 1, dog at 2, snake at 7, rabbit at 4. The surface is as wide as the distance from (cat, dog) to snake. Add "python-the-language" and the surface might expand to 43 — its semantic distance from snakes is large even though the semiotic distance is zero.

## The two-factor model

Trajectory and content are two separate factors:

- **Trajectory** (1a, 2a, 7a, 4a, 7k) — the *shape* of thinking. Lightweight, content-free, shareable. Describes attention without describing what was attended to.
- **Content** — what was actually said at each position. The substance. Lives in the user's context window or transcript.

Together they reconstruct the full ideation. Apart, each is useful independently:

- Trajectory alone = ideation patterns, attentional fingerprint, training signal for how humans navigate semantic space
- Content alone = what was said, but not how it connected
- Together = full provenance, reproducible path through meaning-space with meaning at each stop

This separation matters for any architecture that wants to learn from the *shape* of human thinking without consuming the substance. The trajectory can be released; the content stays private. See `../docs/llm-implications.md`.

## Worked use cases

**Long-conversation memory.** As a session accumulates, the trajectory is the compact representation of where the conversation has been. On context-window pressure, the trajectory survives even when individual turns are evicted.

**Cross-session continuity.** Resuming a project after a gap, the trajectory tells the model where the prior conversation was operating. The model can re-enter at the right depth instead of starting at 7a.

**Multi-agent handoff.** Agent A passes Agent B a trajectory + the current position. Agent B knows the shape of the prior reasoning without needing the full transcript.

**Surface comparison.** Two analysts working on the same domain produce two trajectories. Comparing the trajectories shows where their attention diverged even if their conclusions look similar.

## Related

- `../docs/trajectory-notation.md` — full notation spec
- `../docs/semiotic-semantic-split.md` — the underlying mechanic
- [`idea-topography`](../../idea-topography) — the early prototype, ideas on a flat semantic surface
