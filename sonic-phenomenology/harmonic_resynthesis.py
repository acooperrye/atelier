"""
HARMONIC RESYNTHESIS ENGINE
Rhythm Dictionary — D1 (Diagnostic Resynthesis)

Two modes:

  FRAME MODE (original):
    Per-frame peak picking → per-frame cosine synthesis.
    Fast. No phase continuity. Diagnostic of spectral content only.

  TRAJECTORY MODE (new):
    Peak picking → cross-frame trajectory linking → coherence grouping →
    phase-coherent oscillator synthesis. Slower. Phase-continuous.
    Produces trajectory map, residual, and diagnostic metrics.
    This is the D1 pipeline output.

Both modes read an audio file, measure its harmonic content, and rebuild
it from sinusoids. No neural networks, no models, no training data.

Usage:
    python harmonic_resynthesis.py <input_file> [options]

    Options:
        --mode MODE        "frame" (original) or "trajectory" (D1)
        --harmonics N      Number of harmonics to track (default: 16)
        --peaks N          Number of spectral peaks per frame (default: 30)
        --output PATH      Output file path (default: auto-generated)
        --sr RATE          Sample rate (default: 22050)
        --fft N            FFT size (default: 4096)
        --hop N            Hop length (default: 512)
        --residual         Also output residual (original - resynth)
        --ladder           Generate full quality ladder (frame mode)

Positioning:
    D1 in the architecture. Post-pipeline. Background. Does not compete
    for main analysis budget. Consumes Phase1Output (cached STFT) +
    Phase2 results. Feeds back to equipment registry, modifier log,
    percussion validation, research agenda. The monitoring bus.
"""

import numpy as np
import librosa
import soundfile as sf
from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter1d
import argparse
import os
import gc
import json
import warnings
warnings.filterwarnings('ignore')


# ═══════════════════════════════════════════════════════════════
# TRAJECTORY TRACKING
# ═══════════════════════════════════════════════════════════════

def _pick_peaks(spectrum, freqs, n_peaks, freq_res):
    """Pick the N strongest spectral peaks in a frame."""
    search_mask = (freqs >= 30) & (freqs <= freqs[-1] - 100)
    search_spec = spectrum.copy()
    search_spec[~search_mask] = 0

    if np.max(search_spec) < 1e-10:
        return np.array([]), np.array([]), np.array([])

    min_dist = max(1, int(20 / freq_res))
    peak_indices, _ = find_peaks(search_spec, height=np.max(search_spec) * 0.01,
                                  distance=min_dist)

    if len(peak_indices) == 0:
        return np.array([]), np.array([]), np.array([])

    peak_amps = spectrum[peak_indices]
    top_order = np.argsort(peak_amps)[::-1][:n_peaks]
    top_indices = peak_indices[top_order]

    return top_indices, freqs[top_indices], spectrum[top_indices]


def build_trajectories(S_mag, freqs, n_peaks, hop_length, sr,
                       freq_tolerance_hz=20.0, amp_tolerance_db=12.0,
                       min_duration_frames=3, verbose=True):
    """
    Link spectral peaks across frames into continuous trajectories.

    Each trajectory is a living peak: born when it first appears,
    tracked as it moves through frequency/amplitude space, dead
    when it disappears. The trajectory IS how the harmonic is
    being played — its frequency motion is pitch bends and vibrato,
    its amplitude envelope is the ADSR, its lifespan is the note.

    Parameters:
        S_mag:              STFT magnitude matrix (bins × frames)
        freqs:              Frequency array for STFT bins
        n_peaks:            Peaks to track per frame
        hop_length:         STFT hop in samples
        sr:                 Sample rate
        freq_tolerance_hz:  Max frequency drift per frame for linking
        amp_tolerance_db:   Max amplitude change per frame for linking
        min_duration_frames: Minimum trajectory length to keep
        verbose:            Print progress

    Returns:
        trajectories:       List of trajectory dicts
    """
    n_frames = S_mag.shape[1]
    freq_res = freqs[1] - freqs[0]
    frame_dur_ms = hop_length / sr * 1000

    if verbose:
        print(f"\n  Building trajectories...")
        print(f"    Tolerance: ±{freq_tolerance_hz}Hz freq, ±{amp_tolerance_db}dB amp")
        print(f"    Min duration: {min_duration_frames} frames ({min_duration_frames * frame_dur_ms:.0f}ms)")

    # Active trajectories (currently being tracked)
    active = []  # list of {id, frames, freqs, amps, bins}
    # Completed trajectories
    completed = []
    next_id = 0

    for fi in range(n_frames):
        spectrum = S_mag[:, fi]
        peak_bins, peak_freqs, peak_amps = _pick_peaks(spectrum, freqs, n_peaks, freq_res)

        if len(peak_bins) == 0:
            # Kill all active trajectories
            for traj in active:
                if len(traj['frames']) >= min_duration_frames:
                    completed.append(traj)
            active = []
            continue

        # Match active trajectories to current peaks
        matched_peaks = set()
        matched_trajs = set()

        if active:
            # Build cost matrix: frequency distance between each active
            # trajectory's last position and each current peak
            for ti, traj in enumerate(active):
                last_freq = traj['freqs'][-1]
                last_amp = traj['amps'][-1]

                # Find closest peak within tolerance
                freq_diffs = np.abs(peak_freqs - last_freq)
                amp_diffs_db = np.abs(20 * np.log10(
                    np.maximum(peak_amps, 1e-20) / max(last_amp, 1e-20)))

                # Candidates: within both tolerances
                candidates = np.where(
                    (freq_diffs <= freq_tolerance_hz) &
                    (amp_diffs_db <= amp_tolerance_db)
                )[0]

                if len(candidates) > 0:
                    # Pick the one with smallest frequency distance
                    best = candidates[np.argmin(freq_diffs[candidates])]
                    if best not in matched_peaks:
                        matched_peaks.add(best)
                        matched_trajs.add(ti)
                        traj['frames'].append(fi)
                        traj['freqs'].append(float(peak_freqs[best]))
                        traj['amps'].append(float(peak_amps[best]))
                        traj['bins'].append(int(peak_bins[best]))

        # Kill unmatched active trajectories
        new_active = []
        for ti, traj in enumerate(active):
            if ti in matched_trajs:
                new_active.append(traj)
            elif len(traj['frames']) >= min_duration_frames:
                completed.append(traj)
            # else: too short, discard

        # Birth new trajectories from unmatched peaks
        for pi in range(len(peak_bins)):
            if pi not in matched_peaks:
                new_active.append({
                    'id': next_id,
                    'frames': [fi],
                    'freqs': [float(peak_freqs[pi])],
                    'amps': [float(peak_amps[pi])],
                    'bins': [int(peak_bins[pi])],
                })
                next_id += 1

        active = new_active

        if verbose and fi % 1000 == 0 and fi > 0:
            pct = fi / n_frames * 100
            print(f"      {pct:.0f}% — {len(active)} active, {len(completed)} completed")

    # Finalize remaining active trajectories
    for traj in active:
        if len(traj['frames']) >= min_duration_frames:
            completed.append(traj)

    if verbose:
        print(f"    Done: {len(completed)} trajectories ({next_id} total peaks tracked)")
        durations = [len(t['frames']) * frame_dur_ms for t in completed]
        if durations:
            print(f"    Duration range: {min(durations):.0f}ms – {max(durations):.0f}ms "
                  f"(median {np.median(durations):.0f}ms)")

    return completed


def classify_trajectories(trajectories, hop_length, sr, verbose=True):
    """
    Classify each trajectory's onset, sustain, and offset character.
    This is the envelope classification from the D1 spec.

    Adds to each trajectory dict:
        onset_class:   "impulsive" | "fast" | "moderate" | "slow"
        sustain_class: "steady" | "decaying" | "modulated"
        offset_class:  "abrupt" | "gradual" | "gated"
        duration_ms:   total duration in milliseconds
        mean_freq_hz:  mean frequency across trajectory
        freq_drift_hz: total frequency drift (last - first)
    """
    frame_dur_ms = hop_length / sr * 1000

    for traj in trajectories:
        amps = np.array(traj['amps'])
        fqs = np.array(traj['freqs'])
        n = len(amps)
        traj['duration_ms'] = n * frame_dur_ms
        traj['mean_freq_hz'] = float(np.mean(fqs))
        traj['freq_drift_hz'] = float(fqs[-1] - fqs[0]) if n > 1 else 0.0

        if n < 3:
            traj['onset_class'] = 'impulsive'
            traj['sustain_class'] = 'decaying'
            traj['offset_class'] = 'abrupt'
            continue

        # Onset: how many frames to reach peak amplitude
        peak_idx = np.argmax(amps)
        onset_ms = peak_idx * frame_dur_ms

        if onset_ms < 5:
            traj['onset_class'] = 'impulsive'
        elif onset_ms < 20:
            traj['onset_class'] = 'fast'
        elif onset_ms < 100:
            traj['onset_class'] = 'moderate'
        else:
            traj['onset_class'] = 'slow'

        # Sustain: character of amplitude after peak
        if peak_idx < n - 2:
            sustain_amps = amps[peak_idx:]
            # Check for modulation (variance relative to trend)
            if len(sustain_amps) > 4:
                trend = np.polyval(np.polyfit(np.arange(len(sustain_amps)), sustain_amps, 1),
                                    np.arange(len(sustain_amps)))
                residual_var = np.var(sustain_amps - trend)
                trend_var = np.var(trend)
                if residual_var > 0.1 * trend_var and trend_var > 1e-20:
                    traj['sustain_class'] = 'modulated'
                elif sustain_amps[-1] < sustain_amps[0] * 0.5:
                    traj['sustain_class'] = 'decaying'
                else:
                    traj['sustain_class'] = 'steady'
            elif sustain_amps[-1] < sustain_amps[0] * 0.5:
                traj['sustain_class'] = 'decaying'
            else:
                traj['sustain_class'] = 'steady'
        else:
            traj['sustain_class'] = 'decaying'

        # Offset: how the trajectory ends
        if n >= 3:
            final_amps = amps[-3:]
            if final_amps[-1] < final_amps[0] * 0.1:
                traj['offset_class'] = 'abrupt'
            elif final_amps[-1] < final_amps[0] * 0.5:
                traj['offset_class'] = 'gradual'
            else:
                traj['offset_class'] = 'gated'
        else:
            traj['offset_class'] = 'abrupt'

    if verbose:
        onsets = {}
        for t in trajectories:
            c = t['onset_class']
            onsets[c] = onsets.get(c, 0) + 1
        print(f"\n  Onset classification: {onsets}")

    return trajectories


def group_coherent(trajectories, freq_ratio_tolerance=0.03, amp_corr_threshold=0.7,
                   verbose=True):
    """
    Group trajectories that move together (same source).

    Coherence criteria:
      - Frequency ratio is near-integer (harmonic relationship)
      - Amplitude envelopes correlate (rise and fall together)
      - Temporal overlap (exist during the same frames)

    Returns:
        groups: list of {group_id, trajectory_ids, fundamental_hz,
                         harmonic_coherence, envelope_shape}
    """
    if verbose:
        print(f"\n  Grouping coherent trajectories...")

    n = len(trajectories)
    if n == 0:
        return []

    # Build frame-overlap + frequency-ratio matrix for nearby trajectories
    assigned = set()
    groups = []
    group_id = 0

    # Sort by mean frequency for efficient pairing
    sorted_idx = sorted(range(n), key=lambda i: trajectories[i]['mean_freq_hz'])

    for si in range(n):
        i = sorted_idx[si]
        if i in assigned:
            continue

        t_i = trajectories[i]
        group_members = [i]
        assigned.add(i)
        fundamental = t_i['mean_freq_hz']

        # Look for harmonically related trajectories
        for sj in range(si + 1, n):
            j = sorted_idx[sj]
            if j in assigned:
                continue

            t_j = trajectories[j]

            # Check temporal overlap
            frames_i = set(t_i['frames'])
            frames_j = set(t_j['frames'])
            overlap = frames_i & frames_j
            if len(overlap) < 3:
                continue

            # Check harmonic relationship
            ratio = t_j['mean_freq_hz'] / fundamental
            nearest_int = round(ratio)
            if nearest_int < 1 or nearest_int > 20:
                continue
            if abs(ratio - nearest_int) / nearest_int > freq_ratio_tolerance:
                continue

            # Check amplitude correlation on overlapping frames
            overlap_sorted = sorted(overlap)
            amps_i = []
            amps_j = []
            for f in overlap_sorted:
                fi_idx = t_i['frames'].index(f) if f in t_i['frames'] else -1
                fj_idx = t_j['frames'].index(f) if f in t_j['frames'] else -1
                if fi_idx >= 0 and fj_idx >= 0:
                    amps_i.append(t_i['amps'][fi_idx])
                    amps_j.append(t_j['amps'][fj_idx])

            if len(amps_i) >= 3:
                corr = np.corrcoef(amps_i, amps_j)[0, 1]
                if not np.isnan(corr) and corr >= amp_corr_threshold:
                    group_members.append(j)
                    assigned.add(j)

        # Build group record
        member_trajs = [trajectories[m] for m in group_members]
        harm_ratios = [t['mean_freq_hz'] / fundamental for t in member_trajs]
        integer_errors = [abs(r - round(r)) for r in harm_ratios]
        harmonic_coherence = 1.0 - np.mean(integer_errors) if integer_errors else 1.0

        # Envelope shape from the fundamental trajectory
        onset = t_i.get('onset_class', 'unknown')
        sustain = t_i.get('sustain_class', 'unknown')
        offset = t_i.get('offset_class', 'unknown')

        groups.append({
            'group_id': group_id,
            'trajectory_ids': group_members,
            'fundamental_hz': float(fundamental),
            'harmonic_coherence': float(harmonic_coherence),
            'n_harmonics': len(group_members),
            'envelope_shape': f"{onset}/{sustain}/{offset}",
        })
        group_id += 1

    if verbose:
        print(f"    {len(groups)} coherence groups from {n} trajectories")
        sizes = [g['n_harmonics'] for g in groups]
        if sizes:
            print(f"    Group sizes: 1-partial={sizes.count(1)}, "
                  f"2-3={sum(1 for s in sizes if 2<=s<=3)}, "
                  f"4+={sum(1 for s in sizes if s>=4)}")

    return groups


# ═══════════════════════════════════════════════════════════════
# SYNTHESIS
# ═══════════════════════════════════════════════════════════════

def synthesize_from_trajectories(trajectories, n_samples, hop_length, sr, verbose=True):
    """
    Phase-coherent additive synthesis from trajectories.

    Instead of per-frame phase readings (which decorrelate),
    each trajectory maintains continuous phase:
        φ(t) = φ₀ + ∫ 2π·f(t)·dt

    This means the synthesized waveform has no inter-frame
    phase discontinuities. The phase evolves naturally from
    the frequency trajectory.
    """
    if verbose:
        print(f"\n  Synthesizing from {len(trajectories)} trajectories (phase-coherent)...")

    y = np.zeros(n_samples, dtype=np.float64)

    for ti, traj in enumerate(trajectories):
        frames = traj['frames']
        traj_freqs = np.array(traj['freqs'])
        traj_amps = np.array(traj['amps'])

        if len(frames) < 2:
            continue

        # Sample range this trajectory covers
        start_sample = frames[0] * hop_length
        end_sample = min((frames[-1] + 1) * hop_length, n_samples)
        n_traj_samples = end_sample - start_sample

        if n_traj_samples <= 0:
            continue

        # Interpolate frequency and amplitude to sample rate
        # Frame centers in samples
        frame_centers = np.array(frames) * hop_length + hop_length // 2
        # Map to trajectory-local sample indices
        local_centers = frame_centers - start_sample
        local_samples = np.arange(n_traj_samples)

        # Clamp interpolation range
        local_centers = np.clip(local_centers, 0, n_traj_samples - 1)

        freq_interp = np.interp(local_samples, local_centers, traj_freqs)
        amp_interp = np.interp(local_samples, local_centers, traj_amps)

        # Fade in/out to avoid clicks (2ms ramp)
        ramp_samples = min(int(0.002 * sr), n_traj_samples // 4)
        if ramp_samples > 0:
            amp_interp[:ramp_samples] *= np.linspace(0, 1, ramp_samples)
            amp_interp[-ramp_samples:] *= np.linspace(1, 0, ramp_samples)

        # Phase-coherent synthesis: integrate frequency
        # φ(t) = φ₀ + cumulative_sum(2π·f(t)·dt)
        dt = 1.0 / sr
        phase = np.cumsum(2 * np.pi * freq_interp * dt)

        # Synthesize
        signal = amp_interp * np.cos(phase)
        y[start_sample:end_sample] += signal

        if verbose and ti % 5000 == 0 and ti > 0:
            print(f"      {ti}/{len(trajectories)} trajectories rendered")

    if verbose:
        print(f"    Done: {len(trajectories)} trajectories rendered")

    return y


# ═══════════════════════════════════════════════════════════════
# MAIN ENTRY POINTS
# ═══════════════════════════════════════════════════════════════

def trajectory_resynth(input_path, output_path=None, n_peaks=40,
                       sr=22050, n_fft=4096, hop_length=512,
                       emit_residual=True, emit_trajectory_map=True,
                       verbose=True):
    """
    D1 Diagnostic Resynthesis — trajectory mode.

    Builds trajectories from STFT peaks, groups them by coherence,
    classifies envelopes, synthesizes with phase continuity,
    computes residual.

    Returns:
        y_resynth:      Phase-coherent resynthesized audio
        y_residual:     Original minus resynth (if emit_residual)
        trajectory_data: Full trajectory map (if emit_trajectory_map)
        stats:          Diagnostic metrics
    """
    if output_path is None:
        base = os.path.splitext(os.path.basename(input_path))[0]
        out_dir = os.path.dirname(input_path)
        output_path = os.path.join(out_dir, f"{base}_RESYNTH_trajectory.wav")

    if verbose:
        print("=" * 70)
        print("D1: DIAGNOSTIC RESYNTHESIS — TRAJECTORY MODE")
        print("=" * 70)

    # ── LOAD ──
    y, sr = librosa.load(input_path, sr=sr, mono=True)
    duration = len(y) / sr
    n_samples = len(y)

    if verbose:
        print(f"  Input:  {os.path.basename(input_path)}")
        print(f"  Length: {duration:.1f}s at {sr}Hz")

    # ── STFT ──
    S_complex = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_mag = np.abs(S_complex)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    freq_res = freqs[1] - freqs[0]

    del S_complex
    gc.collect()

    if verbose:
        print(f"  STFT:   {S_mag.shape[0]} bins × {S_mag.shape[1]} frames")

    # ── TRAJECTORIES ──
    trajectories = build_trajectories(
        S_mag, freqs, n_peaks, hop_length, sr, verbose=verbose)

    trajectories = classify_trajectories(
        trajectories, hop_length, sr, verbose=verbose)

    groups = group_coherent(trajectories, verbose=verbose)

    # ── SYNTHESIZE ──
    y_resynth = synthesize_from_trajectories(
        trajectories, n_samples, hop_length, sr, verbose=verbose)

    # ── NORMALISE ──
    orig_rms = np.sqrt(np.mean(y ** 2))
    resynth_rms = np.sqrt(np.mean(y_resynth ** 2))
    if resynth_rms > 1e-10:
        y_resynth = y_resynth * (orig_rms / resynth_rms)

    peak = np.max(np.abs(y_resynth))
    if peak > 0:
        y_resynth = y_resynth / peak * 0.9

    # ── RESIDUAL ──
    y_residual = None
    if emit_residual:
        y_residual = y - y_resynth
        if verbose:
            resid_rms = np.sqrt(np.mean(y_residual ** 2))
            print(f"\n  Residual RMS: {resid_rms:.4f} (original: {orig_rms:.4f})")
            print(f"  Capture ratio: {1.0 - resid_rms/orig_rms:.3f}" if orig_rms > 0 else "")

    # ── DIAGNOSTIC METRICS ──
    if verbose:
        print(f"\n  Diagnostic metrics:")

    # Waveform correlation (should be much higher with trajectory synthesis)
    window_size = int(0.05 * sr)
    n_check = 200
    check_indices = np.linspace(
        int(sr * 2), int(min(sr * (duration - 2), n_samples - window_size)),
        n_check, dtype=int)
    correlations = []
    for idx in check_indices:
        if idx + window_size > n_samples:
            continue
        o = y[idx:idx + window_size]
        r = y_resynth[idx:idx + window_size]
        if np.max(np.abs(o)) < 1e-10 or np.max(np.abs(r)) < 1e-10:
            continue
        corr = np.corrcoef(o / np.max(np.abs(o)), r / np.max(np.abs(r)))[0, 1]
        if not np.isnan(corr):
            correlations.append(corr)

    mean_corr = np.mean(correlations) if correlations else 0

    # Spectral similarity
    S_resynth = np.abs(librosa.stft(y_resynth, n_fft=n_fft, hop_length=hop_length))
    flat_len = min(100000, S_mag.flatten().shape[0], S_resynth.flatten().shape[0])
    spectral_corr = np.corrcoef(
        S_mag.flatten()[:flat_len], S_resynth.flatten()[:flat_len])[0, 1]

    if verbose:
        print(f"    Waveform correlation:  {mean_corr:.4f}")
        print(f"    Spectral correlation:  {spectral_corr:.4f}")
        print(f"    Trajectories:          {len(trajectories)}")
        print(f"    Coherence groups:      {len(groups)}")

    # ── EXPORT ──
    sf.write(output_path, y_resynth, sr)
    if verbose:
        print(f"\n  Output: {os.path.basename(output_path)}")

    if emit_residual and y_residual is not None:
        resid_path = output_path.replace('.wav', '_RESIDUAL.wav')
        sf.write(resid_path, y_residual, sr)
        if verbose:
            print(f"  Residual: {os.path.basename(resid_path)}")

    # ── TRAJECTORY MAP ──
    trajectory_data = None
    if emit_trajectory_map:
        trajectory_data = {
            'trajectories': [{
                'id': t['id'],
                'onset_frame': t['frames'][0],
                'offset_frame': t['frames'][-1],
                'duration_ms': t['duration_ms'],
                'mean_freq_hz': t['mean_freq_hz'],
                'freq_drift_hz': t['freq_drift_hz'],
                'onset_class': t['onset_class'],
                'sustain_class': t['sustain_class'],
                'offset_class': t['offset_class'],
                'n_frames': len(t['frames']),
            } for t in trajectories],
            'coherence_groups': groups,
            'summary': {
                'n_trajectories': len(trajectories),
                'n_groups': len(groups),
                'waveform_correlation': float(mean_corr),
                'spectral_correlation': float(spectral_corr),
            }
        }

        map_path = output_path.replace('.wav', '_MAP.json')
        with open(map_path, 'w') as f:
            json.dump(trajectory_data, f, indent=2)
        if verbose:
            print(f"  Map: {os.path.basename(map_path)}")

    if verbose:
        print("=" * 70)

    stats = {
        'duration': duration,
        'n_trajectories': len(trajectories),
        'n_groups': len(groups),
        'waveform_correlation': float(mean_corr),
        'spectral_correlation': float(spectral_corr),
    }

    del S_mag, S_resynth
    gc.collect()

    return y_resynth, y_residual, trajectory_data, stats


# ═══════════════════════════════════════════════════════════════
# ORIGINAL FRAME-BY-FRAME MODE (preserved)
# ═══════════════════════════════════════════════════════════════

def harmonic_resynth(input_path, output_path=None, n_harmonics=16, n_peaks=30,
                     sr=22050, n_fft=4096, hop_length=512, verbose=True):
    """
    Resynthesize an audio file from its harmonic content (frame mode).

    Original implementation: per-frame peak picking, per-frame cosine
    synthesis. Fast but no phase continuity. Useful for quick quality
    ladder comparisons.

    Parameters:
        input_path:     Path to input audio file
        output_path:    Path for output WAV (default: auto-generated)
        n_harmonics:    Harmonics per spectral peak (default: 16)
        n_peaks:        Spectral peaks to track per frame (default: 30)
        sr:             Sample rate (default: 22050)
        n_fft:          FFT size (default: 4096)
        hop_length:     STFT hop length (default: 512)
        verbose:        Print progress (default: True)

    Returns:
        y_resynth:      Resynthesized audio array
        sr:             Sample rate
        stats:          Dictionary of statistics
    """

    if output_path is None:
        base = os.path.splitext(os.path.basename(input_path))[0]
        out_dir = os.path.dirname(input_path)
        output_path = os.path.join(out_dir, f"{base}_RESYNTH_{n_peaks}p_{n_harmonics}h.wav")

    if verbose:
        print("=" * 70)
        print("HARMONIC RESYNTHESIS ENGINE (frame mode)")
        print("=" * 70)

    # ── LOAD ──
    y, sr = librosa.load(input_path, sr=sr, mono=True)
    duration = len(y) / sr
    if verbose:
        print(f"  Input:  {os.path.basename(input_path)}")
        print(f"  Length: {duration:.1f}s at {sr}Hz")
        print(f"  Config: {n_peaks} peaks × {n_harmonics} harmonics = {n_peaks * n_harmonics} sinusoids/frame")

    # ── STFT ──
    S_complex = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_mag = np.abs(S_complex)
    S_phase = np.angle(S_complex)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    n_frames = S_mag.shape[1]
    freq_res = freqs[1] - freqs[0]
    frame_dur = hop_length / sr

    del S_complex
    gc.collect()

    if verbose:
        print(f"  STFT:   {S_mag.shape[0]} bins × {n_frames} frames")
        print(f"  Resolution: {freq_res:.1f}Hz × {frame_dur*1000:.1f}ms")

    # ── MEASURE SPECTRAL PEAKS PER FRAME ──
    if verbose:
        print(f"\n  Measuring spectral peaks...")

    h_window = max(1, int(8 / freq_res))  # ±8Hz search window per harmonic

    # Pre-allocate the resynthesis buffer
    n_samples = len(y)
    y_resynth = np.zeros(n_samples, dtype=np.float64)

    # Progress tracking
    total_sinusoids = 0
    frames_processed = 0

    # Process frame by frame
    for fi in range(n_frames):
        spectrum = S_mag[:, fi]
        phase_spectrum = S_phase[:, fi]

        # Find the N strongest spectral peaks in this frame
        # Only search in musical range (30Hz to sr/2)
        search_mask = (freqs >= 30) & (freqs <= sr / 2 - 100)
        search_spec = spectrum.copy()
        search_spec[~search_mask] = 0

        if np.max(search_spec) < 1e-10:
            continue

        # Find peaks with minimum separation (~20Hz to avoid picking harmonics of same note)
        min_dist = max(1, int(20 / freq_res))
        peak_indices, peak_props = find_peaks(search_spec, height=np.max(search_spec) * 0.01,
                                                distance=min_dist)

        if len(peak_indices) == 0:
            continue

        # Sort by amplitude, take top N
        peak_amps = spectrum[peak_indices]
        top_order = np.argsort(peak_amps)[::-1][:n_peaks]
        top_peaks = peak_indices[top_order]

        # Sample range this frame covers
        frame_start = fi * hop_length
        frame_end = min((fi + 1) * hop_length, n_samples)
        if frame_start >= n_samples:
            break

        n_frame_samples = frame_end - frame_start
        t_abs = (frame_start + np.arange(n_frame_samples)) / sr
        frame_center_time = fi * hop_length / sr

        # For each spectral peak, synthesize its harmonics
        for peak_bin in top_peaks:
            f0 = freqs[peak_bin]
            if f0 < 30:
                continue

            for h in range(1, n_harmonics + 1):
                h_freq = f0 * h
                if h_freq > sr / 2 - 50:
                    break

                # Find the actual amplitude and phase at this harmonic
                h_bin = np.argmin(np.abs(freqs - h_freq))
                lo = max(0, h_bin - h_window)
                hi = min(len(freqs), h_bin + h_window + 1)

                local_peak = lo + np.argmax(spectrum[lo:hi])
                amp = spectrum[local_peak]
                phase = phase_spectrum[local_peak]

                if amp < 1e-10:
                    continue

                # For harmonics > 1, scale amplitude by 1/h to avoid
                # double-counting energy (the harmonic might also be
                # another peak's fundamental)
                if h > 1:
                    amp *= (1.0 / h)

                # Synthesize
                phase_at_samples = phase + 2 * np.pi * h_freq * (t_abs - frame_center_time)
                y_resynth[frame_start:frame_end] += amp * np.cos(phase_at_samples)
                total_sinusoids += 1

        frames_processed += 1

        if verbose and fi % 500 == 0 and fi > 0:
            pct = fi / n_frames * 100
            print(f"    {pct:.0f}% ({fi}/{n_frames} frames, {total_sinusoids} sinusoids so far)")

    if verbose:
        print(f"    100% — {total_sinusoids} total sinusoids across {frames_processed} frames")
        avg_per_frame = total_sinusoids / max(1, frames_processed)
        print(f"    Average: {avg_per_frame:.0f} sinusoids per frame")

    # ── NORMALISE ──
    # Match RMS of original
    orig_rms = np.sqrt(np.mean(y ** 2))
    resynth_rms = np.sqrt(np.mean(y_resynth ** 2))

    if resynth_rms > 1e-10:
        y_resynth = y_resynth * (orig_rms / resynth_rms)

    # Peak normalise to 0.9
    peak = np.max(np.abs(y_resynth))
    if peak > 0:
        y_resynth = y_resynth / peak * 0.9

    # ── QUALITY METRICS ──
    if verbose:
        print(f"\n  Quality metrics:")

    # Waveform correlation
    window_size = int(0.05 * sr)
    n_check = 200
    check_indices = np.linspace(int(sr * 2), int(min(sr * (duration - 2), len(y) - window_size)),
                                 n_check, dtype=int)
    correlations = []
    for idx in check_indices:
        if idx + window_size > len(y):
            continue
        o = y[idx:idx + window_size]
        r = y_resynth[idx:idx + window_size]
        if np.max(np.abs(o)) < 1e-10 or np.max(np.abs(r)) < 1e-10:
            continue
        corr = np.corrcoef(o / np.max(np.abs(o)), r / np.max(np.abs(r)))[0, 1]
        if not np.isnan(corr):
            correlations.append(corr)

    mean_corr = np.mean(correlations) if correlations else 0

    # Spectral similarity (compare STFT magnitudes)
    S_resynth = np.abs(librosa.stft(y_resynth, n_fft=n_fft, hop_length=hop_length))
    spectral_corr = np.corrcoef(S_mag.flatten()[:100000], S_resynth.flatten()[:100000])[0, 1]
    del S_resynth

    if verbose:
        print(f"    Waveform correlation: {mean_corr:.4f}")
        print(f"    Spectral correlation: {spectral_corr:.4f}")

    # ── EXPORT ──
    sf.write(output_path, y_resynth, sr)

    if verbose:
        print(f"\n  Output: {os.path.basename(output_path)}")
        print(f"  Size:   {os.path.getsize(output_path) / 1024 / 1024:.1f}MB")
        print("=" * 70)

    stats = {
        'duration': duration,
        'n_frames': n_frames,
        'n_peaks': n_peaks,
        'n_harmonics': n_harmonics,
        'total_sinusoids': total_sinusoids,
        'avg_sinusoids_per_frame': total_sinusoids / max(1, frames_processed),
        'waveform_correlation': mean_corr,
        'spectral_correlation': float(spectral_corr),
    }

    del S_mag, S_phase
    gc.collect()

    return y_resynth, sr, stats


def multi_resynth(input_path, output_dir=None, sr=22050, verbose=True):
    """
    Generate multiple resynthesis at different fidelity levels.
    Useful for hearing how the reconstruction builds up from sparse to dense.
    """

    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    base = os.path.splitext(os.path.basename(input_path))[0]

    configs = [
        (3,   4,  "ghost"),       # 12 sinusoids/frame — bare skeleton
        (5,   8,  "sketch"),      # 40 sinusoids — recognisable outline
        (10, 12,  "draft"),       # 120 sinusoids — clearly the song
        (20, 16,  "clear"),       # 320 sinusoids — high fidelity
        (40, 16,  "hifi"),        # 640 sinusoids — near-original
    ]

    results = []

    for n_peaks, n_harmonics, label in configs:
        out_path = os.path.join(output_dir, f"{base}_RESYNTH_{label}.wav")

        if verbose:
            print(f"\n{'─' * 70}")
            print(f"  Config: {label} ({n_peaks}p × {n_harmonics}h = {n_peaks * n_harmonics}/frame)")
            print(f"{'─' * 70}")

        _, _, stats = harmonic_resynth(
            input_path, out_path,
            n_harmonics=n_harmonics, n_peaks=n_peaks,
            sr=sr, verbose=verbose
        )
        stats['label'] = label
        results.append(stats)

    # Summary table
    if verbose:
        print(f"\n{'=' * 70}")
        print(f"RESYNTHESIS QUALITY LADDER")
        print(f"{'=' * 70}")
        print(f"\n  {'Label':<8s} {'Peaks':<7s} {'Harm':<6s} {'Sin/frame':<11s} {'Waveform r':<12s} {'Spectral r':<12s}")
        print(f"  {'─'*8} {'─'*7} {'─'*6} {'─'*11} {'─'*12} {'─'*12}")

        for s in results:
            print(f"  {s['label']:<8s} {s['n_peaks']:<7d} {s['n_harmonics']:<6d} "
                  f"{s['avg_sinusoids_per_frame']:<11.0f} "
                  f"{s['waveform_correlation']:<12.4f} "
                  f"{s['spectral_correlation']:<12.4f}")

    return results


# ── CLI ──
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="D1: Diagnostic Resynthesis Engine")
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("--mode", type=str, default="frame",
                        choices=["frame", "trajectory"],
                        help="Synthesis mode: 'frame' (original) or 'trajectory' (D1)")
    parser.add_argument("--harmonics", type=int, default=16, help="Harmonics per peak (frame mode)")
    parser.add_argument("--peaks", type=int, default=30, help="Spectral peaks per frame")
    parser.add_argument("--output", type=str, default=None, help="Output path")
    parser.add_argument("--sr", type=int, default=22050, help="Sample rate")
    parser.add_argument("--fft", type=int, default=4096, help="FFT size")
    parser.add_argument("--hop", type=int, default=512, help="Hop length")
    parser.add_argument("--residual", action="store_true", help="Output residual (trajectory mode)")
    parser.add_argument("--ladder", action="store_true", help="Generate full quality ladder (frame mode)")

    args = parser.parse_args()

    if args.ladder:
        multi_resynth(args.input, sr=args.sr)
    elif args.mode == "trajectory":
        trajectory_resynth(
            args.input, args.output,
            n_peaks=args.peaks, sr=args.sr,
            n_fft=args.fft, hop_length=args.hop,
            emit_residual=args.residual
        )
    else:
        harmonic_resynth(
            args.input, args.output,
            n_harmonics=args.harmonics, n_peaks=args.peaks,
            sr=args.sr, n_fft=args.fft, hop_length=args.hop
        )
