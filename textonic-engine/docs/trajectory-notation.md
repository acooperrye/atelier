# Trajectory Notation

The compact, content-free record of how attention moved through semantic space.

## Why a notation

The position-mode coordinate system assigns each idea a place on a flat 2D semantic surface. As a conversation accumulates, the *sequence* of positions visited is a higher-order object than any individual position. The sequence is the trajectory — the record of how attention moved, not where it ended up.

Trajectory notation is the storable form of that sequence. It's the bridge between the semantic surface (an abstract structure) and any concrete persistence channel (an ignition file, a session handoff, a training-data annotation).

## The format

A trajectory is a comma-separated sequence of coordinates:

```
1a, 2a, 7a, 4a, 7k
```

Each coordinate is `<grid><depth>` where:
- **grid** is an integer (1, 2, 7, 4, 7) — position on the 2D semantic surface
- **depth** is a single lowercase letter (a..z) — specificity within the grid position

Optionally, each coordinate can be tagged with a content hint in parentheses for human readability:

```
1a(instruments), 2a(percussion), 7a(metallophones), 4a(orchestral), 7k(glockenspiel)
```

The content hint is for *humans reading the annotation*. It is not the content of the conversation. It's a short label naming the semantic region.

## Reading a trajectory

A trajectory tells you:

- **Where the conversation has been** — the set of distinct grid positions visited.
- **In what order** — the sequence reveals the path, not just the destinations.
- **How deep at each stop** — the depth letters show whether the conversation lingered at a surface level or pushed into specifics.
- **Where it's currently sitting** — the last coordinate is the live position.

A trajectory that visits many grid positions at depth `a` is exploratory, surface-level. A trajectory that holds one or two grid positions but pushes through depths `a → e → k → t` is investigative, drilling. A trajectory that oscillates between two grid positions at deepening levels is a comparison or a dialectic.

## Worked example

A user's morning conversation:

```
1a(coffee), 1c(espresso pressure), 4a(physics of fluids),
4f(Reynolds number), 7a(weather), 7c(humidity effects on extraction)
```

The trajectory shows: started at coffee (1a), pushed into specifics about espresso pressure (1c), bridged to a physics analogy (4a), pushed into the relevant physics specific (4f), then noticed a connection to weather (7a), and tied weather back to the original coffee question (7c).

The shape — out from 1, into 4 for analogy, into 7 for return-with-modification — is recognisable as a particular kind of analogical reasoning. The same shape will appear in many conversations on completely different topics. The trajectory abstracts the pattern.

## What gets stored

A trajectory annotation packs into a single line:

```
trajectory: 1a, 2a, 7a, 4a, 7k
```

For storage in an ignition file or a handoff ledger:

```yaml
trajectory:
  notation: "1a, 2a, 7a, 4a, 7k"
  current: 7k
  grid_width: 7
  max_depth: k
  positions_visited: 5
  hints:
    1a: instruments
    2a: percussion
    7a: metallophones
    4a: orchestral
    7k: glockenspiel
```

The hints are optional. The notation alone is sufficient for the engine to reconstruct the trajectory shape; the hints make it legible to a human reading the annotation later.

## The two-factor model

Trajectory and content are independent factors:

- **Trajectory** (the notation) — the *shape* of thinking. Lightweight, content-free, shareable.
- **Content** — what was said at each position. The substance. Lives in the user's transcript or context window.

A trajectory can be released or shared without releasing the content. A content transcript without the trajectory is what was said but not the shape of how it connected.

For training, this distinction matters: a model trained on trajectories alone learns the patterns of human reasoning without consuming the substance. A model trained on content alone learns the surface text without the shape. The pair, kept as independent factors, is the full picture; either alone is partial in different ways. See `llm-implications.md` for the broader argument.

## Operations on trajectories

### Append

The most common operation. A new position arrives; the engine appends it.

```
before: 1a, 2a, 7a
after:  1a, 2a, 7a, 4a
```

### Deepen

Pushing into an existing grid position at greater depth.

```
before: 1a, 2a, 7a
after:  1a, 2a, 7a, 7k
```

Note the grid position 7 appears twice — once at depth `a`, once at depth `k`. The surface is append-only: the earlier shallow visit remains as a record.

### Return

Visiting a previously-occupied position. Logged as a re-visit, not as a new position.

```
before:  1a, 2a, 7a, 4a, 7k
returns: 1a, 2a, 7a, 4a, 7k, 2a
                                ^ return to 2a, sequence #6
```

### Diverge

A new grid position far from anything currently on the surface. Triggers a grid expansion.

```
before: 1a, 2a, 7a, 4a, 7k          (grid width = 7)
after:  1a, 2a, 7a, 4a, 7k, 43a     (grid expands to 43)
```

## Comparing trajectories

Two trajectories on the same surface can be compared:

- **Overlap** — positions visited by both
- **Divergence** — positions visited by only one
- **Order** — same positions in different sequences (different reasoning paths to the same destinations)
- **Depth profile** — one trajectory may push to depth `t` where the other holds at `c`

For collaborators working in the same domain, trajectory comparison shows where their attention diverged even when their conclusions look similar.

## Limitations

- The grid coordinate is dependent on the current surface state. A coordinate `7k` in one session is not the same `7k` in another — the surface was constructed from different ideas. Trajectories are not portable across surfaces without a re-anchoring step.
- The depth letter is heuristic. There is no precise definition of "depth `k`" — it's the engine's relative judgment at the time of positioning. For high-stakes use, store the natural-language hint alongside.
- The notation does not capture *why* attention moved from one position to the next. Trajectories show the path, not the reason. For some uses (training on reasoning patterns) this is fine; for others (explaining a decision) the trajectory is necessary but not sufficient.

## Related

- `../modes/position.md` — the coordinate system this notation records
- `../modes/protect.md` — how trajectory annotations get attached to compressed context
- `llm-implications.md` — why this matters at scale
