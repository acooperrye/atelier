# SONIC FINGERPRINT REGISTRY
## Rhythm Dictionary — Universal Reference
## 2026-02-10 · Continuously updatable

---

## PURPOSE

A universal, genre-agnostic catalogue of sonic fingerprints. Each fingerprint is a single measurable shape that sound can take — an atom. Genres are molecules assembled from these atoms (see: genre-fingerprint-map.md).

Every fingerprint has three parts:
1. **ID** — unique, permanent, categorical (FP-E01, FP-S03, etc.)
2. **Binary code** — compact measurement instruction (what to measure, what threshold)
3. **Prose** — what it sounds or feels like in plain language

**Adding a new fingerprint:** assign the next ID in its category, write the binary code and prose, then check genre-fingerprint-map.md for which genres exhibit it.

**Cross-reference:** genre-fingerprint-map.md assigns fingerprint IDs to genres. engine-cultural.md uses fingerprint IDs in convention definitions.

---

## CATEGORIES

| Prefix | Category | What it measures |
|--------|----------|-----------------|
| FP-E | Envelope | How energy arrives and leaves over time |
| FP-D | Dynamics | Loudness variation and compression |
| FP-S | Spectral | Where energy sits across the frequency spectrum |
| FP-H | HPSS | Harmonic vs percussive character per band |
| FP-W | Stereo | Spatial width and placement |
| FP-T | Temporal | Tempo, rhythm, event density |
| FP-X | Cross-band | Relationships between frequency bands |
| FP-V | Vocal | Vocal presence, role, and treatment |
| FP-R | Structure | Song-level architecture and form |
| FP-P | Production | Recording/mixing/mastering character |

---

## ENVELOPE (FP-E)

### FP-E01 · Sharp attack / natural decay
```
onset_ratio > 10
decay_type = "exponential"
crest_factor_db > 12
```
Standard percussive hit. Snare, kick, plucked string, any acoustic impact. Energy arrives fast, leaves gradually. The default. Most violations are violations of this.

### FP-E02 · Sharp attack / gated decay
```
onset_ratio > 15
decay_type = "hard_gate"
decay_time_ms < 80
```
Reverb blooms then cuts dead. The 80s gated snare. Somatic: severance — the body reads the gradient of the whole edge, not attack and silence separately (correspondence #11, metallic edge principle).

### FP-E03 · Slow onset / long sustain
```
onset_ratio < 3
sustain_duration_ms > 2000
offset_slope < 0.5 (normalised)
```
Pads, drones, atmosphere. Energy arrives gradually and stays. In sub-bass: creates place/weightlessness rather than impact (Blade Runner). The polling model predicts acclimatisation within ~10s — the sound becomes the new silence.

### FP-E04 · Bloom envelope
```
onset_ratio: initial_peak at 1.0x
envelope_trajectory: grows to 1.2-1.5x over 100-500ms
decay_type = "natural" (after bloom peak)
```
Energy GROWS after initial onset. The 808 bloom: attack at 1.0x, swells to 1.37x over 250ms, then decays. The body reads three phases: impact, resistance, immersion (correspondence #1: "throwing a punch into a pool of water"). Reproduces the plucked-string physics of upper harmonics arriving first, fundamental blooming in underneath.

### FP-E05 · Two-stage envelope
```
envelope_stages = 2
stage_1: sharp onset in band_A, fast decay
stage_2: onset in band_B at +50-150ms delay
stage_1_band ≠ stage_2_band
```
Two frequency bands peak at different times. SOPHIE's rubber: sub-bass snaps first (hard shell), mid-range rubber bloom peaks 93ms later (elastic filling). No acoustic instrument does this — it's a material statement. The body reads it as a compound object with shell and interior.

### FP-E06 · Reversed envelope
```
onset_ratio < 1.0
energy_trajectory: grows over time (ramp up)
peak_position > 0.7 (normalised to event duration)
```
Energy builds instead of decaying. Reversed cymbals, swells, risers. Creates anticipation — the body expects an event at the peak. Common in build-ups and transitions.

### FP-E07 · Sidechain pump
```
envelope_trajectory: periodic ducking
duck_depth_db > 3
duck_correlation: locked to kick or other trigger
duck_release_ms: 50-300
```
Rhythmic volume ducking tied to another element (usually kick). Creates breathing/pumping effect. The mix inhales and exhales. Ubiquitous in electronic dance music.

### FP-E08 · Sustained with micro-variation
```
onset_ratio < 3
sustain_duration_ms > 2000
micro_variation: amplitude wobble 0.5-3Hz
```
Long sustained tone with subtle internal movement. Analog oscillator drift, tape wobble, tremolo. The CS-80 pad: not beating, not static — undulating. Alive movement without human quality (correspondence #10).

---

## DYNAMICS (FP-D)

### FP-D01 · High crest factor
```
crest_factor_db > 15
```
Big dynamic range. Transients punch well above the average level. Individual hits are events. Shout: crest 16.1dB — the gated snare slices through everything.

### FP-D02 · Moderate crest factor
```
crest_factor_db: 8-15
```
Balanced dynamics. Some punch, some sustain. Most well-mixed popular music lives here.

### FP-D03 · Low crest factor
```
crest_factor_db: 4-8
```
Compressed. Transients tamed, average level high. Dense, loud, relentless. Common in modern mastering.

### FP-D04 · Brick-wall limited
```
crest_factor_db < 4
peak_sample > 0.99
clipping_pct > 0.5%
```
Extreme limiting. Waveform hits the ceiling. Circle Pit: 3.1dB crest, 2% clipping. The loudness IS the texture.

### FP-D05 · Section-level dynamic contrast
```
rms_difference(loudest_section, quietest_section) > 6dB
```
Verses quiet, choruses loud (or equivalent). The song breathes at the structural level. Dynamic emphasis = structural hierarchy.

### FP-D06 · Relentless escalation
```
spectral_flux_trajectory: monotonically increasing
flux_ratio(end / start) > 2.0
```
Intensity only goes up. No plateaus, no releases, no breathing room. Circle Pit: spectral flux triples (78→237). The track as tightening screw.

---

## SPECTRAL (FP-S)

### FP-S01 · Sub-bass dominant
```
band_energy_pct(sub_bass) > 40%
```
More than 40% of total energy below 80Hz. PUTP: 55%. Blade Runner: 61.9%. Lemonade: 48.5%. The body is the primary receiver at this ratio (somatic-weighted: 94-97% of felt energy).

### FP-S02 · Bass-heavy
```
band_energy_pct(sub_bass + bass) > 50%
band_energy_pct(sub_bass) < 40%
```
Strong low end but not sub-bass dominated. Bass guitar territory, warm mixes. The upper bass provides foundation without the extreme sub-bass immersion.

### FP-S03 · Mid-heavy
```
spectral_centroid: 800-2500Hz
band_energy_pct(mid) > 30%
```
Energy concentrated in the vocal/guitar range. Presence-forward mixes. Rock, singer-songwriter, anything where the 1-3kHz range carries the message.

### FP-S04 · Treble-bright
```
spectral_centroid > 3000Hz
band_energy_pct(hi_mid + high) > 40%
```
Sparkly, airy, sharp. Hi-hat forward mixes, acoustic with shimmer, crisp electronic production.

### FP-S05 · Full-band even distribution
```
max(band_energy_pct) - min(band_energy_pct) < 15%
```
Energy spread roughly evenly across the spectrum. No single band dominates. Circle Pit approaches this: sub 25%, bass 29%, mid 22%, hi-mid 16%, high 8%.

### FP-S06 · Spectral scoop / notch
```
band_energy_pct(target_band) < adjacent_bands * 0.3
```
Deliberate absence of energy in a band. The anti-voice (80-1100Hz removed) that sounded like VHS hum. Feltness module origin: the hollowness was visible in numbers but not felt.

### FP-S07 · Sub-bass / upper-bass coupling
```
cross_correlation(sub_bass_envelope, bass_envelope) > 0.5
bass_onset leads sub_bass_onset by 5-50ms
```
Upper bass functions as primer/notification for sub-bass content. The plucked-string physics: harmonics arrive first, fundamental blooms underneath. PUTP 808 attack centroid 715Hz → body centroid 519Hz → sub-bass bloom at 50Hz. The body already knows this sequence.

---

## HPSS — HARMONIC / PERCUSSIVE (FP-H)

### FP-H01 · Hi-mid percussive dominant
```
hpss_balance(hi_mid): percussive > 0.5
```
Standard: drums and percussion in the hi-mid band read as percussive. Individual hits are discrete events. The default for nearly all music.

### FP-H02 · Hi-mid harmonic dominant
```
hpss_balance(hi_mid): harmonic > 0.6
```
Percussion has become tonal. Either through density (Circle Pit: snares at 5.7/sec fuse into continuous excitation → 70.8% harmonic) or through pitched percussion. When FP-H01 flips to FP-H02, something fundamental has changed about what drums are doing.

### FP-H03 · Sub-bass harmonic
```
hpss_balance(sub_bass): harmonic > 0.6
```
Pitched bass content. Normal — bass notes, 808 tones, synth bass. The default for sub-bass.

### FP-H04 · Sub-bass percussive / noise
```
hpss_balance(sub_bass): percussive > 0.5
```
Bass that isn't pitched — noise-bass, distortion, rumble. Unusual. Could indicate extended bass techniques, extreme distortion, or sub-bass used as texture rather than pitch.

### FP-H05 · HPSS ambiguous
```
|hpss_balance - 0.5| < 0.1
```
Material that reads as neither clearly harmonic nor clearly percussive. Dense textures, granular synthesis, some noise music. The engine can't confidently separate.

---

## STEREO (FP-W)

### FP-W01 · Mono / near-mono
```
ms_ratio < 1.0
```
Everything centered. PUTP: M/S 0.168. Sub-bass narrow concentrates force into a point — somatic read: pressure, weight, directional (correspondence #10 implication).

### FP-W02 · Moderate stereo
```
ms_ratio: 1.0-5.0
```
Some width, elements placed across the field. Blade Runner: M/S 4.936. Standard stereo mixing.

### FP-W03 · Wide stereo
```
ms_ratio > 5.0
```
Very wide. Lemonade: M/S 8.619. Energy dispersed around the listener. Somatic: omnidirectional rather than directional. Width prevents sub-bass from condensing into force (correspondence #10).

### FP-W04 · Center-priority mixing
```
ms_ratio(sub_bass) < 2.0
ms_ratio(bass) < 3.0
ms_ratio(mid+) > ms_ratio(bass)
```
Lead elements centered, support elements wider. Standard mixing practice. Physics enforces sub-bass centering; convention extends it to vocals and kick.

### FP-W05 · Stereo extremes / hard-panned
```
energy_at_extremes (L-only or R-only) > 15% of total
```
Elements placed hard left or hard right. Beatle-era panning, some experimental production. Creates spatial drama but can feel unbalanced.

---

## TEMPORAL (FP-T)

### FP-T01 · Slow tempo
```
bpm < 80
```
Ballads, downtempo, ambient with pulse. The body has time to complete full somatic gestures between events.

### FP-T02 · Standard tempo
```
bpm: 80-140
```
Most popular music. The 120 BPM sweet spot may correspond to the somatic polling rate (hypothesis — challenged by jungle/breakcore).

### FP-T03 · Fast tempo
```
bpm: 140-180
```
Drum and bass, jungle, fast rock, punk. Sub-bass events at this tempo start challenging buffer-clearing (polling model).

### FP-T04 · Extreme tempo
```
bpm > 180
```
Breakcore, speedcore, some thrash metal. Circle Pit: 172 BPM (sub-bass), 343 BPM equivalent (breaks). Physics constrains sub-bass gestures at these rates.

### FP-T05 · Regular beat grid
```
tempo_stability: autocorrelation_peak > 0.8
beat_deviation < 5ms
```
Quantized, locked to grid. Electronic production, click-tracked recording. Predictable pulse.

### FP-T06 · Human-feel timing
```
tempo_stability: autocorrelation_peak > 0.6
beat_deviation: 5-30ms
```
Played by humans or humanized electronically. Swing, groove, push/pull. The timing deviations ARE the feel.

### FP-T07 · Irregular / shifting meter
```
time_signature ≠ 4/4
OR time_signature_changes > 0
OR beat_grouping_varies
```
Non-standard time signatures, polymeter, metric modulation. Venetian Snares' 7/4 work. Math rock odd meters. The pulse exists but the grouping surprises.

### FP-T08 · Free time / no pulse
```
tempo_stability: autocorrelation_peak < 0.4
```
No detectable regular beat. Rubato, free jazz, ambient without pulse, some noise.

### FP-T09 · High onset density
```
onset_rate_hz > 4
```
More than 4 discrete events per second across the full mix. Busy, dense. Typical in breakcore, some jazz, blast-beat metal.

### FP-T10 · Extreme onset density / tonal threshold
```
onset_rate_hz > 8 (in any single band)
```
Repetition rate approaching the threshold where rhythm becomes tone. Circle Pit snares at ~5.7/sec are in this zone. Above ~10/sec, individual events are typically imperceptible — the stream becomes texture.

---

## CROSS-BAND (FP-X)

### FP-X01 · Rhythm-heard-bass-felt hierarchy
```
onset_ratio(hi_mid) > onset_ratio(sub_bass)
hpss_balance(hi_mid) > 0.5 (percussive)
```
The default: you hear the beat (percussion is sharp, discrete) and feel the bass (sub-bass is weight, not countable). Violation of this is Type 7 (Inversion).

### FP-X02 · Shadow bass
```
envelope_correlation(sub_bass, hi_mid_onsets) > 0.3
onset_ratio(sub_bass) < 3
sub_bass_onset_leads_hi_mid_peak by < 10ms
```
Sub-bass is tethered underneath higher-frequency events. It doesn't have its own attacks — the hi-mid transients ARE its onset events. Circle Pit: correlation 0.481, onset ratio 1.1x, sub-bass peak at +2.3ms after hi-mid. The breaks provide dE/dt, the sub-bass provides mass.

### FP-X03 · Envelope staging
```
peak_time(band_A) ≠ peak_time(band_B)
delay_between_peaks > 5ms
```
Different frequency bands peak at different times in response to the same musical event. Natural in acoustic instruments (higher modes establish first). Exaggerated in production (SOPHIE's 93ms between sub-bass snap and mid-range rubber bloom).

### FP-X04 · Independent layers
```
envelope_correlation(sub_bass, hi_mid) < 0.2
```
Bass and breaks operating as separate rhythmic systems. Jungle's dual system: the bass has its own rhythm, the breaks have theirs. They coexist without being tethered.

### FP-X05 · Frequency roles standard
```
hpss_balance(sub_bass) > 0.5 (harmonic = pitched bass)
hpss_balance(hi_mid) > 0.4 (percussive leaning)
spectral_centroid(vocal_band) in expected range
```
Every band is doing its conventional job. Bass provides harmonic foundation, mids carry melody, hi-mids carry percussion, highs carry air. The frequency spectrum is a well-ordered workplace.

---

## VOCAL (FP-V)

### FP-V01 · Vocal foreground
```
vocal_detected = true
vocal_band_energy_pct > adjacent_bands
ms_ratio(vocal_band) < 2.0
```
Voice is present, centered, louder than accompaniment. Standard pop/rock/R&B. The self-referential resonance map activates in full (correspondence #9).

### FP-V02 · Vocal as texture
```
vocal_detected = true
vocal_chopped = true OR vocal_effects_heavy = true
vocal_band_energy_pct < adjacent_bands
```
Voice is present but treated as material — chopped, pitched, effected, buried. The body recognizes it as human but doesn't map it to self-production. SOPHIE's Lemonade: recognized as voice, placed as falsetto, but NOT invited for matching.

### FP-V03 · No vocal
```
vocal_detected = false
```
Instrumental. The self-referential vocal map doesn't activate. No ceiling applies. Most electronic, classical instrumental, post-rock.

### FP-V04 · Vocal non-address
```
vocal_detected = true
vocal_spatial_position: above/away (not centered in listener space)
vocal_function: not addressing listener
```
Voice is present but doesn't speak TO the listener. SOPHIE: "the vocals sit above the mix, well away from 'us' the listener." Pop convention inverted — synthetic elements are intimate, human voice is distant.

### FP-V05 · Vocal phrase contour
```
phrase_count > 5
mean_phrase_duration: 2.5-9.0s
breath_range_gap_pct > 30%
```
Breath-scale phrasing detected in the vocal band. Amplitude in 200-4000Hz rises, sustains, falls at intervals determined by lung capacity, not by beat grid. The biological clock cross-cutting the metric clock. Phoneline: 26 phrases at 6.1s mean — textbook. This fingerprint fires from the Vocal Silhouette Engine (P-VOX), not from the binary engine's broken element #49.

### FP-V06 · Sibilance coupling
```
vocal_sibilance_corr > 0.2
peak_lag_ms: -50 to +50
coupling_over_sub_bass > 0.2
```
Cross-band correlation between vocal band (200-4000Hz) and sibilance band (4-8kHz) at consonant-vowel timescales. The most voice-specific measure in the system: no instrument produces both tonal content at 200-4000Hz AND broadband noise at 4-8kHz from the same physical source at syllabic alternation rates. Phoneline: correlation 0.320, lag +23.2ms, coupling over sub-bass 0.424. The lag is the consonant arriving before the vowel — the mouth opening.

### FP-V07 · Vocal pitch continuity
```
voiced_fraction > 0.4
glide_fraction > 0.5
median_pitch_hz: 80-1000 (singing fundamental range)
```
Pitched content in the vocal band that GLIDES between notes rather than stepping. The vocal folds adjust continuously — even staccato singing has portamento. Visible in the spectrogram as curved pitch lines rather than rectangular blocks. Phoneline: 74.6% voiced, glide fraction 0.660, median 279Hz (C#4/D4 — female vocal range). Contaminated by break artifacts in mixed signal; purest when vocal band is isolated.

### FP-V08 · Vocal vibrato
```
vibrato_peak_hz: 4.5-7.5
vibrato_ratio > 0.3
```
Periodic pitch modulation at the characteristic rate of laryngeal muscle oscillation (~5-7Hz). Depth and prominence vary by genre and style: operatic/soul = strong (ratio >1.5), DnB/electronic/pop = subtle (ratio 0.3-0.8), some styles suppress it entirely. Phoneline: 5.8Hz peak, ratio 0.338 — Emily Makis's controlled DnB vibrato. The frequency is human; the depth is genre.

### FP-V09 · Formant movement
```
formant_count >= 2
mean_formant_continuity > 0.4
f1_continuity > 0.6
```
Two or more spectral ridges in the vocal band that move independently and continuously. The formant signature: F1 (jaw), F2 (tongue), F3 (lips) reshape as the singer moves between vowels. No instrument does this — instruments have fixed or slowly-varying resonance structures. Phoneline: F1 at 420Hz with 0.715 continuity (strong), F2 and F3 degraded by break contamination. In clean vocal production this measure is decisive; in drum-heavy production F1 survives best because it sits below the break energy.

### FP-V10 · Vocal-percussion independence
```
biological_clock ≠ beat_interval (±20%)
phrase_onset_times not aligned to beat grid
vocal_section_shape ≠ energy_section_shape
```
Vocal phrases are timed by breath, not by bars. In most sung music, the voice enters mid-bar, trails across bar lines, and breathes at irregular intervals relative to the beat grid. This independence — the biological clock cutting across the metric clock — is a voice signature. Phoneline: voice enters at 30s and persists continuously while the DnB energy structure cycles through drop/breakdown/buildup. The vocal thread is structurally independent of the drum thread. In heavily quantised vocal production (autotune, beat-locked phrasing), this independence is reduced but the breath gaps remain.

### FP-V11 · Vocal continuity (sustained presence)
```
vocal_coverage_pct > 60%
sectional_map.shape = "continuous"
```
Voice is present across the majority of the track as a sustained presence, not appearing and disappearing with verse/chorus structure. Phoneline: 86% coverage, continuous shape. Contrast with verse-chorus vocal pattern (60-70% coverage, intermittent shape) or textural vocal (30-50% coverage, sporadic shape). A continuous vocal thread suggests the voice IS the structural spine of the arrangement, not a feature layered on top.

---

## STRUCTURE (FP-R)

### FP-R01 · Verse-chorus form
```
section_count > 4
section_types include "verse" AND "chorus" (or energy-equivalent alternation)
section_recurrence = true
```
AABA, ABABCB, or similar. The dominant form in Western popular music since the 1950s.

### FP-R02 · Build-drop form
```
energy_trajectory: rising section → sudden increase at "drop"
spectral_flux at drop > 2x pre-drop
```
EDM architecture. Tension builds via addition/filtering, releases at the drop. The body anticipates the drop physically.

### FP-R03 · Through-composed / continuous
```
section_boundaries: minimal or none
energy_trajectory: no repeated sections
```
No verse-chorus alternation. Could be escalating (Circle Pit), static (ambient), or narrative (classical). The form unfolds rather than repeating.

### FP-R04 · Sample-based / chopped material
```
spectral_variation_per_event: high (each event has different spectral profile)
source_material: pre-existing recordings
```
Built from samples rather than played or synthesized from scratch. Each slice carries the spectral fingerprint of its source. Breakcore's amen chops, hip-hop sample flips.

### FP-R05 · Loop-based / repetitive
```
pattern_recurrence_within_section > 0.8
loop_length: 1-8 bars
variation_per_cycle: minimal
```
Short patterns repeated with minimal variation. Minimal techno, some ambient, lo-fi hip-hop. Hypnotic through repetition.

### FP-R06 · Additive layering
```
element_count increases over time
elements_removed < elements_added (net accumulation)
```
Starts sparse, adds elements. Post-rock builds, some EDM, Bolero-style accumulation. Tension through density increase.

---

## PRODUCTION (FP-P)

### FP-P01 · Natural room / reverb
```
reverb_estimation: present
decay_time > 200ms
early_reflections: detectable
```
Sound exists in a space. Acoustic recordings, live rooms, studio ambience. The reverb tells the body about the physical environment.

### FP-P02 · Dry / close-miked
```
reverb_estimation: minimal
direct_to_reverb_ratio > 10
```
No room. Intimate, in-your-ear. A close-miked vocal at max SPL is "hideously uncomfortable" — it exceeds the body's internal reference for what a voice should mechanically do (correspondence #9).

### FP-P03 · Gated reverb
```
reverb_detected = true
reverb_decay: hard_cutoff
gate_time < 100ms
```
Room sound that cuts dead. The 80s signature. Combines FP-E02 with spatial information — the gate shapes both the envelope AND the sense of space.

### FP-P04 · Analog warmth / saturation
```
harmonic_distortion: even-order > odd-order
spectral_rolloff: gradual high-frequency decline
```
Tube, tape, transformer color. Adds even harmonics that the ear reads as warmth. Softens transients. Vintage character.

### FP-P05 · Digital precision / clean
```
harmonic_distortion: minimal
spectral_rolloff: sharp at Nyquist
transient_preservation: high
```
Clinical, transparent, precise. Modern digital production. Each element is exactly what it was designed to be.

### FP-P06 · Intentional distortion / clipping
```
peak_sample > 1.0 (intersample) OR clipping_pct > 0.5%
harmonic_distortion: high
distortion_type: hard-clip or saturation
```
Deliberate overdriving. Circle Pit: peak 1.299, 2% clipping. Distortion as aesthetic choice, not accident. The loudness IS the texture.

### FP-P07 · Detuned oscillators / analog instability
```
pitch_variation: 0.5-5Hz wobble in sustained tones
source: multiple oscillators at slightly different frequencies
```
The CS-80 character. Not beating (too slow for amplitude modulation), not static (too variable for pure tone). Undulating, alive, "like a lava lamp looks" (correspondence #10). Organic quality without human quality.

### FP-P08 · Tracker / sample-level precision
```
event_placement_resolution < 1ms
quantization: sample-accurate
source: tracker DAW (Renoise, etc.)
```
Events placed with sub-millisecond precision impossible in real-time performance. Venetian Snares' shadow bass is deliberately sequenced at this resolution — the sub-bass/hi-mid timing relationship (2.3ms delay) requires tracker-level control.

---

## REGISTRY STATISTICS

| Category | Count | ID range |
|----------|-------|----------|
| Envelope | 8 | FP-E01 to FP-E08 |
| Dynamics | 6 | FP-D01 to FP-D06 |
| Spectral | 7 | FP-S01 to FP-S07 |
| HPSS | 5 | FP-H01 to FP-H05 |
| Stereo | 5 | FP-W01 to FP-W05 |
| Temporal | 10 | FP-T01 to FP-T10 |
| Cross-band | 5 | FP-X01 to FP-X05 |
| Vocal | 11 | FP-V01 to FP-V11 |
| Structure | 6 | FP-R01 to FP-R06 |
| Production | 8 | FP-P01 to FP-P08 |
| **TOTAL** | **71** | |

Note: FP-V01 through FP-V04 are measured by the Binary Engine (element-level, vertical). FP-V05 through FP-V11 are measured by the Vocal Silhouette Engine (P-VOX/A-VOX, horizontal). The 64 Binary Engine fingerprints include FP-V01-V04. The 7 Vocal Engine fingerprints (FP-V05-V11) have their own suppression gridline section (7 positions), bringing the total suppression gridline to 110 positions.

---

*Registry created: 10 February 2026*
*Expanded: 11 February 2026 — FP-V05 through FP-V11 added (Vocal Silhouette Engine). See module-vocal.md. Validated against Phoneline (Pola & Bryson & Emily Makis).*
*Cross-references: genre-fingerprint-map.md, engine-cultural.md, module-vocal.md*
*Status: Continuously updatable — add new fingerprints as analysis discovers them.*
