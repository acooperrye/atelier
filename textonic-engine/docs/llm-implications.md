# LLM Implications

The connector use case was the entry door. The mechanism is broader.

## The basic argument

Anywhere a language model has to compress and then restore — long-context summarisation, session boundary, multi-agent handoff, training on conversation logs, retrieval-augmented generation — the sign-versus-meaning gap is doing damage that nobody is currently auditing.

The summary keeps the word "Glock." The fine-tuned model keeps the surface features and quietly normalises the semantic. Across millions of conversations, that's not just lossy; it's a systematic bias toward the part of language that's easiest to encode.

The engine, as currently scoped, is a single-user instrument. The mechanism it implements is general.

## Why current LLM pipelines don't address this

A model treats its context window as if everything currently in it constrains current meaning, and everything outside it doesn't exist. This is approximately true. What it misses is that the *path* by which the current window came to look the way it does carries information the window itself does not.

A 4-turn context that ended with `[turn 21: "the shiny Glock is the focal point"]` looks identical regardless of whether turns 1–17 were about orchestral percussion or urban crime. The model picks a reading and proceeds. If the reading is wrong, nothing in the model's architecture flags it.

This is fine for short, self-contained tasks. It fails systematically for:

- Long conversations where the disambiguating context has been evicted
- Resumed sessions where prior turns have been summarised
- Multi-agent systems where context is reshaped between hops
- Training corpora compiled from compressed conversation logs

Each of these is a place where attentional inertia would have constrained the interpretation, and the system has discarded the inertia.

## Three implications

### 1. Training-data integrity

A conversation log is a compression of an attentional process. The participants knew which Glock — their attention had inertia. The log captures the words but not the inertia, and a model fine-tuned on the log inherits the words.

Across a corpus of millions of conversations, this produces a systematic bias: the model learns the parts of human language that survive the lossy channel and grows blind to the parts that don't. The parts that don't are exactly the parts where meaning is constructed across a trajectory rather than in any single utterance.

The fix: train on trajectory and content as independent factors. Trajectory notation is compact (a few bytes per turn), content-free (no PII, no proprietary substance), and reproducible. A model can learn the *shape* of attention from trajectories without consuming the substance from content. Done at scale, this would give models the missing axis — they would learn how attention moves through semantic space, not just what's on the page.

This is not a hypothetical. The data exists. Every active LLM deployment is producing trajectories every second. They are not being captured because nothing in the pipeline knows how to encode them.

### 2. Attentional inertia as a first-class property

Models behave as though context window content alone determines current meaning. Inside a long live conversation, the accumulated trajectory of what's been attended to is what makes "Glock" disambiguate to glockenspiel. That trajectory is implicit in the conversation flow today and lost at every truncation boundary.

Making it explicit — a stored record of which semantic positions a conversation has occupied, attached to but distinct from the conversation content — would survive truncation and could be reattached to a resumed session.

Architecturally, this is small. A trajectory annotation is a metadata field on the session. The model reads it the way it reads system prompts. The benefit is that the model would re-enter a conversation with the *right meaning*, not just the right words.

Two related properties become available once attentional inertia is stored:

- **Trajectory-conditioned attention.** The model can weight context-window content by alignment with the trajectory. Recent turns that match the trajectory get higher weight; turns that look like noise relative to the trajectory get lower weight. This is a softer, more selective form of context management than truncation.
- **Trajectory-aware compression.** A summariser that knows the trajectory can write summaries that preserve the disambiguating context, even when individual turns get dropped.

### 3. Compression-aware infrastructure

[solenoid](../../surface-steps) (session close/open), [handoff](../) (cross-session bridges), [tumbler](../) (reflective passes across compression boundaries) — these are compression cycles inside a single user's working environment. The engine sits at the boundary in each of them.

At larger scale, every multi-agent system, every long-context summariser, every retrieval-augmented pipeline is a compression cycle too. Each one is making decisions about what to keep, what to discard, and how to reconstruct on the other side. None of them currently distinguishes sign-survival from semantic-survival.

The longer-term claim: any LLM system that handles compression should have something like the engine in the pipeline, scanning for what's about to be lost and emitting trajectory annotations that travel with the compressed version.

Concretely, what this looks like:

- **At ingestion time** (training data, RAG indexing): tag documents with their semantic trajectory, not just their content. Retrieval can then be trajectory-aware — match on shape of reasoning as well as topic.
- **At session close**: emit a trajectory annotation alongside the compressed transcript. On resume, the model re-reads the annotation and reconstructs the inertia.
- **At handoff** (multi-agent, multi-session): pass the trajectory with the substance. Agent B inherits not just what Agent A said but the shape of where Agent A's attention was going.
- **At summarisation**: the summariser is informed by the trajectory so that compression preserves the disambiguating context, not just the salient nouns.

## What's required to build any of this

The engine, as a Cowork skill operating on one user's working context, demonstrates the mechanism. Scaling it to LLM infrastructure requires three things, in order of difficulty:

### Trajectory notation as a portable schema

The notation needs to be standardised enough that models from different builders can read and emit it. The current notation (see `trajectory-notation.md`) is a working draft. The semantic-surface coordinates are session-relative, which is fine for single-user contexts but needs an anchoring mechanism for cross-context portability.

### A model that recognises semiotic/semantic binding strength

The engine's split currently relies on a human (or current Claude) making judgments about whether an idea's sign-meaning binding is loose, tight, or fused. For automated emission of trajectory annotations, the model needs to make this judgment itself, reliably. This is a training problem — the data exists in the engine's worked examples; the labels are derivable from the engine's outputs.

### Pipeline hooks at compression boundaries

The engine has to run *before* compression to do anything useful. This means inference-time runtimes need a hook at every place context gets reduced. In current architectures these hooks are not exposed. Building them is straightforward; getting them adopted is the harder problem.

## The bet

Meaning has a shape. With enough trajectory data, the shape pattern-matches reliably. Until then, the engine proposes and the user verifies. Same discipline as the surface itself — no force-pushes to the semantic layer.

The path from "single-user instrument" to "compression-aware LLM infrastructure" is unlikely to be linear. The first useful step is small: tag the data that already exists. The second is incremental: train models that can read the tags. The third is structural: build pipelines that emit and consume the tags at every compression boundary.

The engine is the demonstration. The argument is that the rest of the field should care about the same problem.

## Related

- `semiotic-semantic-split.md` — the mechanism this argument is built on
- `trajectory-notation.md` — the candidate portable schema
- `monkey-jesus-restoration.md` — why "compress confidently" is the wrong default
- `../modes/protect.md` — the boundary instrument
