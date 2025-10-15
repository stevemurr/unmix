# Unmix

A Python-based audio separation tool that uses AI models to separate stereo mixes into individual stems (vocals, drums, bass, other) and further separate drum tracks into individual components (kick, snare, hi-hat, toms).

## Features

- **Stem Separation**: Separate any stereo mix into 4 stems using Facebook's Demucs model
  - Drums
  - Vocals
  - Bass
  - Other (instruments)
  
- **Drum Component Separation**: Further separate drum stems into individual components
  - Kick drum
  - Snare
  - Hi-hats/Cymbals
  - Toms

- **Hardware Acceleration**: Automatic detection and use of:
  - MPS (Metal Performance Shaders) on Apple Silicon (M1/M2/M3)
  - CUDA on NVIDIA GPUs
  - CPU fallback for compatibility

## Requirements

- Python 3.8+
- macOS (with Apple Silicon recommended for best performance) or Linux/Windows

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd unmix

# Build environment and install dependencies
make env-build

# Activate the virtual environment
source .venv/bin/activate
```

### Usage

```bash
# Separate a stereo mix into stems
unmix --mode=stems --input-file=your_song.mp3

# Separate a drum stem into components
unmix --mode=drums --input-file=drum_stem.wav

# Full pipeline (separate mix, then drums)
unmix --mode=both --input-file=your_song.mp3
```

### Advanced Options

```bash
# Use a different model
unmix --mode=stems --input-file=input.mp3 --model=htdemucs_ft

# Specify custom output directories
unmix --mode=stems --input-file=input.mp3 --output-stems=my_stems/
unmix --mode=drums --input-file=drums.wav --output-drums=my_drums/
```

Available models:
- `htdemucs` (default) - Hybrid Transformer Demucs
- `htdemucs_ft` - Fine-tuned version
- `hdemucs_mmi` - Alternative model

For all options:
```bash
unmix --help
```

## Development

### Available Make Commands

```bash
make help          # Show all available commands
make env-build     # Create virtual environment and install dependencies
make install       # Install/reinstall production dependencies
make install-dev   # Install development dependencies
make clean         # Remove virtual environment and cache files
make format        # Format code with black
make lint          # Lint code with ruff
make test          # Run pytest unit tests
make test-audio    # Run test separation on sample audio
```

### Running Tests

```bash
# Install dev dependencies
make install-dev

# Run unit tests
make test

# Run audio separation test (requires sample audio file)
make test-audio
```

### Project Structure

```
unmix/
├── src/
│   └── unmix/
│       ├── __init__.py      # Package initialization
│       ├── cli.py           # Command-line interface
│       ├── audio_io.py      # Audio I/O utilities
│       ├── separator.py     # Stem separation logic
│       └── filters.py       # Drum filtering logic
├── tests/
│   ├── test_audio_io.py     # Audio I/O tests
│   └── test_filters.py      # Filter tests
├── pyproject.toml           # Project configuration
├── Makefile                 # Build automation
└── README.md
```

## Output Structure

After running stem separation:
```
output_stems/
├── song_drums.wav
├── song_vocals.wav
├── song_bass.wav
└── song_other.wav
```

After running drum separation:
```
output_drums/
├── drums_kick.wav
├── drums_snare.wav
├── drums_hihat.wav
└── drums_toms.wav
```

## Technical Details

### Stem Separation

Uses Meta's [Demucs](https://github.com/facebookresearch/demucs) model, a state-of-the-art source separation system based on hybrid spectrogram and waveform processing.

### Drum Separation

Employs frequency-based filtering to isolate drum components:
- Kick: 20-200 Hz
- Snare: 150-4000 Hz
- Hi-hats/Cymbals: 5 kHz+
- Toms: 80-500 Hz

**Note**: The drum separation uses frequency-based filtering as a baseline approach. For production-quality results, consider using specialized drum separation models like [ADTof](https://github.com/CarlSouthall/ADTof).

## Performance Notes

- **Apple Silicon (M1/M2/M3)**: Uses Metal Performance Shaders for GPU acceleration
- **NVIDIA GPUs**: Uses CUDA for acceleration
- **CPU**: Fallback mode (slower but functional)

Processing time depends on:
- Audio file length
- Hardware capabilities
- Selected model

Typical processing: 3-5 minutes for a 3-minute song on Apple Silicon.

## Dependencies

- `demucs` - AI-powered source separation
- `librosa` - Audio analysis
- `soundfile` - Audio I/O
- `scipy` - Signal processing
- `numpy` - Numerical computing
- `pydub` - Audio manipulation

## License

See LICENSE file for details.

## Acknowledgments

- [Demucs](https://github.com/facebookresearch/demucs) by Meta Research
- [Librosa](https://librosa.org/) audio processing library
