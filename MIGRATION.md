# Migration to Modern src/ Layout (Split → Unmix)

This document describes the migration from a flat project structure to the modern `src/` layout, and the rename from `split` to `unmix`.

## What Changed

### Package Rename: `split` → `unmix`

The package has been renamed from `split` to `unmix` to:
- Avoid conflicts with the Unix `split` command
- Better reflect what the tool does (unmixing audio)
- Create a more unique, brandable name

### Directory Structure

**Before:**
```
split/
├── main.py
├── audio_io.py
├── requirements.txt
└── pyproject.toml
```

**After:**
```
unmix/
├── src/
│   └── unmix/
│       ├── __init__.py
│       ├── cli.py          # Entry point (was main.py)
│       ├── audio_io.py     # Audio I/O utilities
│       ├── separator.py    # Stem separation logic
│       └── filters.py      # Drum filtering logic
├── tests/
│   ├── __init__.py
│   ├── test_audio_io.py
│   └── test_filters.py
├── pyproject.toml
├── Makefile
├── README.md
└── .gitignore
```

### Module Changes

1. **`main.py` → Split into modules:**
   - `src/unmix/cli.py` - Command-line interface
   - `src/unmix/separator.py` - Stem separation with Demucs
   - `src/unmix/filters.py` - Drum component filtering

2. **`audio_io.py` → `src/unmix/audio_io.py`:**
   - Moved to package directory
   - No functional changes

3. **New `src/unmix/__init__.py`:**
   - Package initialization
   - Public API exports
   - Version metadata

### Command Changes

**Before:**
```bash
python main.py stems input.mp3
```

**After:**
```bash
# After installation
unmix --mode=stems --input-file=input.mp3

# Or with venv
.venv/bin/unmix --mode=stems --input-file=input.mp3
```

### Configuration Changes

**pyproject.toml:**
- Package name: `audio-stem-separator` → `unmix`
- Entry point: `split.cli:main` → `unmix.cli:main`
- Command: `split` → `unmix`
- Updated `[tool.setuptools]` to use `src/` layout

**Makefile:**
- Updated paths to point to `src/unmix/`
- Changed `test` to run pytest
- Added `test-audio` for audio file testing
- Updated all command references from `split` to `unmix`

## Migration Steps

If you have an existing installation:

1. **Clean old installation:**
   ```bash
   make clean
   ```

2. **Rebuild environment:**
   ```bash
   make env-build
   ```

3. **Activate environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Test installation:**
   ```bash
   unmix --help
   ```

## Benefits of New Structure

✅ **No command conflicts** - Doesn't clash with Unix `split` command  
✅ **Better organization** - Clear separation of concerns  
✅ **Testable** - Proper test isolation  
✅ **Standard** - Follows modern Python packaging standards  
✅ **Installable** - Can be installed as a proper package  
✅ **Maintainable** - Easier to navigate and extend  
✅ **Professional** - Industry-standard structure  
✅ **Memorable** - "Unmix" is intuitive and brandable  

## Breaking Changes

- Package renamed from `split` to `unmix`
- Command changed from `python main.py` to `unmix`
- Positional arguments now use `--mode` and `--input-file` flags
- All import statements changed from `split.*` to `unmix.*`

## Old Files

The following files in the root directory are now deprecated and can be removed:
- `main.py` (replaced by `src/unmix/cli.py`)
- `audio_io.py` (moved to `src/unmix/audio_io.py`)
- `requirements.txt` (optional - can keep for compatibility)
