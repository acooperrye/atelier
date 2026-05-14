# karyotype-terrain

Music genre as geography, not taxonomy.

→ Live: [atcooper.net/tools/karyotype-terrain](https://atcooper.net/tools/karyotype-terrain)
→ Brief: [atcooper.net/tools/karyotype-terrain](https://atcooper.net/tools/karyotype-terrain) (same URL — the brief embeds the visualisation; the bare canvas is at `/tools/karyotype-terrain/`)

## What this is

A single self-contained HTML file rendering forty-one genre territories as a continuous topographic landscape. Each peak is a chromosome territory — a genre. Height = chromosome density. Ridges between peaks = lineage paths weighted by shared genetic material. Valleys = transition zones where genre boundaries gradient into each other. Hover the canvas to read territory name and density; in transition zones, it reports the two nearest genres and the saddle elevation.

The two axes:
- Horizontal: acoustic / organic ← → electronic / synthetic
- Vertical (inverted from screen Y): high energy / dense → low energy / sparse

The colour palette runs from deep purple (valleys) through plum and rose (slopes) to amber-gold (peaks). Forty-five lineage ridges are weighted by strength. Pop is the largest peak because most other genres exchange genetic material with it.

## Why terrain, not taxonomy

The standard model treats genres as discrete labels — sharp boundaries, mutual exclusion, tree-shaped inheritance. The terrain model treats genres as cell types — persistent configurations of which conventions are expressed and which are suppressed. Two genres are close when they ignore the same things. The map is continuous. Saddle-dwellers — songs that sit between two genre centres — are not misclassifications. They're residents of a third territory the discrete model has no name for.

## Source

`map.html` is the whole thing. No build step. No dependencies. Vanilla Canvas + JavaScript. The genre coordinates, the ridge weights, and the terrain renderer are all inline. Open it in a browser to run it.

Modifying the registry:
- Add a genre by appending to the `genres` array (name, x, y, radius, height, colour bucket).
- Add a lineage by appending to the `ridges` array (from, to, strength 0–1).
- The terrain re-bakes on page load.

## Relationship to Sonic Phenomenology

The terrain is a sibling view of the [sonic-phenomenology](../sonic-phenomenology) framework. The same suppression vectors that drive the engine's attention budget are what determine genre proximity here. Fingerprint a new song → place its suppression vector → the terrain locates it on the appropriate saddle. The visualisation is the analysis output, made navigable.

## Status

Live and deployed at `/tools/karyotype-terrain/`. Snapshot of the registry as of May 2026 — 41 territories, 20 genre baselines fully characterised, 11 songs anchoring the geometry. The map updates as the dictionary grows.
