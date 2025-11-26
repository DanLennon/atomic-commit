# Commit Score

A Python tool that provides visual feedback on your Git commit size using colored emojis.

## Features

- 🟩 Small commits (< 20 lines changed): Green indicator
- 🟧 Medium commits (20-99 lines changed): Orange indicator  
- 🟥 Large commits (100+ lines changed): Red indicator

## Installation

```bash
uv install
```

## Usage

After installation, you can run the tool from any Git repository:

```bash
commit-size
```

The tool will:
1. Check if you're in a Git repository
2. Count the lines changed in your current diff
3. Display a colored emoji indicator based on the size

## How it works

The tool uses `git diff --unified=0` to count added and removed lines (excluding file headers). It encourages atomic commits by providing visual feedback on commit size:

- **Green (🟩)**: Small, focused changes that are easy to review
- **Orange (🟧)**: Medium-sized changes that might need more careful review
- **Red (🟥)**: Large changes that could benefit from being split into smaller commits

## Requirements

- Python 3.12+
- Git
- Must be run within a Git repository

## Dependencies

- `ruff>=0.13.0` (for code formatting and linting)
