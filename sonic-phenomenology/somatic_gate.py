"""
SOMATIC GATE MODEL
==================
The body as a threshold detector.

For a given song, compute:
1. Which frequency bands cross from "heard" to "felt" first as SPL increases
2. Do they cross alone (isolated penetration) or together (broadband)
3. The spectral shape of penetration — the song's physical signature

Replaces the tissue displacement model with a simpler, more useful approach.
"""

import numpy as np
import librosa
import scipy.signal as sig
import json
import sys
import glob

# Perception thresholds by frequency band (dB SPL at which band becomes FELT)
# Based on vibrotactile research and whole-body vibration standards
# Lower = easier to feel. Sub-bass is felt at lower SPL than highs.
GATE_THRESHOLDS_DB = {
    'sub_bass':  85,   # 20-80Hz — felt earliest (chest, organs)
    'bass':      95,   # 80-250Hz — felt via bone conduction, seat
    'low_mid':   105,  # 250-500Hz — transitional
    'mid':       110,  # 500-2kHz — mainly surface/skin at extreme SPL
    'hi_mid':    115,  # 2-8kHz — surface pain before feeling
    'high':      120,  # 8kHz+ — rarely felt, airborne
}

# Band definitions
BANDS = [
    ('sub_bass', 20, 80),
    ('bass', 80, 250),
    ('low_mid', 250, 500),
    ('mid', 500, 2000),
    ('hi_mid', 2000, 8000),
    ('high', 8000, 20000),
]


def compute_band_energies(filepath, sr=22050):
    """Compute energy in each frequency band for a song."""

    y, sr = librosa.load(filepath, sr=sr, mono=True)
    duration = len(y) / sr

    results = {}
    total_energy = np.sum(y**2) / len(y)
    total_rms_db = 10 * np.log10(total_energy + 1e-10)

    for name, low, high in BANDS:
        high_actual = min(high, sr/2 - 1)
        if low >= high_actual:
            results[name] = {'rms_db': -100, 'fraction': 0, 'relative_db': -100}
            continue

        sos = sig.butter(4, [low, high_actual], btype='band', fs=sr, output='sos')
        y_band = sig.sosfilt(sos, y)

        band_energy = np.sum(y_band**2) / len(y_band)
        band_rms_db = 10 * np.log10(band_energy + 1e-10)
        fraction = band_energy / (total_energy + 1e-10)

        results[name] = {
            'rms_db': float(band_rms_db),
            'fraction': float(fraction),
            'relative_db': float(band_rms_db - total_rms_db),
        }

    return results, total_rms_db, duration


def compute_transient_isolation(filepath, sr=22050):
    """
    Measure how much transients stick out above the sustained bed in each band.
    High isolation = something engineered to HIT.
    Low isolation = broadband, nothing meant to punch through.
    """
    y, sr = librosa.load(filepath, sr=sr, mono=True)

    results = {}

    for name, low, high in BANDS:
        high_actual = min(high, sr/2 - 1)
        if low >= high_actual:
            results[name] = {'transient_ratio_db': 0, 'crest_factor_db': 0}
            continue

        sos = sig.butter(4, [low, high_actual], btype='band', fs=sr, output='sos')
        y_band = sig.sosfilt(sos, y)

        # Crest factor: peak / RMS (how much transients exceed average)
        rms = np.sqrt(np.mean(y_band**2))
        peak = np.max(np.abs(y_band))
        if rms > 0:
            crest_db = 20 * np.log10(peak / rms)
        else:
            crest_db = 0

        # Onset strength in this band
        onset_env = librosa.onset.onset_strength(y=y_band, sr=sr)
        if len(onset_env) > 0 and np.mean(onset_env) > 0:
            onset_ratio = np.max(onset_env) / np.mean(onset_env)
        else:
            onset_ratio = 1.0

        results[name] = {
            'crest_factor_db': float(crest_db),
            'onset_peak_ratio': float(onset_ratio),
        }

    return results


def somatic_gate_analysis(filepath, playback_spl=108, label='Unknown'):
    """
    Full somatic gate analysis for a song.

    playback_spl: estimated SPL at listener position (dB)
    """
    print(f"\n{'=' * 70}")
    print(f"SOMATIC GATE ANALYSIS: {label}")
    print(f"{'=' * 70}")

    # Step 1: Band energies
    band_energies, total_rms_db, duration = compute_band_energies(filepath)

    print(f"\n  Duration: {duration:.1f}s")
    print(f"  Total RMS: {total_rms_db:.1f}dB (relative)")

    # Step 2: What each band's SPL would be at playback volume
    # The playback_spl is the total SPL. Each band gets a fraction.
    print(f"\n  BAND ENERGIES AT {playback_spl}dB PLAYBACK:")
    print(f"  {'Band':<12} {'Share':>8} {'SPL at vol':>10} {'Gate threshold':>15} {'Headroom':>10} {'Status':>12}")
    print(f"  {'-'*12} {'-'*8} {'-'*10} {'-'*15} {'-'*10} {'-'*12}")

    gate_results = {}
    for name, _, _ in BANDS:
        be = band_energies[name]
        # Band SPL = total SPL + relative dB of this band
        band_spl = playback_spl + be['relative_db']
        gate = GATE_THRESHOLDS_DB[name]
        headroom = band_spl - gate  # positive = above gate = FELT

        status = 'FELT (strong)' if headroom > 10 else 'FELT' if headroom > 0 else 'heard' if headroom > -10 else 'faint'

        print(f"  {name:<12} {be['fraction']*100:>7.1f}% {band_spl:>9.1f}dB {gate:>14d}dB {headroom:>+9.1f}dB {status:>12}")

        gate_results[name] = {
            'band_spl': float(band_spl),
            'gate_threshold': gate,
            'headroom_db': float(headroom),
            'above_gate': headroom > 0,
            'energy_fraction': float(be['fraction']),
        }

    # Step 3: Order of penetration (which band crosses first as volume increases)
    print(f"\n  ORDER OF PENETRATION (first to cross gate as volume increases):")

    # For each band, find what total SPL would cause it to cross
    crossing_spls = {}
    for name, _, _ in BANDS:
        be = band_energies[name]
        gate = GATE_THRESHOLDS_DB[name]
        # band_spl = total_spl + relative_db = gate at crossing
        # total_spl = gate - relative_db
        crossing_spl = gate - be['relative_db']
        crossing_spls[name] = crossing_spl

    sorted_crossings = sorted(crossing_spls.items(), key=lambda x: x[1])

    first_crossing = sorted_crossings[0][1]
    for i, (name, spl) in enumerate(sorted_crossings):
        gap = spl - first_crossing
        marker = '◄ FIRST' if i == 0 else f'+{gap:.1f}dB' if gap < 15 else 'distant'
        print(f"    {i+1}. {name:<12} crosses at total SPL {spl:.1f}dB  {marker}")

    # Step 4: Isolation vs broadband
    print(f"\n  PENETRATION SHAPE:")
    crossings = [s for _, s in sorted_crossings]
    spread = crossings[-1] - crossings[0]  # dB range between first and last crossing
    top3_spread = crossings[2] - crossings[0] if len(crossings) > 2 else crossings[-1] - crossings[0]

    if top3_spread < 5:
        shape = 'BROADBAND — multiple bands cross together. Nothing engineered to hit alone. Intimacy/closeness.'
    elif top3_spread < 12:
        shape = 'MODERATE ISOLATION — lead band crosses first but others follow soon. Focused but not surgical.'
    else:
        shape = 'SHARP ISOLATION — one band punches through well before others. Engineered to HIT.'

    print(f"    Spread (first to last): {spread:.1f}dB")
    print(f"    Spread (first 3): {top3_spread:.1f}dB")
    print(f"    Shape: {shape}")

    # Step 5: Transient isolation
    print(f"\n  TRANSIENT ISOLATION (do individual hits stick out above the bed?):")
    transients = compute_transient_isolation(filepath)
    for name, _, _ in BANDS:
        t = transients[name]
        isolation = 'SHARP HIT' if t['crest_factor_db'] > 15 else 'punchy' if t['crest_factor_db'] > 10 else 'blended'
        print(f"    {name:<12} crest: {t['crest_factor_db']:>6.1f}dB  onset ratio: {t['onset_peak_ratio']:>6.1f}x  → {isolation}")

    # Step 6: Somatic prediction
    print(f"\n  SOMATIC PREDICTION:")

    above_gate = [name for name in gate_results if gate_results[name]['above_gate']]
    first_band = sorted_crossings[0][0]

    if len(above_gate) == 0:
        print(f"    At {playback_spl}dB: NOTHING crosses the gate. Sound only, no physical sensation.")
    elif len(above_gate) == 1:
        print(f"    At {playback_spl}dB: ONLY {above_gate[0]} crosses the gate.")
        print(f"    → Isolated physical sensation in {above_gate[0]} range only.")
    else:
        print(f"    At {playback_spl}dB: {', '.join(above_gate)} cross the gate.")
        if top3_spread < 5:
            print(f"    → Broadband physical sensation. Immersive, intimate, 'all there at once.'")
        else:
            print(f"    → {first_band} leads. Physical sensation dominated by {first_band}, others present but secondary.")

    # Transient shape
    max_crest_band = max(transients.items(), key=lambda x: x[1]['crest_factor_db'])
    if max_crest_band[1]['crest_factor_db'] > 15 and max_crest_band[0] in above_gate:
        print(f"    → {max_crest_band[0]} has SHARP transients ({max_crest_band[1]['crest_factor_db']:.1f}dB crest).")
        print(f"      These will be felt as IMPACTS/CUTS, not continuous vibration.")
    elif all(transients[name]['crest_factor_db'] < 10 for name, _, _ in BANDS):
        print(f"    → No sharp transients in any band. Physical sensation is CONTINUOUS/SUSTAINED.")
    else:
        print(f"    → Mixed transient profile. Some bands hit, others sustain.")

    return {
        'gate_results': gate_results,
        'crossing_order': sorted_crossings,
        'penetration_spread_db': float(spread),
        'top3_spread_db': float(top3_spread),
        'transients': {k: v for k, v in transients.items()},
    }


if __name__ == '__main__':
    audio_dir = '/sessions/cool-zealous-ride/mnt/Rhythm Dictionary Cowork/audio'

    # Find all our analysis tracks
    tracks = {
        'PUTP': f'{audio_dir}/pick_up_the_phone.mp3',
        'Shout': f'{audio_dir}/Shout - Tears for Fears.mp3',
        'Blade Runner': f'{audio_dir}/blade_runner_main_titles.mp3',
    }

    all_results = {}
    for label, path in tracks.items():
        try:
            results = somatic_gate_analysis(path, playback_spl=108, label=label)
            all_results[label] = results
        except Exception as e:
            print(f"Error analyzing {label}: {e}")

    # Comparison
    print(f"\n\n{'=' * 70}")
    print("CROSS-SONG SOMATIC GATE COMPARISON")
    print(f"{'=' * 70}")

    print(f"\n  {'Song':<20} {'First to penetrate':<18} {'Spread (top 3)':>15} {'Shape':>20}")
    print(f"  {'-'*20} {'-'*18} {'-'*15} {'-'*20}")
    for label in tracks:
        if label in all_results:
            r = all_results[label]
            first = r['crossing_order'][0][0]
            spread = r['top3_spread_db']
            shape = 'ISOLATED' if spread > 12 else 'MODERATE' if spread > 5 else 'BROADBAND'
            print(f"  {label:<20} {first:<18} {spread:>14.1f}dB {shape:>20}")

    # Save
    with open('/sessions/cool-zealous-ride/somatic_gate_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n  Results saved to somatic_gate_results.json")
