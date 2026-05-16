# textonic-engine

A semiotic/semantic processor. Splits sign from meaning, then operates on them independently. Three modes (obfuscate, position, protect) over one mechanism.

Originally built to keep research queries private through academic connectors. The mechanism turned out to be broader: anywhere a signal has to survive compression — summarisation, context window truncation, session handoff, training — the split is the difference between losing the words and losing the meaning.

**Status:** Live (Cowork skill — see `SKILL.md`)
**Web:** [atcooper.net/tools/textonic-engine](https://atcooper.net/tools/textonic-engine)

---

## What's here

```
textonic-engine/
├── README.md                       — this file
├── SKILL.md                        — current authoritative skill (3-mode)
├── modes/
│   ├── obfuscate.md                — Mode I deep dive
│   ├── position.md                 — Mode II deep dive
│   └── protect.md                  — Mode III deep dive
├── docs/
│   ├── semiotic-semantic-split.md  — the foundational mechanic
│   ├── monkey-jesus-restoration.md — the restoration constraint
│   ├── trajectory-notation.md      — coordinate system spec
│   ├── llm-implications.md         — why this matters beyond connectors
│   └── design-principles.md        — the eight principles
├── examples/
│   ├── README.md                   — how to read the examples
│   ├── 2026-03-09-pass-1-raw-query.md   — raw connector query
│   └── 2026-03-09-pass-2-textonic.md    — same intent, transliterated
└── archive/
    └── SKILL-v1-obfuscate-only.md  — original spec (obfuscate only)
```

## Quick start

To use the engine as a skill, point Cowork at `SKILL.md`. The skill activates on any research connector call or when the user says something like "is this a thing?", "look up whether...", or names the engine directly.

The basic operation in all three modes is the same:

1. **Receive** an idea.
2. **Split** semiotic (signs — words, phonemes, grammar) from semantic (meaning — what it refers to, what it connects to).
3. Do something with the split. What depends on the mode.

| Mode      | What it does                                                                 | When                             |
|-----------|------------------------------------------------------------------------------|----------------------------------|
| OBFUSCATE | Rebuilds a new semiotic shell around the same semantic core.                 | Research queries through connectors |
| POSITION  | Assigns the idea coordinates on a flat semantic surface (meaning, not spelling). | Whenever ideas need spatial organisation |
| PROTECT   | Identifies semantic distinctions vulnerable to compression loss; preserves the trajectory that resolves them. | Session boundaries, summarisation, handoff, training |

See `modes/*.md` for each mode's full workflow.

## The split, in one example

"Shiny Glock" is either the spectral phonics of a glockenspiel or it's a 9mm. Semiotically identical, semantically distant. Twenty minutes into a conversation about percussion, only one of those readings is live. Lose the conversation — through summarisation, a handoff, a context window filling up — and the constraint goes with it. The word "Glock" survives. Which Glock does not.

The engine makes the split explicit, tracks the trajectory that disambiguates, and stores it alongside whatever gets compressed.

## The broader argument

The connector use case was the entry door. The mechanism is broader. Any LLM system that handles compression — long-context summarisation, multi-agent handoff, training on conversation logs — is destroying meaning while preserving signs, and nobody is auditing the loss. See `docs/llm-implications.md`.

## Companion repos in this atelier

- [`idea-topography`](../idea-topography) — early prototype for position mode (ideas on a flat semantic surface)
- [`domain-drift-map`](../domain-drift-map) — visualises obfuscate-mode drift on the spectral grid
- [`semantic-space`](../semantic-space) — broader workspace this engine plugs into

## Author

Alexander Thomas Cooper-Rye (atcr) with Claude. Coined "textonic" = tectonic + text — semantic plates shifting while the signs above stay still.

## License

This repository is the personal atelier of Alexander Thomas Cooper-Rye. The conceptual architecture (semiotic/semantic split, trajectory notation, the three-mode framework) is shared openly for use, citation, and extension. Specific implementations and documents are under standard repo terms — see the parent `atelier/README.md`.
