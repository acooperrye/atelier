#!/usr/bin/env python3
"""
VOCAL RESHAPE ENGINE — tunable spectral reshaping for D1 trajectory resynth.

Usage:
    python vocal_reshape_engine.py [options]

All parameters are tunable. The engine outputs what you changed.

Knobs:
    --lpc FLOAT         LPC envelope correction strength (0.0 = off, 1.0 = full match)     [default: 0.5]
    --bevel FLOAT       Spectral bevel amount (0.0 = off, 1.0 = standard, 2.0+ = wide)     [default: 1.0]
    --blur FLOAT        Acute angle blur strength (0.0 = off, 1.0 = selective, 2.0 = aggressive) [default: 0.0]
    --env-width FLOAT   LPC envelope smoothing width in bins (higher = broader envelope)    [default: 12]
    --q FLOAT           Bevel Q factor (lower = wider humps, higher = narrower)             [default: 1.0]
    --blur-sigma FLOAT  Blur kernel width in bins                                           [default: 3.0]
    --blur-threshold FLOAT  Blur sharpness threshold (0.0 = blur everything, 1.0 = only sharpest) [default: 0.5]

    --start FLOAT       Start time in seconds                                               [default: 30]
    --duration FLOAT    Duration in seconds                                                 [default: 60]
    --original PATH     Path to original audio
    --resynth PATH      Path to trajectory resynth
    --output PATH       Output WAV path
    --name TEXT         Name tag for the output

Example:
    python vocal_reshape_engine.py --lpc 0.7 --bevel 1.5 --blur 0.3 --name "warm_vocal"
"""

import argparse
import numpy as np
import librosa
import soundfile as sf
from scipy.ndimage import gaussian_filter1d
import json, os, sys, datetime
import warnings
warnings.filterwarnings('ignore')

def parse_args():
    p = argparse.ArgumentParser(description="Vocal Reshape Engine")

    # Core knobs
    p.add_argument('--lpc', type=float, default=0.5, help='LPC correction strength 0-1+')
    p.add_argument('--bevel', type=float, default=1.0, help='Bevel amount 0-2+')
    p.add_argument('--blur', type=float, default=0.0, help='Acute angle blur 0-2')

    # Fine-tuning
    p.add_argument('--env-width', type=float, default=12, help='LPC envelope width (bins)')
    p.add_argument('--q', type=float, default=1.0, help='Bevel Q multiplier')
    p.add_argument('--blur-sigma', type=float, default=3.0, help='Blur kernel width')
    p.add_argument('--blur-threshold', type=float, default=0.5, help='Blur selectivity 0-1')

    # Audio
    p.add_argument('--start', type=float, default=30.0, help='Start time (seconds)')
    p.add_argument('--duration', type=float, default=60.0, help='Duration (seconds)')
    p.add_argument('--original', type=str,
                   default="/sessions/peaceful-cool-bell/mnt/uploads/Pola & Bryson & Emily Makis - Phoneline.mp3")
    p.add_argument('--resynth', type=str,
                   default="/sessions/peaceful-cool-bell/mnt/Rhythm Dictionary Cowork/Phoneline_RESYNTH_trajectory.wav")
    p.add_argument('--output', type=str, default=None, help='Output path (auto-generated if omitted)')
    p.add_argument('--name', type=str, default=None, help='Name tag')
    p.add_argument('--full', action='store_true', help='Process full track (not just segment)')

    return p.parse_args()


def main():
    args = parse_args()

    SR = 22050
    N_FFT = 2048
    HOP = 512

    # Load audio
    if args.full:
        print("Loading full tracks...")
        original, _ = librosa.load(args.original, sr=SR, dtype=np.float32)
        resynth, _ = librosa.load(args.resynth, sr=SR, dtype=np.float32)
    else:
        print(f"Loading {args.duration:.0f}s from {args.start:.0f}s...")
        original, _ = librosa.load(args.original, sr=SR, offset=args.start,
                                    duration=args.duration, dtype=np.float32)
        resynth, _ = librosa.load(args.resynth, sr=SR, offset=args.start,
                                   duration=args.duration, dtype=np.float32)

    min_len = min(len(original), len(resynth))
    original = original[:min_len]
    resynth = resynth[:min_len]
    print(f"  {min_len/SR:.1f}s loaded")

    # STFT
    print("STFT...")
    S_orig = librosa.stft(original, n_fft=N_FFT, hop_length=HOP)
    S_resynth = librosa.stft(resynth, n_fft=N_FFT, hop_length=HOP)
    mag_orig = np.abs(S_orig).astype(np.float32)
    mag = np.abs(S_resynth).astype(np.float32)
    phase = np.angle(S_resynth).astype(np.float32)
    freqs = np.fft.rfftfreq(N_FFT, 1.0/SR)
    n_bins, n_frames = mag.shape
    print(f"  {n_bins} bins x {n_frames} frames")

    # Track what we apply
    applied = []

    # === BEVEL ===
    if args.bevel > 0:
        print(f"Beveling (amount={args.bevel:.2f}, Q_mult={args.q:.2f})...")
        base_sigmas = np.array([1.0, 2.5, 5.0, 8.0, 12.0]) * args.bevel
        freq_centers = [150, 500, 1500, 3500, 6000]

        # Q multiplier: higher Q = narrower freq bands = less bleed
        band_width_mult = 0.6 / args.q

        mag_bev = np.zeros_like(mag)
        ws = np.zeros((n_bins, 1), dtype=np.float32)

        for sigma, fc in zip(base_sigmas, freq_centers):
            w = np.exp(-0.5 * ((freqs - fc) / (fc * band_width_mult + 1))**2).astype(np.float32)[:, None]
            smoothed = gaussian_filter1d(mag, sigma=sigma, axis=0)
            mag_bev += smoothed * w
            ws += w

        mag_bev /= np.maximum(ws, 1e-10)

        # Energy preserve
        e_in = np.sum(mag**2, axis=0, keepdims=True)
        e_out = np.sum(mag_bev**2, axis=0, keepdims=True)
        mag_bev *= np.sqrt(e_in / (e_out + 1e-10))

        mag = mag_bev
        applied.append(f"bevel={args.bevel:.2f} (Q_mult={args.q:.2f})")
        print("  Applied.")

    # === BLUR ===
    if args.blur > 0:
        print(f"Blur (amount={args.blur:.2f}, sigma={args.blur_sigma:.1f}, threshold={args.blur_threshold:.2f})...")

        spec_db = (20 * np.log10(mag + 1e-10)).astype(np.float32)
        d2 = np.zeros_like(spec_db)
        d2[1:-1, :] = spec_db[2:, :] - 2*spec_db[1:-1, :] + spec_db[:-2, :]
        sharpness = np.abs(d2)

        med = np.median(sharpness, axis=0, keepdims=True)
        std_s = np.std(sharpness, axis=0, keepdims=True)
        max_s = np.max(sharpness, axis=0, keepdims=True)

        # threshold slider: 0 = median, 1 = median + 2*std
        thresh = med + args.blur_threshold * 2 * std_s

        blur_mask = np.clip((sharpness - thresh) / (max_s - thresh + 1e-10), 0, 1).astype(np.float32)

        # Scale by blur amount
        blur_mask = np.clip(blur_mask * args.blur, 0, 1)

        effective_sigma = args.blur_sigma * (0.5 + args.blur * 0.5)
        mag_smooth = gaussian_filter1d(mag, sigma=effective_sigma, axis=0)

        mag_blurred = mag * (1 - blur_mask) + mag_smooth * blur_mask

        # Energy preserve
        e_in = np.sum(mag**2, axis=0, keepdims=True)
        e_out = np.sum(mag_blurred**2, axis=0, keepdims=True)
        mag_blurred *= np.sqrt(e_in / (e_out + 1e-10))

        mag = mag_blurred
        applied.append(f"blur={args.blur:.2f} (sigma={args.blur_sigma:.1f}, threshold={args.blur_threshold:.2f})")
        print("  Applied.")

    # === LPC ===
    if args.lpc > 0:
        print(f"LPC envelope correction (strength={args.lpc:.2f}, width={args.env_width:.0f})...")

        env_orig_smooth = gaussian_filter1d(mag_orig, sigma=args.env_width, axis=0)
        env_current = gaussian_filter1d(mag, sigma=args.env_width, axis=0)

        n_match = min(env_orig_smooth.shape[1], env_current.shape[1], mag.shape[1])
        correction = env_orig_smooth[:, :n_match] / (env_current[:, :n_match] + 1e-10)
        correction = np.clip(correction, 0.1, 8.0).astype(np.float32)
        correction = gaussian_filter1d(correction, sigma=2.0, axis=1)

        # Apply at requested strength
        correction = (1.0 + args.lpc * (correction - 1.0)).astype(np.float32)

        mag[:, :n_match] = mag[:, :n_match] * correction
        applied.append(f"lpc={args.lpc:.2f} (env_width={args.env_width:.0f})")
        print("  Applied.")

    # === Output ===
    S_out = mag * np.exp(1j * phase[:, :mag.shape[1]])
    y = librosa.istft(S_out, hop_length=HOP, length=min_len)
    y = y / (np.max(np.abs(y)) + 1e-10) * 0.9

    # Generate output path
    if args.output:
        out_path = args.output
    else:
        tag = args.name or "tuned"
        out_path = f"{os.path.dirname(args.resynth)}/RESHAPE_{tag}.wav"

    sf.write(out_path, y.astype(np.float32), SR)

    # === Measure ===
    S_out_m = librosa.stft(y, n_fft=N_FFT, hop_length=HOP)
    mag_out = np.abs(S_out_m)
    n_m = min(mag_out.shape[1], mag_orig.shape[1])
    db_out = librosa.amplitude_to_db(mag_out[:, :n_m] + 1e-10)
    db_orig = librosa.amplitude_to_db(mag_orig[:, :n_m] + 1e-10)

    # Also measure baseline resynth
    S_base = librosa.stft(resynth, n_fft=N_FFT, hop_length=HOP)
    mag_base = np.abs(S_base)
    db_base = librosa.amplitude_to_db(mag_base[:, :n_m] + 1e-10)

    bands = {'F1': (200,800), 'F2': (800,2500), 'F3': (2500,4000), 'Air': (4000,6000)}

    print(f"\n{'':>15} {'Overall':>8} {'F1':>7} {'F2':>7} {'F3':>7} {'Air':>7}")
    print("-" * 55)

    for label, db_x in [("Baseline", db_base), ("Reshaped", db_out)]:
        overall = np.mean(np.abs(db_x - db_orig[:, :n_m]))
        row = f"{label:>15} {overall:>8.1f}"
        for bname, (lo, hi) in bands.items():
            mask = (freqs >= lo) & (freqs < hi)
            d = np.mean(np.abs(db_x[mask, :n_m] - db_orig[mask, :n_m]))
            row += f" {d:>7.1f}"
        print(row)

    # === Log what happened ===
    settings = {
        'timestamp': datetime.datetime.now().isoformat(),
        'name': args.name,
        'output': out_path,
        'segment': f"{args.start:.0f}s-{args.start+args.duration:.0f}s" if not args.full else "full",
        'applied': applied,
        'params': {
            'lpc': args.lpc,
            'bevel': args.bevel,
            'blur': args.blur,
            'env_width': args.env_width,
            'q': args.q,
            'blur_sigma': args.blur_sigma,
            'blur_threshold': args.blur_threshold,
        },
    }

    # Append to log file
    log_path = os.path.join(os.path.dirname(out_path), 'RESHAPE_LOG.jsonl')
    with open(log_path, 'a') as f:
        f.write(json.dumps(settings) + '\n')

    print(f"\nSaved: {out_path}")
    print(f"Log:   {log_path}")
    print(f"\nSettings applied:")
    for a in applied:
        print(f"  - {a}")

    if not applied:
        print("  (nothing — all knobs at 0)")


if __name__ == '__main__':
    main()
