# Atomic Commit

A Python tool that provides visual feedback on your Git changes using colored emojis and tracks time since your last commit.

## Features

- 🟩 Small changes (< 20 lines): Green indicator for focused commits
- 🟧 Medium changes (20-99 lines): Orange indicator for moderate commits
- 🟥 Large changes (100+ lines): Red indicator suggesting commit splitting
- ⏰ Time tracking: Shows time since last commit (seconds/minutes/hours/days)
- 📊 Comprehensive change detection: Tracks unstaged, staged, and untracked files
- 🔄 Two modes: Single check or continuous monitoring

## Installation

### From Source

Clone the repository and install with uv:

```bash
git clone <repository-url>
cd atomic-commit
uv install .
```

### Development Installation

For development with editable installation:

```bash
uv install -e .
```

## Building

To build the package:

```bash
uv build
```

This creates both wheel and source distributions in the `dist/` directory.

## Usage

After installation, you can run the tool from any Git repository:

### Single Check Mode (default)
```bash
atomic-commit
```

### Continuous Monitoring Mode
```bash
atomic-commit --monitor
# or
atomic-commit -m
```

The tool will:
1. Check if you're in a Git repository
2. Count lines changed across all unstaged, staged, and untracked files
3. Display a colored emoji indicator based on total change size
4. Show time elapsed since your last commit

Example output: `🟧 45 ⏰2h` (45 lines changed, 2 hours since last commit)

## How it works

The tool uses multiple Git commands to get a comprehensive view of your changes:

- `git diff --unified=0`: Counts unstaged changes
- `git diff --staged --unified=0`: Counts staged changes  
- `git ls-files --others --exclude-standard`: Finds untracked files
- `git log -1 --format=%ct`: Gets last commit timestamp

It encourages atomic commits by providing visual feedback:

- **Green (🟩)**: Small, focused changes that are easy to review
- **Orange (🟧)**: Medium-sized changes that might need careful review
- **Red (🟥)**: Large changes that should be split into smaller commits

The time indicator helps you stay aware of how long you've been working without committing.

## Requirements

- Python 3.12+
- Git
- Must be run within a Git repository

## Dependencies

- `ruff>=0.13.0` (for code formatting and linting)

## Project Structure

```
atomic-commit/
├── src/
│   ├── __init__.py
│   └── atomic_commit.py    # Main application code
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
└── README.md              # This file
```

