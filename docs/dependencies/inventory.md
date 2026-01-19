# Dependency Inventory

> Generated: 2026-01-19
> Project: git-tree-project-structure-to-yaml v0.1.0

## Summary

| Category | Count |
|----------|-------|
| Direct Production Dependencies | 7 |
| Direct Dev Dependencies | 6 |
| Release Dependencies | 1 |
| Transitive Dependencies | 33 |
| **Total Packages** | **47** |
| Known Vulnerabilities | 0 (all patched) |
| Outdated Packages | 22 |

## Python Version Requirement

- **Minimum**: Python 3.12+
- **Target**: Python 3.12

## Direct Production Dependencies

| Package | Declared | Locked | Latest | Purpose | Security Status |
|---------|----------|--------|--------|---------|-----------------|
| gitpython | >=3.1.44 | 3.1.44 | 3.1.46 | Git repository interaction and parsing | Safe (CVE-2024-22190 fixed in 3.1.41) |
| nutree | >=1.1.0 | 1.1.0 | 1.1.0 | Tree data structure for directory representation | No known CVEs |
| packaging | >=25.0 | 25.0 | 25.0 | Version parsing and specifiers | No known CVEs |
| pydantic | >=2.11.4 | 2.11.4 | 2.12.5 | Data validation and settings management | Safe (CVE-2024-3772 fixed in 2.4.0) |
| pyyaml | >=6.0.2 | 6.0.2 | 6.0.3 | YAML parsing and serialization | Safe (CVE-2020-14343 fixed in 5.4) |
| typer | >=0.15.4 | 0.15.4 | 0.21.1 | CLI framework with type hints | No known CVEs |
| types-pyyaml | >=6.0.12.20250516 | 6.0.12.20250516 | 6.0.12.20250915 | Type stubs for PyYAML | No known CVEs |

### Dependency Details

#### gitpython (3.1.44)
- **Purpose**: Provides Python interface to Git repositories for reading repository structure
- **License**: BSD-3-Clause
- **Transitive Dependencies**: gitdb -> smmap
- **Notes**: Core functionality for reading git repositories and file trees

#### nutree (1.1.0)
- **Purpose**: Tree data structure library for building hierarchical directory representations
- **License**: MIT
- **Transitive Dependencies**: typing-extensions
- **Notes**: Used to construct the tree output format

#### packaging (25.0)
- **Purpose**: Core utilities for Python packages - version parsing, specifiers, markers
- **License**: BSD-2-Clause or Apache-2.0
- **Transitive Dependencies**: None
- **Notes**: Used for version comparisons

#### pydantic (2.11.4)
- **Purpose**: Data validation using Python type annotations
- **License**: MIT
- **Transitive Dependencies**: annotated-types, pydantic-core, typing-extensions, typing-inspection
- **Notes**: Model definitions and configuration validation

#### pyyaml (6.0.2)
- **Purpose**: YAML parser and emitter for Python
- **License**: MIT
- **Transitive Dependencies**: None
- **Notes**: Core output format generation. Always use `safe_load()` for untrusted input.

#### typer (0.15.4)
- **Purpose**: CLI framework built on top of Click with type hints support
- **License**: MIT
- **Transitive Dependencies**: click, rich, shellingham, typing-extensions
- **Notes**: Provides the command-line interface

#### types-pyyaml (6.0.12.20250516)
- **Purpose**: Type stubs for PyYAML for static type checking
- **License**: Apache-2.0
- **Transitive Dependencies**: None
- **Notes**: Development aid for type checking

## Direct Development Dependencies

| Package | Declared | Locked | Latest | Purpose | Security Status |
|---------|----------|--------|--------|---------|-----------------|
| inline-snapshot | >=0.23.0 | 0.23.0 | 0.31.1 | Snapshot testing for pytest | No known CVEs |
| mypy | >=1.15.0 | 1.15.0 | 1.19.1 | Static type checker | No known CVEs |
| pytest | >=8.3.5 | 8.3.5 | 9.0.2 | Testing framework | No known CVEs |
| pytest-cov | >=6.1.1 | 6.1.1 | 7.0.0 | Coverage plugin for pytest | No known CVEs |
| ruff | >=0.11.10 | 0.11.10 | 0.14.13 | Fast Python linter and formatter | No known CVEs |
| ty | >=0.0.1a5 | 0.0.1a5 | 0.0.12 | Type checking tool (alpha) | No known CVEs |

### Development Dependency Details

#### inline-snapshot (0.23.0)
- **Purpose**: Inline snapshot testing - stores expected values directly in test code
- **Transitive Dependencies**: asttokens, executing, pytest, rich
- **Notes**: Useful for testing YAML/tree output formats

#### mypy (1.15.0)
- **Purpose**: Optional static type checker for Python
- **Transitive Dependencies**: mypy-extensions, typing-extensions
- **Notes**: Used alongside or as alternative to ty

#### pytest (8.3.5)
- **Purpose**: Python testing framework
- **Transitive Dependencies**: iniconfig, packaging, pluggy
- **Notes**: Primary test runner

#### pytest-cov (6.1.1)
- **Purpose**: Code coverage measurement for pytest
- **Transitive Dependencies**: coverage, pytest
- **Notes**: Generates coverage reports

#### ruff (0.11.10)
- **Purpose**: Extremely fast Python linter and formatter (Rust-based)
- **Transitive Dependencies**: None (standalone binary)
- **Notes**: Replaces flake8, isort, and black with superior performance

#### ty (0.0.1a5)
- **Purpose**: New type checker (alpha stage)
- **Transitive Dependencies**: None
- **Notes**: Experimental - from Astral (same as Ruff)

## Release Dependencies

| Package | Source | Purpose |
|---------|--------|---------|
| rooster-blue | Git: zanieb/rooster@cf27242 | Release management and changelog generation |

## Transitive Dependencies

The following packages are installed as dependencies of direct dependencies:

| Package | Version | Required By | Purpose |
|---------|---------|-------------|---------|
| annotated-types | 0.7.0 | pydantic | Runtime support for typing.Annotated |
| anyio | 4.9.0 | httpx, httpcore | Async networking library |
| asttokens | 3.0.0 | inline-snapshot | AST token mapping |
| certifi | 2025.4.26 | httpx, httpcore | CA certificate bundle |
| cffi | 1.17.1 | pygit2 | C FFI interface |
| click | 8.1.8 | typer | CLI toolkit |
| colorama | 0.4.6 | click (Windows) | Terminal colors |
| coverage | 7.8.1 | pytest-cov | Code coverage measurement |
| executing | 2.2.0 | inline-snapshot | Identifying executing AST nodes |
| gitdb | 4.0.12 | gitpython | Git object database |
| h11 | 0.16.0 | httpcore | HTTP/1.1 implementation |
| hishel | 0.1.2 | rooster-blue | HTTP caching |
| httpcore | 1.0.9 | httpx | HTTP transport layer |
| httpx | 0.28.1 | rooster-blue | HTTP client |
| idna | 3.10 | httpx, anyio | Internationalized domain names |
| iniconfig | 2.1.0 | pytest | INI file parsing |
| markdown-it-py | 3.0.0 | rich | Markdown parsing |
| marko | 2.1.3 | rooster-blue | Markdown processing |
| mdurl | 0.1.2 | markdown-it-py | URL utilities for markdown |
| mypy-extensions | 1.1.0 | mypy | Mypy extensions |
| pluggy | 1.6.0 | pytest | Plugin framework |
| pycparser | 2.22 | cffi | C parser |
| pydantic-core | 2.33.2 | pydantic | Core validation logic (Rust) |
| pygit2 | 1.18.0 | rooster-blue | Git bindings |
| pygments | 2.19.1 | rich | Syntax highlighting |
| rich | 14.0.0 | typer, inline-snapshot | Terminal formatting |
| shellingham | 1.5.4 | typer | Shell detection |
| smmap | 5.0.2 | gitdb | Sliding window memory map |
| sniffio | 1.3.1 | anyio | Async library detection |
| tqdm | 4.67.1 | rooster-blue | Progress bars |
| typing-extensions | 4.13.2 | multiple | Typing backports |
| typing-inspection | 0.4.0 | pydantic | Runtime typing introspection |

## Dependency Tree

```
git-tree-project-structure-to-yaml v0.1.0
├── gitpython v3.1.44
│   └── gitdb v4.0.12
│       └── smmap v5.0.2
├── nutree v1.1.0
│   └── typing-extensions v4.13.2
├── packaging v25.0
├── pydantic v2.11.4
│   ├── annotated-types v0.7.0
│   ├── pydantic-core v2.33.2
│   │   └── typing-extensions v4.13.2
│   ├── typing-extensions v4.13.2
│   └── typing-inspection v0.4.0
│       └── typing-extensions v4.13.2
├── pyyaml v6.0.2
├── typer v0.15.4
│   ├── click v8.1.8
│   ├── rich v14.0.0
│   │   ├── markdown-it-py v3.0.0
│   │   │   └── mdurl v0.1.2
│   │   └── pygments v2.19.1
│   ├── shellingham v1.5.4
│   └── typing-extensions v4.13.2
├── types-pyyaml v6.0.12.20250516
├── inline-snapshot v0.23.0 (dev)
│   ├── asttokens v3.0.0
│   ├── executing v2.2.0
│   ├── pytest v8.3.5
│   │   ├── iniconfig v2.1.0
│   │   ├── packaging v25.0
│   │   └── pluggy v1.6.0
│   └── rich v14.0.0 (*)
├── mypy v1.15.0 (dev)
│   ├── mypy-extensions v1.1.0
│   └── typing-extensions v4.13.2
├── pytest v8.3.5 (dev) (*)
├── pytest-cov v6.1.1 (dev)
│   ├── coverage v7.8.1
│   └── pytest v8.3.5 (*)
├── ruff v0.11.10 (dev)
└── ty v0.0.1a5 (dev)

(*) Package tree already displayed
```

## Security Vulnerabilities

### Critical
*None found*

### High
*None found*

### Medium
*None found*

### Low
*None found*

### Historical (Patched)

All historical vulnerabilities in the dependency chain have been addressed:

| CVE | Package | Affected | Fixed | Current | Status |
|-----|---------|----------|-------|---------|--------|
| CVE-2024-22190 | gitpython | <3.1.41 | 3.1.41 | 3.1.44 | PATCHED |
| CVE-2024-3772 | pydantic | <2.4.0 | 2.4.0 | 2.11.4 | PATCHED |
| CVE-2020-14343 | pyyaml | <5.4 | 5.4 | 6.0.2 | PATCHED |

## Version Pinning Strategy

The project uses **minimum version pinning** (`>=`) rather than exact pinning:

**Advantages:**
- Allows automatic security patches
- Reduces maintenance burden
- Better compatibility with other packages

**Risks:**
- Potential for breaking changes on major updates
- Less reproducible builds without lock file

**Mitigation:**
- `uv.lock` provides exact reproducibility
- Dependency groups separate runtime from dev dependencies

## Node.js Dependencies (package.json)

| Package | Version | Purpose |
|---------|---------|---------|
| @biomejs/biome | 1.9.4 (dev) | JavaScript/TypeScript linter and formatter |

This is used for linting configuration files (JSON, etc.) but not for the core Python application.

## Build System

| Package | Version | Purpose |
|---------|---------|---------|
| uv_build | >=0.6.16,<0.8 | Build backend for Python packages |

## References

- [GitPython Security Advisories](https://security.snyk.io/package/pip/gitpython)
- [Pydantic Security Advisories](https://security.snyk.io/package/pip/pydantic)
- [PyYAML Security Advisories](https://security.snyk.io/package/pip/pyyaml)
- [GitHub Advisory Database](https://github.com/advisories)
