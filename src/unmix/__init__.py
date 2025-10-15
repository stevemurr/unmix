"""
Unmix - Audio Source Separation Tool

An AI-powered audio separation tool that separates stereo mixes into individual
stems (vocals, drums, bass, other) and further separates drum tracks into
individual components (kick, snare, hi-hat, toms).
"""

__version__ = "0.1.0"
__author__ = "Steve Murr"
__license__ = "MIT"

from unmix.audio_io import load_audio_file, write_audio_file, get_audio_info
from unmix.separator import separate_stems
from unmix.filters import separate_drums

__all__ = [
    "load_audio_file",
    "write_audio_file",
    "get_audio_info",
    "separate_stems",
    "separate_drums",
]
