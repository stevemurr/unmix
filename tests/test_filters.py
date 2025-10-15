"""
Tests for filters module
"""

import pytest
import numpy as np

from unmix.filters import filter_frequency_range


def test_filter_frequency_range_mono():
    """Test frequency filtering on mono audio"""
    # Create simple mono audio signal
    sample_rate = 44100
    duration = 0.1
    samples = int(sample_rate * duration)
    audio = np.random.randn(samples).astype(np.float32)

    # Apply filter
    filtered = filter_frequency_range(audio, sample_rate, 100, 1000)

    # Verify output shape matches input
    assert filtered.shape == audio.shape

    # Verify output is different from input (filtering happened)
    assert not np.array_equal(filtered, audio)


def test_filter_frequency_range_stereo():
    """Test frequency filtering on stereo audio"""
    # Create simple stereo audio signal
    sample_rate = 44100
    duration = 0.1
    samples = int(sample_rate * duration)
    audio = np.random.randn(2, samples).astype(np.float32)

    # Apply filter
    filtered = filter_frequency_range(audio, sample_rate, 100, 1000)

    # Verify output shape matches input
    assert filtered.shape == audio.shape

    # Verify output is different from input
    assert not np.array_equal(filtered, audio)


def test_filter_frequency_range_nyquist_limit():
    """Test that filter handles frequencies near Nyquist properly"""
    sample_rate = 44100
    audio = np.random.randn(1000).astype(np.float32)

    # This should not raise an error
    filtered = filter_frequency_range(audio, sample_rate, 100, sample_rate // 2)

    assert filtered.shape == audio.shape
