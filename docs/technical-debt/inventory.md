# Technical Debt Inventory

**Project**: git-tree-project-structure-to-yaml
**Assessment Date**: 2026-01-19
**Assessed By**: Technical Debt Assessor Agent

---

## Executive Summary

| Category | Count | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Lint Violations (Core) | 0 | 0 | 0 | 0 | 0 |
| Lint Violations (Extended) | 73 | 0 | 5 | 18 | 50 |
| Type Errors | 0 | 0 | 0 | 0 | 0 |
| Complexity Issues | 2 | 0 | 2 | 0 | 0 |
| Coverage Gaps | 1 | 0 | 1 | 0 | 0 |
| Documentation Gaps | 5 | 0 | 0 | 3 | 2 |

**Technical Debt Score**: 4.5/10 (moderate - needs attention)

---

## Current Metrics

### Test Coverage

| File | Statements | Missing | Coverage | Status |
|------|------------|---------|----------|--------|
| `src/git_tree_project_structure_to_yaml/__init__.py` | 3 | 0 | 100% | Good |
| `src/git_tree_project_structure_to_yaml/_cli.py` | 181 | 124 | 31% | Critical |
| **TOTAL** | **184** | **124** | **33%** | **Needs Work** |

**Missing Coverage Lines in `_cli.py`**:
- Lines 122-128: Exception handling in `git_lsfiles_to_path_list`
- Lines 141-153: Tree node creation logic
- Lines 187-237: `build_tree_from_git` core logic
- Line 255: Tree formatting edge case
- Lines 403-410: Repository validation error handling
- Lines 429-433: Path validation error handling
- Line 452: `empty_list_if_none` function
- Lines 509-606: Main function execution flow
- Line 610: Module execution guard

### Code Complexity

| Function | Location | Complexity | Threshold | Status |
|----------|----------|------------|-----------|--------|
| `build_tree_from_git` | `_cli.py:156` | 11 | 10 | Exceeds |
| `main` | `_cli.py:456` | 14 | 10 | Exceeds |

### File Size Metrics

| File | Lines | Threshold | Status |
|------|-------|-----------|--------|
| `_cli.py` | 594 | 500 | Slightly exceeds recommended size |

### Type Coverage

- **mypy Status**: Success - no issues found in 2 source files
- **Type Coverage**: Adequate (types-pyyaml stub package installed)
- **Note**: Deprecation warning for `--strict-concatenate` option in pyproject.toml

---

## Detailed Issue Inventory

### 1. Lint Violations (Core Rules - Currently Enabled)

**Status**: All checks passed

The project has comprehensive ruff configuration with the following rules enabled:
- E (pycodestyle errors)
- F (pyflakes)
- B, B9 (bugbear)
- C4 (flake8-comprehensions)
- SIM (flake8-simplify)
- I (isort)
- UP (pyupgrade)
- PIE (flake8-pie)
- PGH (pygrep-hooks)
- PYI (flake8-pyi)
- RUF (ruff-specific)

### 2. Lint Violations (Extended Rules - Not Currently Enabled)

These are violations against rules not currently enabled in the project configuration:

| Rule | Count | Description | Location |
|------|-------|-------------|----------|
| S101 | 28 | Use of `assert` | tests/*.py (expected in tests) |
| FBT002 | 10 | Boolean default value in positional argument | `_cli.py` |
| ANN001 | 5 | Missing type annotation for function argument | `_cli.py`, tests |
| FBT001 | 4 | Boolean type hint in positional argument | `_cli.py` |
| TRY401 | 4 | Verbose log message (redundant exception info) | `_cli.py` |
| ANN202 | 2 | Missing return type for private function | tests |
| D101 | 2 | Missing docstring in public class | `_cli.py` |
| D104 | 2 | Missing docstring in public package | `__init__.py`, tests |
| PLR0913 | 2 | Too many function arguments (>5) | `_cli.py` |
| A002 | 1 | Argument shadows built-in (`format`) | `_cli.py:469` |
| EXE001 | 1 | Shebang present but file not executable | `_cli.py` |
| PTH123 | 1 | Use `Path.open()` instead of `open()` | `_cli.py:598` |
| PERF401 | 1 | Manual list comprehension opportunity | `_cli.py` |
| D100 | 1 | Missing docstring in public module | tests |
| PLR0912 | 1 | Too many branches (>12) | `_cli.py:main` |
| PLR0915 | 1 | Too many statements (>50) | `_cli.py:main` |
| PLR1704 | 1 | Redefines argument from local scope | `_cli.py` |
| PLR2004 | 1 | Magic value comparison | `_cli.py` |
| TRY300 | 1 | Consider using else clause | `_cli.py` |
| INP001 | 1 | Implicit namespace package | tests |

### 3. Type Checking Issues

**Status**: No issues found

The project has good type coverage with:
- Strict equality checking enabled
- Strict concatenate checking enabled
- Unused configs/casts/ignores warnings enabled
- Missing imports ignored (appropriate for dependencies)

### 4. Complexity Issues

#### Issue 4.1: `build_tree_from_git` Function Too Complex

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:156`
- **Cyclomatic Complexity**: 11 (threshold: 10)
- **Description**: Function handles multiple responsibilities including option building, file listing, and tree construction
- **Contributing Factors**:
  - Multiple conditional branches for different git options (others, stage, cached, exclude_standard)
  - Nested loop for file processing
  - Multiple early returns/conditionals

#### Issue 4.2: `main` Function Too Complex

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:456`
- **Cyclomatic Complexity**: 14 (threshold: 10)
- **Description**: CLI entry point handles too many responsibilities
- **Contributing Factors**:
  - Logging configuration
  - Path validation
  - Repository validation
  - Multiple option processing
  - Output format handling
  - File writing vs stdout
  - Error handling

### 5. Documentation Gaps

| Type | Location | Description |
|------|----------|-------------|
| D104 | `tests/__init__.py` | Missing package docstring |
| D101 | `_cli.py:IndentType` | Missing class docstring (has attribute docs only) |
| D101 | `_cli.py:OutputFormat` | Missing class docstring (has attribute docs only) |
| D100 | `tests/cli/test_yaml_tree.py` | Missing module docstring |
| D104 | `src/git_tree_project_structure_to_yaml/__init__.py` | Limited package documentation |

**Note**: The main `_cli.py` module has excellent documentation with comprehensive docstrings for all public functions.

### 6. Code Structure Issues

#### Issue 6.1: Monolithic CLI File

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py`
- **Lines**: 594
- **Description**: Single file contains all functionality including enums, helpers, tree building, formatters, validators, and CLI command
- **Recommendation**: Consider splitting into:
  - `enums.py` - IndentType, OutputFormat
  - `tree.py` - Tree building and formatting functions
  - `validators.py` - Path and repository validation
  - `cli.py` - CLI command and app setup

#### Issue 6.2: Boolean Arguments in CLI

- **Location**: `_cli.py:456-481` (main function)
- **Description**: Multiple boolean flags (`others`, `stage`, `cached`, `exclude_standard`, `repo_as_root`, `verbose`) as positional arguments
- **Impact**: Makes function signature complex and harder to test

### 7. Deprecated Patterns

| Pattern | Location | Description |
|---------|----------|-------------|
| `--strict-concatenate` | `pyproject.toml:123` | Deprecated mypy option, use `--extra-checks` instead |

---

## Codebase Statistics

```
Source Files: 2
Test Files: 2
Total Lines (src): ~600
Total Lines (tests): ~241
Test/Code Ratio: 0.40

Functions: 17
Classes: 2
Tests: 6
```

---

## Tool Versions Used

| Tool | Version |
|------|---------|
| ruff | 0.11.10 |
| mypy | 1.15.0 |
| pytest | 8.3.5 |
| pytest-cov | 6.1.1 |
| Python | 3.12.3 |
