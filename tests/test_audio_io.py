"""
Tests for audio_io module
"""

import pytest
import numpy as np
from pathlib import Path

from unmix.audio_io import load_audio_file, write_audio_file, get_audio_info


def test_load_audio_file_not_found():
    """Test that loading a non-existent file raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_audio_file("nonexistent_file.wav")


def test_write_audio_file_mono(tmp_path):
    """Test writing a mono audio file"""
    # Create dummy audio data
    sample_rate = 44100
    duration = 1.0  # seconds
    samples = int(sample_rate * duration)
    audio = np.random.randn(samples).astype(np.float32)

    # Write to temporary file
    output_file = tmp_path / "test_mono.wav"
    write_audio_file(output_file, audio, sample_rate)

    # Verify file exists
    assert output_file.exists()


def test_write_audio_file_stereo(tmp_path):
    """Test writing a stereo audio file"""
    # Create dummy stereo audio data
    sample_rate = 44100
    duration = 0.5  # seconds
    samples = int(sample_rate * duration)
    audio = np.random.randn(2, samples).astype(np.float32)

    # Write to temporary file
    output_file = tmp_path / "test_stereo.wav"
    write_audio_file(output_file, audio, sample_rate)

    # Verify file exists
    assert output_file.exists()


def test_write_audio_file_invalid_bit_depth(tmp_path):
    """Test that invalid bit depth raises ValueError"""
    audio = np.random.randn(1000).astype(np.float32)
    output_file = tmp_path / "test.wav"

    with pytest.raises(ValueError):
        write_audio_file(output_file, audio, 44100, bit_depth=48)


def test_write_and_load_roundtrip(tmp_path):
    """Test that we can write and then load an audio file"""
    # Create dummy audio data
    sample_rate = 22050
    audio_original = np.random.randn(1000).astype(np.float32)

    # Write to file
    output_file = tmp_path / "test_roundtrip.wav"
    write_audio_file(output_file, audio_original, sample_rate)

    # Load back
    audio_loaded, sr_loaded = load_audio_file(output_file)

    # Verify sample rate matches
    assert sr_loaded == sample_rate

    # Verify shape matches (allowing for minor differences due to encoding)
    assert len(audio_loaded) == len(audio_original)
