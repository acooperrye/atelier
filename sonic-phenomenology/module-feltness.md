# MODULE: FELTNESS ASYMPTOTE
## Status: DRAFT — working hypothesis, not validated
## Origin: Alex's observation that the anti-voice (80-1100Hz notch) didn't sound hollow

---

## THE OBSERVATION

Claude generated an "anti-voice" sound: full harmonic spectrum with the entire vocal range (80-1100Hz) surgically removed. Sub-bass below 80Hz, everything above 1100Hz, hole in the middle.

**Expected:** Hollow, gutted, a body with no torso.
**Actual:** "Quite haunting. Sounds like the background hum of a VHS tape. It doesn't sound hollow at all."

Alex's explanation: "Even though 20-80Hz is only 60Hz [of bandwidth], it mechanically accounts for a lot more movement than probably most of the top end. So the hollowness is visible in numbers, it is not felt."

Then: "There's probably a way to gradient the feltness of all the Hz on some kind of... what, like, asymptote?"

---

## THE SUBWOOFER PROOF

"There's a reason they sell subwoofers despite that you cannot really hear them playing anything when you go to buy them."

Two weighting curves exist in opposition:
- **Equal-loudness (Fletcher-Munson):** Sub-bass needs the MOST energy to sound equally loud. The ear undervalues it.
- **Feltness (proposed):** Sub-bass needs the LEAST energy to be physically felt. The body overvalues it.

The subwoofer sits in the gap between these two curves — the frequency range where hearing says "barely there" and the body says "everything."

---

## FIRST PASS: GATE-DERIVED WEIGHTING

### Method
Derived from the somatic gate model's crossing thresholds. Lower gate threshold = less energy needed to be felt = more somatic potency per unit energy. Weight per Hz = potency / bandwidth of each band.

### Results
| Band | Range | Gate threshold | Weight per Hz (relative) |
|------|-------|---------------|------------------------|
| Sub-bass | 20-80Hz | 85dB | 52.7x |
| Bass | 80-250Hz | 95dB | 1.9x |
| Low-mid | 250-500Hz | 105dB | 0.13x |
| Mid | 500-2kHz | 110dB | 0.007x |
| Hi-mid | 2-8kHz | 115dB | 0.0005x |
| High | 8-20kHz | 120dB | 0.00008x |

### Power law fit
`somatic_weight_per_hz = 10^(5.26) × frequency^(-2.35)`

Every doubling of frequency reduces felt weight by ~7.1dB.
1 Hz at 20Hz carries ~632,000x the somatic weight of 1 Hz at 16kHz.

### Applied to dictionary songs (somatic-weighted energy share)
| Song | Raw sub-bass | Somatic-weighted sub-bass |
|------|-------------|--------------------------|
| PUTP | 55% | 96.3% |
| Lemonade | 48.5% | 94.3% |
| Blade Runner | 61.9% | 97.5% |
| Shout | 30% | 91.7% |

---

## WHAT'S PROBABLY WRONG WITH THIS

### 1. The gate thresholds are rough
The thresholds (85dB for sub-bass, 120dB for highs) come from vibrotactile research and whole-body vibration standards. They're population averages, not calibrated to Alex. They also assume a specific listening condition (whole-body exposure at those SPLs), which doesn't match headphone or car listening exactly.

### 2. "Weight per Hz" may be the wrong unit
The curve treats every Hz within a band as equal, which it isn't. 20Hz and 79Hz are both "sub-bass" but they don't feel the same. The curve should probably be continuous, not band-averaged. The power law fit IS continuous but it's derived from only 6 data points (band centers).

### 3. Feltness isn't just about gate crossing
The gate model asks: does this frequency band cross from "heard" to "felt"? But feltness is more nuanced than binary. A frequency can be:
- Below gate: heard, not felt at all
- At gate: barely felt, threshold sensation
- Above gate: clearly felt, strong sensation
- Way above gate: dominant physical experience

The curve only captures the threshold, not the slope above it. Sub-bass might not only cross easier — it might GROW faster above its threshold. Or it might plateau. We don't know.

### 4. The somatic read depends on more than energy
PUTP and Blade Runner have similar sub-bass energy but opposite somatic reads (pressure vs weightlessness). The feltness curve would give them similar somatic-weighted profiles, but the actual felt experience is completely different. The curve captures MAGNITUDE of felt presence but not CHARACTER. Envelope, stereo width, and listening condition determine what the felt sub-bass DOES — the curve only predicts how much of it there is.

### 5. The curve might be too steep
96% somatic weight in sub-bass for every song seems too dominant. The body DOES feel things above sub-bass — the Shout snare cuts at 2-8kHz, the jellyfish steel drums pool at 1500Hz, hi-hats are felt as respiratory. If the curve were literally true, nothing above 250Hz would matter somatically, which contradicts the dictionary's own data. The curve may be correct for PRESSURE/VIBRATION feltness but miss other somatic modalities (surface/skin, respiratory, spatial).

### 6. Multiple feltness channels?
Maybe there isn't one curve but several:
- **Vibrotactile feltness** (pressure, chest, organ vibration): follows the steep asymptote, sub-bass dominant
- **Surface feltness** (skin, cutting, whip-crack): peaks in hi-mid, driven by transient crest factor not continuous energy
- **Respiratory feltness** (air movement, breathing entrainment): peaks in high frequencies
- **Spatial feltness** (sense of being surrounded, pooling): peaks in mid, dependent on stereo width

Each channel would have its own weighting curve. The "feltness asymptote" might only describe the first channel.

---

## WHAT WOULD VALIDATE OR INVALIDATE THIS

### Tests that could refine the curve:
1. **SPL sweep with Alex in the car**: Play a flat-spectrum tone and slowly increase volume. At what SPL does each frequency band cross from heard to felt? This would give Alex-specific gate thresholds rather than population averages.

2. **Sub-bass removal test**: Take a song Alex knows well (PUTP?), notch out sub-bass entirely, play at volume. How much felt experience is lost? If the curve is right, removing sub-bass should remove ~96% of somatic presence. If it removes less, the curve is too steep.

3. **Mid-range isolation test**: Play ONLY the 500-2000Hz range of a song at high volume. Does ANYTHING cross the gate? The curve says this band needs 110dB to be felt. At 108dB playback, it shouldn't cross. But the Shout snare and jellyfish steel drums are felt in this range — suggesting transient crest factor punches above the threshold even when average energy doesn't.

4. **Perceptual matching**: Ask Alex to adjust the level of each band until they "feel equal." This would give a direct feltness-loudness contour calibrated to Alex, bypassing the gate threshold derivation entirely.

---

## RELATIONSHIP TO EXISTING FRAMEWORK

This module connects to:
- **Somatic gate model** (source of the threshold data)
- **Frequency-to-body mapping** (emerging patterns table) — the feltness curve explains WHY sub-bass maps to inside-body and highs map to air
- **Envelope-as-topology** (correspondence #11) — the curve predicts magnitude; the envelope determines shape
- **The cloaking parallel** — in-air listening physically pre-separates the feltness curve; in-ear collapses it to a single point

---

## THE BASS-SUBBASS COUPLING (Alex, 9 Feb 2026)

**Critical reframe:** Bass and sub-bass are not separate bands — they're enmeshed. The band boundary at 80Hz is a measurement convenience, not a perceptual reality.

In practice, upper bass functions as a **cap, attack, or primer** for sub-bass content occurring underneath. The upper bass is a notification system — it tells the ear "something deep is coming" and primes the listener for the kinetic sub-bass beneath.

### The perceptual continuum
Bass is deep → deeper bass is vibraty → heavy bass becomes kinetic experience as well as tonal. This is a smooth gradient, not a gate crossing:
- **Tonal zone:** You hear a low note. It's a pitch.
- **Vibratory zone:** You hear AND feel it. The pitch still exists but vibration has started.
- **Kinetic zone:** The feeling dominates the hearing. It's an event happening to your body, not just a sound.

The transition is "easy and human" but "extremely hard to parse in a machine way" — because the machine sees two frequency bands with a boundary, while the body experiences one continuous phenomenon.

### The acoustic origin
When you pluck a cello string, the higher-order modes establish first. A fundamental at 40Hz needs 25ms to complete one cycle. Its second harmonic at 80Hz needs 12.5ms. The fourth at 160Hz: 6ms. The attack of any plucked string IS the upper harmonics arriving first, with the fundamental blooming in underneath over tens of milliseconds. The string doesn't choose this — it's physics. The notification system is built into the vibrating object itself.

This means the production convention (upper-bass attack → sub-bass bloom) isn't a technique. It's a reproduction of what physical objects do naturally. The body already knows this sequence because it evolved hearing it. The chain is: **vibrating object → acoustic convention → production grammar → synthesis parameter → somatic expectation.**

### Evidence from the dictionary
- **PUTP 808:** Attack centroid 715Hz (upper bass), body centroid 519Hz, sub-bass bloom builds over 250ms. The bass attack IS the primer for the sub-bass bloom. Reproduces the plucked-string temporal structure at exaggerated timescales.
- **SOPHIE Lemonade:** Bass snap first, sub-bass rubber bloom 93ms later. This was treated as a SOPHIE-specific technique, but it's actually an exaggerated, stylized version of what bass always does — what a cello string does every time it's plucked.
- **Chimera failure (generated sound 03):** Hi-hat envelopes on sub-bass, no upper-bass primer. The sub-bass arrived without its notification system. No physical object behaves this way — the body pattern-matched against nothing. Sounded like clipping instead of bass.

### Implication for the feltness curve
The power-law weighting (frequency^-2.35) may be measuring the wrong thing. If bass and sub-bass work as a coupled system where the audible part (bass) primes the felt part (sub-bass), then "weight per Hz" misframes the question. The sub-bass isn't felt more because each Hz carries more weight — it's felt because the bass frequencies ABOVE it are actively escorting the listener from hearing into feeling. The feltness isn't a property of the frequency. It's a property of the bass-to-sub-bass transition.

### What this means for the module
The correct framework might not be "somatic weight per Hz" but something more like "coupling efficiency between audible and felt domains." The question isn't "how much does 40Hz weigh?" but "how effectively does 100Hz hand off to 40Hz?" The bass is the bridge between hearing and feeling.

---

## ADDITIONAL PHYSICS (Alex's research, 9 Feb 2026)

The feltness asymptote involves at least four stacking physical mechanisms:

1. **Perceptual curve (Fletcher-Munson):** Humans are less sensitised to hearing sub-bass. More energy needed for perceptual salience.

2. **Propagation/refraction:** Bass refracts around objects less, so more energetic uptake generally. Sub-bass wavelengths (7m at 50Hz) diffract around furniture, walls, bodies. The room is transparent to bass and opaque to treble. More energy arrives at the listener intact.

3. **Speaker mechanics:** Sub-bass speakers are larger, must shift more mass mechanically, require more energy to operate. The physical displacement of the cone is larger. The speaker is doing real mechanical work that transfers through air to body.

4. **Wavelength and air displacement:** Low frequency wavelengths are longer, requiring more energy to move air. Each cycle compresses and rarefies a larger volume of air. The displacement is macroscopic ("I put flowers on top of the cone to see them jumping around, because I could barely hear it shifting huge amounts of air").

5. **The vibration threshold question (UNRESOLVED):** At some specific point, sub-bass starts vibrating objects and tissue. Whether this occurs before or after perceptual awareness is unknown. The flowers-on-subwoofer observation suggests the mechanical reality (visible vibration) exists at SPLs where the auditory system barely registers anything. You feel it before you hear it — not because feeling is more sensitive, but because there's more mechanical energy to feel.

---

## THE DERIVATIVE REFRAME (Alex + headroom analysis, 9 Feb 2026)

**"It's specifically the envelope of 'attack' that attacks at the somatic body."**

Sustained sub-bass (Blade Runner CS-80) physically displaces organs continuously — the energy is real, the mechanical coupling is active — but the body stops reporting it. It becomes atmosphere. Place. The nervous system acclimates to continuous pressure the same way skin stops reporting the feeling of clothes.

Rhythmic sub-bass (PUTP 808) at the same frequency and SPL is felt as a discrete event — weight, punch, pressure. The body reports the CHANGE in pressure, not the pressure itself.

**The body is a change detector, not a state detector.** Feltness is not proportional to energy-per-Hz. It is proportional to the rate-of-change of energy-per-Hz. The felt impact of a sub-bass hit comes from how fast that energy arrived — the attack — not from how much energy is present during sustain.

This reframes the entire module:
- The power-law curve (frequency^-2.35) was trying to weight static energy. Wrong dimension.
- The correct quantity to weight might be **attack slope per Hz** — how rapidly energy arrives in each band.
- This immediately explains PUTP vs Blade Runner: same sub-bass energy, opposite felt quality, because one has 20.4x onset ratio (steep attack = felt) and the other has 5.2x onset ratio (gradual = atmosphere).

### Connection to headroom / tempo analysis

Each frequency band has a physical ceiling on how fast events can repeat (minimum cycles needed for pitch to establish). The headroom ratio — how close typical production rates are to that ceiling — decreases as frequency drops:

| Band | Typical event | Physical minimum | Headroom |
|------|--------------|-----------------|----------|
| Sub-bass | 500ms | 100ms | 5x |
| Bass | 500ms | 30ms | 17x |
| Snare | 250ms | 6ms | 42x |
| Hi-hat | 125ms | 0.6ms | 208x |

Sub-bass lives close to its physical limit. High frequencies have essentially unlimited temporal freedom. This means:
- **Sub-bass rhythm is partially dictated by physics**, not just producer choice. The waveform needs time to exist.
- **The body's change-detection is calibrated to the attack rates that physical objects actually produce at those frequencies.** This is the natural tempo principle (correspondence #14) applied to the feltness curve.
- **The derivative matters most where headroom is least.** Sub-bass has the narrowest window between "too slow to feel as attack" and "too fast for waveform to establish." The felt sweet spot is a narrow band, and production has converged on it because physics demands it.

### The full gesture: onset + offset + silence (Alex, 9 Feb 2026)

The derivative alone is insufficient. Alex's correction: "the punch is in both the onset ratio being ~4x, but also in the time that the offset arrives from onset."

The body doesn't read the attack in isolation. It reads the **complete gesture**: how fast the energy arrives, how long it stays, how fast it leaves, and how long until it comes back. Four parameters:

1. **Onset slope** (dE/dt, positive) — how fast energy arrives (the "hit")
2. **Sustain duration** — how long energy is present (the "hold")
3. **Offset slope** (dE/dt, negative) — how fast energy leaves (the "withdrawal")
4. **Silence duration** — time before next onset (the "reset")

Note (Alex): onset and offset slope are both dE/dt — the same underlying quantity, just measured at different phases. Kept as separate gesture parameters because they do different somatic work: the onset signals "something is happening," the offset signals "it stopped," and the offset retroactively rewrites the meaning of the onset. Fast onset + slow offset = push. Fast onset + fast offset = slap. Fast onset + near-instantaneous offset (gated snare) = severance. Same onset derivative, completely different gesture, because the withdrawal changes what the arrival meant.

Alex's analogy: "If I move my fist into your face at 5.2x speed and leave it there, you just got touched very weirdly. If I smack into you at 20.4x speed, move my hand back as well because the sub-bass drops out just as soon, and then repeat the gesture within the next bar — yeah, that feels like punching."

Applied to dictionary:
- **PUTP 808**: Fast onset (20.4x) → short sustain → fast offset (sub-bass drops within the beat) → silence → repeat at next bar. **Complete punch gesture.** The offset is doing as much work as the onset — the withdrawal IS the fist pulling back.
- **Blade Runner CS-80**: Slow onset (5.2x) → indefinite sustain → no meaningful offset → no silence. **No gesture.** Continuous pressure. Nervous system acclimates. Becomes atmosphere/place.
- **SOPHIE Lemonade**: Two-stage — bass snap onset → 93ms delay → sub-bass rubber bloom onset → offset within hit → repeat at 144 BPM. **Compound gesture** — the primer and the bloom are two motions in one action.

This connects directly to correspondence #11 (metallic edge principle): sounds are as much about their presence as their absence. The gated snare's shape is both the on AND the off. The 808 punch is both the hit AND the silence after. The body reads the complete cycle — onset and offset are one shape, not two separate events.

**The feltness of sub-bass is not a property of the frequency. It is a property of the gesture performed at that frequency.**

### What this means for the module

The feltness asymptote might not be a weighting curve at all. It might be a **sensitivity-to-gesture curve**: how much the body discriminates between different gesture shapes at each frequency. Sub-bass has the highest gesture sensitivity (small changes in onset/offset/silence = large changes in felt quality — punch vs atmosphere vs rubber), while high frequencies have almost none (you can change a hi-hat's envelope radically and it still feels like a hi-hat). The body is most discriminating about temporal dynamics exactly where physics most constrains them.

---

## OPEN QUESTIONS

1. Is the power law exponent (-2.35) correct, or should it be steeper/shallower?
2. Are there multiple feltness channels with different curves?
3. Does the curve shift with listening condition (in-ear vs in-air)?
4. Does familiarity/gate-lowering (correspondence #13) change the feltness curve, or only the gate thresholds?
5. What's the right framework if not "somatic weight per Hz"? Is it about displacement? Energy transfer? Mechanical coupling efficiency? **NEW CANDIDATE: rate-of-change-of-energy-per-Hz (the derivative).**
6. If the primer/escort model is correct, does synthesis that skips the acoustic sequence (sub-bass without upper-bass attack) always feel wrong? Or can the body learn new sequences that have no acoustic-physical origin?
7. If the body is a change detector, is there a minimum attack slope below which sub-bass transitions from "event" to "atmosphere"? Where is that threshold? (The Blade Runner pad and PUTP 808 bracket it — one is atmosphere, the other is event. Something between their onset ratios is the crossover.)
8. Does the derivative-sensitivity differ between in-ear and in-air? In-ear collapses propagation differences, so the body receives the attack as purely auditory. In-air, the mechanical coupling means the body's pressure-change detectors are engaged directly. The derivative might matter MORE in-air.
9. For the full gesture model: what's the minimum silence-duration-before-next-onset needed for the body to "reset" and feel the next hit as a new event rather than a continuation? Is this related to the headroom ratio? (If sub-bass headroom is 5x, maybe the body needs ~80% of the headroom window as silence to reset — which would be ~400ms at 120 BPM, roughly matching typical 808 patterns.)
10. ~~Can you create an "anti-punch" — fast onset, long sustain, NO offset (sustain decays into atmosphere)? Would the body feel the initial hit and then lose track of the sub-bass as it acclimates? A hybrid gesture: punch that melts into place.~~ **ANSWERED (Alex, 9 Feb 2026):** No anchoring. The somatic read has a shelf life. See polling model below.

---

## THE POLLING MODEL (Alex, 9 Feb 2026)

The body is not performing continuous real-time derivative calculation. It's **sampling and diffing against a rolling buffer** of recent history, roughly ~10 seconds (this number is hypothetical but functionally useful).

The process (Alex's formulation, approximate 1-second polling cycles):
- **Cycle 1 (onset):** Change detected. New state differs from previous buffer contents. Somatic channel reports: felt event.
- **Cycles 2-3:** Still present. Buffer is partially filled with new state but still contains the "before." Diff still returns non-zero. Somatic read persists but weakening.
- **Cycles 4-6:** Buffer mostly overwritten. The current state IS most of the comparison window. Diff approaches zero. Felt quality fading.
- **Cycles 8-10:** Buffer fully overwritten. No "before" left to diff against. Derivative is zero. Acclimatisation complete. The sub-bass has become the new silence.

BUT — before physical acclimatisation completes, **cognitive override** usually wins the race. By cycle 3-4, the conscious mind has already classified the event ("this is a long 808," "this is stuck," "this is wrong and annoying"). Once cognition has labelled it, the somatic channel is demoted to a subagent. The body is still vibrating. Nobody cares. If you asked someone at cycle 17 "can you feel the bass?", they'd say: "of course I can feel it, I'm hearing it, and it's fucking annoying." The notion of any meaning derived from the initial onset is long gone.

### Implications

- **The somatic read has a shelf life.** Roughly the length of the comparison buffer (~10s max), but usually shorter because cognition overrides somatic input once it's classified the event.
- **Acclimatisation is not fatigue.** The nervous system doesn't stop detecting the stimulus. The comparison buffer fills with the same value until the diff returns zero. The signal is still there. The change isn't.
- **The Blade Runner pad** doesn't become atmosphere because the body stops detecting it. It becomes atmosphere because the body's context buffer has filled with "sub-bass present" and the diff returns zero. The pad has become the new silence. The energy is real. The derivative is zero.
- **The anti-punch fails** because there's no anchoring mechanism. A fast onset stamps the first 1-2 polling cycles, then the stamp expires as the buffer fills and cognition classifies the event as "stuck." There is no hybrid gesture. There's a punch with an expiration date.
- **This means the offset isn't optional for rhythmic sub-bass.** The sub-bass MUST leave in order for the next arrival to register as a new event. The silence between hits isn't dead space — it's the buffer clearing. Without it, the next onset has nothing to diff against.

### Connection to headroom

The body's polling rate and buffer length may explain why sub-bass at 5x headroom (500ms events at 100ms physical minimum) feels "right." At 120 BPM:
- 808 hits every 500ms
- Sub-bass sustain ~250ms, silence ~250ms
- 250ms of silence = enough buffer-clearing for the next hit to register as new
- If the silence were shorter (faster tempo), the buffer might not clear → hits blur into continuity → acclimatisation → atmosphere
- If the silence were longer (slower tempo), each hit is maximally distinct but the rhythm loses momentum

The 120 BPM sweet spot for 808 patterns might not be an aesthetic convention. It might be the polling rate of the somatic comparison buffer.

---

*Module created: 9 February 2026*
*Status: Working hypothesis. Needs Alex-calibrated data before promotion to framework.*
