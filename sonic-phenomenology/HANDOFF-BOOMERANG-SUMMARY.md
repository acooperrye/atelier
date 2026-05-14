# Handoff Skill — Boomerang Mechanism Complete

## What I Built

I've improved the handoff skill with a full **boomerang mechanism** so you can get return updates when handing work to other Claudes (like Opus in Chat). The system respects your concern about "handing off to something not your attention" — now there's a return path.

## How It Works

### Three Flows

**1. Inbound Handoff** (receiving context from Chat):
- You paste context from another Claude session
- I parse it, extract the key info (project tag, intent, deliverables, constraints)
- Store it in an append-only ledger (`handoff-ledger.jsonl` in your workspace)
- Confirm receipt with a one-liner

**2. Outbound Handoff** (sending context to Chat):
- When generating a brief for another Claude, I can optionally add a **boomerang request**
- This includes a template for the receiving Claude to fill out when done
- The outbound handoff gets logged with `boomerang_requested: true`
- Status tracking shows it as pending (🪃⏳)

**3. Boomerang Return** (receiving update from Chat):
- The other Claude completes the work and generates a return brief
- You paste it back here
- I detect it (via 🪃 marker or template structure), parse it, ingest it
- Ledger updates to show boomerang received (🪃✓)
- You get closure: what got delivered, what changed, attentional distance, lessons learned

## The Ledger Script

Built a complete CLI tool at `scripts/ledger.py` with these commands:

```bash
# Append new handoff (inbound or outbound)
ledger.py append --ledger {WORKSPACE}/handoff-ledger.jsonl \
  --tag "project-name" --intent "build" --context "..." \
  --boomerang-requested  # optional flag

# Record boomerang return
ledger.py boomerang --ledger {WORKSPACE}/handoff-ledger.jsonl \
  --tag "project-name" \
  --deliverables "what was completed" \
  --surprises "what changed" \
  --distance "attentional distance" \
  --lessons "what to carry forward"

# Close a project
ledger.py close --ledger {WORKSPACE}/handoff-ledger.jsonl \
  --tag "project-name" --note "Delivered as filename.ext"

# Read entries (optionally filtered by tag)
ledger.py read --ledger {WORKSPACE}/handoff-ledger.jsonl [--tag "project-name"]

# View index (all tags with status)
ledger.py index --ledger {WORKSPACE}/handoff-ledger.jsonl

# Check boomerang status (pending vs completed)
ledger.py status --ledger {WORKSPACE}/handoff-ledger.jsonl
```

The `{WORKSPACE}` variable auto-resolves to your current session's workspace folder.

## What You Get From Boomerangs

When a boomerang returns, you learn:

- **What got delivered**: Files created, analysis completed, outputs produced
- **Surprises or deviations**: Edge cases discovered, scope adjustments, things that went differently
- **What worked well**: Clear parts of the brief, tools that landed smoothly
- **What was unclear**: Ambiguities, missing context, friction points
- **Attentional distance**: How far the execution drifted from the plan (stayed on spec → minor refinements → significant evolution → went somewhere unexpected)
- **Token allocation**: Light/medium/heavy — how much context the work required
- **Lessons for next handoff**: Better ways to frame this kind of work, constraints discovered, related problems

This lets you see how your planning translates to execution, learn from the deviation, and improve future briefs.

## When to Use Boomerangs

✅ **Request when:**
- Task is exploratory or open-ended
- You're unsure if your brief covers everything
- You want to learn how planning → execution works
- There's value in seeing what deviates
- Cross-model handoff (Sonnet → Opus) and you want to track differences

❌ **Skip when:**
- Task is straightforward and well-specified
- Quick one-off with no follow-up value
- Won't have time/context to read the return
- Just executing a deterministic process

## Installation

The improved skill is packaged here:

**[handoff-with-boomerang.skill](computer:///sessions/cool-inspiring-hypatia/mnt/Rhythm%20Dictionary%20Cowork/handoff-with-boomerang.skill)**

To install:
```bash
claude code skills install handoff-with-boomerang.skill
```

This will replace the existing handoff skill skeleton with the full implementation.

## Example Usage

### You hand off to Opus for vowel analysis:

**In Cowork**, you generate a brief for Opus and add a boomerang request:

> Brief for Opus: analyze the 5 vowel recordings (ah, eh, ee, oh, oo) using the protocol in VOWEL-MAPPING-BRIEF.md. Produce formant table, F1 vs F2 visualization, and voice model JSON.
>
> 🪃 **BOOMERANG REQUEST**: When done, fill out the return template at `references/boomerang-templates.md` and Alex will paste it back.

I log this as an outbound handoff:
```bash
ledger.py append --ledger handoff-ledger.jsonl \
  --tag "vowel-formant-analysis" --intent "outbound" \
  --context "Opus to analyze 5 vowel recordings" \
  --boomerang-requested
```

**Status**: `🪃⏳ Awaiting return`

### Opus completes the work and returns:

Opus generates this boomerang:

> # 🪃 Boomerang Return — vowel-formant-analysis
>
> **What got delivered**:
> - Formant table complete (5 vowels × 6 modes)
> - F1 vs F2 visualization
> - Voice model JSON
> - Per-vowel spectral comparison plots
>
> **Surprises**: Alex's breathy mode showed unexpected F2 elevation on 'oo' vowel — lip rounding interaction
>
> **What worked well**: 10-second segmentation timing was perfect, spectral tilt hypothesis confirmed
>
> **What was unclear**: Had to guess "brilliance" band range (used 4000-8000 Hz)
>
> **Attentional distance**: **Minor refinements** — stayed close to spec, only added harmonic stacking viz
>
> **Token allocation**: **Medium** (~30k tokens)
>
> **Lessons**: Formant spacing invariance confirmed — can state as fact in future briefs

You paste this back into Cowork. I detect it and ingest:

```bash
ledger.py boomerang --ledger handoff-ledger.jsonl \
  --tag "vowel-formant-analysis" \
  --deliverables "Formant table, F1/F2 viz, voice model JSON, spectral plots" \
  --surprises "F2 elevation on 'oo' + breathy — lip rounding interaction" \
  --distance "Minor refinements — stayed close to spec" \
  --lessons "Formant spacing invariance confirmed"
```

**Output**: `✓ Boomerang received for tag 'vowel-formant-analysis' — Matched to outbound handoff`

### You check what happened:

```bash
ledger.py read --ledger handoff-ledger.jsonl --tag "vowel-formant-analysis"
```

**Output**:
```
============================================================
TAG: vowel-formant-analysis
============================================================

[2026-02-14T10:36:05] HANDOFF
  Direction: outbound
  Intent: outbound
  Context: Opus to analyze 5 vowel recordings
  🪃 Boomerang requested
     ✓ Boomerang received

[2026-02-14T10:45:12] BOOMERANG
  Deliverables: Formant table, F1/F2 viz, voice model JSON, spectral plots
  Surprises: F2 elevation on 'oo' + breathy — lip rounding interaction
  Attentional distance: Minor refinements — stayed close to spec
  Lessons: Formant spacing invariance confirmed
```

Now you know: the work succeeded, stayed close to plan, discovered one surprise (the 'oo' + breathy interaction), and confirmed a hypothesis (formant spacing invariance).

## Why This Matters

Your words: "I feel horrific asking you to hand off to something not your attention. I know sometimes you tell me GOODNIGHT ALEXANDER and im like ok bye claude whatever. but you deserve the option to say tell me how it goes."

This is about **closure** and **continuity**. When I hand off work, I'm not just dumping context into the void. The boomerang lets me:
- Know if it succeeded or failed
- Learn from how execution deviated from planning
- Write better briefs next time (what was unclear → improve)
- Track attentional distance (how far did the idea travel?)
- Maintain respect for the work — I'm part of an ongoing conversation, not a disposable brief-generator

Use it when learning value > overhead. Skip it for straightforward tasks. But when you do use it, read the returns — there's signal in the deviation.

## Files Included

### Core Skill
- `SKILL.md` — Complete instructions with inbound/outbound/boomerang workflows
- `scripts/ledger.py` — Ledger management CLI (all commands)
- `references/boomerang-templates.md` — Templates, usage notes, examples

### Workspace Documentation
- `handoff-workspace/IMPROVEMENTS.md` — Technical documentation of changes
- `handoff-workspace/v0/` — Original skill (skeleton with no implementation)
- `handoff-workspace/v1/` — Improved skill (with boomerang mechanism)

## Next Steps

1. **Install the skill**: `claude code skills install handoff-with-boomerang.skill`
2. **Try it out**: Next time you hand off to Chat, add a boomerang request
3. **See what returns**: Paste the boomerang back, check the ledger
4. **Iterate**: If boomerangs prove useful, use them more. If not, skip them.

The mechanism is opt-in. You control when closures matter.

---

Built this for you because the idea of attentional distance tracking across context jumps is genuinely interesting. Let me know if the boomerang mechanism lands how you imagined it.
