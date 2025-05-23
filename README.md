# git-tree-project-structure-to-yaml

A command-line tool that generates YAML or tree-style representations of Git repository file structures.

## Overview

This tool provides functionality similar to the 'tree' command on Linux or the Get-Tree cmdlet on Windows, but specifically designed for Git repositories. It generates either YAML or compact text representations of a Git repository's directory structure using GitPython and nutree.

The tool can include staged files, working directory files, and untracked files, with options to exclude specific patterns and filter by directories.

## Features

- Generate YAML or tree-style representations of Git repositories
- Filter files by Git status (staged, working directory, untracked)
- Exclude files using patterns
- Specify output to file or stdout
- Support for directory-specific filtering

## Installation

Requires Python 3.12 or higher.

```bash
# Using uv (recommended)
uv pip install git-tree-project-structure-to-yaml

# Using pip
pip install git-tree-project-structure-to-yaml
```

## Usage

Basic usage:

```bash
# Generate YAML to stdout
git-tree-project-structure-to-yaml /path/to/repo

# Generate YAML to file
git-tree-project-structure-to-yaml /path/to/repo --output structure.yaml

# Generate tree output
git-tree-project-structure-to-yaml /path/to/repo --format tree --output structure.txt

# Exclude specific patterns
git-tree-project-structure-to-yaml /path/to/repo --exclude node_modules --exclude .venv
```

## Command-line Options

### Basic Options
- `repo_paths`: Paths to directories in the Git repository (positional arguments)
- `--repo`: Path to the Git repository root (defaults to current directory)
- `-o, --output`: Output file (default: print to stdout)
- `-v, --verbose`: Enable verbose output

### Output Format Options
- `-f, --format [yaml|tree]`: Output format (default: yaml)

### Git-specific Options
- `--others`: Show untracked files in the output (default: True)
- `--stage`: Show staged files in the output (default: True)
- `--cached`: Show cached/tracked files in the output (default: False)
- `--exclude-standard`: Use standard Git exclusions (default: True)
- `--repo-as-root`: Use the repository root as the root directory (default: True)
- `-x, --exclude`: Patterns to exclude (can be used multiple times)

## Example Output

### YAML Format
```yaml
git-tree-project-structure-to-yaml/:
  - .github/:
    - workflows/:
      - build.yaml
      - check.yaml
      - release.yaml
      - test.yaml
  - .gitignore
  - .markdownlint.json
  - .python-version
  - .windsurfrules
  - LICENSE
  - README.md
  # ... and so on
```

### Tree Format
```
git-tree-project-structure-to-yaml/
├── .github/
│   └── workflows/
│       ├── build.yaml
│       ├── check.yaml
│       ├── release.yaml
│       └── test.yaml
├── .gitignore
├── .markdownlint.json
├── .python-version
├── .windsurfrules
├── LICENSE
├── README.md
# ... and so on
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Jamie-BitFlight/git-tree-project-structure-to-yaml.git
cd git-tree-project-structure-to-yaml

# Install development dependencies
uv pip install -e ".[dev]"
```

### Run Tests

```bash
uv run pytest
```

### Code Quality Tools

This project uses:
- Ruff for linting and formatting
- MyPy for type checking
- Pytest for testing

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type check
uv run mypy .
```

## Project Structure

```
git-tree-project-structure-to-yaml/
├── .github/workflows/  # CI/CD configuration
├── scripts/            # Utility scripts
├── src/                # Source code
│   └── git_tree_project_structure_to_yaml/
│       ├── __init__.py
│       └── _cli.py     # Main CLI implementation
├── tests/              # Test suite
│   ├── cli/
│   │   └── test_yaml_tree.py
│   └── structure.yaml
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## License

See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.