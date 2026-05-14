# pentatonic

The Pentatonic Suite — playable artifacts treating the pentatonic scale as geometry rather than a list of notes.

→ Live: [atcooper.net/tools](https://atcooper.net/tools) (Interactive — The Pentatonic Suite section)

## The idea

Every musical note already contains every other note — the overtone series means a played D also produces A, F♯, E, and so on up the harmonic ladder. The starting condition of sound is closeness. A song is therefore not a construction built from chosen notes; it is a *suppression pattern* — the shape left behind after most of what's already there has been quieted and specific intervals left audible. Two songs sound alike when they suppress the same things.

The pentatonic scale is five notes spaced as evenly as possible around twelve. Perfect even spacing would put each note 2.4 semitones apart; since you can't play 2.4 semitones, the pentatonic alternates steps of 2 and 3 — a slightly irregular pentagon inscribed in the circle of twelve. It contains no semitones and no tritones: the two most dissonant interval types are structurally excluded. The pentagon is a pre-solved consonance structure.

`pentagon-model.md` is the full conceptual writeup — the angles, the socket/rotation comparison method, and the rest of the model.

## Contents

All three artifacts are self-contained single-file HTML (SVG/Canvas + Web Audio, no dependencies). Each mirrors a live deployment under `/tools/pentatonic/` on the site.

- `pentatonic-pentagon.html` — the **Pentatonic Pentagon**. Draws the pentatonic pentagon in the twelve-note circle; rotate it (continuous or notched to whole semitones), play the chord, arpeggiate, click vertices to sound individual notes. The pentagon's diagonals cross at *ghost notes* — pitches the geometry implies that the scale itself never plays — sounded on click.
- `heartbeat-tuning.html` — **Heartbeat Tuning**. Plots the midpoint fret of each string as a waveform: the fretboard becomes a wave. Dragging the tuning interval reshapes the cam profile — fourths pulse, fifths breathe, minor thirds flutter. Controls for string count and playback speed; plays the heartbeat as audio.
- `squish.html` — **Squish**. Folds pitch space into fret space with a squish slider; click any dot to hear it, run the pentatonic sequence. The pentagon doesn't close — it keeps running.
- `pentagon-model.md` — the conceptual model behind the suite: closeness as the starting condition, the song as suppression pattern, melodic movement as angle, song comparison as a pentagon-rotation problem.

## Note on source

Pentatonic Pentagon is the locally-archived `pentagon-audible-ghosts-notch.html` (Alex Cooper & Claude, 17–18 March 2026). Heartbeat Tuning and Squish were brought across from their published Claude artifacts.
