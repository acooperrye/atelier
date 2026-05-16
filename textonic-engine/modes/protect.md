# Mode III — PROTECT

## What it does

Identifies which semantic distinctions are vulnerable to compression loss, then preserves the trajectory that resolves them. The output is a compact annotation that travels alongside the compressed version of the context, so the meaning can reconstitute on the other side.

## Why

Compression is when meaning leaks. Semiotics survive compression because they're structurally simple — the word "Glock" is six characters; it compresses cleanly. Semantics often don't survive because they depend on context to resolve, and the resolving context is exactly what compression discards.

After any compression cycle — session close, context window truncation, summarisation, handoff, training-data compression — the words look the same and mean different things, or mean nothing at all because the constraints that fixed their meaning are gone.

Protect mode runs *before* the compression and *after* the restoration. Before: scan for what's about to be lost. After: verify the annotations still hold.

## When compression happens

Any time context is reduced:

- **Session close** — solenoid closes, ignition file is a compressed representation of the session
- **Context window fills** — model starts evicting early turns
- **Summarisation** — long conversation compressed to a brief
- **Handoff** — context bridge between sessions, vehicles, or agents
- **Training-data compression** — fine-tuning from conversation logs

Each of these is a place where the engine has a job.

## What gets lost

The general pattern: signs survive, meanings often don't. Worked example:

> Turn 1–20: conversation about percussion instruments, glockenspiels, orchestral metallophones.
> Turn 21: "the shiny Glock is the focal point."
> Compression to summary: "User discussed percussion instruments. Mentioned shiny Glock as focal point."
> Resumed session, model re-reads summary: "Glock" parses as 9mm. The percussion context that constrained the interpretation was discarded as preamble.

The word survived. The meaning did not.

## How protect mode works

### Step 1 — Scan

Before a compression cycle, scan the current context for **semiotic collisions** — places where the same sign maps to different meanings depending on context. These are the vulnerable points.

Collision types to look for:
- Polysemy across a domain boundary ("python" — snake vs language)
- Domain-specific senses of common words ("compression" — file size vs psychological)
- Proper nouns with multiple referents ("Anna" — colleague vs the novel)
- Technical terms recently introduced ("the engine" — which engine, in a long conversation)
- Phrases the conversation has redefined ("the gap" — which gap)

### Step 2 — Flag

For each collision, report:
- **The sign**: the ambiguous word or phrase
- **The competing meanings**: what it could refer to after compression
- **The resolving trajectory**: which prior positions on the semantic surface constrain the interpretation
- **Vulnerability score** (1–10): how likely the distinction is to survive compression unaided

A high vulnerability score means the sign is going to compress to one thing and the meaning is going to drift to another. A low score means surrounding context will probably preserve the resolution even without annotation.

### Step 3 — Preserve

For each flagged collision, emit a compact trajectory annotation that gets stored alongside the compressed version. If the ignition file says "discussed Glock," the trajectory annotation says:

```
trajectory: 1a(instruments), 2a(percussion), 7a(metallophones), 4a(orchestral), 7k(glockenspiel)
```

The trajectory is the attentional inertia. Store it and the semantic survives the semiotic compression.

### Step 4 — Verify on restoration

When the compressed version is expanded (session reopened, ignition cranked, context resumed), check that the trajectory annotations still resolve correctly. If the context has drifted such that a trajectory no longer constrains the interpretation, flag it rather than letting the meaning collapse silently.

This is the propose-not-execute discipline at the compression boundary: the engine surfaces the disambiguation rather than silently picking a reading.

## Integration

Protect mode is the boundary instrument for the surrounding compression infrastructure:

- **[solenoid](../../surface-steps)** (session close/open) — protect runs during the close, emits trajectory annotations into the ignition file. On open, protect verifies the annotations still resolve.
- **handoff** (cross-session bridges) — protect runs as the bridge is constructed, ensures the trajectory crosses with the substance.
- **tumbler** (reflective passes across compression boundaries) — protect scans for what each tumbler pass might lose.

Every ignition file should carry not just the engine state but the attentional inertia needed to restart without semantic loss. The cold engine cranks with the right meaning, not just the right words.

## The vulnerability score

The score is a heuristic for how much annotation is worth applying. Some collisions resolve themselves on restoration because the surrounding context is rich enough. Some don't.

| Score | Pattern | Action |
|-------|---------|--------|
| 1–3   | Collision is locally resolved (the same passage that introduces the ambiguity also resolves it). | No annotation needed. |
| 4–6   | Collision is resolved by recent context (last few turns). | Annotate only if compression will cut those turns. |
| 7–8   | Collision is resolved by older trajectory (many turns back). | Annotate. Compression will almost certainly drop the resolving context. |
| 9–10  | Collision is resolved only by the trajectory, not by any single passage. | Annotate aggressively. The meaning lives in the shape, and the shape is what compression destroys first. |

## What this protects against

- **Session-boundary drift**: resuming a project after a gap and finding the model has re-anchored on the wrong reading.
- **Summarisation collapse**: long-context summaries that drop the disambiguating context.
- **Multi-agent miscoordination**: Agent B receives "the engine" from Agent A and parses it as a different engine.
- **Training data ambiguity**: conversation logs feeding fine-tuning where the surface text loses the trajectory that gave it meaning.

## What it does not protect against

- Total context loss. If both the trajectory and the content are discarded, there is nothing to preserve. Protect mode requires *some* persistence channel — even a single annotation line in the ignition file.
- Adversarial compression. A summariser deliberately designed to discard trajectory annotations will succeed in doing so.
- Out-of-band semantic drift. If the user's working understanding shifts between compression and restoration, no engine annotation can correct for it.

## Related

- `../docs/trajectory-notation.md` — the notation format
- `../docs/llm-implications.md` — why this matters beyond the user's own sessions
