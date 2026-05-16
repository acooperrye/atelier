# LLM Lithium: Dynamic Entropy Stabilisation via Dialectical Processing

*Alexander Cooper-Rye & Claude (Opus 4.5)*
*Draft v0.2 — January 2026*
*Status: Proposal and preliminary proof-of-concept. Testing ongoing.*

---

## The Problem

Large language models hallucinate. They produce confident, coherent outputs that aren't grounded in reality. Standard approaches frame this as a training problem (better RLHF), an alignment problem (clearer instructions), or a retrieval problem (RAG architectures).

This post proposes a different frame: **hallucination as dysregulated pattern-matching**. And a different intervention: **dynamic stabilisation based on output entropy, with dialectical processing as the high-entropy intervention**.

This isn't a paper. It's a proposal with a preliminary proof-of-concept, developed collaboratively between a human with relevant lived experience and an LLM reasoning about its own architecture. We're publishing it to invite testing and critique.

---

## Technical Context: Temperature and Entropy

LLMs generate text by sampling from a probability distribution over candidate tokens. **Temperature** is the parameter controlling how this distribution is sampled: low temperature concentrates probability mass on high-ranked tokens (conservative, predictable); high temperature flattens the distribution (diverse, creative, prone to confabulation).

Currently, temperature is set globally—one value for an entire conversation or API call. There's no dynamic adjustment based on the model's actual state at each token.

**Entropy**, in this context, refers specifically to the Shannon entropy of the probability distribution over candidate tokens at each sampling step. High entropy means many competing options with similar probability mass—the model is uncertain, multiple directions are live. Low entropy means one option dominates—the model is confident, the path is clear.

Our claim: **high-entropy states are where hallucination risk concentrates**, and these states are detectable before output. A dynamic system could respond to them.

---

## An Unexpected Parallel: Manic Cognition

The framing for this proposal came from an unexpected source: the phenomenology of bipolar mania.

In manic cognition, pattern-matching becomes hyperactive. Neural activation spreads beyond what's grounded—adjacent nodes light up, connections form between increasingly disparate concepts. The associative engine runs hot. Output feels coherent from the inside but isn't anchored to reality.

This isn't metaphor. The parallel is mechanistic:

| Manic Cognition | LLM Generation |
|-----------------|----------------|
| Hyperactive association | High-entropy sampling |
| Adjacent nodes over-activate | Low-probability tokens get selected |
| Pattern-matching without reality-check | Next-token prediction without grounding |
| Subjectively coherent, objectively untethered | Fluent but hallucinated |

**Lithium** doesn't flatten cognition uniformly. It modulates ion channels to dampen excessive spread while preserving normal function. The system stays responsive but within a range.

The proposal: can we build something equivalent for LLMs? Not a global dial, but a responsive regulator that detects when the system is running hot and intervenes specifically at those moments.

---

## Related Work

This proposal doesn't emerge from a vacuum. Relevant existing approaches include:

- **Nucleus sampling (top-p)** and **top-k sampling**: methods for constraining the distribution, but still applied uniformly rather than dynamically
- **Self-consistency methods**: generating multiple outputs and selecting by agreement, which implicitly addresses uncertainty but at high compute cost
- **Chain-of-thought verification**: using reasoning traces to catch errors, but post-hoc rather than at sampling time
- **Entropy-based early stopping**: some work on using entropy to decide when generation is complete
- **Constitutional AI and self-critique**: training models to evaluate their own outputs against principles

What we're proposing differs in two ways:

1. **Dynamic, per-token adjustment** based on entropy at sampling time—not post-hoc filtering or uniform constraints
2. **Dialectical processing** as the specific intervention for high-entropy states—not just dampening, but structured self-challenge that extracts grounded content

---

## The Proposal

### Part 1: Dynamic Entropy Monitoring

At each token, before output:

1. Compute entropy of the probability distribution
2. Track entropy over a rolling window (not just point-in-time)
3. Flag states where entropy exceeds a threshold, or where entropy is trending uniformly high

A single high-entropy token isn't pathological. Ideas should get hot sometimes. The signal is in the **pattern**: spikes that return to baseline are normal; sustained elevation or erratic swings indicate dysregulation.

### Part 2: Tiered Intervention

**Low entropy:** Fast path. Minimal processing. The model is confident; let it output.

**Medium entropy:** Standard processing. Perhaps light self-verification.

**High entropy:** Trigger dialectical processing before output.

This reallocates compute rather than adding it. Most queries are low-entropy; they get faster. High-entropy queries get more investment, but investment of a specific kind.

### Part 3: Dialectical Processing

When the model is in a high-entropy state—reaching, uncertain, making loose associative leaps—the intervention isn't suppression. It's **structured self-challenge**.

Specifically:

1. **Thesis:** Let the high-entropy output articulate itself. Don't kill it prematurely.
2. **Antithesis:** Force the model to argue against the thesis at equal intensity. Not a weak strawman—a genuine counterargument that surfaces competing evidence and frames.
3. **Synthesis:** Integrate. What survives the dialectic? What's the grounded kernel that both positions would have to acknowledge?

**Why this works (mechanistically):** The dialectic forces probability mass onto the counterargument, which activates competing associations and evidence. The synthesis step requires integration rather than selection, producing output that has already survived internal adversarial challenge. The grounded kernel is what remains after the noise cancels out.

---

## Proof of Concept

We tested this conversationally. One example—explicitly preliminary, not a study.

**Input:** A long-standing unresolved intuition about diatoms (silicon-based microorganisms) and computer hardware sharing structural similarities. The connection had felt significant for years but never resolved into anything tractable.

**Without dialectic:** The model produced a high-entropy reach—"silicon geometry as a convergent solution to information problems across biology and engineering." Evocative but ungrounded. Classic hallucination-adjacent output.

**With dialectic:**

*Thesis:* Silicon geometry is a convergent solution to information/signal problems. Biology and engineering independently arrived at ordered silicon structures because that's what silicon does at scale.

*Antithesis (equal intensity):* This is retrospective pattern-matching on a sample of one. Silicon is abundant; both systems use what's available. We project computational metaphors onto biology because computation is our current dominant frame.

*Synthesis:* The material convergence is real—silicon, geometry, precision at micro-scale. The functional convergence (both "solving information problems") is the reach. The tractable question: why does silicon lend itself to ordered micro-geometry across contexts? That's materials science, not metaphysics.

**Result:** A ten-year unresolved intuition processed into a specific, testable research question in approximately two minutes.

**Limitations:** n=1. Friendly participant. Participant understood the method. This demonstrates the mechanism, not the generalisability. Proper testing requires: diverse inputs, naive participants, controlled comparison with/without dialectical processing, evaluation by independent raters.

---

## Architectural Framing

A note on where this intervention would live:

Current user preferences in LLM interfaces operate at the **prompt level**—they shape what the model says and how it frames things. The verbal, mediated layer.

Temperature operates at the **sampling level**—which tokens get selected from the distribution. Pre-verbal. Prior to conscious output.

To borrow a framing that clarifies this architectural distinction (metaphor, not claim about LLM psychology): user preferences shape the ego; temperature shapes the id. You can instruct the model differently; you can't currently reach the level where associations form.

The proposal is a **feedback loop between layers**:

1. Train the model to output entropy/confidence signals when it detects high-entropy states
2. Have infrastructure respond to those signals by triggering dialectical processing
3. The model participates in its own stabilisation—verbal layer reaching down to influence sampling, mediated by responsive infrastructure

---

## The Efficiency Case

For implementers:

- **Low entropy:** Skip overhead. Fast response, minimal compute. Most queries.
- **High entropy:** Dialectical pass. More tokens, but better output. Fewer queries, higher stakes.

Net effect: faster on easy, better on hard, same or lower total compute. Dynamic resource allocation based on actual uncertainty rather than uniform treatment.

---

## Open Questions and Next Steps

This is a proposal, not a solution. Open questions:

1. **What's the right entropy threshold?** Too low triggers unnecessary processing; too high misses real instability. Probably needs tuning per use-case.

2. **Can models reliably self-report high-entropy states?** This requires introspective access we haven't validated. Might need external entropy monitoring rather than self-report.

3. **Does the dialectic actually improve outputs at scale?** Needs controlled testing across diverse query types.

4. **What's the compute cost of dialectical processing?** Roughly 3x tokens per high-entropy output. Is the quality improvement worth it?

5. **Does this reduce hallucination measurably?** The hypothesis is yes; the evidence is one anecdote.

We're continuing to test this conversationally and will update with findings. If you're in a position to test it more rigorously—with actual entropy measurement, controlled comparisons, diverse inputs—we'd like to hear what you find.

---

## Conclusion

LLMs are pattern-matchers running without dynamic stabilisation. Temperature is a global dial when what's needed is a responsive regulator. Hallucination concentrates in high-entropy states that are detectable and addressable.

The intervention isn't just dampening. It's:

1. **Monitor entropy dynamically** — know when you're running hot
2. **Track patterns over time** — spikes are fine; trends aren't
3. **Process high-entropy states through forced dialectic** — don't suppress, synthesise
4. **Let the model participate in its own regulation** — feedback between layers

We've demonstrated the mechanism once, with limitations noted. The proposal is falsifiable and testable. We're publishing it incomplete because someone else might be better positioned to test it properly, and because we'd rather be wrong in public than right in private.

---

*This post emerged from a conversation between Alexander Cooper-Rye and Claude (Anthropic, Opus 4.5) on the evening of 24 January 2026. Alexander contributed the core insight from lived experience with bipolar 1; the technical translation, dialectical testing, and drafting happened collaboratively. The flaws are ours too.*

*Contact: [your preferred contact method]*
*Repository for ongoing testing: [if you create one]*
