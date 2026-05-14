"""
Equipment Identification Engine
Rhythm Dictionary â€” Phase A Module

PURPOSE: Given raw audio, identify what MADE each sound.
Sits between spectral roster (role identification) and full extraction.

PRIORITY ORDER:
1. Programmed vs Organic (the "too clean" detector)
2. Synthesis family (FM / analog subtractive / sample-based / wavetable)
3. Drum machine vs live drums
4. Composite source detection (multiple sources per audible element)

DESIGN PRINCIPLE: Synths and programmed drums go first because:
- They dominate modern music
- They have the clearest signatures (mathematical perfection IS the fingerprint)
- They mask other instruments (patches on/off, not gradual)
- When replicating natural instruments, they betray themselves through
  mathematically clean velocities, exposures, and envelope shapes
"""

import numpy as np
import librosa
from scipy import signal as scipy_signal
from scipy.stats import kurtosis
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from enum import Enum


# ============================================================
# DATA STRUCTURES
# ============================================================

class SynthesisFamily(Enum):
    FM = "fm_synthesis"
    ANALOG_SUBTRACTIVE = "analog_subtractive"
    SAMPLE_BASED = "sample_based"
    WAVETABLE = "wavetable"
    ACOUSTIC = "acoustic"
    UNKNOWN = "unknown"


class SourceType(Enum):
    PROGRAMMED = "programmed"      # machine-triggered, sequenced
    ORGANIC = "organic"            # human-performed
    HYBRID = "hybrid"              # human source through machine playback (e.g., Fairlight sampled guitar)
    UNKNOWN = "unknown"


class DrumType(Enum):
    DRUM_MACHINE = "drum_machine"
    LIVE_DRUMS = "live_drums"
    HYBRID_DRUMS = "hybrid_drums"  # e.g., live drums triggered through sampler
    UNKNOWN = "unknown"


@dataclass
class TransientProfile:
    """Extracted from a single onset/hit."""
    onset_time: float
    attack_ms: float
    decay_ms: float
    spectral_centroid: float
    spectral_spread: float
    peak_amplitude: float
    harmonic_ratio: float          # energy in harmonic vs inharmonic partials


@dataclass
class RepetitionAnalysis:
    """How identical are repeated events in a spectral region?"""
    n_events: int
    centroid_cv: float             # coefficient of variation across hits
    amplitude_cv: float
    attack_cv: float
    decay_cv: float
    spectral_correlation_mean: float  # mean pairwise correlation of spectral shapes
    spectral_correlation_std: float
    is_programmed: bool
    confidence: float
    evidence: str


@dataclass
class HarmonicAnalysis:
    """Harmonic structure of a sustained sound."""
    fundamental_hz: float
    n_partials_detected: int
    integer_ratio_score: float     # 1.0 = all partials at integer multiples (acoustic/subtractive)
    sideband_energy: float         # energy at non-integer positions (FM indicator)
    odd_harmonic_bias: float       # ratio of odd to even harmonics (square wave indicator)
    spectral_rolloff_slope: float  # dB/octave above fundamental (filter indicator)
    aliasing_score: float          # energy above Nyquist/2 fold-back zone (sampler indicator)
    drift_hz: float                # pitch instability over time (analog indicator)


@dataclass
class SynthesisClassification:
    """Result of synthesis family classification for one spectral region."""
    role: str                      # from Phase A role taxonomy
    family: SynthesisFamily
    confidence: float
    evidence: List[str]
    harmonic_analysis: Optional[HarmonicAnalysis] = None
    alternative: Optional[SynthesisFamily] = None
    alternative_confidence: float = 0.0


@dataclass
class DrumClassification:
    """Result of drum source classification."""
    drum_type: DrumType
    confidence: float
    evidence: List[str]
    kick_profile: Optional[RepetitionAnalysis] = None
    snare_profile: Optional[RepetitionAnalysis] = None
    hihat_profile: Optional[RepetitionAnalysis] = None


@dataclass
class CompositeSourceEvidence:
    """Evidence that an audible element is actually multiple blended sources."""
    role: str
    is_composite: bool
    confidence: float
    evidence: List[str]
    estimated_n_sources: int
    spectral_discontinuities: int  # frequency bands where envelope behavior changes


@dataclass
class EquipmentReport:
    """Full output of the equipment identification engine."""
    source_type: SourceType
    source_confidence: float
    synthesis_classifications: List[SynthesisClassification]
    drum_classification: Optional[DrumClassification]
    composite_evidence: List[CompositeSourceEvidence]
    overall_programmed_score: float   # 0.0 = fully organic, 1.0 = fully programmed
    summary: str


# ============================================================
# CORE DETECTORS
# ============================================================

class TooCleanDetector:
    """
    The fundamental discriminator: is this sound programmed or organic?
    
    Programmed sources betray themselves through mathematical perfection:
    - Identical transients on repeated hits (no performance variation)
    - Mathematically precise velocities (no human dynamics)
    - Clean envelope shapes (no breath, no finger noise, no room)
    - Zero pitch drift between notes (crystal-locked oscillators)
    - Identical note durations (quantized note-off)
    
    This runs FIRST because it's the broadest, cheapest test and it
    gates everything else: if a region is organic, we skip synthesis
    family classification entirely.
    """
    
    # Thresholds calibrated from EWTRTW analysis
    # Programmed sources show CV < these values
    CENTROID_CV_THRESHOLD = 0.03    # spectral shape variation across hits
    AMPLITUDE_CV_THRESHOLD = 0.05   # velocity variation
    ATTACK_CV_THRESHOLD = 0.08      # attack time variation
    SPECTRAL_CORR_THRESHOLD = 0.95  # pairwise spectral correlation
    
    @staticmethod
    def extract_transient_profiles(
        y: np.ndarray, 
        sr: int,
        onset_frames: np.ndarray,
        window_ms: float = 100.0
    ) -> List[TransientProfile]:
        """Extract spectral/temporal profile for each onset."""
        profiles = []
        window_samples = int(sr * window_ms / 1000)
        
        for frame in onset_frames:
            sample_idx = librosa.frames_to_samples(frame)
            if sample_idx + window_samples > len(y):
                continue
            
            segment = y[sample_idx:sample_idx + window_samples]
            if np.max(np.abs(segment)) < 1e-6:
                continue
            
            # Attack time: samples from onset to peak
            peak_idx = np.argmax(np.abs(segment))
            attack_ms = (peak_idx / sr) * 1000
            
            # Decay time: samples from peak to -6dB
            peak_val = np.abs(segment[peak_idx])
            decay_threshold = peak_val * 0.5  # -6dB
            decay_samples = 0
            for i in range(peak_idx, len(segment)):
                if np.abs(segment[i]) < decay_threshold:
                    decay_samples = i - peak_idx
                    break
            decay_ms = (decay_samples / sr) * 1000
            
            # Spectral features of this hit
            S = np.abs(librosa.stft(segment, n_fft=min(2048, len(segment))))
            if S.shape[1] == 0:
                continue
            
            freqs = librosa.fft_frequencies(sr=sr, n_fft=min(2048, len(segment)))
            mag = np.mean(S, axis=1)
            
            if np.sum(mag) < 1e-10:
                continue
            
            centroid = np.sum(freqs * mag) / np.sum(mag)
            spread = np.sqrt(np.sum(((freqs - centroid) ** 2) * mag) / np.sum(mag))
            
            # Harmonic ratio (energy at harmonic vs inharmonic frequencies)
            # Simplified: use harmonic-to-noise ratio
            try:
                harmonic, percussive = librosa.effects.hpss(segment)
                h_energy = np.sum(harmonic ** 2)
                total_energy = np.sum(segment ** 2)
                harm_ratio = h_energy / total_energy if total_energy > 0 else 0
            except:
                harm_ratio = 0.5
            
            profiles.append(TransientProfile(
                onset_time=librosa.frames_to_time(frame, sr=sr),
                attack_ms=attack_ms,
                decay_ms=decay_ms,
                spectral_centroid=centroid,
                spectral_spread=spread,
                peak_amplitude=float(peak_val),
                harmonic_ratio=harm_ratio
            ))
        
        return profiles
    
    @staticmethod
    def analyze_repetition(profiles: List[TransientProfile]) -> RepetitionAnalysis:
        """
        Given transient profiles from repeated events in the same spectral region,
        measure how identical they are. Low variation = programmed.
        """
        if len(profiles) < 4:
            return RepetitionAnalysis(
                n_events=len(profiles),
                centroid_cv=0, amplitude_cv=0, attack_cv=0, decay_cv=0,
                spectral_correlation_mean=0, spectral_correlation_std=0,
                is_programmed=False, confidence=0.0,
                evidence="Insufficient events for analysis"
            )
        
        centroids = np.array([p.spectral_centroid for p in profiles])
        amplitudes = np.array([p.peak_amplitude for p in profiles])
        attacks = np.array([p.attack_ms for p in profiles])
        decays = np.array([p.decay_ms for p in profiles])
        
        def cv(arr):
            """Coefficient of variation, handling zero mean."""
            m = np.mean(arr)
            if m < 1e-10:
                return 0.0
            return float(np.std(arr) / m)
        
        centroid_cv = cv(centroids)
        amplitude_cv = cv(amplitudes)
        attack_cv = cv(attacks)
        decay_cv = cv(decays[decays > 0]) if np.any(decays > 0) else 0.0
        
        # Programmed score: how many indicators below threshold
        indicators = [
            centroid_cv < TooCleanDetector.CENTROID_CV_THRESHOLD,
            amplitude_cv < TooCleanDetector.AMPLITUDE_CV_THRESHOLD,
            attack_cv < TooCleanDetector.ATTACK_CV_THRESHOLD,
        ]
        
        programmed_score = sum(indicators) / len(indicators)
        
        evidence_parts = []
        if centroid_cv < TooCleanDetector.CENTROID_CV_THRESHOLD:
            evidence_parts.append(f"spectral shape CV={centroid_cv:.4f} (below {TooCleanDetector.CENTROID_CV_THRESHOLD} threshold)")
        if amplitude_cv < TooCleanDetector.AMPLITUDE_CV_THRESHOLD:
            evidence_parts.append(f"velocity CV={amplitude_cv:.4f} (below {TooCleanDetector.AMPLITUDE_CV_THRESHOLD} threshold)")
        if attack_cv < TooCleanDetector.ATTACK_CV_THRESHOLD:
            evidence_parts.append(f"attack CV={attack_cv:.4f} (below {TooCleanDetector.ATTACK_CV_THRESHOLD} threshold)")
        
        is_programmed = programmed_score >= 0.66  # 2/3 indicators
        confidence = programmed_score
        
        if not evidence_parts:
            evidence_parts.append("No programmed indicators detected â€” likely organic source")
        
        return RepetitionAnalysis(
            n_events=len(profiles),
            centroid_cv=centroid_cv,
            amplitude_cv=amplitude_cv,
            attack_cv=attack_cv,
            decay_cv=decay_cv,
            spectral_correlation_mean=0.0,  # computed separately if needed
            spectral_correlation_std=0.0,
            is_programmed=is_programmed,
            confidence=confidence,
            evidence="; ".join(evidence_parts)
        )


class SynthesisFamilyClassifier:
    """
    Given a sustained sound region, classify which synthesis family produced it.
    
    The physics:
    - FM synthesis: energy at carrier Â± nÃ—modulator frequencies (non-integer partial ratios)
    - Analog subtractive: integer harmonics shaped by filter rolloff
    - Sample-based: inherits source spectrum + aliasing artifacts from low bit depth
    - Wavetable: spectral stepping (discrete changes between wave shapes)
    
    Key insight: these leave DIFFERENT harmonic structures that are measurable
    with standard spectral analysis. The hard part is extracting them from a mix.
    """
    
    @staticmethod
    def analyze_harmonics(
        y: np.ndarray, 
        sr: int,
        min_freq: float = 50.0,
        max_freq: float = 8000.0
    ) -> HarmonicAnalysis:
        """
        Extract harmonic structure from a segment of audio.
        Works best on relatively isolated sounds or frequency-banded regions.
        """
        # Estimate fundamental
        f0_candidates = librosa.yin(y, fmin=min_freq, fmax=max_freq, sr=sr)
        f0_candidates = f0_candidates[f0_candidates > 0]
        
        if len(f0_candidates) == 0:
            return HarmonicAnalysis(
                fundamental_hz=0, n_partials_detected=0,
                integer_ratio_score=0, sideband_energy=0,
                odd_harmonic_bias=0.5, spectral_rolloff_slope=0,
                aliasing_score=0, drift_hz=0
            )
        
        f0 = float(np.median(f0_candidates))
        drift = float(np.std(f0_candidates))
        
        # Get spectrum
        S = np.abs(librosa.stft(y, n_fft=4096))
        mag = np.mean(S, axis=1)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)
        
        if np.max(mag) < 1e-10:
            return HarmonicAnalysis(
                fundamental_hz=f0, n_partials_detected=0,
                integer_ratio_score=0, sideband_energy=0,
                odd_harmonic_bias=0.5, spectral_rolloff_slope=0,
                aliasing_score=0, drift_hz=drift
            )
        
        # Find peaks in spectrum
        peak_indices, properties = scipy_signal.find_peaks(
            mag, height=np.max(mag) * 0.01, distance=int(f0 / (sr / 4096) * 0.5)
        )
        
        if len(peak_indices) == 0:
            return HarmonicAnalysis(
                fundamental_hz=f0, n_partials_detected=0,
                integer_ratio_score=0, sideband_energy=0,
                odd_harmonic_bias=0.5, spectral_rolloff_slope=0,
                aliasing_score=0, drift_hz=drift
            )
        
        peak_freqs = freqs[peak_indices]
        peak_mags = mag[peak_indices]
        
        # Classify each peak: is it at an integer multiple of f0?
        integer_energy = 0.0
        non_integer_energy = 0.0
        odd_energy = 0.0
        even_energy = 0.0
        n_partials = 0
        
        tolerance = f0 * 0.03  # 3% tolerance for "integer multiple"
        
        for freq, m in zip(peak_freqs, peak_mags):
            if freq < f0 * 0.5:
                continue
            ratio = freq / f0
            nearest_int = round(ratio)
            deviation = abs(ratio - nearest_int) * f0
            
            energy = float(m ** 2)
            
            if deviation < tolerance and nearest_int > 0:
                integer_energy += energy
                n_partials += 1
                if nearest_int % 2 == 1:
                    odd_energy += energy
                else:
                    even_energy += energy
            else:
                non_integer_energy += energy
        
        total_peak_energy = integer_energy + non_integer_energy
        integer_ratio_score = integer_energy / total_peak_energy if total_peak_energy > 0 else 0
        sideband_energy = non_integer_energy / total_peak_energy if total_peak_energy > 0 else 0
        
        total_harmonic = odd_energy + even_energy
        odd_bias = odd_energy / total_harmonic if total_harmonic > 0 else 0.5
        
        # Spectral rolloff slope (dB/octave above fundamental)
        # Fit a line to the peak magnitudes vs frequency in log space
        if n_partials >= 3:
            log_freqs = np.log2(peak_freqs[peak_freqs > f0] / f0 + 1e-10)
            log_mags = 20 * np.log10(peak_mags[peak_freqs > f0] + 1e-10)
            if len(log_freqs) >= 2:
                slope = float(np.polyfit(log_freqs[:min(10, len(log_freqs))], 
                                        log_mags[:min(10, len(log_mags))], 1)[0])
            else:
                slope = 0.0
        else:
            slope = 0.0
        
        # Aliasing score: energy above sr/4 relative to total
        # 8-bit samplers at ~28kHz create aliasing that folds back
        nyquist_quarter = sr / 4
        high_energy = float(np.sum(mag[freqs > nyquist_quarter] ** 2))
        total_energy = float(np.sum(mag ** 2))
        aliasing = high_energy / total_energy if total_energy > 0 else 0
        
        return HarmonicAnalysis(
            fundamental_hz=f0,
            n_partials_detected=n_partials,
            integer_ratio_score=integer_ratio_score,
            sideband_energy=sideband_energy,
            odd_harmonic_bias=odd_bias,
            spectral_rolloff_slope=slope,
            aliasing_score=aliasing,
            drift_hz=drift
        )
    
    @staticmethod
    def classify(analysis: HarmonicAnalysis) -> Tuple[SynthesisFamily, float, List[str]]:
        """
        Given harmonic analysis, classify synthesis family.
        Returns (family, confidence, evidence_list).
        """
        scores = {
            SynthesisFamily.FM: 0.0,
            SynthesisFamily.ANALOG_SUBTRACTIVE: 0.0,
            SynthesisFamily.SAMPLE_BASED: 0.0,
            SynthesisFamily.WAVETABLE: 0.0,
            SynthesisFamily.ACOUSTIC: 0.0,
        }
        evidence = []
        
        # === FM INDICATORS ===
        # High sideband energy (non-integer partials)
        if analysis.sideband_energy > 0.25:
            scores[SynthesisFamily.FM] += 0.4
            evidence.append(f"FM: sideband energy {analysis.sideband_energy:.2f} (>0.25 threshold)")
        
        # Many partials with non-integer relationships
        if analysis.sideband_energy > 0.15 and analysis.n_partials_detected > 8:
            scores[SynthesisFamily.FM] += 0.2
            evidence.append(f"FM: {analysis.n_partials_detected} partials with non-integer content")
        
        # Low pitch drift (digital oscillator)
        if analysis.drift_hz < 0.5 and analysis.fundamental_hz > 0:
            drift_ratio = analysis.drift_hz / analysis.fundamental_hz
            if drift_ratio < 0.002:
                scores[SynthesisFamily.FM] += 0.1
                evidence.append(f"FM: crystal-stable pitch (drift ratio {drift_ratio:.4f})")
        
        # === ANALOG SUBTRACTIVE INDICATORS ===
        # High integer ratio score (harmonics at integer multiples)
        if analysis.integer_ratio_score > 0.85:
            scores[SynthesisFamily.ANALOG_SUBTRACTIVE] += 0.3
            evidence.append(f"Analog: integer ratio {analysis.integer_ratio_score:.2f} (>0.85)")
        
        # Smooth spectral rolloff (filter characteristic)
        if analysis.spectral_rolloff_slope < -6.0:  # steeper than -6dB/oct
            scores[SynthesisFamily.ANALOG_SUBTRACTIVE] += 0.2
            evidence.append(f"Analog: filter rolloff {analysis.spectral_rolloff_slope:.1f} dB/oct")
        
        # Measurable pitch drift (analog oscillator instability)
        if analysis.drift_hz > 1.0 and analysis.fundamental_hz > 0:
            drift_ratio = analysis.drift_hz / analysis.fundamental_hz
            if 0.002 < drift_ratio < 0.02:
                scores[SynthesisFamily.ANALOG_SUBTRACTIVE] += 0.2
                evidence.append(f"Analog: oscillator drift {analysis.drift_hz:.2f}Hz (ratio {drift_ratio:.4f})")
        
        # High odd-harmonic bias (pulse/square wave indicator)
        if analysis.odd_harmonic_bias > 0.7:
            scores[SynthesisFamily.ANALOG_SUBTRACTIVE] += 0.15
            evidence.append(f"Analog: odd harmonic bias {analysis.odd_harmonic_bias:.2f} (pulse/square)")
        
        # === SAMPLE-BASED INDICATORS ===
        # High aliasing score
        if analysis.aliasing_score > 0.02:
            scores[SynthesisFamily.SAMPLE_BASED] += 0.3
            evidence.append(f"Sample: aliasing score {analysis.aliasing_score:.4f} (>0.02)")
        
        # Integer harmonics (inherited from acoustic source) BUT with aliasing
        if analysis.integer_ratio_score > 0.7 and analysis.aliasing_score > 0.01:
            scores[SynthesisFamily.SAMPLE_BASED] += 0.2
            evidence.append("Sample: acoustic harmonics + aliasing = sampled acoustic source")
        
        # === WAVETABLE INDICATORS ===
        # Moderate sideband energy (less than FM, more than subtractive)
        if 0.1 < analysis.sideband_energy < 0.25:
            scores[SynthesisFamily.WAVETABLE] += 0.2
            evidence.append(f"Wavetable: moderate sideband energy {analysis.sideband_energy:.2f}")
        
        # Low drift (digital) but with non-standard harmonic content
        if analysis.drift_hz < 0.5 and 0.5 < analysis.integer_ratio_score < 0.85:
            scores[SynthesisFamily.WAVETABLE] += 0.2
            evidence.append("Wavetable: digital stability with mixed harmonic content")
        
        # === ACOUSTIC INDICATORS ===
        # High integer ratio + significant drift + no aliasing
        if (analysis.integer_ratio_score > 0.8 and 
            analysis.drift_hz > 0.5 and 
            analysis.aliasing_score < 0.005):
            scores[SynthesisFamily.ACOUSTIC] += 0.4
            evidence.append("Acoustic: integer harmonics + natural drift + no aliasing")
        
        # Get winner
        best_family = max(scores, key=scores.get)
        best_score = scores[best_family]
        
        # Normalize to confidence
        total = sum(scores.values())
        confidence = best_score / total if total > 0 else 0
        
        if best_score < 0.15:
            return SynthesisFamily.UNKNOWN, 0.0, ["Insufficient evidence for classification"]
        
        return best_family, confidence, evidence


class DrumClassifier:
    """
    Classify whether drums are machine-programmed or live-performed.
    
    The core insight: drum machines trigger identical samples every time.
    A human drummer NEVER hits identically twice â€” there's always variation
    in timing, velocity, stick angle, and therefore spectral content.
    
    This variation is measurable as the coefficient of variation across
    repeated hits of the same drum type.
    """
    
    @staticmethod
    def isolate_drum_hits(
        y: np.ndarray, 
        sr: int,
        low_band: Tuple[float, float] = (30, 200),     # kick
        mid_band: Tuple[float, float] = (200, 3000),    # snare
        high_band: Tuple[float, float] = (3000, 16000),  # hihat
    ) -> Dict[str, np.ndarray]:
        """
        Separate audio into frequency bands corresponding to drum roles.
        Returns band-filtered signals.
        """
        bands = {}
        
        for name, (low, high) in [("kick", low_band), ("snare", mid_band), ("hihat", high_band)]:
            # Bandpass filter
            nyq = sr / 2
            low_norm = max(low / nyq, 0.001)
            high_norm = min(high / nyq, 0.999)
            
            if low_norm >= high_norm:
                bands[name] = np.zeros_like(y)
                continue
            
            try:
                b, a = scipy_signal.butter(4, [low_norm, high_norm], btype='band')
                filtered = scipy_signal.filtfilt(b, a, y)
                bands[name] = filtered
            except:
                bands[name] = np.zeros_like(y)
        
        return bands
    
    @staticmethod
    def classify_drums(
        y: np.ndarray, 
        sr: int,
        detector: TooCleanDetector
    ) -> DrumClassification:
        """
        Full drum classification pipeline.
        """
        bands = DrumClassifier.isolate_drum_hits(y, sr)
        
        results = {}
        evidence = []
        programmed_count = 0
        organic_count = 0
        total_analyzed = 0
        
        for band_name, band_signal in bands.items():
            # Detect onsets in this band
            onset_env = librosa.onset.onset_strength(y=band_signal, sr=sr)
            onsets = librosa.onset.onset_detect(
                onset_envelope=onset_env, sr=sr, 
                backtrack=True, units='frames'
            )
            
            if len(onsets) < 6:
                evidence.append(f"{band_name}: too few onsets ({len(onsets)}) for analysis")
                continue
            
            # Extract transient profiles
            profiles = detector.extract_transient_profiles(band_signal, sr, onsets)
            
            if len(profiles) < 4:
                continue
            
            # Analyze repetition consistency
            rep = detector.analyze_repetition(profiles)
            results[band_name] = rep
            total_analyzed += 1
            
            if rep.is_programmed:
                programmed_count += 1
                evidence.append(
                    f"{band_name}: PROGRAMMED â€” {rep.evidence}"
                )
            else:
                organic_count += 1
                evidence.append(
                    f"{band_name}: ORGANIC â€” {rep.evidence}"
                )
        
        if total_analyzed == 0:
            return DrumClassification(
                drum_type=DrumType.UNKNOWN,
                confidence=0.0,
                evidence=["No drum bands had sufficient onsets for analysis"],
                kick_profile=results.get("kick"),
                snare_profile=results.get("snare"),
                hihat_profile=results.get("hihat")
            )
        
        programmed_ratio = programmed_count / total_analyzed
        
        if programmed_ratio >= 0.66:
            dtype = DrumType.DRUM_MACHINE
            conf = programmed_ratio
        elif programmed_ratio <= 0.33:
            dtype = DrumType.LIVE_DRUMS
            conf = 1.0 - programmed_ratio
        else:
            dtype = DrumType.HYBRID_DRUMS
            conf = 0.5
        
        return DrumClassification(
            drum_type=dtype,
            confidence=conf,
            evidence=evidence,
            kick_profile=results.get("kick"),
            snare_profile=results.get("snare"),
            hihat_profile=results.get("hihat")
        )


class CompositeSourceDetector:
    """
    Detect whether an audible element is actually multiple blended sources.
    
    The EWTRTW insight: when every sound is a composite of two+ sources,
    each spectrally incomplete alone, the production literally hides things
    inside other things. This is detectable:
    
    1. Different envelope behaviors in different frequency bands of the
       "same" sound (e.g., DX7 bass has slow attack, PPG click has fast attack)
    2. Spectral discontinuities â€” abrupt changes in harmonic structure at
       specific frequencies where one source hands off to another
    3. Stereo decorrelation between frequency bands (sources panned differently)
    """
    
    @staticmethod
    def analyze_band_envelopes(
        y: np.ndarray,
        sr: int,
        n_bands: int = 8,
        hop_length: int = 512
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Split signal into frequency bands and extract amplitude envelope for each.
        Returns (envelopes: [n_bands, n_frames], band_freqs: [n_bands]).
        """
        # Mel filterbank for perceptually-spaced bands
        S = np.abs(librosa.stft(y, hop_length=hop_length))
        mel_basis = librosa.filters.mel(sr=sr, n_fft=2048, n_mels=n_bands)
        mel_S = np.dot(mel_basis, S)
        
        # Convert to amplitude envelopes
        envelopes = librosa.amplitude_to_db(mel_S + 1e-10, ref=np.max)
        
        # Get center frequencies
        mel_freqs = librosa.mel_frequencies(n_mels=n_bands + 2)
        band_freqs = mel_freqs[1:-1]
        
        return envelopes, band_freqs
    
    @staticmethod
    def detect_composite(
        y: np.ndarray,
        sr: int,
        role: str = "unknown"
    ) -> CompositeSourceEvidence:
        """
        Analyze a spectral region for composite source evidence.
        """
        envelopes, band_freqs = CompositeSourceDetector.analyze_band_envelopes(y, sr)
        evidence = []
        
        # Test 1: Cross-band envelope correlation
        # Single source â†’ all bands correlate highly (same ADSR)
        # Composite â†’ different bands have different envelopes
        n_bands = envelopes.shape[0]
        correlations = []
        
        for i in range(n_bands):
            for j in range(i + 1, n_bands):
                env_i = envelopes[i]
                env_j = envelopes[j]
                if np.std(env_i) < 1e-6 or np.std(env_j) < 1e-6:
                    continue
                corr = float(np.corrcoef(env_i, env_j)[0, 1])
                correlations.append(corr)
        
        if not correlations:
            return CompositeSourceEvidence(
                role=role, is_composite=False, confidence=0.0,
                evidence=["Insufficient data"], estimated_n_sources=1,
                spectral_discontinuities=0
            )
        
        mean_corr = np.mean(correlations)
        min_corr = np.min(correlations)
        
        # Low mean correlation â†’ different envelope behaviors across bands
        if mean_corr < 0.6:
            evidence.append(
                f"Cross-band envelope correlation {mean_corr:.3f} (low = different sources per band)"
            )
        
        # Test 2: Spectral discontinuities
        # Look for abrupt changes in spectral slope at specific frequencies
        S = np.abs(librosa.stft(y, n_fft=4096))
        mean_spectrum = np.mean(S, axis=1)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)
        
        if np.max(mean_spectrum) > 0:
            db_spectrum = 20 * np.log10(mean_spectrum / np.max(mean_spectrum) + 1e-10)
            
            # Smooth and find slope changes
            from scipy.ndimage import uniform_filter1d
            smoothed = uniform_filter1d(db_spectrum, size=20)
            gradient = np.gradient(smoothed)
            gradient2 = np.gradient(gradient)
            
            # Count significant inflection points (slope changes > threshold)
            discontinuities = np.sum(np.abs(gradient2) > 0.5)
        else:
            discontinuities = 0
        
        if discontinuities > 3:
            evidence.append(
                f"{discontinuities} spectral slope discontinuities (multiple sources handoff)"
            )
        
        # Test 3: Attack consistency across bands
        # Single source â†’ coherent attack across all frequencies
        # Composite â†’ different attack times in different bands
        onset_times = []
        for i in range(n_bands):
            env = envelopes[i]
            # Find first significant rise
            threshold = np.max(env) - 12  # -12dB from peak
            rises = np.where(env > threshold)[0]
            if len(rises) > 0:
                onset_times.append(rises[0])
        
        if len(onset_times) >= 3:
            onset_spread = np.std(onset_times)
            if onset_spread > 5:  # frames
                evidence.append(
                    f"Attack onset spread {onset_spread:.1f} frames across bands (different source attacks)"
                )
        
        # Score
        composite_score = 0.0
        if mean_corr < 0.6:
            composite_score += 0.35
        if mean_corr < 0.4:
            composite_score += 0.15
        if discontinuities > 3:
            composite_score += 0.25
        if discontinuities > 6:
            composite_score += 0.1
        if len(onset_times) >= 3 and np.std(onset_times) > 5:
            composite_score += 0.15
        
        is_composite = composite_score >= 0.4
        estimated_sources = 1
        if composite_score >= 0.4:
            estimated_sources = 2
        if composite_score >= 0.7:
            estimated_sources = 3
        
        if not evidence:
            evidence.append("No composite source indicators â€” likely single source")
        
        return CompositeSourceEvidence(
            role=role,
            is_composite=is_composite,
            confidence=composite_score,
            evidence=evidence,
            estimated_n_sources=estimated_sources,
            spectral_discontinuities=discontinuities
        )


# ============================================================
# MAIN ENGINE
# ============================================================

class EquipmentIdentificationEngine:
    """
    Full equipment identification pipeline.
    
    Phase A module: runs after spectral roster, before full extraction.
    
    Input: raw audio (y, sr)
    Output: EquipmentReport
    
    Sequence:
    1. Too Clean detector â†’ programmed vs organic (cheapest, broadest)
    2. Drum classifier â†’ drum machine vs live drums
    3. Synthesis family classifier â†’ FM / analog / sample / wavetable
    4. Composite source detector â†’ multiple sources per element
    """
    
    def __init__(self):
        self.too_clean = TooCleanDetector()
        self.drum_classifier = DrumClassifier()
        self.synth_classifier = SynthesisFamilyClassifier()
        self.composite_detector = CompositeSourceDetector()
    
    def analyze(
        self, 
        y: np.ndarray, 
        sr: int,
        segment_seconds: float = 30.0
    ) -> EquipmentReport:
        """
        Full analysis pipeline.
        
        Uses a representative segment (default 30s from the middle of the track)
        to avoid intros/outros that may not be representative.
        """
        # Take representative segment from middle of track
        total_samples = len(y)
        segment_samples = int(sr * segment_seconds)
        
        if total_samples > segment_samples:
            start = (total_samples - segment_samples) // 2
            y_segment = y[start:start + segment_samples]
        else:
            y_segment = y
        
        # Handle stereo â†’ mono for analysis
        if y_segment.ndim > 1:
            y_mono = librosa.to_mono(y_segment)
        else:
            y_mono = y_segment
        
        # === STEP 1: Global "too clean" assessment ===
        onset_env = librosa.onset.onset_strength(y=y_mono, sr=sr)
        all_onsets = librosa.onset.onset_detect(
            onset_envelope=onset_env, sr=sr, units='frames'
        )
        
        all_profiles = self.too_clean.extract_transient_profiles(
            y_mono, sr, all_onsets
        )
        global_repetition = self.too_clean.analyze_repetition(all_profiles)
        
        # === STEP 2: Drum classification ===
        drum_result = self.drum_classifier.classify_drums(
            y_mono, sr, self.too_clean
        )
        
        # === STEP 3: Synthesis family on sustained regions ===
        # Separate harmonic content for analysis
        synth_classifications = []
        
        try:
            y_harmonic, y_percussive = librosa.effects.hpss(y_mono)
            
            # Analyze low region (bass synth / bass guitar)
            bands = self.drum_classifier.isolate_drum_hits(y_harmonic, sr)
            
            # Bass region synthesis analysis
            nyq = sr / 2
            low_norm = max(30 / nyq, 0.001)
            high_norm = min(500 / nyq, 0.999)
            b, a = scipy_signal.butter(4, [low_norm, high_norm], btype='band')
            bass_signal = scipy_signal.filtfilt(b, a, y_harmonic)
            
            if np.max(np.abs(bass_signal)) > 0.001:
                bass_harmonics = self.synth_classifier.analyze_harmonics(
                    bass_signal, sr, min_freq=30, max_freq=500
                )
                family, conf, ev = self.synth_classifier.classify(bass_harmonics)
                synth_classifications.append(SynthesisClassification(
                    role="sustained-low",
                    family=family,
                    confidence=conf,
                    evidence=ev,
                    harmonic_analysis=bass_harmonics
                ))
            
            # Mid region synthesis analysis
            low_norm = max(500 / nyq, 0.001)
            high_norm = min(4000 / nyq, 0.999)
            b, a = scipy_signal.butter(4, [low_norm, high_norm], btype='band')
            mid_signal = scipy_signal.filtfilt(b, a, y_harmonic)
            
            if np.max(np.abs(mid_signal)) > 0.001:
                mid_harmonics = self.synth_classifier.analyze_harmonics(
                    mid_signal, sr, min_freq=100, max_freq=4000
                )
                family, conf, ev = self.synth_classifier.classify(mid_harmonics)
                synth_classifications.append(SynthesisClassification(
                    role="sustained-mid",
                    family=family,
                    confidence=conf,
                    evidence=ev,
                    harmonic_analysis=mid_harmonics
                ))
            
        except Exception as e:
            synth_classifications.append(SynthesisClassification(
                role="global",
                family=SynthesisFamily.UNKNOWN,
                confidence=0.0,
                evidence=[f"Analysis error: {str(e)}"]
            ))
        
        # === STEP 4: Composite source detection ===
        composite_results = []
        
        try:
            # Check bass region for composite sourcing
            if np.max(np.abs(bass_signal)) > 0.001:
                bass_composite = self.composite_detector.detect_composite(
                    bass_signal, sr, role="sustained-low"
                )
                composite_results.append(bass_composite)
            
            # Check mid region
            if np.max(np.abs(mid_signal)) > 0.001:
                mid_composite = self.composite_detector.detect_composite(
                    mid_signal, sr, role="sustained-mid"
                )
                composite_results.append(mid_composite)
        except:
            pass
        
        # === COMPILE REPORT ===
        # Overall programmed score
        programmed_indicators = []
        if global_repetition.is_programmed:
            programmed_indicators.append(global_repetition.confidence)
        if drum_result.drum_type == DrumType.DRUM_MACHINE:
            programmed_indicators.append(drum_result.confidence)
        
        for sc in synth_classifications:
            if sc.family in (SynthesisFamily.FM, SynthesisFamily.ANALOG_SUBTRACTIVE, 
                           SynthesisFamily.WAVETABLE):
                programmed_indicators.append(sc.confidence * 0.5)
        
        overall_programmed = (
            np.mean(programmed_indicators) if programmed_indicators 
            else 0.5
        )
        
        # Source type
        if overall_programmed > 0.7:
            source_type = SourceType.PROGRAMMED
        elif overall_programmed < 0.3:
            source_type = SourceType.ORGANIC
        else:
            source_type = SourceType.HYBRID
        
        # Build summary
        summary_parts = [
            f"Source: {source_type.value} (score: {overall_programmed:.2f})"
        ]
        
        if drum_result.drum_type != DrumType.UNKNOWN:
            summary_parts.append(f"Drums: {drum_result.drum_type.value}")
        
        for sc in synth_classifications:
            if sc.family != SynthesisFamily.UNKNOWN:
                summary_parts.append(
                    f"{sc.role}: {sc.family.value} ({sc.confidence:.0%})"
                )
        
        composite_count = sum(1 for c in composite_results if c.is_composite)
        if composite_count > 0:
            summary_parts.append(f"Composite sources detected: {composite_count} regions")
        
        return EquipmentReport(
            source_type=source_type,
            source_confidence=abs(overall_programmed - 0.5) * 2,  # distance from uncertain
            synthesis_classifications=synth_classifications,
            drum_classification=drum_result,
            composite_evidence=composite_results,
            overall_programmed_score=overall_programmed,
            summary=" | ".join(summary_parts)
        )


# ============================================================
# CLI / TEST INTERFACE
# ============================================================

def analyze_file(filepath: str, verbose: bool = True) -> EquipmentReport:
    """Convenience function: load audio and run full analysis."""
    print(f"Loading: {filepath}")
    y, sr = librosa.load(filepath, sr=None, mono=False)
    
    if y.ndim > 1:
        y_mono = librosa.to_mono(y)
    else:
        y_mono = y
    
    print(f"  Duration: {len(y_mono)/sr:.1f}s | SR: {sr}Hz")
    
    engine = EquipmentIdentificationEngine()
    report = engine.analyze(y_mono, sr)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"EQUIPMENT IDENTIFICATION REPORT")
        print(f"{'='*60}")
        print(f"\n{report.summary}")
        
        print(f"\n--- Source Classification ---")
        print(f"  Type: {report.source_type.value}")
        print(f"  Confidence: {report.source_confidence:.2f}")
        print(f"  Programmed score: {report.overall_programmed_score:.2f}")
        
        if report.drum_classification:
            dc = report.drum_classification
            print(f"\n--- Drum Classification ---")
            print(f"  Type: {dc.drum_type.value}")
            print(f"  Confidence: {dc.confidence:.2f}")
            for e in dc.evidence:
                print(f"    â€¢ {e}")
        
        print(f"\n--- Synthesis Classifications ---")
        for sc in report.synthesis_classifications:
            print(f"  [{sc.role}] {sc.family.value} ({sc.confidence:.0%})")
            for e in sc.evidence:
                print(f"    â€¢ {e}")
            if sc.harmonic_analysis and sc.harmonic_analysis.fundamental_hz > 0:
                ha = sc.harmonic_analysis
                print(f"    Harmonics: f0={ha.fundamental_hz:.1f}Hz, "
                      f"partials={ha.n_partials_detected}, "
                      f"integer_ratio={ha.integer_ratio_score:.2f}, "
                      f"sideband={ha.sideband_energy:.2f}, "
                      f"drift={ha.drift_hz:.2f}Hz")
        
        if report.composite_evidence:
            print(f"\n--- Composite Source Detection ---")
            for ce in report.composite_evidence:
                status = "COMPOSITE" if ce.is_composite else "single source"
                print(f"  [{ce.role}] {status} ({ce.confidence:.0%}, est. {ce.estimated_n_sources} sources)")
                for e in ce.evidence:
                    print(f"    â€¢ {e}")
    
    return report


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze_file(sys.argv[1])
    else:
        print("Usage: python equipment_engine.py <audio_file>")
        print("Supports: WAV, MP3, FLAC, OGG")
