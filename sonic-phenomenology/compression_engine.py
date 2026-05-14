"""
compression_engine.py — Compression Vector & Spectral Fingerprint Engine

Two complementary approaches for identifying sounds via their compression behavior:

1. COMPRESSION VECTOR ENGINE
   - Builds transfer functions from a bitrate ladder (pure → most distorted)
   - Each sound's compression behavior defines a unique vector in metric space
   - Unknown sounds are identified by projecting onto known reference vectors
   - Works on FULL MIXES (captures aggregate spectral behavior)

2. SPECTRAL CEILING / QUANTIZATION NOISE DETECTOR  
   - Detects hard frequency cutoffs from 1980s hardware samplers
   - Identifies 8-bit vs 12-bit machines via Nyquist ceiling and noise floor
   - Works on ISOLATED SAMPLES (individual hits, clean recordings)
   
Usage:
    from compression_engine import CompressionVectorEngine, SpectralCeilingDetector
    
    # Build a reference vector from a bitrate ladder
    engine = CompressionVectorEngine()
    engine.add_reference('808_kick', {320: metrics_320, 120: metrics_120, ...})
    
    # Identify an unknown sound
    match, confidence, position = engine.identify(unknown_metrics)
    
    # Detect hardware sampler ceiling in an isolated sample
    detector = SpectralCeilingDetector()
    result = detector.analyze('/path/to/sample.wav')
"""
import numpy as np
import json
import os

# Metrics used for compression vectoring — discriminative only (>5% change across ladder)
VECTOR_METRICS = [
    'centroid_mean', 'treble_pct', 'flatness_mean', 'flatness_min',
    'zcr_mean', 'onset_count', 'rms_mean',
    'mfcc_0', 'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5',
    'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12'
]

# Machine specifications for spectral ceiling detection
MACHINE_SPECS = {
    'E-mu Drumulator':    {'bits': 8,  'sr': 28000, 'nyquist': 14000, 'noise_floor_db': -48},
    'LinnDrum LM-2':      {'bits': 8,  'sr': 28000, 'nyquist': 14000, 'noise_floor_db': -48},
    'Fairlight CMI I/II': {'bits': 8,  'sr': 16000, 'nyquist': 8000,  'noise_floor_db': -48},
    'Oberheim DMX':       {'bits': 8,  'sr': 28000, 'nyquist': 14000, 'noise_floor_db': -48},
    'Yamaha DX7':         {'bits': 12, 'sr': 49100, 'nyquist': 24550, 'noise_floor_db': -72},
    'E-mu Emulator':      {'bits': 8,  'sr': 28000, 'nyquist': 14000, 'noise_floor_db': -48},
    'Fairlight CMI III':  {'bits': 16, 'sr': 44100, 'nyquist': 22050, 'noise_floor_db': -96},
    'Akai S900':          {'bits': 12, 'sr': 40000, 'nyquist': 20000, 'noise_floor_db': -72},
}


class CompressionVectorEngine:
    """
    Compression Vector Engine.
    
    Key insight (from Alex Cooper-Rye, 2026-02-09):
    Each sound's compression behavior defines a characteristic vector from
    PURE (highest quality) to MOST DISTORTED (lowest quality). The dictionary
    needs only the two endpoints and the vector relationship. Any variant
    of the sound falls somewhere on that vector.
    
    The position on the vector tells you the COMPRESSION LEVEL.
    The distance from the vector tells you the MATCH CONFIDENCE.
    """
    
    def __init__(self):
        self.references = {}  # name → {pure_vector, distorted_vector, direction, magnitude, transfer_functions}
    
    def extract_metrics_from_audio(self, filepath, sr_target=22050, offset=None, duration=None):
        """Extract the VECTOR_METRICS from an audio file."""
        import librosa
        
        kwargs = {'sr': sr_target, 'mono': True}
        if offset is not None:
            kwargs['offset'] = offset
        if duration is not None:
            kwargs['duration'] = duration
        
        y, sr = librosa.load(filepath, **kwargs)
        results = {}
        
        # Spectral
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        results['centroid_mean'] = float(np.mean(spec_centroid))
        
        spec_flat = librosa.feature.spectral_flatness(y=y)[0]
        results['flatness_mean'] = float(np.mean(spec_flat))
        results['flatness_min'] = float(np.min(spec_flat))
        
        zcr = librosa.feature.zero_crossing_rate(y=y)[0]
        results['zcr_mean'] = float(np.mean(zcr))
        
        rms = librosa.feature.rms(y=y)[0]
        results['rms_mean'] = float(np.mean(rms))
        
        # Band balance
        S = np.abs(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr)
        total_e = float(np.sum(S**2))
        results['treble_pct'] = float(np.sum(S[freqs >= 4000]**2) / total_e * 100)
        
        # MFCCs
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        for i in range(13):
            results[f'mfcc_{i}'] = float(np.mean(mfcc[i]))
        
        # Onsets
        onsets = librosa.onset.onset_detect(y=y, sr=sr)
        results['onset_count'] = int(len(onsets))
        
        return results
    
    def add_reference_from_ladder(self, name, ladder_data):
        """
        Add a reference sound from a bitrate ladder.
        
        ladder_data: dict of {bitrate_kbps: metrics_dict}
            e.g. {320: {...}, 120: {...}, 96: {...}, 64: {...}, 48: {...}, 32: {...}, 16: {...}}
        """
        bitrates = sorted(ladder_data.keys(), reverse=True)
        pure_br = bitrates[0]   # highest quality
        dist_br = bitrates[-1]  # lowest quality
        
        # Build vectors
        pure_vector = np.array([ladder_data[pure_br].get(m, 0.0) for m in VECTOR_METRICS])
        dist_vector = np.array([ladder_data[dist_br].get(m, 0.0) for m in VECTOR_METRICS])
        
        direction = dist_vector - pure_vector
        magnitude = np.linalg.norm(direction)
        unit = direction / (magnitude + 1e-20)
        
        # Build per-metric transfer functions
        transfer_functions = {}
        for m in VECTOR_METRICS:
            pure_val = ladder_data[pure_br].get(m, 0.0)
            if abs(pure_val) < 1e-10:
                continue
            
            trajectory = []
            for br in bitrates:
                val = ladder_data[br].get(m, 0.0)
                trajectory.append({
                    'bitrate': br,
                    'value': val,
                    'normalized': val / pure_val
                })
            
            transfer_functions[m] = {
                'pure': pure_val,
                'distorted': ladder_data[dist_br].get(m, 0.0),
                'trajectory': trajectory,
                'total_delta_pct': abs(trajectory[-1]['normalized'] - 1.0) * 100
            }
        
        self.references[name] = {
            'pure_vector': pure_vector,
            'distorted_vector': dist_vector,
            'direction': direction,
            'unit': unit,
            'magnitude': magnitude,
            'transfer_functions': transfer_functions,
            'bitrates': bitrates,
        }
        
        return {
            'name': name,
            'magnitude': float(magnitude),
            'n_metrics': len(transfer_functions),
            'bitrates': bitrates,
        }
    
    def identify(self, unknown_metrics):
        """
        Identify an unknown sound by projecting it onto reference vectors.
        
        Returns list of (name, confidence, position) sorted by confidence (best first).
        - name: reference sound name
        - confidence: 0-1, where 1 = perfect match (low residual)
        - position: 0 = at pure endpoint, 1 = at distorted endpoint
        """
        unknown = np.array([unknown_metrics.get(m, 0.0) for m in VECTOR_METRICS])
        
        results = []
        for name, ref in self.references.items():
            # Project unknown onto the reference's compression line
            displacement = unknown - ref['pure_vector']
            projection_scalar = np.dot(displacement, ref['unit'])
            position = projection_scalar / (ref['magnitude'] + 1e-20)
            
            # Residual: distance from the line
            projected_point = ref['pure_vector'] + projection_scalar * ref['unit']
            residual = np.linalg.norm(unknown - projected_point)
            
            # Confidence: inverse of residual normalized by magnitude
            # A residual of 0 = perfect match, residual = magnitude = no match
            confidence = max(0.0, 1.0 - residual / (ref['magnitude'] + 1e-20))
            
            results.append({
                'name': name,
                'confidence': float(confidence),
                'position': float(position),
                'residual': float(residual),
                'residual_pct': float(residual / (ref['magnitude'] + 1e-20) * 100),
            })
        
        return sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    def compare_transfer_functions(self, name_a, name_b):
        """
        Compare the transfer function shapes of two reference sounds.
        Returns per-metric similarity scores.
        """
        ref_a = self.references[name_a]
        ref_b = self.references[name_b]
        
        comparisons = []
        for m in VECTOR_METRICS:
            if m in ref_a['transfer_functions'] and m in ref_b['transfer_functions']:
                tf_a = ref_a['transfer_functions'][m]
                tf_b = ref_b['transfer_functions'][m]
                
                normed_a = [t['normalized'] for t in tf_a['trajectory']]
                normed_b = [t['normalized'] for t in tf_b['trajectory']]
                
                # Shape similarity: cosine similarity of normalized trajectories
                a = np.array(normed_a)
                b = np.array(normed_b[:len(a)])
                
                cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-20)
                
                comparisons.append({
                    'metric': m,
                    'cosine_similarity': float(cos_sim),
                    'delta_a': tf_a['total_delta_pct'],
                    'delta_b': tf_b['total_delta_pct'],
                })
        
        return comparisons
    
    def save(self, filepath):
        """Save engine state to JSON."""
        state = {}
        for name, ref in self.references.items():
            state[name] = {
                'pure_vector': ref['pure_vector'].tolist(),
                'distorted_vector': ref['distorted_vector'].tolist(),
                'direction': ref['direction'].tolist(),
                'magnitude': float(ref['magnitude']),
                'bitrates': ref['bitrates'],
                'transfer_functions': ref['transfer_functions'],
            }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load(self, filepath):
        """Load engine state from JSON."""
        with open(filepath) as f:
            state = json.load(f)
        for name, data in state.items():
            data['pure_vector'] = np.array(data['pure_vector'])
            data['distorted_vector'] = np.array(data['distorted_vector'])
            data['direction'] = np.array(data['direction'])
            data['unit'] = data['direction'] / (data['magnitude'] + 1e-20)
            self.references[name] = data


class SpectralCeilingDetector:
    """
    Spectral Ceiling & Quantization Noise Detector.
    
    Identifies 1980s hardware samplers by their fixed compression signatures:
    - Spectral ceiling (Nyquist frequency of the DAC)
    - Quantization noise floor (bit depth of the DAC)
    - Aliasing artifacts (folded energy above Nyquist)
    
    For ISOLATED SAMPLES: use analyze() directly — ceiling is visible.
    For FULL MIXES: use analyze_in_mix() — applies two-axis subtraction:
      Vertical: MID channel isolates center-panned percussion from edge content
      Horizontal: sustained synth bed estimated from pre-onset windows is subtracted
    What remains is the transient contribution of the target machine alone.

    Validated on Shout (Tears for Fears, 1985): Drumulator 14kHz ceiling detected
    as -3.8dB dip + 69.9 dB/kHz cliff at 14,812 Hz after subtraction, invisible
    before subtraction due to synth cloaking (120% energy masking below 14kHz).
    """
    
    def __init__(self):
        self.machines = MACHINE_SPECS
    
    def analyze(self, filepath_or_array, sr=None, sr_analysis=48000):
        """
        Analyze an audio file or array for hardware sampler signatures.
        
        Returns:
            dict with detected ceiling, noise floor, aliasing evidence,
            and best-match machine.
        """
        import librosa
        from scipy.ndimage import uniform_filter1d
        
        if isinstance(filepath_or_array, str):
            y, sr = librosa.load(filepath_or_array, sr=sr_analysis, mono=True)
        else:
            y = filepath_or_array
            if sr is None:
                raise ValueError("Must provide sr when passing array")
        
        # High-resolution spectrum
        n_fft = 8192
        S = np.abs(librosa.stft(y, n_fft=n_fft))**2
        freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
        mean_power = np.mean(S, axis=1)
        mean_power_db = 10 * np.log10(mean_power + 1e-20)
        
        results = {}
        
        # 1. Spectral ceiling detection
        peak_db = np.max(mean_power_db)
        cliff_thresholds = [20, 30, 40]  # dB below peak
        for thresh in cliff_thresholds:
            cliff_level = peak_db - thresh
            cliff_freq = None
            for i in range(len(freqs)-1, 0, -1):
                if mean_power_db[i] > cliff_level:
                    cliff_freq = float(freqs[i])
                    break
            results[f'ceiling_{thresh}dB'] = cliff_freq
        
        # 2. Gradient analysis — find steepest spectral drops
        smoothed = uniform_filter1d(mean_power_db, size=30)
        freq_step = freqs[1] - freqs[0]
        gradient = np.diff(smoothed) / (freq_step / 1000)
        
        steepest_drops = []
        for lo, hi in [(6000, 10000), (12000, 16000), (17000, 22000)]:
            mask = (freqs[:-1] >= lo) & (freqs[:-1] < hi)
            if np.any(mask):
                idx = np.argmin(gradient[mask])
                steepest_drops.append({
                    'range': f'{lo/1000:.0f}-{hi/1000:.0f}kHz',
                    'gradient_db_per_khz': float(gradient[mask][idx]),
                    'frequency': float(freqs[:-1][mask][idx]),
                })
        results['steepest_drops'] = steepest_drops
        
        # 3. Noise floor estimation
        rms_frames = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        if len(rms_frames) > 10:
            # Use quietest 10% of frames
            quiet_threshold = np.percentile(rms_frames, 10)
            quiet_mask = rms_frames < quiet_threshold
            quiet_indices = np.where(quiet_mask)[0]
            
            if len(quiet_indices) > 0:
                quiet_frames = []
                for qi in quiet_indices[:20]:  # sample up to 20 quiet frames
                    start = qi * 512
                    if start + 2048 < len(y):
                        frame = y[start:start+2048]
                        quiet_frames.append(frame)
                
                if quiet_frames:
                    quiet_signal = np.concatenate(quiet_frames)
                    quiet_S = np.abs(np.fft.rfft(quiet_signal))**2
                    quiet_db = 10 * np.log10(np.mean(quiet_S) + 1e-20)
                    results['noise_floor_db'] = float(quiet_db)
        
        # 4. Machine matching
        matches = []
        for machine, specs in self.machines.items():
            score = 0
            reasons = []
            
            # Check spectral ceiling alignment
            ceiling_30 = results.get('ceiling_30dB')
            if ceiling_30:
                ceiling_diff = abs(ceiling_30 - specs['nyquist'])
                if ceiling_diff < 1000:
                    score += 3
                    reasons.append(f"ceiling match ({ceiling_30:.0f} vs {specs['nyquist']})")
                elif ceiling_diff < 2000:
                    score += 1
                    reasons.append(f"ceiling near ({ceiling_30:.0f} vs {specs['nyquist']})")
            
            # Check steep drops near expected Nyquist
            for drop in steepest_drops:
                if abs(drop['frequency'] - specs['nyquist']) < 2000:
                    if drop['gradient_db_per_khz'] < -20:
                        score += 2
                        reasons.append(f"steep drop near Nyquist ({drop['frequency']:.0f}Hz)")
            
            # Check noise floor
            noise = results.get('noise_floor_db')
            if noise:
                noise_diff = abs(noise - specs['noise_floor_db'])
                if noise_diff < 6:
                    score += 2
                    reasons.append(f"noise floor match ({noise:.0f} vs {specs['noise_floor_db']})")
                elif noise_diff < 12:
                    score += 1
                    reasons.append(f"noise floor near ({noise:.0f} vs {specs['noise_floor_db']})")
            
            matches.append({
                'machine': machine,
                'score': score,
                'specs': specs,
                'reasons': reasons,
            })
        
        results['matches'] = sorted(matches, key=lambda x: x['score'], reverse=True)
        
        return results
    
    def analyze_percussion_band(self, filepath, sr_analysis=48000, offset=10, duration=60):
        """
        Isolate percussion via HPSS and analyze for sampler signatures.
        More effective than full-mix analysis for drum machine identification.
        """
        import librosa
        
        y, sr = librosa.load(filepath, sr=sr_analysis, mono=True, offset=offset, duration=duration)
        y_harm, y_perc = librosa.effects.hpss(y, margin=3.0)
        
        full_results = self.analyze(y, sr=sr)
        perc_results = self.analyze(y_perc, sr=sr)
        
        return {
            'full_mix': full_results,
            'percussion_only': perc_results,
            'percussion_ratio': float(np.sum(y_perc**2) / (np.sum(y**2) + 1e-20) * 100),
        }


    def analyze_in_mix(self, filepath, sr_analysis=48000, offset=10, duration=60,
                        beat_phase='backbeat', pre_onset_ms=180, window_ms=80,
                        subtraction_factor=1.0):
        """
        Two-axis subtraction method for detecting sampler ceilings in full mixes.

        Validated on Shout (Tears for Fears, 1985).

        Axis 1 (Vertical/Spatial): Use MID channel to isolate center-panned content
        (kick, snare) from edge content (hi-hats, bells, cowbell).

        Axis 2 (Horizontal/Temporal): Estimate the sustained synth bed from a window
        BEFORE each beat hit. Subtract it from the beat window. What remains is the
        transient contribution of the drum machine alone.

        Args:
            filepath: path to audio file
            sr_analysis: sample rate for analysis (48000 recommended for ceiling detection)
            offset: seconds to skip from start
            duration: seconds to analyze
            beat_phase: 'backbeat' = snare on 2&4, 'downbeat' = kick on 1&3, 'all' = every beat
            pre_onset_ms: how far before the beat to sample the synth bed (ms)
            window_ms: duration of each beat window (ms)
            subtraction_factor: aggressiveness of synth removal (1.0 = full)

        Returns:
            dict with raw spectrum, synth bed spectrum, residual spectrum,
            ceiling analysis, cloaking analysis, and machine matches.
        """
        import librosa
        from scipy.ndimage import uniform_filter1d

        y, sr = librosa.load(filepath, sr=sr_analysis, mono=False,
                             offset=offset, duration=duration)

        if y.ndim == 1:
            mid = y
        else:
            left, right = y[0], y[1]
            mid = (left + right) / 2

        # Beat tracking
        tempo, beats = librosa.beat.beat_track(y=mid, sr=sr)
        beat_samples = librosa.frames_to_samples(beats)

        # Select beats by phase
        if beat_phase == 'backbeat':
            target_beats = beat_samples[1::2]
        elif beat_phase == 'downbeat':
            target_beats = beat_samples[0::2]
        else:
            target_beats = beat_samples

        window_samples = int(sr * window_ms / 1000)
        pre_offset_samples = int(sr * pre_onset_ms / 1000)
        n_fft = 4096

        hit_spectra = []
        bed_spectra = []
        residual_spectra = []

        for tb in target_beats:
            if tb + window_samples >= len(mid) or tb - pre_offset_samples < 0:
                continue

            hit_seg = mid[tb:tb + window_samples]
            bed_seg = mid[tb - pre_offset_samples:tb - pre_offset_samples + window_samples]

            win = np.hanning(window_samples)
            S_hit = np.abs(np.fft.rfft(hit_seg * win, n=n_fft))**2
            S_bed = np.abs(np.fft.rfft(bed_seg * win, n=n_fft))**2

            S_residual = np.maximum(S_hit - subtraction_factor * S_bed, 1e-20)

            hit_spectra.append(S_hit)
            bed_spectra.append(S_bed)
            residual_spectra.append(S_residual)

        if not residual_spectra:
            return {'error': 'No valid beat windows found'}

        hit_avg = np.mean(hit_spectra, axis=0)
        bed_avg = np.mean(bed_spectra, axis=0)
        residual_avg = np.mean(residual_spectra, axis=0)

        residual_db = 10 * np.log10(residual_avg + 1e-20)
        freqs = np.linspace(0, sr / 2, len(residual_avg))

        # Gradient analysis on residual
        smoothed = uniform_filter1d(residual_db, size=15)
        freq_step = freqs[1] - freqs[0]
        gradient = np.diff(smoothed) / (freq_step / 1000)

        # Find steepest drops in machine-ceiling zones
        ceiling_candidates = []
        for lo, hi, label in [(6000, 10000, 'Fairlight zone'),
                               (12000, 16000, '8-bit/28kHz zone'),
                               (17000, 21000, 'MP3/high-res zone')]:
            mask = (freqs[:-1] >= lo) & (freqs[:-1] < hi)
            if np.any(mask):
                steepest = float(np.min(gradient[mask]))
                steepest_freq = float(freqs[:-1][mask][np.argmin(gradient[mask])])
                ceiling_candidates.append({
                    'zone': label,
                    'gradient_db_per_khz': steepest,
                    'frequency': steepest_freq,
                })

        # Cloaking analysis: what % of beat-window energy was synth bed?
        cloaking = {}
        for target_hz in [10000, 12000, 13000, 14000, 15000, 16000, 18000, 20000]:
            idx = np.argmin(np.abs(freqs - target_hz))
            lo_i = max(0, idx - 2)
            hi_i = min(len(hit_avg), idx + 3)

            hit_e = float(np.mean(hit_avg[lo_i:hi_i]))
            bed_e = float(np.mean(bed_avg[lo_i:hi_i]))

            cloaking[f'{target_hz}Hz'] = {
                'synth_pct': bed_e / (hit_e + 1e-20) * 100,
                'transient_pct': max(0, (hit_e - bed_e)) / (hit_e + 1e-20) * 100,
            }

        # Machine matching on residual
        residual_results = self.analyze(
            np.fft.irfft(np.sqrt(residual_avg)), sr=sr
        )

        return {
            'n_windows': len(residual_spectra),
            'beat_phase': beat_phase,
            'tempo': float(np.atleast_1d(tempo)[0]),
            'ceiling_candidates': ceiling_candidates,
            'cloaking': cloaking,
            'machine_matches': residual_results.get('matches', []),
            'residual_db': residual_db.tolist(),
            'freqs': freqs.tolist(),
        }


if __name__ == '__main__':
    print("Compression Engine loaded. Available classes:")
    print("  CompressionVectorEngine - for full-mix compression vector identification")
    print("  SpectralCeilingDetector  - for isolated sample machine identification")
    print(f"\nVector metrics ({len(VECTOR_METRICS)}): {', '.join(VECTOR_METRICS)}")
    print(f"Known machines ({len(MACHINE_SPECS)}): {', '.join(MACHINE_SPECS.keys())}")
