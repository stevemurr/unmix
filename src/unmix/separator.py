#!/usr/bin/env python3
"""
Stem Separation Module

Handles separation of stereo mixes into individual stems (Drums, Vocals, Bass, Other)
using Facebook's Demucs model.
"""

import sys
from pathlib import Path
import torch


def separate_stems(input_file, output_dir="output_stems", model="htdemucs"):
    """
    Separate a stereo mix into stems (Drums, Vocals, Bass, Other)

    Args:
        input_file (str): Path to input audio file
        output_dir (str): Directory to save separated stems
        model (str): Demucs model to use (htdemucs, htdemucs_ft, hdemucs_mmi)

    Returns:
        dict: Paths to separated stem files

    Raises:
        ImportError: If Demucs is not installed
        Exception: If separation fails

    Example:
        >>> stem_files = separate_stems("song.mp3", model="htdemucs_ft")
        >>> print(stem_files['drums'])  # Path to drum stem
    """
    try:
        from demucs.pretrained import get_model
        from demucs.apply import apply_model
        from demucs.audio import AudioFile, save_audio

        print(f"Loading model: {model}...")
        separator = get_model(model)

        print(f"Loading audio file: {input_file}...")
        wav = AudioFile(input_file).read(
            streams=0,
            samplerate=separator.samplerate,
            channels=separator.audio_channels
        )

        # Add batch dimension
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()

        print("Separating stems... This may take a few minutes...")

        # Determine device (MPS for M1/M2/M3 Mac, CUDA for NVIDIA, CPU otherwise)
        device = _get_best_device()
        print(f"Using {device.upper()} acceleration" if device != 'cpu' else "Using CPU (this will be slower)")

        sources = apply_model(
            separator,
            wav[None],
            device=device,
            progress=True
        )[0]

        sources = sources * ref.std() + ref.mean()

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save stems
        stem_names = separator.sources
        output_files = {}

        print("\nSaving separated stems...")
        for i, name in enumerate(stem_names):
            stem_file = output_path / f"{Path(input_file).stem}_{name}.wav"
            save_audio(
                sources[i],
                str(stem_file),
                samplerate=separator.samplerate
            )
            output_files[name] = str(stem_file)
            print(f"  ✓ Saved: {stem_file}")

        print("\n✅ Stem separation complete!")
        return output_files

    except ImportError:
        print("❌ Error: Demucs not installed. Run: pip install demucs")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during stem separation: {e}")
        sys.exit(1)


def _get_best_device():
    """
    Determine the best available device for processing.

    Returns:
        str: Device name ('mps', 'cuda', or 'cpu')
    """
    if torch.backends.mps.is_available():
        return 'mps'
    elif torch.cuda.is_available():
        return 'cuda'
    else:
        return 'cpu'
