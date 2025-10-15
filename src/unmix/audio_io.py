#!/usr/bin/env python3
"""
Audio I/O Module

Provides a clean API for loading and writing audio files with support for
multiple formats and automatic format detection.
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Union, Optional


def load_audio_file(
    filepath: Union[str, Path],
    sample_rate: Optional[int] = None,
    mono: bool = False,
    offset: float = 0.0,
    duration: Optional[float] = None
) -> Tuple[np.ndarray, int]:
    """
    Load an audio file into a numpy array.

    Args:
        filepath: Path to the audio file
        sample_rate: Target sample rate (None = use original sample rate)
        mono: If True, convert to mono by averaging channels
        offset: Start reading after this time (in seconds)
        duration: Only load up to this duration (in seconds)

    Returns:
        Tuple of (audio_data, sample_rate)
        - audio_data: numpy array of shape (channels, samples) or (samples,) if mono
        - sample_rate: Sample rate of the audio

    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ImportError: If required audio library is not installed
        ValueError: If the file format is not supported

    Examples:
        >>> # Load entire file
        >>> audio, sr = load_audio_file("song.mp3")

        >>> # Load as mono at 44.1kHz
        >>> audio, sr = load_audio_file("song.wav", sample_rate=44100, mono=True)

        >>> # Load first 10 seconds
        >>> audio, sr = load_audio_file("song.flac", duration=10.0)
    """
    try:
        import librosa
    except ImportError:
        raise ImportError(
            "librosa is required for audio loading. "
            "Install with: pip install librosa"
        )

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    try:
        # librosa.load returns (audio, sample_rate)
        # audio shape is (samples,) for mono or will be converted based on mono parameter
        audio, sr = librosa.load(
            str(filepath),
            sr=sample_rate,
            mono=mono,
            offset=offset,
            duration=duration
        )

        return audio, sr

    except Exception as e:
        raise ValueError(
            f"Failed to load audio file '{filepath}': {e}"
        ) from e


def write_audio_file(
    filepath: Union[str, Path],
    audio: np.ndarray,
    sample_rate: int,
    bit_depth: int = 16,
    normalize: bool = False
) -> None:
    """
    Write audio data to a file.

    Args:
        filepath: Output file path (format determined by extension)
        audio: Audio data as numpy array
               Shape: (samples,) for mono or (channels, samples) for multi-channel
        sample_rate: Sample rate in Hz
        bit_depth: Bit depth (8, 16, 24, or 32)
        normalize: If True, normalize audio to prevent clipping

    Raises:
        ImportError: If required audio library is not installed
        ValueError: If audio format or parameters are invalid

    Supported formats:
        - WAV (.wav)
        - FLAC (.flac)
        - OGG (.ogg)
        - MP3 (.mp3) - requires additional dependencies

    Examples:
        >>> # Write mono audio
        >>> write_audio_file("output.wav", audio, 44100)

        >>> # Write stereo with normalization
        >>> write_audio_file("output.flac", stereo_audio, 48000, normalize=True)

        >>> # Write 24-bit audio
        >>> write_audio_file("output.wav", audio, 96000, bit_depth=24)
    """
    try:
        import soundfile as sf
    except ImportError:
        raise ImportError(
            "soundfile is required for audio writing. "
            "Install with: pip install soundfile"
        )

    filepath = Path(filepath)

    # Ensure parent directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Validate bit depth
    valid_bit_depths = [8, 16, 24, 32]
    if bit_depth not in valid_bit_depths:
        raise ValueError(
            f"Invalid bit depth: {bit_depth}. "
            f"Must be one of {valid_bit_depths}"
        )

    # Convert bit depth to soundfile subtype
    subtype_map = {
        8: 'PCM_S8',
        16: 'PCM_16',
        24: 'PCM_24',
        32: 'PCM_32'
    }

    # Normalize if requested
    if normalize:
        max_val = np.abs(audio).max()
        if max_val > 0:
            audio = audio / max_val * 0.95  # Leave headroom

    # Ensure audio is in correct format for soundfile
    # soundfile expects (samples, channels) for multi-channel
    if len(audio.shape) > 1:
        # Convert from (channels, samples) to (samples, channels)
        audio = audio.T

    try:
        sf.write(
            str(filepath),
            audio,
            sample_rate,
            subtype=subtype_map[bit_depth]
        )
    except Exception as e:
        raise ValueError(
            f"Failed to write audio file '{filepath}': {e}"
        ) from e


def get_audio_info(filepath: Union[str, Path]) -> dict:
    """
    Get information about an audio file without loading it into memory.

    Args:
        filepath: Path to the audio file

    Returns:
        Dictionary containing:
        - duration: Duration in seconds
        - sample_rate: Sample rate in Hz
        - channels: Number of channels
        - frames: Total number of frames
        - format: File format
        - subtype: Audio encoding subtype

    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ImportError: If required audio library is not installed

    Example:
        >>> info = get_audio_info("song.wav")
        >>> print(f"Duration: {info['duration']:.2f}s")
        >>> print(f"Sample rate: {info['sample_rate']}Hz")
    """
    try:
        import soundfile as sf
    except ImportError:
        raise ImportError(
            "soundfile is required for audio info. "
            "Install with: pip install soundfile"
        )

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    try:
        info = sf.info(str(filepath))

        return {
            'duration': info.duration,
            'sample_rate': info.samplerate,
            'channels': info.channels,
            'frames': info.frames,
            'format': info.format,
            'subtype': info.subtype
        }
    except Exception as e:
        raise ValueError(
            f"Failed to get audio info for '{filepath}': {e}"
        ) from e
