#!/usr/bin/env python3
"""
Command-Line Interface Module

Provides the main entry point for the audio separation tool.
Handles argument parsing and orchestrates the separation workflow.
"""

import os
import sys
import argparse

from unmix.separator import separate_stems
from unmix.filters import separate_drums


def main():
    """
    Main entry point for the CLI application.

    Parses command-line arguments and executes the appropriate separation workflow.
    """
    parser = argparse.ArgumentParser(
        description='Separate audio into stems and drum components',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Separate a stereo mix into stems
  unmix --mode=stems --input-file=input.mp3

  # Separate a drum stem into components
  unmix --mode=drums --input-file=drums.wav

  # Full pipeline: separate mix, then separate drums
  unmix --mode=both --input-file=input.mp3

  # Use a different model
  unmix --mode=stems --input-file=song.mp3 --model=htdemucs_ft
        """
    )

    parser.add_argument(
        '--mode',
        required=True,
        choices=['stems', 'drums', 'both'],
        help='Operation mode: stems, drums, or both'
    )

    parser.add_argument(
        '--input-file',
        required=True,
        dest='input_file',
        help='Input audio file path'
    )

    parser.add_argument(
        '--output-stems',
        default='output_stems',
        help='Output directory for stems (default: output_stems)'
    )

    parser.add_argument(
        '--output-drums',
        default='output_drums',
        help='Output directory for drum components (default: output_drums)'
    )

    parser.add_argument(
        '--model',
        default='htdemucs',
        choices=['htdemucs', 'htdemucs_ft', 'hdemucs_mmi'],
        help='Demucs model to use (default: htdemucs)'
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"❌ Error: Input file '{args.input_file}' not found")
        sys.exit(1)

    print("=" * 60)
    print("Audio Source Separation Tool")
    print("=" * 60)

    if args.mode in ['stems', 'both']:
        print("\n📊 Step 1: Separating stereo mix into stems...")
        stem_files = separate_stems(
            args.input_file,
            args.output_stems,
            args.model
        )

        if args.mode == 'both' and 'drums' in stem_files:
            print("\n📊 Step 2: Separating drum stem into components...")
            drum_files = separate_drums(
                stem_files['drums'],
                args.output_drums
            )

    elif args.mode == 'drums':
        print("\n📊 Separating drum stem into components...")
        drum_files = separate_drums(
            args.input_file,
            args.output_drums
        )

    print("\n" + "=" * 60)
    print("✅ All operations completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
