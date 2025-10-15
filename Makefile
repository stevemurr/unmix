.PHONY: help env-build env-on env-off clean install install-dev test lint format

# Python and venv settings
PYTHON := python3
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
PYTHON_VENV := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

env: ## Create virtual environment and install dependencies
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Upgrading pip..."
	$(PIP) install --upgrade pip
	@echo "Installing project in editable mode..."
	$(PIP) install -e .
	@echo ""
	@echo "✅ Environment built successfully!"
	@echo "To activate, run: source $(VENV_BIN)/activate"

install: ## Install/reinstall production dependencies
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Installing dependencies from pyproject.toml..."; \
		$(PIP) install --upgrade pip; \
		$(PIP) install -e .; \
		echo "✅ Dependencies installed!"; \
	else \
		echo "❌ Virtual environment not found. Run 'make env-build' first."; \
		exit 1; \
	fi

install-dev: ## Install development dependencies
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Installing development dependencies..."; \
		$(PIP) install -e ".[dev]"; \
		echo "✅ Development dependencies installed!"; \
	else \
		echo "❌ Virtual environment not found. Run 'make env-build' first."; \
		exit 1; \
	fi

clean: ## Remove virtual environment and cache files
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleaned up virtual environment and cache files"

format: ## Format code with black
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Formatting code with black..."; \
		$(VENV_BIN)/black src/unmix/; \
		echo "✅ Code formatted!"; \
	else \
		echo "❌ Virtual environment not found. Install dev dependencies first: make install-dev"; \
		exit 1; \
	fi

lint: ## Lint code with ruff
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Linting code with ruff..."; \
		$(VENV_BIN)/ruff check src/unmix/; \
		echo "✅ Linting complete!"; \
	else \
		echo "❌ Virtual environment not found. Install dev dependencies first: make install-dev"; \
		exit 1; \
	fi

test-audio: ## Run test separation on sample audio
	@if [ -f "keepliving.mp3" ]; then \
		echo "Running test separation on keepliving.mp3..."; \
		$(VENV_BIN)/unmix --mode=stems --input-file=keepliving.mp3 --output-stems=test_output; \
		echo "✅ Test complete! Check test_output/ directory"; \
	else \
		echo "No test audio file found. Usage:"; \
		echo "  $(VENV_BIN)/unmix --mode=stems --input-file=<file>"; \
	fi

test: ## Run pytest unit tests
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Running tests..."; \
		$(VENV_BIN)/pytest; \
	else \
		echo "❌ Virtual environment not found. Install dev dependencies first: make install-dev"; \
		exit 1; \
	fi
