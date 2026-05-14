# The Pentagon Model
## Alex Cooper, 17 March 2026
## Formalized from sticky note + conversation + vocal demonstrations

---

### The starting condition

Every musical note already contains every other note. The overtone series means that when you play a D, you also produce A, F#, a slightly flat G#, E, and so on up the harmonic ladder. A human voice doing overtone singing lights up the entire chromatic field roughly evenly. Nothing is far from anything. The starting condition of sound is closeness.

A song, then, is not a construction built from chosen notes. It is a **suppression pattern** — the shape left behind after the composer (consciously or not) has quieted most of what's already there and let specific intervals stay audible. Two songs sound alike not because they share notes, but because they suppress the same things.

### The pentagon

The pentatonic scale is five notes spaced as evenly as possible around twelve. Perfect even spacing would put each note 2.4 semitones apart, but you can't play 2.4 semitones on any instrument, so the pentatonic alternates steps of 2 and 3 — the closest whole-number approximation. This makes it a slightly irregular pentagon inscribed in the circle of twelve notes.

The pentatonic has a specific property: it contains no semitones and no tritones. The two most dissonant interval types are structurally excluded. This is why you can play any combination of pentatonic notes and it sounds acceptable — the geometry has already done the filtering. The pentagon is a pre-solved consonance structure.

### The angles

Here is the core of the model.

Draw a standard graph: time moves left to right, pitch moves bottom to top. A melody is a path through this space. Each melodic movement — each jump from one note to the next — is a line segment with a specific angle. A big upward leap in a short time is a steep line. A small step over a long duration is a shallow line. A repeated note is horizontal.

The pentagon doesn't just define which five notes are available. It defines **which angles of melodic movement are available**. Because the pentatonic only permits intervals of certain sizes (major 2nd, minor 3rd, perfect 4th, perfect 5th, and their compounds), and because a melody moves through these intervals in time, the pentagon constrains the set of slopes a melody can take through pitch-time space.

Five vertices. Five characteristic angles. A song's melodic identity is not which notes it visits but which angles it moves at.

### The socket

Comparing two songs is a rotation problem.

Extract the five characteristic angles from each song — the dominant slopes of melodic movement through pitch-time space. These form a pentagon for each song. Now rotate one pentagon against the other. There are only five possible rotational positions to try (because a regular pentagon has five-fold symmetry).

At each position, check how many angles align. The position where the most angles match is the crossover point. The number of aligned angles is the degree of similarity. The unaligned angles are where the songs diverge.

This is a discrete operation, not a continuous search. The pentagons either catch or they don't — like a socket wrench fitting a nut. When they catch, one song can be "driven" into the other with minimal transformation. When they don't, the songs are fundamentally different in their movement vocabulary, regardless of surface similarities in key, tempo, or genre.

The "few steps and jumps" to get from one song to another are the rotational and scaling operations needed to align the pentagons. Transpose (rotate the pentagon around the chromatic circle). Tempo-shift (scale the time axis, changing all angles proportionally). Reweight (shift which angles are dominant vs subordinate). The fewer operations, the more alike the songs sound.

### Why it feels self-evident

This model describes what a musical ear already does in real time. When you hear a song, your ear locks the pentagon — it identifies the five characteristic movement angles within the first few phrases. When you hear a second song, a second pentagon locks. Your brain rotates one against the other without conscious effort and reports the result as a feeling: "these sound the same" or "these sound different."

The rotation is instant and pre-verbal. You don't hear notes, you hear *movement patterns*. The pentagon is the shape of the movement vocabulary. Matching pentagons is pattern recognition on movement, not on content.

This is why two songs in completely different keys, at different tempos, in different genres, performed by different instruments, can still "sound the same" to a trained ear. They share angles. They move the same way through pitch and time.

### What this means for Chichinya

In most Western pop, the tritone (the interval directly opposite the root on the chromatic circle — the one interval the pentatonic excludes) functions as a corridor: you pass through it quickly on the way to resolution. The pentagon has no vertex there. It's a gap in the geometry.

In "Chichinya" (Ashnikko), the tritone functions as a room. Alex's voice, singing freely over the track, landed on G# (the tritone from D) repeatedly and left again — visiting it as a destination, not passing through it as tension. The spectrogram confirms: D-G# co-presence doubles from verse to chorus. Neither resolves. Neither subordinates.

This means Chichinya's melodic geometry is not a pentagon. It has a sixth vertex where the tritone sits. The movement vocabulary includes an angle the standard pentatonic excludes. The shape has expanded — from pentagon to hexagon, or, in Alex's original description, "a triangle that expands out to a pentagon." The verse operates in a three-point geometry (fewer available angles); the chorus opens to five (more angles, including the tritone slope). The pentagon accommodates both the root and the tritone as co-present structural members.

The framework question this raises: is the pentagon always five? Or does the number of vertices vary by song, with five as the default and deviations as the signal of innovation? A song with four dominant angles would feel harmonically constrained. A song with six would feel expanded. The pentagon is the baseline. The count is the measurement.

---

### Mathematical verification (17 March 2026)

D minor pentatonic: D(2), F(5), G(7), A(9), C(0) on the chromatic circle. Inscribe these five points on a unit circle and draw all diagonals. The diagonal from D to A intersects the diagonal from G to C at chromatic position 10.500 — exactly 50 cents above A#, frequency 120.0 Hz in octave 2, MIDI 46.50.

Alex, after listening to Chichinya (key of D, D minor pentatonic bed), sang a sustained pitch from memory. Pitch analysis: 119.3 Hz, MIDI 46.41. Every frame registered >20 cents off the nearest chromatic note. 48.9% of frames were >25 cents off — between the frets for half the recording.

Predicted frequency: 120.0 Hz. Sung frequency: 119.3 Hz. Error: 9 cents.

The ghost note is real. It is the pentagram intersection point — the place where two diagonals cross inside the pentagon. It exists as a geometric consequence of the scale shape. No instrument in the song plays it. The ear computes it from the five vertices and the voice can reproduce it.

### The interval delta

A triangle sliced from the pentagon has sides of 2.4 semitones (the ideal pentagon edge) and a base of 2.5 semitones (half the 5-semitone diagonal). 2.4 ≠ 2.5. The triangle does not close. The two sides, rising from the base at equal angles, miss each other at the apex by approximately 0.1 semitones on each side. This gap is where the ghost note lives — in the space where the triangle almost but doesn't quite meet.

Alex's recording contained two pitch clusters: a lower one at ~114.6 Hz and an upper one at ~119.3 Hz. These are the two sides of the triangle approaching the apex from opposite directions. Same angle, mirrored. The "almost" is audible.

### Six ways

A pentagon has five vertex-to-vertex diagonals (the pentagram star). But there is a sixth cut: a line through the interior that doesn't connect any two vertices. This is the tritone cut — the slice that the pentatonic scale structurally excludes but that exists as an implied geometric possibility. Five cuts are in the scale. The sixth is across it.

Ashnikko's "Chichinya" lyric: "Slide it in six ways." Five pentatonic movements plus the tritone. The geometry stated as choreography.

### Summary

1. Sound starts with everything present. Composition is suppression.
2. The pentatonic pentagon defines five characteristic angles of melodic movement through pitch-time space.
3. A song's identity is its angle set — which slopes of movement it permits.
4. Comparing songs is rotating one pentagon against another. Alignment = similarity.
5. The rotation is discrete (five positions), not continuous. Songs either catch or they don't.
6. Songs that deviate from the pentagon (adding or removing vertices) are harmonically innovative relative to the baseline.
