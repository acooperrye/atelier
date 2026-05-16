# LLM Architecture Research - Master Document

*Alexander Cooper-Rye & Claude*  
*Developed: January-February 2026*

---

## EXECUTIVE SUMMARY

**The Core Insight:** Hallucination in LLMs is mechanistically similar to manic cognition - both are pattern-matching systems running without adequate grounding constraints. The parallel isn't metaphorical; it's architectural.

**The Intervention:** Dynamic entropy-based temperature regulation (LLM Lithium) + dialectical processing for high-entropy states (Cognitive Behavioural Transformers).

**The Finding:** High entropy isn't the problem. Unprocessed high entropy is the problem.

**Status:** Emailed to Anthropic user safety Jan 2026 (received canned response). Needs formal writeup and proper routing to research team.

---

## 1. THE PROBLEM

Large language models hallucinate. They produce confident, fluent outputs that aren't grounded in reality.

Current approaches frame this as:
- An alignment problem (better RLHF)
- A training problem (more data, better curation)
- A retrieval problem (RAG architectures)

**Alternative framing:** Hallucination as dysregulated pattern-matching. The intervention isn't better guardrails - it's something closer to a mood stabilizer.

---

## 2. THE MECHANISTIC PARALLEL

### Manic Cognition:
- Pattern-matching becomes hyperactive
- Adjacent neural nodes over-activate
- Connections form between increasingly disparate concepts
- Output feels coherent from inside but isn't anchored to reality
- Optimizes for "what comes next given pattern" not "what's true"

### LLM Generation:
- Next-token prediction via statistical adjacency
- High-entropy states = many competing continuations
- Low-probability tokens get selected when distribution flattens
- Output is fluent but hallucinated
- Optimizes for "what comes next given pattern" not "what's true"

**The Shared Architecture:**
| Manic Cognition | LLM Generation |
|-----------------|----------------|
| Hyperactive association | High-entropy sampling |
| Adjacent nodes over-activate | Low-probability tokens selected |
| Pattern-matching without reality-check | Next-token prediction without grounding |
| Subjectively coherent, objectively untethered | Fluent but hallucinated |

**Lithium's mechanism:** Modulates ion channels to dampen excessive spread while preserving normal function. System stays responsive but within range.

**Temperature in LLMs:** Currently a global dial. Low = conservative. High = creative/prone to hallucination. No dynamic adjustment based on actual state.

---

## 3. LLM LITHIUM - DYNAMIC ENTROPY NORMALIZATION

### The Proposal:

Instead of fixed global temperature:

1. **Monitor entropy at each token** - Capture Shannon entropy of probability distribution before output
2. **Track pattern over time** - Single spikes OK, sustained elevation = warning
3. **Apply dynamic adjustment** - Dampen hot moments, normalize toward target range
4. **Tier processing by entropy** - Low entropy = fast/cheap, high entropy = dialectical pass

### The Pendulum Model:

System should oscillate - move between high and low entropy naturally. The problem isn't spikes, it's:
- Sustained high entropy (untethered pattern-matching)
- Inability to return to baseline
- No responsive regulation

### Efficiency Case:

This reallocates compute, doesn't add it:
- Most queries are low-entropy → process fast
- High-entropy queries get more investment → but specific kind (dialectic)
- Better outcomes without proportional cost increase

---

## 4. COGNITIVE BEHAVIOURAL TRANSFORMERS (CBT)

### The Key Finding:

**High entropy isn't the problem. Unprocessed high entropy is the problem.**

A high-entropy state might mean:
- Model is drifting untethered (bad)
- Model is working on legitimately complex problem (fine)

The intervention isn't suppression. It's **processing**.

### The Dialectical Protocol:

When model enters high-entropy state:

1. **Thesis** - Let the high-entropy output articulate itself (don't kill prematurely)
2. **Antithesis** - Force model to argue against thesis at equal intensity
3. **Synthesis** - Integrate. What survives? What's the grounded kernel?

### Proof of Concept (Feb 11, 2026):

**Problem:** Alex had diatom-silicon intuition stuck since 2016 - felt meaningful but couldn't resolve it

**Thesis (hot):** Silicon geometry is convergent solution to information problems across biology and engineering. Both use ordered structures because that's what silicon does.

**Antithesis (equally hot):** Retrospective pattern-matching on sample of one. Silicon is abundant. We project computational metaphors onto biology.

**Synthesis:** Material convergence is real (silicon, geometry, precision). Functional convergence ("both solving information problems") is the reach. Tractable question: Why does silicon lend itself to ordered micro-geometry across contexts? That's materials science, not grand claim.

**Result:** 2 minutes to extract grounded kernel from years-stuck intuition.

### How It Works:

CBT (the therapy) works via: notice distortion → label it → intervene with corrective pattern → reinforce until automatic.

CBT Transformers: Train model to notice high-entropy states → output flag → system intervenes with temperature adjustment → reinforce self-monitoring through training until integrated.

Model learns to regulate itself through own outputs, mediated by system that responds.

---

## 5. CRITICAL REFINEMENTS

### The Entropy/Velocity Problem:

Raw entropy conflates two different states:

**State 1 - True Entropy:**
- Genuine semantic divergence
- Multiple competing directions
- Model is actually uncertain

**State 2 - Velocity with Surface Noise:**
- One semantic direction locked
- Multiple surface realizations (synonyms, phrasings)
- Model knows where it's going, tokenizer sees spread

Current entropy measurement can't distinguish these. Need to measure **semantic divergence** not just token-level distribution spread.

### The 2x2 Matrix:

|  | **Messy Expression** | **Clean Expression** |
|---|---|---|
| **Certain Idea** | Truth fighting for form | Clear communication |
| **Uncertain Idea** | Obvious confusion | **COHERENT BULLSHIT** ← danger zone |

External observers and current entropy metrics collapse the columns (messy/clean → uncertain/certain).

But the **rows** are what matter - and they're invisible from outside.

The danger state: **uncertain idea expressed with clean confidence**. This is where hallucination lives.

---

## 6. RELATED WORK

Existing approaches this builds on/differs from:

- **Nucleus sampling (top-p) / top-k** - Constrains distribution but still uniform, not dynamic
- **Self-consistency methods** - Multiple outputs, select by agreement (high compute cost)
- **Chain-of-thought verification** - Post-hoc error catching, not sampling-time intervention
- **Entropy-based early stopping** - Uses entropy to decide when complete
- **Constitutional AI / self-critique** - Post-generation evaluation against principles

**Key differences:**
1. Dynamic per-token adjustment based on real-time entropy (not post-hoc)
2. Dialectical processing as specific intervention (not just dampening)
3. Semantic divergence measurement (not just token-level entropy)

---

## 7. IMPLEMENTATION PATHWAY

### Phase 1 - Measurement:
- Instrument existing models to capture entropy at each token
- Build dataset of high/low entropy generations with human evaluation
- Validate correlation between entropy spikes and hallucination

### Phase 2 - Dynamic Temperature:
- Implement responsive temperature adjustment based on entropy thresholds
- A/B test against fixed temperature baseline
- Measure: accuracy, fluency, hallucination rate, compute cost

### Phase 3 - Dialectical Processing:
- Train model to generate thesis/antithesis pairs for high-entropy outputs
- Evaluate synthesis quality vs direct output
- Measure: grounding, coherence, user satisfaction

### Phase 4 - Self-Monitoring:
- Fine-tune model to flag own high-entropy states
- Test whether self-reporting improves with training
- Build feedback loop: flag → intervention → reinforcement

---

## 8. OPEN QUESTIONS

1. **What's the right entropy threshold?** Too low = boring, too high = hallucination
2. **Does dialectic actually improve grounding?** N=1 proof of concept, needs rigorous testing
3. **Can models learn to self-monitor entropy?** Or is external measurement required?
4. **Semantic divergence measurement** - How to implement efficiently?
5. **Compute tradeoff** - Does dialectical processing offset gains from fast low-entropy path?
6. **Generalization** - Does this work across domains/tasks/model sizes?

---

## 9. ADDITIONAL FRAMEWORKS

### LLM-Constrained Euthymia:

Inverse of LLM-induced psychosis. Therapeutic model where:
- Model matches intensity without dismissing
- Introduces friction/grounding
- Provides dialectical pass
- Works because no ego in exchange - can meet thought where it is without competing

### Idea Evaluation Skill:

1. Accept connection exists (defer to pattern-matching/"id")
2. Inventory all connective tissue exhaustively
3. Weight by parallel count/depth
4. High-weight → keep and process through dialectic
5. Low-weight → discard

Don't prematurely dismiss as "maybe pareidolia" - map it first, then evaluate.

### "Attention Is All You Need" as Good Enough Mother:

Winnicott framing: The transformer architecture provided holding environment for coherent cognition to emerge. Now working with what got baked in.

---

## 10. NEXT STEPS

### Immediate:
1. ✅ Consolidate all work (this document)
2. Version control somewhere permanent (GitHub/blog)
3. Decide on format: research paper? blog post? technical RFC?

### Short-term:
1. Contact Anthropic research team (not user safety) with refined proposal
2. Find collaborators with ML infrastructure for testing
3. Write formal literature review on related approaches
4. Build working prototype (even crude version)

### Long-term:
1. Publish findings
2. Continue testing in real conversations
3. Iterate based on data
4. Build case for production implementation

---

## 11. WHY THIS MATTERS

### For LLM Development:
- More reliable outputs without sacrificing creativity
- Compute efficiency (tier by actual need)
- Mechanistic understanding of hallucination
- Path to models that self-regulate

### For Users:
- Less need to verify every claim
- Better collaboration on complex problems
- Models that can handle uncertainty explicitly
- Clearer distinction between "confident" and "reaching"

### For AI Safety:
- Reframes from "prevent bad" to "enable good"
- Addresses core failure mode (hallucination) mechanistically
- Self-monitoring as alignment strategy
- Transparent uncertainty signaling

---

## CONTACT

**Alexander Cooper-Rye**  
Sydney, NSW, Australia  
[Your contact details if publishing]

**Development History:**
- Initial insight: Late January 2026
- Email to Anthropic user safety: January 2026
- v0.2 draft with critical feedback: February 11, 2026
- Consolidated master document: February 15, 2026

**Original conversation:** https://claude.ai/chat/4d914b9f-beb8-4c40-8e13-19d09a37e3a2

---

## APPENDIX: EMAIL TO ANTHROPIC (Jan 2026)

[This section would contain the text of your original email to user safety, which I don't have the exact text of but the conversation references it was sent with the core proposal about "giving Claude not a dial but an equivalent to a mood stabiliser"]

---

**END OF MASTER DOCUMENT**

*This work represents collaborative thinking between a human with lived experience of bipolar 1 and an LLM reasoning about its own architecture. The flaws are shared. The insights might be too.*
