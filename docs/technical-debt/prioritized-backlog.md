# Technical Debt Prioritized Backlog

**Project**: git-tree-project-structure-to-yaml
**Assessment Date**: 2026-01-19
**Assessed By**: Technical Debt Assessor Agent

---

## Priority Scoring Matrix

Each item is scored using the following factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Security Impact | 3x | Potential security vulnerabilities |
| Maintainability Impact | 2x | Affects code readability and future changes |
| Performance Impact | 1x | Affects runtime performance |
| Ease of Fix | 1x | How easy to implement (inverted: easier = higher) |
| Risk of Change | -1x | Risk of introducing bugs (higher = more penalty) |

**Priority Score** = (Security x 3) + (Maintainability x 2) + (Performance x 1) + (Ease x 1) - Risk

### Priority Levels

- **Critical** (Score > 15): Fix immediately
- **High** (Score 10-15): Fix this sprint
- **Medium** (Score 5-10): Schedule for next sprint
- **Low** (Score < 5): Add to backlog

---

## High Priority Items (Score 10-15)

### 1. Improve Test Coverage for `_cli.py`

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 3 | 9 |
| Maintainability | 4 | 8 |
| Performance | 1 | 1 |
| Ease of Fix | 3 | 3 |
| Risk | 2 | -2 |
| **Total** | | **19** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py`
- **Current Coverage**: 31% (124 lines missing)
- **Target Coverage**: 80%
- **Effort**: High (8-12 hours)
- **Description**: Critical functionality including Git operations, error handling, and main CLI flow are untested

**Priority Tests Needed**:
1. `validate_and_return_repo()` - Lines 403-410 (error paths)
2. `validate_and_return_path()` - Lines 429-433 (error paths)
3. `git_lsfiles_to_path_list()` - Lines 122-128 (exception handling)
4. `build_tree_from_git()` - Lines 187-237 (core logic)
5. `main()` - Lines 509-606 (CLI integration)

```python
# Example test to add for error handling
def test_validate_and_return_repo_invalid_path():
    """Test validation with non-git directory."""
    with pytest.raises(SystemExit) as exc_info:
        validate_and_return_repo(Path("/tmp/not-a-repo"))
    assert exc_info.value.code == 1
```

---

### 2. Reduce Complexity of `main()` Function

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 5 | 10 |
| Performance | 1 | 1 |
| Ease of Fix | 3 | 3 |
| Risk | 3 | -3 |
| **Total** | | **14** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:456`
- **Current Complexity**: 14 (threshold: 10)
- **Target Complexity**: < 10
- **Effort**: Medium (4-6 hours)
- **Description**: Extract responsibilities into helper functions

**Recommended Refactoring**:

```python
# Current: All logic in main()

# Proposed: Extract into focused functions
def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    ...

def resolve_paths(
    repo_paths: list[Path] | None,
    repo_path: Path | None,
    repo_as_root: bool
) -> tuple[Path, set[Path]]:
    """Resolve and validate all paths."""
    ...

def generate_output(
    tree: Tree[Path],
    format: OutputFormat,
    options_set: set[str]
) -> str:
    """Generate output in the requested format."""
    ...

def write_output(content: str, output: Path | None) -> None:
    """Write content to file or stdout."""
    ...
```

---

### 3. Reduce Complexity of `build_tree_from_git()` Function

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 4 | 8 |
| Performance | 2 | 2 |
| Ease of Fix | 3 | 3 |
| Risk | 3 | -3 |
| **Total** | | **13** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:156`
- **Current Complexity**: 11 (threshold: 10)
- **Target Complexity**: < 10
- **Effort**: Medium (3-4 hours)
- **Description**: Extract git option building into separate function

**Recommended Refactoring**:

```python
def build_ls_files_args(
    others: bool,
    stage: bool,
    cached: bool,
    exclude_standard: bool,
    exclude: set[str],
    directory: Path
) -> list[str]:
    """Build git ls-files command arguments."""
    args: list[str] = []
    if others:
        args.append("--others")
    if stage:
        args.append("--stage")
    if cached:
        args.append("--cached")
    if exclude_standard:
        args.append("--exclude-standard")
    for pattern in exclude:
        args.append(f"--exclude={pattern}")
    if not others:
        args.append("--recurse-submodules")
    args.append(str(directory))
    return args
```

---

## Medium Priority Items (Score 5-10)

### 4. Fix Deprecated mypy Configuration

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 2 | 4 |
| Performance | 1 | 1 |
| Ease of Fix | 5 | 5 |
| Risk | 1 | -1 |
| **Total** | | **12** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/pyproject.toml:123`
- **Issue**: `strict_concatenate` is deprecated
- **Effort**: Low (5 minutes)
- **Fix**: Replace with `extra_checks`

```toml
# Current
strict_concatenate = true

# Fixed
extra_checks = true
```

---

### 5. Replace Built-in Shadow (`format`)

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 3 | 6 |
| Performance | 1 | 1 |
| Ease of Fix | 5 | 5 |
| Risk | 2 | -2 |
| **Total** | | **13** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:469`
- **Issue**: Parameter `format` shadows Python built-in
- **Effort**: Low (15 minutes)
- **Fix**: Rename to `output_format`

```python
# Current
format: Annotated[OutputFormat, typer.Option("-f", "--format", help="Output format")] = OutputFormat.YAML,

# Fixed
output_format: Annotated[OutputFormat, typer.Option("-f", "--format", help="Output format")] = OutputFormat.YAML,
```

---

### 6. Use `Path.open()` Instead of `open()`

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 2 | 4 |
| Performance | 1 | 1 |
| Ease of Fix | 5 | 5 |
| Risk | 1 | -1 |
| **Total** | | **12** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:598`
- **Issue**: Using `open()` instead of pathlib's `Path.open()`
- **Effort**: Low (5 minutes)
- **Fix**:

```python
# Current
with open(output, "w") as f:
    f.write(output_content)

# Fixed
with output.open("w") as f:
    f.write(output_content)
```

---

### 7. Add Missing Package Docstrings

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 2 | 4 |
| Performance | 1 | 1 |
| Ease of Fix | 5 | 5 |
| Risk | 1 | -1 |
| **Total** | | **12** |

- **Locations**:
  - `/home/user/git-tree-project-structure-to-yaml/tests/__init__.py`
  - `/home/user/git-tree-project-structure-to-yaml/tests/cli/test_yaml_tree.py`
- **Effort**: Low (15 minutes)

---

## Low Priority Items (Score < 5)

### 8. Split Monolithic `_cli.py` File

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 3 | 6 |
| Performance | 1 | 1 |
| Ease of Fix | 2 | 2 |
| Risk | 4 | -4 |
| **Total** | | **8** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py`
- **Issue**: 594 lines in single file
- **Effort**: High (6-8 hours)
- **Risk**: High (affects imports throughout codebase)

**Proposed Structure**:
```
src/git_tree_project_structure_to_yaml/
    __init__.py
    cli.py          # CLI app and command
    enums.py        # IndentType, OutputFormat
    tree.py         # Tree building and formatting
    validators.py   # Path and repo validation
    formatters.py   # YAML and tree formatters
```

---

### 9. Address Boolean Positional Arguments

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 2 | 4 |
| Performance | 1 | 1 |
| Ease of Fix | 2 | 2 |
| Risk | 3 | -3 |
| **Total** | | **7** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py:156, 456`
- **Issue**: Many boolean parameters make function signatures complex
- **Effort**: Medium (2-3 hours)
- **Recommendation**: Consider using a configuration dataclass

```python
from dataclasses import dataclass

@dataclass
class GitTreeOptions:
    """Options for building git tree."""
    others: bool = True
    stage: bool = True
    cached: bool = False
    exclude_standard: bool = True
    exclude: set[str] = field(default_factory=set)
```

---

### 10. Make Shebang File Executable

| Factor | Score (1-5) | Weighted |
|--------|-------------|----------|
| Security | 1 | 3 |
| Maintainability | 1 | 2 |
| Performance | 1 | 1 |
| Ease of Fix | 5 | 5 |
| Risk | 1 | -1 |
| **Total** | | **10** |

- **Location**: `/home/user/git-tree-project-structure-to-yaml/src/git_tree_project_structure_to_yaml/_cli.py`
- **Issue**: Has shebang (`#!/usr/bin/env python3.12`) but file is not executable
- **Effort**: Trivial (1 command)
- **Fix**: `chmod +x src/git_tree_project_structure_to_yaml/_cli.py` OR remove shebang

---

## Remediation Roadmap

### Sprint 1: Quick Wins and Configuration (1-2 days)

| Task | Effort | Priority |
|------|--------|----------|
| Fix deprecated mypy config | 5 min | Medium |
| Rename `format` parameter | 15 min | Medium |
| Use `Path.open()` | 5 min | Medium |
| Add package docstrings | 15 min | Medium |
| Fix/remove shebang | 1 min | Low |

**Estimated Total**: 45 minutes

### Sprint 2: Complexity Reduction (3-5 days)

| Task | Effort | Priority |
|------|--------|----------|
| Extract `build_ls_files_args()` helper | 3-4 hours | High |
| Refactor `main()` into helper functions | 4-6 hours | High |

**Estimated Total**: 7-10 hours

### Sprint 3: Test Coverage Improvement (5-7 days)

| Task | Effort | Priority |
|------|--------|----------|
| Add tests for error handling paths | 2-3 hours | High |
| Add tests for `build_tree_from_git()` | 3-4 hours | High |
| Add integration tests for `main()` | 3-4 hours | High |
| Achieve 80% coverage target | 2-3 hours | High |

**Estimated Total**: 10-14 hours

### Sprint 4: Code Structure (Optional, 1 week)

| Task | Effort | Priority |
|------|--------|----------|
| Split `_cli.py` into modules | 6-8 hours | Low |
| Introduce configuration dataclass | 2-3 hours | Low |
| Update imports and tests | 2-3 hours | Low |

**Estimated Total**: 10-14 hours

---

## Metrics Baseline (For Progress Tracking)

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Test Coverage | 33% | 80% | 47% |
| Type Coverage | 100% | 100% | 0% |
| Core Lint Violations | 0 | 0 | 0 |
| Complexity Violations | 2 | 0 | 2 |
| Max Cyclomatic Complexity | 14 | 10 | 4 |
| Documentation Coverage | ~85% | 95% | ~10% |

---

## Summary Table

| # | Issue | Priority | Effort | Score |
|---|-------|----------|--------|-------|
| 1 | Improve test coverage to 80% | High | High | 19 |
| 2 | Reduce `main()` complexity | High | Medium | 14 |
| 3 | Reduce `build_tree_from_git()` complexity | High | Medium | 13 |
| 4 | Fix deprecated mypy config | Medium | Low | 12 |
| 5 | Rename `format` parameter | Medium | Low | 13 |
| 6 | Use `Path.open()` | Medium | Low | 12 |
| 7 | Add package docstrings | Medium | Low | 12 |
| 8 | Split `_cli.py` file | Low | High | 8 |
| 9 | Refactor boolean arguments | Low | Medium | 7 |
| 10 | Fix shebang permissions | Low | Trivial | 10 |
