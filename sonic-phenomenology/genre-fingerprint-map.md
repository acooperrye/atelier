# GENRE → FINGERPRINT MAP
## Rhythm Dictionary — Lookup Table
## 2026-02-10 · Continuously updatable

---

## PURPOSE

Once genre is committed (Phase A), this document is the search function. Look up the genre, get back a list of fingerprint IDs. Each ID points to a full definition in fingerprint-registry.md.

No need to define every genre from scratch. Genres are assembled from universal fingerprint atoms.

**Adding a new genre:** list its fingerprint IDs from fingerprint-registry.md. Mark each as ● defining, ○ common, or △ occasional.

**Cross-reference:** fingerprint-registry.md defines each fingerprint. engine-cultural.md uses these for convention detection.

---

## KEY

| Symbol | Meaning |
|--------|---------|
| ● | **Defining** — if this fingerprint is absent, question the genre classification |
| ○ | **Common** — expected but not genre-defining; absence is unremarkable |
| △ | **Occasional** — appears in some tracks of this genre, not most |
| ✱ | **Violation marker** — this fingerprint's ABSENCE or INVERSION is the convention (the genre deliberately subverts this shape) |

---

## ELECTRONIC

### House
```
● FP-T02 (standard tempo, 118-132 BPM)
● FP-T05 (regular beat grid)
● FP-E01 (sharp attack / natural decay — kick)
● FP-S01 (sub-bass dominant) or FP-S02 (bass-heavy)
● FP-R05 (loop-based / repetitive)
○ FP-E07 (sidechain pump)
○ FP-D02 (moderate crest factor)
○ FP-W04 (center-priority mixing)
○ FP-H01 (hi-mid percussive)
○ FP-X01 (rhythm heard, bass felt)
○ FP-R02 (build-drop form) — in progressive/big room
△ FP-V01 (vocal foreground) — in vocal house
△ FP-V02 (vocal as texture) — in deep house
△ FP-P04 (analog warmth)
```

### Techno
```
● FP-T02 (standard tempo, 125-145 BPM)
● FP-T05 (regular beat grid)
● FP-E01 (sharp attack / natural decay)
● FP-R05 (loop-based / repetitive)
● FP-S02 (bass-heavy)
○ FP-D03 (low crest factor)
○ FP-E07 (sidechain pump)
○ FP-W04 (center-priority mixing)
○ FP-H01 (hi-mid percussive)
○ FP-V03 (no vocal)
○ FP-P05 (digital precision) — in minimal/industrial techno
△ FP-R06 (additive layering)
△ FP-E08 (sustained with micro-variation) — in atmospheric techno
△ FP-P04 (analog warmth) — in classic/Detroit techno
```

### Trance
```
● FP-T02 or FP-T03 (128-150 BPM)
● FP-T05 (regular beat grid)
● FP-R02 (build-drop form)
● FP-E07 (sidechain pump)
● FP-R06 (additive layering)
○ FP-S01 (sub-bass dominant)
○ FP-D05 (section-level dynamic contrast)
○ FP-E03 (slow onset / long sustain — pads)
○ FP-W02 (moderate stereo)
○ FP-H01 (hi-mid percussive)
△ FP-V01 (vocal foreground) — in vocal trance
△ FP-E08 (sustained micro-variation — supersaw detuning)
```

### Drum and Bass
```
● FP-T03 (fast tempo, 160-180 BPM)
● FP-S01 (sub-bass dominant)
● FP-X04 (independent layers — bass and breaks as dual system)
● FP-H01 (hi-mid percussive)
● FP-T09 (high onset density)
○ FP-T05 (regular beat grid)
○ FP-E04 (bloom envelope — reese bass)
○ FP-D02 (moderate crest factor)
○ FP-W04 (center-priority mixing)
○ FP-R04 (sample-based — chopped amen)
○ FP-V03 (no vocal)
△ FP-E07 (sidechain pump) — in liquid DnB
△ FP-R02 (build-drop form) — in jump-up
△ FP-V02 (vocal as texture)
```

### Jungle
```
● FP-T03 (fast tempo, 155-175 BPM)
● FP-S01 (sub-bass dominant)
● FP-X04 (independent layers — breaks and bass separate)
● FP-R04 (sample-based — amen break source)
● FP-T09 (high onset density)
● FP-H01 (hi-mid percussive)
○ FP-E04 (bloom envelope)
○ FP-T06 (human-feel timing — original break groove)
○ FP-W04 (center-priority mixing)
○ FP-D02 (moderate crest factor)
△ FP-V02 (vocal as texture — ragga samples)
△ FP-P04 (analog warmth)
```

### Breakcore
```
● FP-T04 (extreme tempo, 160-220+ BPM)
● FP-T10 (extreme onset density — approaching tonal threshold)
● FP-R04 (sample-based / chopped)
● FP-D04 (brick-wall limited)
● FP-R03 (through-composed / continuous)
○ FP-S01 (sub-bass dominant) or FP-S05 (even distribution)
○ FP-X02 (shadow bass) — may be Venetian Snares-specific
○ FP-T07 (irregular meter)
○ FP-V03 (no vocal)
○ FP-P06 (intentional distortion/clipping)
○ FP-P08 (tracker precision)
○ FP-D06 (relentless escalation)
△ FP-H02 (hi-mid harmonic — drums becoming tonal through density)
△ FP-V02 (vocal as texture)
✱ FP-H01 → FP-H02 (VIOLATION: drums cross from rhythmic to tonal)
✱ FP-X01 → inverted (VIOLATION: bass becomes beat, drums become drone)
```

### Dubstep
```
● FP-T02 (standard tempo, 138-142 BPM, half-time feel)
● FP-S01 (sub-bass dominant)
● FP-E04 (bloom envelope — wobble bass)
● FP-D05 (section-level dynamic contrast)
○ FP-R02 (build-drop form)
○ FP-D01 (high crest factor) — in classic dubstep
○ FP-D04 (brick-wall limited) — in brostep
○ FP-W04 (center-priority mixing)
○ FP-H01 (hi-mid percussive)
○ FP-P06 (intentional distortion) — in brostep
△ FP-V02 (vocal as texture)
△ FP-T06 (human-feel timing)
```

### Ambient
```
● FP-E03 (slow onset / long sustain)
● FP-E08 (sustained with micro-variation)
● FP-T08 (free time / no pulse) or FP-T01 (slow tempo)
● FP-R03 (through-composed)
○ FP-W03 (wide stereo)
○ FP-P01 (natural room / reverb)
○ FP-P07 (detuned oscillators)
○ FP-V03 (no vocal)
○ FP-D02 (moderate crest factor) or FP-D01 (high crest)
○ FP-S06 (spectral scoop) — in some subtractive ambient
△ FP-S01 (sub-bass dominant) — in dark ambient
△ FP-R06 (additive layering)
△ FP-T05 (regular beat grid) — in ambient with pulse
```

### IDM (Intelligent Dance Music)
```
● FP-T07 (irregular meter)
● FP-P05 (digital precision)
○ FP-T09 (high onset density)
○ FP-R04 (sample-based)
○ FP-S05 (even distribution) or FP-S01 (sub-bass dominant)
○ FP-W02 (moderate stereo)
○ FP-D02 (moderate crest factor)
○ FP-V03 (no vocal) or FP-V02 (vocal as texture)
△ FP-E05 (two-stage envelope — Autechre-style multi-phase events)
△ FP-R05 (loop-based) — in Boards of Canada territory
△ FP-P07 (detuned oscillators)
△ FP-T10 (extreme onset density)
```

### Garage / UK Garage
```
● FP-T02 (standard tempo, 128-135 BPM)
● FP-T06 (human-feel timing — shuffle/swing)
● FP-S01 (sub-bass dominant)
○ FP-V01 (vocal foreground)
○ FP-E01 (sharp attack / natural decay)
○ FP-H01 (hi-mid percussive)
○ FP-W04 (center-priority mixing)
○ FP-R01 (verse-chorus form)
△ FP-E07 (sidechain pump)
△ FP-P04 (analog warmth)
```

### Grime
```
● FP-T02 (standard tempo, 138-142 BPM)
● FP-S01 (sub-bass dominant)
● FP-V01 (vocal foreground — MC)
● FP-T05 (regular beat grid)
○ FP-D03 (low crest factor)
○ FP-H01 (hi-mid percussive)
○ FP-P05 (digital precision)
○ FP-W04 (center-priority mixing)
△ FP-R04 (sample-based)
△ FP-E07 (sidechain pump)
```

### Trap (Electronic)
```
● FP-T02 (standard tempo, 130-170 BPM, half-time feel)
● FP-S01 (sub-bass dominant)
● FP-E04 (bloom envelope — 808)
● FP-T05 (regular beat grid)
○ FP-T09 (high onset density — hi-hat rolls)
○ FP-D03 (low crest factor)
○ FP-W01 (mono/near-mono — for bass)
○ FP-X01 (rhythm heard, bass felt)
○ FP-P05 (digital precision)
△ FP-R02 (build-drop form)
△ FP-V02 (vocal as texture)
```

### Synthwave / Retrowave
```
● FP-P04 (analog warmth / saturation)
● FP-E08 (sustained with micro-variation — synth pads)
● FP-T02 (standard tempo, 80-130 BPM)
○ FP-R01 (verse-chorus form) or FP-R05 (loop-based)
○ FP-S02 (bass-heavy)
○ FP-E02 (sharp attack / gated decay — retro snare)
○ FP-P03 (gated reverb)
○ FP-W02 (moderate stereo)
○ FP-D02 (moderate crest factor)
△ FP-V01 (vocal foreground) or FP-V03 (no vocal)
△ FP-P07 (detuned oscillators)
```

### Industrial
```
● FP-P06 (intentional distortion)
● FP-D03 or FP-D04 (low/brick-wall crest factor)
● FP-T05 (regular beat grid)
○ FP-T02 (standard tempo, 110-140 BPM)
○ FP-S03 (mid-heavy)
○ FP-H04 (sub-bass noise/percussive) — in power electronics
○ FP-R05 (loop-based)
○ FP-V01 (vocal foreground) or FP-V02 (vocal as texture)
△ FP-E02 (gated decay)
△ FP-P03 (gated reverb) — in EBM
△ FP-T09 (high onset density)
```

### Noise
```
● FP-H05 (HPSS ambiguous)
● FP-P06 (intentional distortion)
● FP-T08 (free time / no pulse) or FP-T05 (regular grid — in HNW)
● FP-R03 (through-composed)
○ FP-D04 (brick-wall limited)
○ FP-V03 (no vocal)
○ FP-S04 (treble-bright) or FP-S05 (even distribution)
△ FP-E03 (slow onset / long sustain) — in drone-noise
△ FP-W03 (wide stereo)
```

### Downtempo / Trip-Hop
```
● FP-T01 or FP-T02 (slow-to-standard, 70-110 BPM)
● FP-S01 or FP-S02 (bass-heavy)
● FP-T06 (human-feel timing)
○ FP-R04 (sample-based)
○ FP-E04 (bloom envelope)
○ FP-D01 (high crest factor)
○ FP-P01 (natural room / reverb)
○ FP-W02 (moderate stereo)
△ FP-V01 (vocal foreground)
△ FP-E08 (sustained micro-variation)
△ FP-P04 (analog warmth)
```

### Footwork / Juke
```
● FP-T04 (extreme tempo, 155-165 BPM)
● FP-R04 (sample-based)
● FP-R05 (loop-based)
● FP-V02 (vocal as texture — chopped vocal samples)
○ FP-S01 (sub-bass dominant)
○ FP-T09 (high onset density)
○ FP-D03 (low crest factor)
○ FP-T05 (regular beat grid)
△ FP-E05 (two-stage envelope)
△ FP-P05 (digital precision)
```

### Future Bass
```
● FP-E07 (sidechain pump)
● FP-R02 (build-drop form)
● FP-W03 (wide stereo)
○ FP-T02 (standard tempo, 130-170 BPM)
○ FP-S01 (sub-bass dominant)
○ FP-V02 (vocal as texture — pitched-up vocal chops)
○ FP-D05 (section-level dynamic contrast)
○ FP-P05 (digital precision)
△ FP-E08 (sustained micro-variation — supersaws)
△ FP-R06 (additive layering)
```

---

## HIP-HOP / RAP

### Boom Bap
```
● FP-T02 (standard tempo, 80-100 BPM)
● FP-R04 (sample-based)
● FP-V01 (vocal foreground — MC)
● FP-T06 (human-feel timing — swing)
● FP-E01 (sharp attack / natural decay)
○ FP-S02 (bass-heavy)
○ FP-D01 (high crest factor)
○ FP-W04 (center-priority mixing)
○ FP-R01 (verse-chorus form)
○ FP-P04 (analog warmth)
△ FP-H01 (hi-mid percussive)
△ FP-R05 (loop-based)
```

### Trap (Hip-Hop)
```
● FP-T02 (standard tempo, 130-170 BPM, half-time vocal)
● FP-S01 (sub-bass dominant)
● FP-E04 (bloom envelope — 808)
● FP-V01 (vocal foreground)
● FP-T05 (regular beat grid)
● FP-W01 (mono bass / near-mono)
○ FP-T09 (high onset density — hi-hat rolls)
○ FP-D03 (low crest factor)
○ FP-R01 (verse-chorus form)
○ FP-X01 (rhythm heard, bass felt)
○ FP-S07 (sub/upper-bass coupling)
△ FP-V02 (vocal as texture — ad-libs)
△ FP-E07 (sidechain pump)
```

### Cloud Rap
```
● FP-E03 (slow onset — atmospheric pads)
● FP-S01 (sub-bass dominant)
● FP-V01 (vocal foreground)
● FP-P01 (natural room / reverb — heavy)
○ FP-T02 (standard tempo, 60-80 BPM effective)
○ FP-W02 (moderate stereo)
○ FP-E04 (bloom envelope)
○ FP-D02 (moderate crest factor)
△ FP-R05 (loop-based)
△ FP-E08 (sustained micro-variation)
```

### Drill
```
● FP-T02 (standard tempo, 138-145 BPM)
● FP-S01 (sub-bass dominant)
● FP-V01 (vocal foreground)
● FP-T05 (regular beat grid)
● FP-E04 (bloom envelope — sliding 808)
○ FP-D03 (low crest factor)
○ FP-T09 (high onset density — hi-hat patterns)
○ FP-W01 (mono bass)
○ FP-P05 (digital precision)
△ FP-R01 (verse-chorus form)
```

### Lo-Fi Hip-Hop
```
● FP-T02 (standard tempo, 70-90 BPM)
● FP-P04 (analog warmth / saturation — tape sim)
● FP-R05 (loop-based)
● FP-T06 (human-feel timing)
○ FP-R04 (sample-based)
○ FP-S02 (bass-heavy)
○ FP-V03 (no vocal) or FP-V02 (vocal as texture — sample)
○ FP-D02 (moderate crest factor)
○ FP-E01 (sharp attack / natural decay)
△ FP-E08 (sustained micro-variation — vinyl crackle, tape wobble)
△ FP-W02 (moderate stereo)
```

---

## ROCK

### Rock (Classic / General)
```
● FP-E01 (sharp attack / natural decay)
● FP-V01 (vocal foreground)
● FP-R01 (verse-chorus form)
● FP-T02 (standard tempo, 100-140 BPM)
● FP-T06 (human-feel timing)
○ FP-S03 (mid-heavy)
○ FP-D01 (high crest factor)
○ FP-H01 (hi-mid percussive)
○ FP-P01 (natural room)
○ FP-W04 (center-priority mixing)
○ FP-D05 (section-level dynamic contrast)
△ FP-P04 (analog warmth)
△ FP-S02 (bass-heavy)
```

### Indie Rock
```
● FP-V01 (vocal foreground)
● FP-R01 (verse-chorus form)
● FP-T02 (standard tempo)
● FP-T06 (human-feel timing)
○ FP-E01 (sharp attack / natural decay)
○ FP-S03 (mid-heavy)
○ FP-D02 (moderate crest factor)
○ FP-P01 (natural room)
○ FP-P04 (analog warmth) or FP-P02 (dry) — varies by era
△ FP-W02 (moderate stereo)
△ FP-D05 (section-level dynamic contrast)
```

### Post-Punk
```
● FP-S02 (bass-heavy — bass guitar as lead)
● FP-P01 (natural room / reverb — often heavy)
● FP-V01 (vocal foreground)
● FP-T02 (standard tempo)
○ FP-E01 (sharp attack / natural decay)
○ FP-T05 (regular beat grid — metronomic)
○ FP-R01 (verse-chorus) or FP-R05 (loop/repetitive)
○ FP-D02 (moderate crest factor)
○ FP-W02 (moderate stereo)
△ FP-E02 (gated decay) — in 80s-influenced
△ FP-P03 (gated reverb) — in 80s-influenced
```

### Shoegaze
```
● FP-W03 (wide stereo)
● FP-P01 (natural room / reverb — extreme)
● FP-E03 (slow onset / long sustain — guitar wash)
● FP-D03 (low crest factor — wall of sound)
○ FP-S03 (mid-heavy) or FP-S04 (treble-bright)
○ FP-V02 (vocal as texture — buried in mix)
○ FP-R01 (verse-chorus form — buried under texture)
○ FP-T02 (standard tempo)
○ FP-P07 (detuned oscillators — detuned guitars)
△ FP-H05 (HPSS ambiguous — guitar texture reads as neither)
△ FP-E08 (sustained micro-variation)
```

### Grunge
```
● FP-P06 (intentional distortion)
● FP-V01 (vocal foreground)
● FP-D05 (section-level dynamic contrast — quiet verse, loud chorus)
● FP-R01 (verse-chorus form)
○ FP-T02 (standard tempo)
○ FP-S03 (mid-heavy)
○ FP-T06 (human-feel timing)
○ FP-E01 (sharp attack / natural decay)
○ FP-D01 (high crest factor)
△ FP-P02 (dry) — in some recordings
△ FP-S02 (bass-heavy) — in sludgier tracks
```

### Progressive Rock
```
● FP-T07 (irregular meter)
● FP-R03 (through-composed) or FP-R06 (additive layering)
● FP-D05 (section-level dynamic contrast)
○ FP-V01 (vocal foreground)
○ FP-T02 or FP-T03 (variable tempo)
○ FP-S05 (even distribution — full arrangement)
○ FP-P01 (natural room)
○ FP-T06 (human-feel timing)
○ FP-E08 (sustained micro-variation — synths)
△ FP-P07 (detuned oscillators — mellotron, analog synths)
△ FP-W02 (moderate stereo)
```

### Psychedelic Rock
```
● FP-P01 (natural room / reverb — heavy/experimental)
● FP-E08 (sustained micro-variation — phaser, flanger, wobble)
● FP-W03 (wide stereo — psychedelic panning)
○ FP-V01 (vocal foreground)
○ FP-R01 (verse-chorus) or FP-R03 (through-composed — extended jams)
○ FP-T02 (standard tempo)
○ FP-T06 (human-feel timing)
○ FP-S03 (mid-heavy)
△ FP-E06 (reversed envelope — reversed cymbals, tape effects)
△ FP-P04 (analog warmth)
△ FP-W05 (stereo extremes — hard panning)
```

### Post-Rock
```
● FP-R06 (additive layering — the signature build)
● FP-D05 (section-level dynamic contrast — extreme quiet→loud)
● FP-V03 (no vocal) — mostly instrumental
● FP-R03 (through-composed)
○ FP-E03 (slow onset / long sustain)
○ FP-P01 (natural room / reverb)
○ FP-T01 or FP-T02 (slow to standard tempo)
○ FP-W03 (wide stereo)
○ FP-T06 (human-feel timing)
△ FP-P07 (detuned oscillators — guitars through effects)
△ FP-E08 (sustained micro-variation)
```

### Math Rock
```
● FP-T07 (irregular meter — defining feature)
● FP-T06 (human-feel timing)
● FP-P02 (dry / close-miked)
○ FP-V03 (no vocal) or FP-V01 (vocal foreground)
○ FP-T02 (standard tempo)
○ FP-D01 (high crest factor)
○ FP-S03 (mid-heavy)
○ FP-E01 (sharp attack / natural decay)
△ FP-H01 (hi-mid percussive — angular guitar tapping)
△ FP-R03 (through-composed)
```

### Noise Rock
```
● FP-P06 (intentional distortion)
● FP-D03 or FP-D04 (low crest / brick-wall)
● FP-S03 (mid-heavy)
○ FP-V01 (vocal foreground) or FP-V02 (vocal as texture)
○ FP-T02 (standard tempo)
○ FP-R01 (verse-chorus — buried under noise)
○ FP-T06 (human-feel timing)
○ FP-H05 (HPSS ambiguous)
△ FP-R05 (loop-based / repetitive)
△ FP-E03 (slow onset — feedback/drone)
```

---

## METAL

### Metal (General / Heavy)
```
● FP-P06 (intentional distortion — guitars)
● FP-V01 (vocal foreground)
● FP-S02 (bass-heavy) or FP-S03 (mid-heavy)
● FP-T02 or FP-T03 (standard to fast tempo)
● FP-E01 (sharp attack / natural decay)
○ FP-R01 (verse-chorus form)
○ FP-D01 (high crest factor)
○ FP-H01 (hi-mid percussive — double kick, aggressive drums)
○ FP-T06 (human-feel timing)
○ FP-D05 (section-level dynamic contrast)
△ FP-T09 (high onset density — in faster subgenres)
```

### Thrash Metal
```
● FP-T03 (fast tempo, 150-220 BPM)
● FP-P06 (intentional distortion)
● FP-T09 (high onset density)
● FP-V01 (vocal foreground)
○ FP-E01 (sharp attack / natural decay)
○ FP-R01 (verse-chorus form)
○ FP-D01 (high crest factor)
○ FP-S03 (mid-heavy — scooped guitars)
○ FP-T06 (human-feel timing)
△ FP-D04 (brick-wall limited) — in modern remastering
```

### Death Metal
```
● FP-T03 or FP-T04 (fast to extreme tempo)
● FP-T09 or FP-T10 (high/extreme onset density — blast beats)
● FP-P06 (intentional distortion)
● FP-D03 (low crest factor)
● FP-V01 (vocal foreground — guttural)
○ FP-S02 (bass-heavy) — detuned guitars
○ FP-R03 (through-composed)
○ FP-T06 (human-feel timing) or FP-T05 (grid — in technical DM)
△ FP-H02 (hi-mid harmonic — blast beats approaching tonal zone)
△ FP-R01 (verse-chorus — in catchier DM)
```

### Black Metal
```
● FP-P06 (intentional distortion)
● FP-S04 (treble-bright — lo-fi guitar tone)
● FP-T10 (extreme onset density — blast beats)
● FP-P02 (dry) or FP-P01 (cavernous reverb — varies by school)
○ FP-T04 (extreme tempo)
○ FP-V01 (vocal foreground — shriek)
○ FP-D04 (brick-wall limited)
○ FP-R03 (through-composed — long songs)
○ FP-E03 (slow onset — in atmospheric BM)
△ FP-V02 (vocal as texture) — in DSBM, post-BM
△ FP-W03 (wide stereo) — in atmospheric BM
△ FP-H02 (hi-mid harmonic — tremolo picking as texture)
```

### Doom Metal
```
● FP-T01 (slow tempo, 40-80 BPM)
● FP-S01 (sub-bass dominant) or FP-S02 (bass-heavy)
● FP-P06 (intentional distortion)
● FP-E03 (slow onset / long sustain)
○ FP-D01 (high crest factor)
○ FP-V01 (vocal foreground)
○ FP-P01 (natural room — cavernous)
○ FP-R03 (through-composed)
○ FP-T06 (human-feel timing)
△ FP-E08 (sustained micro-variation — feedback, oscillation)
△ FP-P07 (detuned oscillators — detuned guitars)
```

### Metalcore
```
● FP-D05 (section-level dynamic contrast — heavy/clean alternation)
● FP-P06 (intentional distortion)
● FP-V01 (vocal foreground — screamed and clean)
● FP-T02 or FP-T03 (standard to fast tempo)
○ FP-R02 (build-drop form — in modern metalcore)
○ FP-E01 (sharp attack / natural decay)
○ FP-D03 (low crest factor — modern production)
○ FP-R01 (verse-chorus form)
○ FP-S03 (mid-heavy)
△ FP-T05 (regular beat grid — in djent-influenced)
△ FP-T09 (high onset density)
```

---

## POP

### Pop (General)
```
● FP-V01 (vocal foreground)
● FP-R01 (verse-chorus form)
● FP-T02 (standard tempo, 100-130 BPM)
● FP-D05 (section-level dynamic contrast)
● FP-W04 (center-priority mixing)
○ FP-T05 (regular beat grid)
○ FP-S03 (mid-heavy)
○ FP-D02 (moderate crest factor)
○ FP-E01 (sharp attack / natural decay)
○ FP-X01 (rhythm heard, bass felt)
△ FP-E07 (sidechain pump) — in dance-pop
△ FP-P05 (digital precision) — in modern pop
```

### Synth Pop
```
● FP-V01 (vocal foreground)
● FP-P05 (digital precision) or FP-P04 (analog warmth)
● FP-T02 (standard tempo)
● FP-T05 (regular beat grid — machine rhythm)
● FP-R01 (verse-chorus form)
○ FP-E08 (sustained micro-variation — synth pads)
○ FP-S02 (bass-heavy — synth bass)
○ FP-E02 (gated decay) — in 80s era
○ FP-P03 (gated reverb) — in 80s era
○ FP-W02 (moderate stereo)
△ FP-P07 (detuned oscillators)
△ FP-E07 (sidechain pump)
```

### Art Pop
```
● FP-V01 (vocal foreground)
○ FP-R01 (verse-chorus) or FP-R03 (through-composed)
○ FP-T07 (irregular meter) — occasionally
○ FP-D05 (section-level dynamic contrast)
○ FP-W02 or FP-W03 (moderate to wide stereo)
○ FP-S05 (even distribution — full palette)
△ FP-E05 (two-stage envelope — experimental production)
△ FP-P07 (detuned oscillators)
△ FP-V04 (vocal non-address) — in more experimental tracks
```

### Hyperpop
```
● FP-P06 (intentional distortion)
● FP-D04 (brick-wall limited)
● FP-V02 (vocal as texture — pitched, chopped, effected)
● FP-P05 (digital precision)
○ FP-T02 or FP-T03 (standard to fast tempo)
○ FP-S04 (treble-bright)
○ FP-E05 (two-stage envelope) — in SOPHIE-influenced
○ FP-R02 (build-drop form)
○ FP-W03 (wide stereo)
△ FP-V04 (vocal non-address)
△ FP-T09 (high onset density)
✱ FP-E01 → FP-E05 (VIOLATION: natural envelope replaced by synthetic multi-stage)
```

### K-Pop
```
● FP-V01 (vocal foreground)
● FP-R01 (verse-chorus form — often with rap verse)
● FP-D05 (section-level dynamic contrast — genre changes within song)
● FP-T02 (standard tempo)
○ FP-P05 (digital precision)
○ FP-D03 (low crest factor — loud mastering)
○ FP-S01 (sub-bass dominant) — in hip-hop-influenced sections
○ FP-T05 (regular beat grid)
○ FP-W04 (center-priority mixing)
△ FP-E07 (sidechain pump) — in EDM sections
△ FP-R02 (build-drop form) — in EDM sections
```

---

## R&B / SOUL / FUNK

### R&B (Contemporary)
```
● FP-V01 (vocal foreground)
● FP-S01 (sub-bass dominant)
● FP-T02 (standard tempo, 60-100 BPM effective)
● FP-T06 (human-feel timing — groove)
○ FP-E04 (bloom envelope — 808)
○ FP-R01 (verse-chorus form)
○ FP-D02 (moderate crest factor)
○ FP-W04 (center-priority mixing)
○ FP-P05 (digital precision)
△ FP-E07 (sidechain pump)
△ FP-E08 (sustained micro-variation — synth pads)
```

### Soul
```
● FP-V01 (vocal foreground — expressive, dynamic)
● FP-T06 (human-feel timing)
● FP-P01 (natural room)
● FP-D01 (high crest factor)
○ FP-R01 (verse-chorus form)
○ FP-S02 (bass-heavy)
○ FP-T02 (standard tempo)
○ FP-E01 (sharp attack / natural decay)
○ FP-P04 (analog warmth)
△ FP-D05 (section-level dynamic contrast)
△ FP-W04 (center-priority mixing)
```

### Funk
```
● FP-T06 (human-feel timing — the groove IS the song)
● FP-V01 (vocal foreground)
● FP-S02 (bass-heavy — bass guitar prominence)
● FP-D01 (high crest factor — punchy, dynamic)
○ FP-T02 (standard tempo, 100-130 BPM)
○ FP-E01 (sharp attack / natural decay)
○ FP-H01 (hi-mid percussive)
○ FP-R01 (verse-chorus) or FP-R05 (loop-based — vamp)
○ FP-P01 (natural room)
○ FP-P04 (analog warmth)
△ FP-X01 (rhythm heard, bass felt — though bass is also very rhythmic in funk)
```

---

## OTHER GENRES

### Jazz
```
● FP-T06 (human-feel timing — swing, rubato)
● FP-D01 (high crest factor — unamplified dynamics)
● FP-P01 (natural room)
○ FP-V03 (no vocal) — in instrumental jazz
○ FP-V01 (vocal foreground) — in vocal jazz
○ FP-T07 (irregular meter) — in modern/avant jazz
○ FP-R03 (through-composed) or FP-R05 (loop — head-solos-head)
○ FP-S05 (even distribution) or FP-S03 (mid-heavy)
○ FP-T02 (standard tempo) — highly variable
△ FP-T08 (free time) — in free jazz
△ FP-E08 (sustained micro-variation — breath, embouchure)
```

### Blues
```
● FP-V01 (vocal foreground)
● FP-T06 (human-feel timing — shuffle)
● FP-P01 (natural room) or FP-P04 (analog warmth)
● FP-R01 (verse-chorus — 12-bar form)
○ FP-T02 (standard tempo)
○ FP-S03 (mid-heavy)
○ FP-D01 (high crest factor)
○ FP-E01 (sharp attack / natural decay)
△ FP-P06 (intentional distortion) — in electric blues
△ FP-D05 (section-level dynamic contrast)
```

### Country
```
● FP-V01 (vocal foreground)
● FP-R01 (verse-chorus form)
● FP-T02 (standard tempo)
● FP-P01 (natural room)
○ FP-T06 (human-feel timing)
○ FP-S03 (mid-heavy)
○ FP-D01 or FP-D02 (moderate-high crest factor)
○ FP-E01 (sharp attack / natural decay)
○ FP-W04 (center-priority mixing)
△ FP-P04 (analog warmth) — in classic country
△ FP-S02 (bass-heavy) — in modern country-pop
```

### Folk
```
● FP-V01 (vocal foreground)
● FP-T06 (human-feel timing)
● FP-P01 (natural room) or FP-P02 (dry / close-miked)
● FP-D01 (high crest factor — acoustic dynamics)
○ FP-R01 (verse-chorus form)
○ FP-T02 (standard tempo) or FP-T01 (slow)
○ FP-S03 (mid-heavy)
○ FP-E01 (sharp attack / natural decay)
△ FP-V03 (no vocal) — in instrumental folk
△ FP-P04 (analog warmth) — in lo-fi folk
```

### Classical (Orchestral)
```
● FP-D01 (high crest factor — extreme dynamics)
● FP-T06 (human-feel timing) or FP-T08 (free time — rubato)
● FP-P01 (natural room — concert hall acoustics)
● FP-V03 (no vocal) — in orchestral
● FP-R03 (through-composed)
○ FP-S05 (even distribution — full orchestra)
○ FP-D05 (section-level dynamic contrast — pp to ff)
○ FP-T07 (irregular meter) or FP-T02 (standard)
○ FP-W02 (moderate stereo — orchestral image)
△ FP-E03 (slow onset — strings, sustained brass)
△ FP-R06 (additive layering)
```

### Reggae
```
● FP-S01 (sub-bass dominant)
● FP-T02 (standard tempo, 60-90 BPM)
● FP-V01 (vocal foreground)
● FP-T06 (human-feel timing)
○ FP-E01 (sharp attack / natural decay)
○ FP-P01 (natural room) or FP-P04 (analog warmth)
○ FP-R01 (verse-chorus form)
○ FP-W04 (center-priority mixing)
△ FP-P01 (natural room) — heavy dub reverb
△ FP-E07 (sidechain pump) — in dub
```

### Dub
```
● FP-S01 (sub-bass dominant)
● FP-P01 (natural room / reverb — extreme, creative)
● FP-E06 (reversed envelope) — tape echo effects
● FP-R04 (sample-based — remixed from reggae sources)
○ FP-T02 (standard tempo, 60-90 BPM)
○ FP-V02 (vocal as texture — echoed, fragmented)
○ FP-W03 (wide stereo — spatial experimentation)
○ FP-R05 (loop-based)
○ FP-D05 (section-level dynamic contrast — drop-outs)
△ FP-E08 (sustained micro-variation — spring reverb, tape wobble)
△ FP-P04 (analog warmth)
```

### Ska
```
● FP-T02 (standard tempo, 100-170 BPM)
● FP-V01 (vocal foreground)
● FP-T06 (human-feel timing)
● FP-E01 (sharp attack / natural decay — upstroke guitar)
○ FP-S02 (bass-heavy)
○ FP-R01 (verse-chorus form)
○ FP-D01 (high crest factor)
○ FP-H01 (hi-mid percussive)
△ FP-P06 (intentional distortion) — in ska-punk
△ FP-P01 (natural room)
```

### Gospel
```
● FP-V01 (vocal foreground — choir/solo, dynamic)
● FP-D01 (high crest factor)
● FP-P01 (natural room — church acoustics)
● FP-T06 (human-feel timing)
○ FP-R01 (verse-chorus form)
○ FP-D05 (section-level dynamic contrast)
○ FP-S03 (mid-heavy)
○ FP-T02 (standard tempo) — variable
△ FP-E03 (slow onset — organ sustain)
△ FP-W02 (moderate stereo)
```

### Reggaeton
```
● FP-T02 (standard tempo, 85-100 BPM — dembow rhythm)
● FP-T05 (regular beat grid)
● FP-S01 (sub-bass dominant)
● FP-V01 (vocal foreground)
○ FP-E04 (bloom envelope — 808)
○ FP-P05 (digital precision)
○ FP-R01 (verse-chorus form)
○ FP-D03 (low crest factor)
△ FP-E07 (sidechain pump)
△ FP-W04 (center-priority mixing)
```

### Afrobeats
```
● FP-T02 (standard tempo, 100-130 BPM)
● FP-V01 (vocal foreground)
● FP-T06 (human-feel timing — polyrhythmic)
● FP-T09 (high onset density — layered percussion)
○ FP-S02 (bass-heavy)
○ FP-R01 (verse-chorus form)
○ FP-E01 (sharp attack / natural decay)
○ FP-H01 (hi-mid percussive)
○ FP-P05 (digital precision) — in modern Afrobeats
△ FP-P04 (analog warmth) — in Afrobeat (Fela era)
△ FP-R05 (loop-based)
```

### Dancehall
```
● FP-T02 (standard tempo, 90-110 BPM)
● FP-S01 (sub-bass dominant)
● FP-V01 (vocal foreground)
● FP-T05 (regular beat grid)
○ FP-P05 (digital precision)
○ FP-E04 (bloom envelope)
○ FP-D03 (low crest factor)
○ FP-R01 (verse-chorus form)
△ FP-V02 (vocal as texture — chant, ad-lib)
△ FP-T06 (human-feel timing)
```

### Bossa Nova
```
● FP-T06 (human-feel timing — the subtle pulse)
● FP-T01 or FP-T02 (slow to standard, 70-110 BPM)
● FP-V01 (vocal foreground — intimate, breathy)
● FP-P02 (dry / close-miked) or FP-P01 (natural room — subtle)
○ FP-D01 (high crest factor)
○ FP-S03 (mid-heavy)
○ FP-E01 (sharp attack / natural decay — nylon guitar)
○ FP-R01 (verse-chorus form)
△ FP-W02 (moderate stereo)
△ FP-P04 (analog warmth)
```

### Punk
```
● FP-T03 (fast tempo, 150-200 BPM)
● FP-P06 (intentional distortion)
● FP-V01 (vocal foreground)
● FP-D04 or FP-D03 (brick-wall / low crest — raw recording)
● FP-R01 (verse-chorus form)
○ FP-S03 (mid-heavy)
○ FP-E01 (sharp attack / natural decay)
○ FP-T06 (human-feel timing)
○ FP-P02 (dry — stripped-down recording)
△ FP-T09 (high onset density) — in hardcore punk
△ FP-D05 (section-level dynamic contrast) — minimal in punk
```

### New Age
```
● FP-E03 (slow onset / long sustain)
● FP-E08 (sustained micro-variation)
● FP-P01 (natural room / reverb)
● FP-W03 (wide stereo)
○ FP-V03 (no vocal) or FP-V01 (vocal — breathy, ethereal)
○ FP-T01 (slow tempo) or FP-T08 (free time)
○ FP-S03 (mid-heavy)
○ FP-R05 (loop-based) or FP-R03 (through-composed)
○ FP-D01 (high crest factor — delicate dynamics)
△ FP-P07 (detuned oscillators)
△ FP-P04 (analog warmth)
```

### Soundtrack / Film Score
```
● FP-D05 (section-level dynamic contrast — extreme)
● FP-P01 (natural room — large ensemble)
● FP-R03 (through-composed)
○ FP-D01 (high crest factor)
○ FP-S05 (even distribution — full palette)
○ FP-V03 (no vocal) or FP-V01 (vocal — choral)
○ FP-T06 (human-feel timing) or FP-T05 (click-tracked)
○ FP-W02 (moderate stereo — cinematic image)
○ FP-E03 (slow onset) and FP-E01 (sharp attack) — both
△ FP-S01 (sub-bass dominant) — in action/sci-fi
△ FP-P05 (digital precision) — in electronic scores
△ FP-E06 (reversed envelope) — in horror/tension
```

---

## MAP STATISTICS

| Category | Genre count |
|----------|-------------|
| Electronic | 16 |
| Hip-Hop / Rap | 5 |
| Rock | 9 |
| Metal | 6 |
| Pop | 5 |
| R&B / Soul / Funk | 3 |
| Other | 14 |
| **TOTAL** | **58** |

---

## USAGE

1. **Phase A commits genre** (e.g., "breakcore")
2. **Look up genre in this document** → get list of fingerprint IDs with ●/○/△ markers
3. **Load fingerprint definitions from fingerprint-registry.md** using the IDs
4. **Run binary measurements** against each fingerprint's binary code
5. **Check for ✱ violation markers** — these are conventions the genre is known to subvert
6. **Flag matches and mismatches** → pass to Cultural Engine for convention analysis

The ● fingerprints are your first-pass sanity check (does this actually sound like the committed genre?). The ○ fingerprints are your full-pass measurement targets. The ✱ fingerprints are your bridge-type detection candidates.

---

*Map created: 10 February 2026*
*Cross-references: fingerprint-registry.md, engine-cultural.md*
*Status: First population (58 genres, 64 fingerprints). Continuously updatable.*
