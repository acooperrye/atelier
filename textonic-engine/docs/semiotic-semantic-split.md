# The Semiotic/Semantic Split

The engine's fundamental operation. Every mode depends on it.

## Definitions

**Semiotics** — the signs. The word "python." The phonemes. The spelling. The surface grammar. The features that survive compression because they're structurally simple — characters, tokens, byte-pair encodings.

**Semantics** — the meaning. Python-the-snake or Python-the-language. The features that depend on context to resolve.

The split: separate the signs from the meanings and operate on them independently.

## Why this is non-trivial

Most operations on language conflate the two. A search index treats the sign as a proxy for the meaning. A summariser treats meaning-preservation as automatic if the signs survive. A token-level training loop treats the surface as the only addressable layer.

This works most of the time because most language has a stable sign-meaning binding. "The capital of France" maps to one referent in most contexts. The engine is interested in the cases where it doesn't.

## The diagnostic example

"Shiny Glock" is either the spectral phonics of a glockenspiel or it's a 9mm pistol. Semiotically identical — same eleven characters, same phonemes, same surface grammar. Semantically distant — one is an orchestral metallophone, the other is a firearm.

Both readings are alive in language. Which one is *correct* in a given utterance depends entirely on what the conversation has been doing for the prior twenty minutes. If the conversation has been about percussion, only one reading is live. If the conversation has been about urban crime, only the other. The constraint is not in the words. It's in the surrounding trajectory.

When the conversation gets compressed — summarised, truncated, handed off — the constraint goes with it. The sign survives. The disambiguation does not. The new reader (a model resuming context, an analyst reading the summary, a fine-tuning corpus consuming the log) has no way to know which Glock.

## Attentional inertia

The mechanism that resolves "Shiny Glock" in a live conversation is **attentional inertia**: the accumulated trajectory of what's been attended to, what semantic region the conversation has been occupying. It's the conversational equivalent of a moving frame of reference — the listener's interpretive defaults are set by where attention has been, not by where it could in principle go.

Attentional inertia is implicit in any in-progress conversation. The engine makes it explicit. Trajectory notation (`1a, 2a, 7a, 4a, 7k`) is a record of the inertia in a form that can be stored, transmitted, and reattached to a resumed context.

## Where the split is easy

Some ideas are loosely coupled to their signs. "The capital of France" → "Paris" is a near-trivial split. The meaning is portable across many possible signs ("Frankreichs Hauptstadt," "the city the Eiffel Tower is in," "Lutetia"). Compression-safe. The semantic survives whatever shell it gets re-encoded into.

Most reference-stable factual content is in this category. The engine generally has nothing to do here.

## Where the split is hard

Some ideas are tightly bound to their signs. Register is meaning. Informality is meaning. The phrase "the medium that knows it's flat" is not a casual rendering of a formal concept — it *is* the concept. Splitting the sign from the meaning produces two dead halves: a formal paraphrase that loses the recursive joke, and an empty register without the reference.

The diagnostic question: would a competent rephrase preserve what mattered? If yes, the binding is loose and the split is safe. If no, the binding is tight and the engine should leave the idea alone or flag it as a non-split.

This is the boundary at which Mode III's protect operation does its work — these tight bindings are exactly what compression destroys, because compression preserves the easy-to-encode part (the surface) and discards the hard-to-encode part (the register and the trajectory that made the register meaningful).

## Where the split must be refused

Some ideas live in a particular utterance and cannot be moved without destruction. The engine treats these as **fused** — sign and meaning are not separable, even in principle. Examples:

- Self-referential phrasings (the joke that depends on its own form)
- Performative speech acts ("I now pronounce you...")
- Linguistic art where the substrate is the artwork (poetry, certain kinds of philosophical prose)
- Identity statements ("I am the one who...")

For fused ideas, the engine documents the fusion rather than performing the split. The output is "this resists the operation, here's why."

## Methodological consequence

The engine cannot operate as a pipeline. Every operation requires a judgment about whether the binding is loose, tight, or fused. The judgment is per-idea, not per-domain.

This is why the engine *proposes* rather than *executes*. It outputs a differential: here is the current state, here is what the split would look like, here is what it would cost. The user reads the gap and approves before anything moves.

See `monkey-jesus-restoration.md` for why the propose-not-execute discipline is non-negotiable.

## Practical workflow

When the engine receives an idea, the first operation is always the same:

1. Read the idea.
2. Identify the sign layer (words, phrasing, register, surface grammar).
3. Identify the semantic layer (what it refers to, what it connects to, what it's about).
4. Estimate the binding strength (loose / tight / fused).
5. If loose: proceed with the mode's specific operation.
6. If tight: proceed but flag what the split costs.
7. If fused: refuse the split. Output the fusion description.

Steps 1–4 are the split. Steps 5–7 are everything else.
