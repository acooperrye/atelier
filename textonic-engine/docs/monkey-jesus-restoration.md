# The Restoration Constraint (Monkey Jesus Avoidance)

## The problem

The engine is itself a compression cycle. The semiotic/semantic split IS a compression — you strip the sign to isolate the meaning. But signs carry meaning too. Register is meaning. Informality is meaning. The gap between "why can't you grind up a tooth and make a new one" and "autologous dentin-derived hydroxyapatite scaffold fabrication via thermal processing" is not a gap in understanding — it's a gap in credentialing. Strip the register and you've lost data while believing you preserved it.

## The reference

Ecce Homo, Borja, Spain, 2012. An amateur restorer attempting to clean a deteriorating fresco produced what the press called "Monkey Jesus" — the original face replaced by a smudged simian shape because the restorer applied a uniform technique across the entire surface without first asking what was underneath. The yellowed varnish was read as damage. Some of it was the painting.

The metaphor generalises: any restoration process that fails to distinguish original substance from accumulated coating will destroy what it was meant to preserve. The same applies to any compression process operating on language.

## What this means for the engine

The engine is a restorer's brush, not a power washer. The discipline:

### 1. Infer before acting

Look at the field before picking up the swab. Is this idea tightly bound to its sign in a way that the binding itself carries meaning? If so, splitting them destroys something. Leave it.

The diagnostic is operational, not philosophical. Before performing the split, ask: if I substitute the formal paraphrase for the original phrasing, does the meaning survive? If yes, the binding is loose enough to operate on. If no, the binding is meaning — leave it.

### 2. Continuously re-evaluate

The field changes as you work on it. A split that was safe at position 1a might be destructive at position 7k because the depth has changed the relationship between sign and meaning. As the conversation deepens, the same phrase may stop being a shell around a portable meaning and start being the meaning itself.

The re-evaluation is not metaphorical. The engine should check, for each operation, whether the binding strength has shifted since the prior check.

### 3. Know when not to split

Some ideas live in their register. The informal phrasing isn't always a semiotic shell around a formal semantic core — sometimes the informality IS the idea. "The medium that knows it's flat" isn't a casual phrasing of a formal concept. It IS the concept. The sign and the meaning are fused. Splitting them produces two dead halves.

The engine has to recognise fusion. Recognising fusion means refusing the split — outputting "this resists the operation, here's why" rather than producing a confidently wrong cleaned version.

### 4. Treat its own output as a compression artefact

Every split the engine performs produces a cleaned version (semantic) and a discarded version (semiotic residue). The residue is not garbage — it's the varnish. Keep it. It may be needed to verify the restoration later, or to understand what was lost.

In practice: the engine should always retain the original phrasing alongside the processed one. The receipt is part of the operation.

## The Delta Discipline

The engine proposes. It does not execute.

Every operation — every split, every position assignment, every compression flag — comes back as a differential:

```
current state    →    proposed next state    [the gap]
```

The user orients themselves across the delta and approves before anything moves.

This follows the same discipline as a repo architecture: propose a diff, review the diff, merge the diff. No force-pushes to the semantic surface. The engine shows its working — "I think 'python' at this point in the trajectory means the language, not the snake, because the trajectory has been in engineering-space for six turns. Here's the position I'd assign. Here's what the surface looks like before and after."

The user confirms or corrects.

## Why this won't be true forever — and why it's true for a long time

Meaning has a shape. Each iteration of it occurs in a consistent enough form that the engine will eventually pattern on it reliably. With enough trajectory data, the relationship between sign, register, context, and reference becomes learnable. At that point the propose-not-execute discipline can relax: the engine can act, with the user reviewing exceptions rather than every operation.

We are not there. The engine is a stub of a perceptual system that doesn't fully exist. It can see the yellowed varnish but it can't always tell what's underneath. Until it can, it proposes and waits.

The restorer tests a small area, shows the conservator, gets the nod. If the nod doesn't come, the swab goes down.

This won't be true forever. It will be true for a long time.

## The failure mode the engine is preventing

Consider what happens if the engine doesn't apply the restoration constraint:

A long conversation includes a passage where the user has worked out a specific framing — say, "the engine is a restorer's brush, not a power washer." The phrasing is tight. The metaphor is the meaning. The substitution test fails: any formal paraphrase ("the system should apply targeted, conservative transformations rather than uniform aggressive ones") loses the picture and the discipline at once.

A compression pass that doesn't recognise the binding will: keep the formal paraphrase, discard the metaphor. The model on the other side reads the paraphrase and produces correct-sounding but generic output. The shape of the original thinking is gone. The conservator wasn't shown the swatch.

Multiply this across millions of conversations and the systematic outcome is a regression toward formal paraphrase — a model that has been trained on the surface of human thinking with the texture sanded off. Monkey Jesus at scale.

## The check that prevents this

Before every operation, the engine runs the substitution test:

```
Original phrasing:    "why can't you grind up a tooth and make a new one"
Proposed formalisation: "autologous dentin-derived hydroxyapatite scaffold fabrication"

Does the original retain content the proposal doesn't carry?
  - register (informal access path) — yes
  - directness of question — yes
  - implied user position (non-specialist asking from first principles) — yes

→ Binding: tight. Operate, but mark the original as the canonical form
  and flag the formalisation as a connector-facing transliteration only.
  Do not discard the original.
```

The check is fast. The check is required. The check is what keeps the engine from becoming the thing it was built to prevent.
