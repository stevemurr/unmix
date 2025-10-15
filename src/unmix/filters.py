#!/usr/bin/env python3
"""
Audio Filtering Module

Handles drum separation using frequency-based filtering to isolate individual
drum components (kick, snare, hi-hat, toms).
"""

import sys
import numpy as np
from pathlib import Path

from unmix.audio_io import load_audio_file, write_audio_file


def separate_drums(drum_file, output_dir="output_drums", threshold=0.3):
    """
    Separate a drum stem into constituent components (kick, snare, hi-hat, etc.)

    Args:
        drum_file (str): Path to drum stem audio file
        output_dir (str): Directory to save separated drum components
        threshold (float): Detection threshold for onset detection (unused currently)

    Returns:
        dict: Paths to separated drum component files

    Raises:
        ImportError: If required libraries are not installed
        Exception: If drum separation fails

    Note:
        This uses frequency-based filtering as a baseline approach.
        For production-quality results, consider using specialized drum
        separation models like ADTof.

    Example:
        >>> drum_files = separate_drums("drums.wav")
        >>> print(drum_files['kick'])  # Path to kick drum file
    """
    try:
        from scipy import signal

        print(f"\nLoading drum file: {drum_file}...")
        y, sr = load_audio_file(drum_file, sample_rate=44100, mono=False)

        print("Analyzing drum components...")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_files = {}

        # Frequency-based separation
        # This is a simplified approach - for production use, consider using
        # specialized drum separation models like DrumSep or similar

        # Low frequencies (Kick drum: 20-200 Hz)
        kick_filtered = filter_frequency_range(y, sr, 20, 200)
        kick_file = output_path / f"{Path(drum_file).stem}_kick.wav"
        write_audio_file(kick_file, kick_filtered, sr)
        output_files['kick'] = str(kick_file)
        print(f"  ✓ Saved: {kick_file}")

        # Mid frequencies (Snare: 150-400 Hz fundamental, 1-4 kHz brightness)
        snare_filtered = filter_frequency_range(y, sr, 150, 4000)
        snare_file = output_path / f"{Path(drum_file).stem}_snare.wav"
        write_audio_file(snare_file, snare_filtered, sr)
        output_files['snare'] = str(snare_file)
        print(f"  ✓ Saved: {snare_file}")

        # High frequencies (Hi-hats and cymbals: 5 kHz+)
        hihat_filtered = filter_frequency_range(y, sr, 5000, sr//2)
        hihat_file = output_path / f"{Path(drum_file).stem}_hihat.wav"
        write_audio_file(hihat_file, hihat_filtered, sr)
        output_files['hihat'] = str(hihat_file)
        print(f"  ✓ Saved: {hihat_file}")

        # Toms (Mid-range: 80-500 Hz)
        toms_filtered = filter_frequency_range(y, sr, 80, 500)
        toms_file = output_path / f"{Path(drum_file).stem}_toms.wav"
        write_audio_file(toms_file, toms_filtered, sr)
        output_files['toms'] = str(toms_file)
        print(f"  ✓ Saved: {toms_file}")

        print("\n✅ Drum separation complete!")
        print("\n⚠️  Note: This uses frequency-based filtering as a baseline.")
        print("    For better results, consider using specialized drum separation models")
        print("    like ADTof (https://github.com/CarlSouthall/ADTof) or similar tools.")

        return output_files

    except ImportError as e:
        print(f"❌ Error: Missing library. Run: pip install librosa scipy soundfile")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during drum separation: {e}")
        sys.exit(1)


def filter_frequency_range(audio, sr, low_freq, high_freq):
    """
    Apply bandpass filter to isolate frequency range.

    Args:
        audio: Audio signal (numpy array)
        sr: Sample rate
        low_freq: Low frequency cutoff in Hz
        high_freq: High frequency cutoff in Hz

    Returns:
        Filtered audio signal (numpy array)

    Example:
        >>> # Extract bass frequencies (20-200 Hz)
        >>> bass = filter_frequency_range(audio, 44100, 20, 200)
    """
    from scipy import signal

    # Design bandpass filter
    nyquist = sr / 2
    low = low_freq / nyquist
    high = min(high_freq / nyquist, 0.99)  # Ensure below Nyquist

    sos = signal.butter(4, [low, high], btype='band', output='sos')

    # Apply filter
    if len(audio.shape) > 1:
        # Stereo
        filtered = np.zeros_like(audio)
        for i in range(audio.shape[0]):
            filtered[i] = signal.sosfilt(sos, audio[i])
    else:
        # Mono
        filtered = signal.sosfilt(sos, audio)

    return filtered
