#!/usr/bin/env python3
"""
RHYTHM DICTIONARY — SUPPRESSION VECTOR AUDIO CODEC
====================================================

Encodes genre suppression waveforms as audio. Decodes them back.

The audio IS the data:
  - Pitch contour = suppression profile (y-level → frequency)
  - Spectrogram view = the gridline diagram, literally
  - 17kHz watermark = "this is a suppression vector file"
  - Footer section = encoded metadata (genre, engine, positions, version)

Each fingerprint position → 250ms tone.
Pitch: silence=subfloor, 110Hz=floor, 220Hz=centre, 440Hz=ceiling, 880Hz=surprise.
The spectrogram of this audio IS the suppression waveform drawn on paper.

Timbres per engine:
  Binary:       sine (clean, mathematical)
  Cultural:     triangle (softer, convention-like)
  Percussion:   sine + noise transient (percussive)
  Feltness:     filtered noise (warm, bodily)
  Interpretive: FM synthesis (complex, layered)

Self-documenting: footer encodes JSON metadata as FSK tones at 13-16kHz.
Any future decoder detects 17kHz watermark → looks for footer → reconstructs vector.

Usage:
    python3 suppression_audio.py generate
    python3 suppression_audio.py read <file.wav>
"""

import numpy as np
import wave
import struct
import json
import sys
import os

# ============================================================
# AUDIO CONSTANTS
# ============================================================

SAMPLE_RATE = 44100
BIT_DEPTH = 16
MAX_AMP = 32767  # 16-bit signed

POSITION_DURATION = 0.25   # seconds per gridline position
CROSSFADE_S = 0.012        # 12ms crossfade between positions
HEADER_DURATION = 0.6      # identification header
FOOTER_DURATION = 2.0      # metadata footer
SILENCE_GAP = 0.1          # gap between header/body/footer

WATERMARK_FREQ = 17000     # Hz — present throughout, marks file type
WATERMARK_AMP = 0.04       # quiet but detectable

# ============================================================
# Y-LEVEL MAPPING
# ============================================================

# Named y-levels map to 0-1 float
Y_LEVELS = {
    'SUBFLOOR':      0.00,
    'FLOOR':         0.18,
    'sub_CENTRE':    0.32,
    'CENTRE':        0.42,
    'low_ACTIVE':    0.52,
    'mid_ACTIVE':    0.62,
    'upper_ACTIVE':  0.75,
    'CEILING':       0.90,
    'ABOVE_CEILING': 1.00,
}

def y_to_freq(y):
    """Map y-level float (0-1) to frequency Hz."""
    if y < 0.05:
        return 0  # subfloor = silence
    # Exponential: 0.18→110Hz, 0.42→220Hz, 0.75→440Hz, 0.90→554Hz, 1.0→880Hz
    return 110 * (2 ** ((y - 0.18) * 3.0))

def y_to_amp(y):
    """Map y-level to amplitude (0-1)."""
    if y < 0.05:
        return 0.0
    return 0.12 + y * 0.78

def freq_to_y(freq):
    """Reverse: frequency back to y-level."""
    if freq < 50:
        return 0.0
    return (np.log2(freq / 110) / 3.0) + 0.18

# ============================================================
# WAVEFORM GENERATORS (per-engine timbres)
# ============================================================

def gen_sine(freq, duration, amp, sr=SAMPLE_RATE):
    """Pure sine wave."""
    t = np.arange(int(sr * duration)) / sr
    if freq <= 0:
        return np.zeros_like(t)
    return amp * np.sin(2 * np.pi * freq * t)

def gen_triangle(freq, duration, amp, sr=SAMPLE_RATE):
    """Triangle wave — softer harmonics."""
    t = np.arange(int(sr * duration)) / sr
    if freq <= 0:
        return np.zeros_like(t)
    # Triangle from sawtooth
    phase = (t * freq) % 1.0
    tri = 2 * np.abs(2 * phase - 1) - 1
    return amp * tri

def gen_percussive(freq, duration, amp, sr=SAMPLE_RATE):
    """Sine with noise transient on attack."""
    t = np.arange(int(sr * duration)) / sr
    if freq <= 0:
        return np.zeros_like(t)
    # Sine body
    body = amp * np.sin(2 * np.pi * freq * t)
    # Noise transient (first 15ms)
    noise_dur = min(0.015, duration)
    noise_samples = int(sr * noise_dur)
    noise_env = np.exp(-t[:noise_samples] * 200)
    noise = np.zeros_like(t)
    noise[:noise_samples] = amp * 0.4 * np.random.randn(noise_samples) * noise_env
    return body + noise

def gen_warm(freq, duration, amp, sr=SAMPLE_RATE):
    """Filtered noise — warm, bodily."""
    t = np.arange(int(sr * duration)) / sr
    if freq <= 0:
        return np.zeros_like(t)
    n = len(t)
    # Band-pass noise around the target frequency
    noise = np.random.randn(n)
    # Simple resonant filter: multiply by modulated sine
    filtered = noise * np.sin(2 * np.pi * freq * t) * amp * 0.7
    # Add a quiet sine for pitch clarity
    filtered += amp * 0.4 * np.sin(2 * np.pi * freq * t)
    return filtered

def gen_fm(freq, duration, amp, sr=SAMPLE_RATE):
    """FM synthesis — complex, interpretive."""
    t = np.arange(int(sr * duration)) / sr
    if freq <= 0:
        return np.zeros_like(t)
    mod_freq = freq * 1.5
    mod_depth = freq * 0.3
    modulator = mod_depth * np.sin(2 * np.pi * mod_freq * t)
    carrier = amp * np.sin(2 * np.pi * (freq * t + modulator / (2 * np.pi * freq)))
    return carrier

ENGINE_GENERATORS = {
    'binary':       gen_sine,
    'cultural':     gen_triangle,
    'percussion':   gen_percussive,
    'feltness':     gen_warm,
    'interpretive': gen_fm,
}

# ============================================================
# DIRECTION MODIFIERS
# ============================================================

def apply_direction(audio, direction, y_level, freq, engine, sr=SAMPLE_RATE):
    """Modify the audio segment based on direction arrow."""
    n = len(audio)
    if direction == 'stable':
        return audio
    elif direction == 'rising':
        # Slight pitch ramp up (via amplitude envelope rising)
        env = np.linspace(0.85, 1.0, n)
        return audio * env
    elif direction == 'sinking':
        # Slight pitch ramp down
        env = np.linspace(1.0, 0.85, n)
        return audio * env
    elif direction == 'surprise':
        # Sharp transient click at start + full tone
        click_samples = int(sr * 0.008)
        click = np.zeros(n)
        if click_samples > 0 and click_samples < n:
            click[:click_samples] = 0.9 * np.random.randn(click_samples)
            click[:click_samples] *= np.exp(-np.arange(click_samples) / (sr * 0.002))
        return np.clip(audio + click, -1.0, 1.0)
    return audio

# ============================================================
# HEADER: IDENTIFICATION TONES
# ============================================================

def generate_header(engine, sr=SAMPLE_RATE):
    """Three-tone handshake: 'this is a suppression vector'
    Tone 1: 1000Hz (100ms) — marker
    Tone 2: engine-specific freq (100ms) — which engine
    Tone 3: 1000Hz (100ms) — confirmation
    """
    engine_freqs = {
        'binary':       1200,
        'cultural':     1400,
        'percussion':   1600,
        'feltness':     1800,
        'interpretive': 2000,
    }
    tone_dur = 0.12
    gap_dur = 0.04
    gen = gen_sine  # header always sine for clarity

    t1 = gen(1000, tone_dur, 0.7, sr)
    gap = np.zeros(int(sr * gap_dur))
    t2 = gen(engine_freqs.get(engine, 1200), tone_dur, 0.7, sr)
    t3 = gen(1000, tone_dur, 0.7, sr)

    header = np.concatenate([t1, gap, t2, gap, t3, gap])
    # Pad to HEADER_DURATION
    target_len = int(sr * HEADER_DURATION)
    if len(header) < target_len:
        header = np.concatenate([header, np.zeros(target_len - len(header))])
    return header[:target_len]

# ============================================================
# FOOTER: METADATA ENCODED AS FSK TONES
# ============================================================

def encode_metadata_footer(metadata_dict, sr=SAMPLE_RATE):
    """Encode a JSON metadata dict as FSK tones in the 13-16kHz range.

    Each byte → two 25ms tones:
      High nibble: 13000 + (nibble * 180) Hz
      Low nibble:  14500 + (nibble * 180) Hz

    Preceded by a 50ms sync tone at 12500Hz.
    """
    json_str = json.dumps(metadata_dict, separators=(',', ':'))
    json_bytes = json_str.encode('ascii')

    tone_dur = 0.022  # 22ms per tone
    gap_dur = 0.003   # 3ms gap

    # Sync tone
    sync = gen_sine(12500, 0.05, 0.3, sr)

    parts = [sync, np.zeros(int(sr * gap_dur))]

    for byte in json_bytes:
        high_nib = (byte >> 4) & 0x0F
        low_nib = byte & 0x0F
        f_high = 13000 + high_nib * 180
        f_low = 14500 + low_nib * 180
        parts.append(gen_sine(f_high, tone_dur, 0.25, sr))
        parts.append(gen_sine(f_low, tone_dur, 0.25, sr))
        parts.append(np.zeros(int(sr * gap_dur)))

    # End sync
    parts.append(gen_sine(12500, 0.05, 0.3, sr))

    footer = np.concatenate(parts)

    # Pad or trim to FOOTER_DURATION
    target_len = int(sr * FOOTER_DURATION)
    if len(footer) < target_len:
        footer = np.concatenate([footer, np.zeros(target_len - len(footer))])
    return footer[:target_len]

# ============================================================
# MAIN ENCODER
# ============================================================

def encode_engine_waveform(positions, engine, genre, sr=SAMPLE_RATE):
    """Encode a list of (fp_id, y_level_name, direction) tuples into audio.

    Returns: numpy array of float64 samples, normalized to [-1, 1]
    """
    generator = ENGINE_GENERATORS.get(engine, gen_sine)

    # 1. Header
    header = generate_header(engine, sr)

    # 2. Body: one tone per position
    body_parts = []
    cf_samples = int(sr * CROSSFADE_S)

    for i, (fp_id, y_name, direction) in enumerate(positions):
        y = Y_LEVELS.get(y_name, 0.0)
        freq = y_to_freq(y)
        amp = y_to_amp(y)

        segment = generator(freq, POSITION_DURATION, amp, sr)
        segment = apply_direction(segment, direction, y, freq, engine, sr)

        # Crossfade with previous
        if i > 0 and cf_samples > 0 and len(segment) > cf_samples:
            fade_in = np.linspace(0, 1, cf_samples)
            segment[:cf_samples] *= fade_in

        if i < len(positions) - 1 and cf_samples > 0 and len(segment) > cf_samples:
            fade_out = np.linspace(1, 0, cf_samples)
            segment[-cf_samples:] *= fade_out

        body_parts.append(segment)

    body = np.concatenate(body_parts)

    # 3. Footer: encoded metadata
    metadata = {
        'type': 'RD_SUPPRESSION_V1',
        'genre': genre,
        'engine': engine,
        'positions': len(positions),
        'pos_dur_ms': int(POSITION_DURATION * 1000),
        'version': '0.1',
        'decode': 'pitch_contour→y_level→status',
        'fp_ids': [p[0] for p in positions],
    }
    footer = encode_metadata_footer(metadata, sr)

    # 4. Assemble: header + gap + body + gap + footer
    gap = np.zeros(int(sr * SILENCE_GAP))
    audio = np.concatenate([header, gap, body, gap, footer])

    # 5. Add watermark throughout (17kHz marker)
    t = np.arange(len(audio)) / sr
    watermark = WATERMARK_AMP * np.sin(2 * np.pi * WATERMARK_FREQ * t)
    audio = audio + watermark

    # Normalize
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.95

    return audio

def write_wav(filename, audio, sr=SAMPLE_RATE):
    """Write float64 audio array to 16-bit WAV."""
    audio_int = np.clip(audio * MAX_AMP, -MAX_AMP, MAX_AMP).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int.tobytes())

# ============================================================
# DECODER
# ============================================================

def read_wav(filename):
    """Read WAV file, return float64 array and sample rate."""
    with wave.open(filename, 'r') as wf:
        sr = wf.getframerate()
        n = wf.getnframes()
        raw = wf.readframes(n)
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / MAX_AMP
    return audio, sr

def detect_watermark(audio, sr=SAMPLE_RATE):
    """Check for 17kHz watermark presence."""
    # Windowed FFT looking for 17kHz energy
    window_size = 4096
    if len(audio) < window_size:
        return False
    segment = audio[len(audio)//2 : len(audio)//2 + window_size]
    fft = np.abs(np.fft.rfft(segment))
    freqs = np.fft.rfftfreq(window_size, 1/sr)
    # Check for peak near 17kHz
    target_idx = np.argmin(np.abs(freqs - WATERMARK_FREQ))
    local_mean = np.mean(fft[max(0,target_idx-20):target_idx-5])
    if local_mean > 0:
        ratio = fft[target_idx] / local_mean
        return ratio > 2.0  # 17kHz should be notably above neighbors
    return False

def extract_pitch_contour(audio, sr=SAMPLE_RATE, n_positions=64):
    """Extract the pitch contour from the body section.

    Skips header, analyzes body in POSITION_DURATION windows,
    returns list of (frequency, y_level) tuples.
    """
    header_samples = int(sr * (HEADER_DURATION + SILENCE_GAP))
    footer_samples = int(sr * (FOOTER_DURATION + SILENCE_GAP))
    body = audio[header_samples : len(audio) - footer_samples]

    pos_samples = int(sr * POSITION_DURATION)
    results = []

    for i in range(n_positions):
        start = i * pos_samples
        end = start + pos_samples
        if end > len(body):
            break
        segment = body[start:end]

        # Find dominant frequency via FFT
        if np.max(np.abs(segment)) < 0.02:
            # Silence = subfloor
            results.append((0, 0.0, 'SUBFLOOR'))
            continue

        # Windowed FFT
        windowed = segment * np.hanning(len(segment))
        fft = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(segment), 1/sr)

        # Mask out watermark region (16-18kHz) and footer region (12-16kHz)
        mask = freqs < 11000
        fft_masked = fft * mask

        if np.max(fft_masked) < 0.1:
            results.append((0, 0.0, 'SUBFLOOR'))
            continue

        peak_idx = np.argmax(fft_masked)
        peak_freq = freqs[peak_idx]

        # Map back to y-level
        y = freq_to_y(peak_freq)
        y = np.clip(y, 0, 1)

        # Find nearest named level
        best_name = 'SUBFLOOR'
        best_dist = 999
        for name, val in Y_LEVELS.items():
            if abs(y - val) < best_dist:
                best_dist = abs(y - val)
                best_name = name

        results.append((peak_freq, y, best_name))

    return results

def decode_suppression_wav(filename):
    """Full decode: read WAV, detect watermark, extract contour, return vector."""
    audio, sr = read_wav(filename)

    has_watermark = detect_watermark(audio, sr)
    contour = extract_pitch_contour(audio, sr)

    return {
        'file': filename,
        'watermark_detected': has_watermark,
        'positions': len(contour),
        'contour': contour,
    }

# ============================================================
# BREAKCORE DATA — ALL 5 ENGINES
# ============================================================

BREAKCORE_BINARY = [
    # (fp_id, y_level, direction)
    # Positions 1-10: genre splitters
    ('FP-T04', 'CEILING',       'surprise'),   #  1 extreme tempo — bimodal, was surprised
    ('FP-V01', 'SUBFLOOR',      'stable'),     #  2 vocal foreground — silent
    ('FP-T08', 'SUBFLOOR',      'stable'),     #  3 free time — silent
    ('FP-E03', 'FLOOR',         'stable'),     #  4 slow onset — dormant
    ('FP-D06', 'CEILING',       'rising'),     #  5 relentless escalation — defining
    ('FP-T10', 'CEILING',       'surprise'),   #  6 extreme density — surprised back
    ('FP-D04', 'mid_ACTIVE',    'stable'),     #  7 brick-wall — present not always
    ('FP-T01', 'SUBFLOOR',      'stable'),     #  8 slow tempo — silent
    ('FP-H02', 'mid_ACTIVE',    'sinking'),    #  9 hi-mid harmonic — fusion, sinking
    ('FP-E07', 'SUBFLOOR',      'stable'),     # 10 sidechain — silent
    # Positions 11-20: strong differentiators
    ('FP-T09', 'CEILING',       'stable'),     # 11 high density — reliable
    ('FP-D05', 'FLOOR',         'sinking'),    # 12 section contrast — approaching silent
    ('FP-R03', 'upper_ACTIVE',  'stable'),     # 13 through-composed — yes
    ('FP-R04', 'CEILING',       'stable'),     # 14 sample-based — always
    ('FP-V02', 'low_ACTIVE',    'surprise'),   # 15 vocal texture — Shitmat surprise
    ('FP-E04', 'mid_ACTIVE',    'stable'),     # 16 bloom — 808 dependent
    ('FP-X04', 'FLOOR',         'stable'),     # 17 independent layers — dormant
    ('FP-X02', 'upper_ACTIVE',  'stable'),     # 18 shadow bass — confirmed
    ('FP-P08', 'FLOOR',         'stable'),     # 19 tracker precision — dormant
    ('FP-R02', 'FLOOR',         'stable'),     # 20 build-drop — dormant
    # Positions 21-30: moderate differentiators
    ('FP-T03', 'CEILING',       'stable'),     # 21 fast tempo — always
    ('FP-T07', 'mid_ACTIVE',    'stable'),     # 22 irregular meter — variable
    ('FP-H01', 'sub_CENTRE',    'rising'),     # 23 hi-mid percussive — below threshold (fusion)
    ('FP-D03', 'mid_ACTIVE',    'stable'),     # 24 low crest — compressed
    ('FP-E01', 'CEILING',       'stable'),     # 25 sharp attack — every track
    ('FP-E02', 'FLOOR',         'stable'),     # 26 gated decay — dormant
    ('FP-S01', 'mid_ACTIVE',    'stable'),     # 27 sub-bass dominant — varies
    ('FP-P06', 'upper_ACTIVE',  'stable'),     # 28 distortion — aesthetic
    ('FP-R01', 'SUBFLOOR',      'stable'),     # 29 verse-chorus — silent
    ('FP-V04', 'SUBFLOOR',      'stable'),     # 30 vocal non-address — silent
    # Positions 31-42: long dormant plateau
    ('FP-W01', 'FLOOR',         'stable'),     # 31
    ('FP-W03', 'FLOOR',         'stable'),     # 32
    ('FP-R06', 'FLOOR',         'stable'),     # 33
    ('FP-E05', 'FLOOR',         'stable'),     # 34
    ('FP-E06', 'FLOOR',         'stable'),     # 35
    ('FP-H04', 'FLOOR',         'stable'),     # 36
    ('FP-H05', 'FLOOR',         'stable'),     # 37
    ('FP-P03', 'FLOOR',         'stable'),     # 38
    ('FP-S06', 'FLOOR',         'stable'),     # 39
    ('FP-E08', 'FLOOR',         'stable'),     # 40
    ('FP-R05', 'FLOOR',         'stable'),     # 41
    ('FP-X03', 'FLOOR',         'stable'),     # 42
    # Positions 43-50: scattered pops
    ('FP-V03', 'CEILING',       'stable'),     # 43 no vocal — always fires
    ('FP-S07', 'mid_ACTIVE',    'stable'),     # 44 coupling
    ('FP-T05', 'upper_ACTIVE',  'stable'),     # 45 regular grid
    ('FP-T06', 'SUBFLOOR',      'stable'),     # 46 human feel — silent
    ('FP-W05', 'FLOOR',         'stable'),     # 47
    ('FP-X01', 'FLOOR',         'sinking'),    # 48 hierarchy disrupted
    ('FP-P07', 'FLOOR',         'stable'),     # 49
    ('FP-S04', 'FLOOR',         'stable'),     # 50
    # Positions 51-64: baseline
    ('FP-T02', 'SUBFLOOR',      'stable'),     # 51 standard tempo — silent
    ('FP-D01', 'FLOOR',         'stable'),     # 52
    ('FP-D02', 'FLOOR',         'stable'),     # 53
    ('FP-H03', 'upper_ACTIVE',  'stable'),     # 54 sub-bass harmonic
    ('FP-S02', 'FLOOR',         'stable'),     # 55
    ('FP-S03', 'FLOOR',         'stable'),     # 56
    ('FP-S05', 'FLOOR',         'stable'),     # 57
    ('FP-P01', 'FLOOR',         'stable'),     # 58
    ('FP-P02', 'upper_ACTIVE',  'stable'),     # 59 dry
    ('FP-P04', 'FLOOR',         'stable'),     # 60
    ('FP-P05', 'upper_ACTIVE',  'stable'),     # 61 digital precision
    ('FP-W02', 'FLOOR',         'stable'),     # 62
    ('FP-W04', 'FLOOR',         'stable'),     # 63
    ('FP-X05', 'FLOOR',         'stable'),     # 64
]

BREAKCORE_CULTURAL = [
    ('U8-vocals_foreground',   'FLOOR',         'sinking'),    #  1
    ('U6-dynamic_emphasis',    'FLOOR',         'stable'),     #  2
    ('U4-sounds_decay',        'mid_ACTIVE',    'stable'),     #  3
    ('U10-structure_sections', 'mid_ACTIVE',    'stable'),     #  4
    ('G-extreme_tempo',        'CEILING',       'stable'),     #  5
    ('G-sample_atomization',   'CEILING',       'stable'),     #  6
    ('G-relentless_escalation','upper_ACTIVE',  'stable'),     #  7
    ('G-no_address',           'upper_ACTIVE',  'stable'),     #  8
    ('G-sub_bass_shadow',      'mid_ACTIVE',    'sinking'),    #  9
    ('U1-drums_rhythmic',      'CEILING',       'stable'),     # 10
    ('U5-freq_roles_fixed',    'CEILING',       'stable'),     # 11 (VIOLATED → discovery spike)
    ('U7-temporal_regularity', 'CEILING',       'stable'),     # 12
    ('U2-rhythm_bass_felt',    'CEILING',       'stable'),     # 13
    ('U3-bass_foundation',     'CEILING',       'stable'),     # 14
    ('U9-stereo_center',       'upper_ACTIVE',  'stable'),     # 15
]

BREAKCORE_PERCUSSION = [
    ('fusion_test',        'CEILING',       'stable'),     #  1 defining
    ('ghost_note',         'FLOOR',         'stable'),     #  2 dormant
    ('crash_ride',         'FLOOR',         'stable'),     #  3 dormant
    ('percussion_active',  'CEILING',       'stable'),     #  4 yes
    ('hat_open',           'mid_ACTIVE',    'stable'),     #  5 present
    ('deviation_density',  'CEILING',       'stable'),     #  6 high
    ('kick',               'CEILING',       'stable'),     #  7
    ('snare',              'CEILING',       'stable'),     #  8
    ('hat_closed',         'CEILING',       'stable'),     #  9
    ('pairwise_ratios',    'CEILING',       'stable'),     # 10
]

BREAKCORE_FELTNESS = [
    ('gesture_hi_mid',     'CEILING',       'stable'),     #  1 main somatic
    ('gesture_high',       'FLOOR',         'stable'),     #  2 dormant
    ('polling_rate',       'CEILING',       'stable'),     #  3 1Hz
    ('acclimatisation',    'FLOOR',         'sinking'),    #  4 never settles
    ('gesture_sub_bass',   'CEILING',       'stable'),     #  5 felt
    ('gesture_bass',       'mid_ACTIVE',    'stable'),     #  6
    ('gesture_mid',        'FLOOR',         'stable'),     #  7 dormant
]

BREAKCORE_INTERPRETIVE = [
    ('bridge_7_inversion',    'CEILING',     'stable'),     #  1 fusion
    ('bridge_6_excision',     'CEILING',     'stable'),     #  2 absent conventions
    ('bridge_5_mutation',     'mid_ACTIVE',  'stable'),     #  3
    ('bridge_4_displacement', 'mid_ACTIVE',  'stable'),     #  4
    ('bridge_1_concealment',  'FLOOR',       'sinking'),    #  5 demoted
    ('bridge_3_contradiction','FLOOR',       'stable'),     #  6 dormant
    ('bridge_2_compensation', 'FLOOR',       'stable'),     #  7 dormant
]

ALL_ENGINES = {
    'binary':       BREAKCORE_BINARY,
    'cultural':     BREAKCORE_CULTURAL,
    'percussion':   BREAKCORE_PERCUSSION,
    'feltness':     BREAKCORE_FELTNESS,
    'interpretive': BREAKCORE_INTERPRETIVE,
}

# ============================================================
# GENERATE
# ============================================================

def generate_all(output_dir):
    """Generate all breakcore suppression WAVs."""
    os.makedirs(output_dir, exist_ok=True)

    all_audio = []

    for engine_name, positions in ALL_ENGINES.items():
        print(f"  Generating {engine_name} ({len(positions)} positions)...")
        audio = encode_engine_waveform(positions, engine_name, 'breakcore')

        filename = os.path.join(output_dir, f'breakcore_{engine_name}_suppression.wav')
        write_wav(filename, audio)
        print(f"    → {filename} ({len(audio)/SAMPLE_RATE:.1f}s)")

        all_audio.append(audio)
        # Add 0.5s gap between engines in combined file
        all_audio.append(np.zeros(int(SAMPLE_RATE * 0.5)))

    # Combined file
    combined = np.concatenate(all_audio[:-1])  # drop trailing gap
    combined_file = os.path.join(output_dir, 'breakcore_COMPLETE_suppression.wav')
    write_wav(combined_file, combined)
    print(f"  Combined → {combined_file} ({len(combined)/SAMPLE_RATE:.1f}s)")

    # Write decode instructions as companion file
    instructions = {
        'format': 'RD_SUPPRESSION_V1',
        'description': 'Rhythm Dictionary Suppression Vector Audio',
        'genre': 'breakcore',
        'encoding': {
            'pitch_contour': 'Each 250ms window = one gridline position. '
                           'Pitch maps to y-level: silence=SUBFLOOR, 110Hz=FLOOR, '
                           '220Hz=CENTRE, 440Hz=upper-ACTIVE, 554Hz=CEILING, 880Hz=ABOVE_CEILING.',
            'watermark': '17kHz sine present throughout. Detect this to identify file type.',
            'header': '3-tone handshake in first 0.6s. 1000Hz-[engine]-1000Hz.',
            'footer': 'FSK-encoded JSON metadata at 13-16kHz in final 2s.',
            'timbres': {
                'binary': 'sine (clean)',
                'cultural': 'triangle (soft)',
                'percussion': 'sine + noise transient',
                'feltness': 'filtered noise (warm)',
                'interpretive': 'FM synthesis (complex)'
            }
        },
        'to_decode': 'Run: python3 suppression_audio.py read <file.wav>',
        'y_level_map': Y_LEVELS,
        'engines': {name: len(pos) for name, pos in ALL_ENGINES.items()},
    }
    instructions_file = os.path.join(output_dir, 'SUPPRESSION_DECODE_INSTRUCTIONS.json')
    with open(instructions_file, 'w') as f:
        json.dump(instructions, f, indent=2)
    print(f"  Instructions → {instructions_file}")

# ============================================================
# CLI
# ============================================================

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'generate':
        output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
        print("RHYTHM DICTIONARY — Generating Breakcore Suppression Audio")
        print("=" * 60)
        generate_all(output_dir)
        print("=" * 60)
        print("Done. The audio IS the suppression vector.")
        print("Open in a DAW spectrogram view to SEE the gridline.")

    elif command == 'read':
        if len(sys.argv) < 3:
            print("Usage: python3 suppression_audio.py read <file.wav>")
            sys.exit(1)
        filename = sys.argv[2]
        print(f"RHYTHM DICTIONARY — Decoding: {filename}")
        print("=" * 60)
        result = decode_suppression_wav(filename)
        print(f"  Watermark detected: {result['watermark_detected']}")
        print(f"  Positions decoded:  {result['positions']}")
        print()
        print("  Pos  Freq(Hz)  Y-Level       Status")
        print("  ───  ────────  ────────────  ──────────")
        for i, (freq, y, name) in enumerate(result['contour']):
            print(f"  {i+1:3d}  {freq:7.1f}  {y:.2f}          {name}")
        print("=" * 60)

    else:
        print(f"Unknown command: {command}")
        print("Use 'generate' or 'read'")
        sys.exit(1)
