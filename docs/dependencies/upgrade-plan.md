# Dependency Upgrade Plan

> Generated: 2026-01-19
> Project: git-tree-project-structure-to-yaml v0.1.0

## Executive Summary

| Priority | Count | Action Required |
|----------|-------|-----------------|
| Critical (Security) | 0 | None |
| High (Breaking Changes) | 3 | Plan for major version upgrades |
| Medium (Feature Updates) | 8 | Update when convenient |
| Low (Patch Updates) | 11 | Update during regular maintenance |

**Overall Status**: The project has no known security vulnerabilities. All upgrades are for feature improvements or maintenance.

## Upgrade Priority Matrix

### Priority 1: Critical Security Updates

**None Required** - All dependencies are on secure versions.

---

### Priority 2: High - Major Version Updates (Breaking Changes Possible)

These packages have major version updates available that may include breaking changes.

#### 1. pytest 8.3.5 -> 9.0.2

| Aspect | Details |
|--------|---------|
| Current | 8.3.5 |
| Latest | 9.0.2 |
| Type | Major version |
| Risk | Medium |

**Breaking Changes in pytest 9.x:**
- Requires Python 3.9+
- Some deprecated features removed
- Plugin API changes possible

**Migration Steps:**
1. Review [pytest 9.0 changelog](https://docs.pytest.org/en/stable/changelog.html)
2. Run test suite with `pytest==9.0.2` in isolated environment
3. Update any deprecated test syntax
4. Update pytest plugins (pytest-cov)

**Compatibility Check:**
- pytest-cov 7.0.0 is compatible with pytest 9.x
- inline-snapshot may need update

**Recommendation:** Update together with pytest-cov to 7.0.0

---

#### 2. pytest-cov 6.1.1 -> 7.0.0

| Aspect | Details |
|--------|---------|
| Current | 6.1.1 |
| Latest | 7.0.0 |
| Type | Major version |
| Risk | Low-Medium |

**Breaking Changes:**
- Requires pytest >= 8.0
- Configuration options may have changed

**Migration Steps:**
1. Update alongside pytest
2. Review coverage configuration in pyproject.toml
3. Verify coverage reports generate correctly

**Recommendation:** Bundle with pytest 9.x upgrade

---

#### 3. typer 0.15.4 -> 0.21.1

| Aspect | Details |
|--------|---------|
| Current | 0.15.4 |
| Latest | 0.21.1 |
| Type | Minor version (significant jump) |
| Risk | Medium |

**Notable Changes (0.15 -> 0.21):**
- New CLI features
- Improved type hint support
- Possible API changes

**Migration Steps:**
1. Review [typer changelog](https://typer.tiangolo.com/release-notes/)
2. Test CLI commands thoroughly
3. Update any deprecated option syntax

**Recommendation:** Test in development environment first

---

### Priority 3: Medium - Feature Updates

These updates provide new features or significant improvements.

#### 4. pydantic 2.11.4 -> 2.12.5

| Aspect | Details |
|--------|---------|
| Current | 2.11.4 |
| Latest | 2.12.5 |
| Type | Minor version |
| Risk | Low |

**Changes:**
- Bug fixes
- Performance improvements
- New validation features

**Migration Steps:**
1. Update version constraint: `pydantic>=2.12.0`
2. Run test suite
3. Review any new deprecation warnings

**Recommendation:** Safe to update

---

#### 5. mypy 1.15.0 -> 1.19.1

| Aspect | Details |
|--------|---------|
| Current | 1.15.0 |
| Latest | 1.19.1 |
| Type | Minor version |
| Risk | Low |

**Changes:**
- Improved type inference
- New error codes
- Better Python 3.12+ support

**Migration Steps:**
1. Update version: `mypy>=1.19.0`
2. Run `mypy` and review any new errors
3. Update `pyproject.toml` settings if needed

**Recommendation:** Safe to update, may surface new type errors

---

#### 6. ruff 0.11.10 -> 0.14.13

| Aspect | Details |
|--------|---------|
| Current | 0.11.10 |
| Latest | 0.14.13 |
| Type | Minor version (significant jump) |
| Risk | Low |

**Changes:**
- New lint rules
- Improved formatting
- Better Python 3.12+ support

**Migration Steps:**
1. Update version: `ruff>=0.14.0`
2. Run `ruff check` and `ruff format`
3. Review any new violations
4. Update rule configurations if needed

**Recommendation:** Safe to update, may flag new issues

---

#### 7. inline-snapshot 0.23.0 -> 0.31.1

| Aspect | Details |
|--------|---------|
| Current | 0.23.0 |
| Latest | 0.31.1 |
| Type | Minor version (significant jump) |
| Risk | Low-Medium |

**Changes:**
- New snapshot features
- pytest integration improvements

**Migration Steps:**
1. Update version: `inline-snapshot>=0.31.0`
2. Run tests to verify snapshots still work
3. Review any API changes

**Recommendation:** Update if using snapshot tests actively

---

#### 8. ty 0.0.1a5 -> 0.0.12

| Aspect | Details |
|--------|---------|
| Current | 0.0.1a5 |
| Latest | 0.0.12 |
| Type | Alpha version |
| Risk | Medium |

**Notes:**
- Experimental type checker from Astral
- Rapidly evolving API
- May have significant changes between alpha versions

**Recommendation:** Update for latest features, expect potential breakage

---

#### 9. click 8.1.8 -> 8.3.1 (transitive)

| Aspect | Details |
|--------|---------|
| Current | 8.1.8 |
| Latest | 8.3.1 |
| Required By | typer |
| Type | Minor version |

**Notes:** Will update automatically with typer upgrade.

---

#### 10. rich 14.0.0 -> 14.2.0 (transitive)

| Aspect | Details |
|--------|---------|
| Current | 14.0.0 |
| Latest | 14.2.0 |
| Required By | typer, inline-snapshot |
| Type | Minor version |

**Notes:** Will update automatically with parent dependencies.

---

#### 11. markdown-it-py 3.0.0 -> 4.0.0 (transitive)

| Aspect | Details |
|--------|---------|
| Current | 3.0.0 |
| Latest | 4.0.0 |
| Required By | rich |
| Type | Major version |

**Notes:** Major version update in transitive dependency. Monitor for compatibility issues when updating rich.

---

### Priority 4: Low - Patch Updates

These are minor bug fixes and can be updated during regular maintenance.

| Package | Current | Latest | Type | Notes |
|---------|---------|--------|------|-------|
| gitpython | 3.1.44 | 3.1.46 | Patch | Bug fixes |
| pyyaml | 6.0.2 | 6.0.3 | Patch | Bug fixes |
| types-pyyaml | 6.0.12.20250516 | 6.0.12.20250915 | Patch | Updated type stubs |
| typing-extensions | 4.13.2 | 4.15.0 | Minor | New typing features |
| typing-inspection | 0.4.0 | 0.4.2 | Patch | Bug fixes |
| asttokens | 3.0.0 | 3.0.1 | Patch | Bug fixes |
| coverage | 7.8.1 | 7.13.1 | Minor | Bug fixes, new features |
| executing | 2.2.0 | 2.2.1 | Patch | Bug fixes |
| iniconfig | 2.1.0 | 2.3.0 | Minor | Bug fixes |
| pygments | 2.19.1 | 2.19.2 | Patch | Bug fixes |
| pydantic-core | 2.33.2 | 2.41.5 | Minor | Updates with pydantic |

## Recommended Upgrade Order

### Phase 1: Immediate (Safe Updates)
```bash
# Update patch versions - no breaking changes expected
uv add "gitpython>=3.1.46"
uv add "pyyaml>=6.0.3"
uv add "pydantic>=2.12.0"
uv add --dev "types-pyyaml>=6.0.12.20250915"
```

### Phase 2: Development Tools
```bash
# Update linting and type checking tools
uv add --dev "ruff>=0.14.0"
uv add --dev "mypy>=1.19.0"
uv add --dev "ty>=0.0.12"
```

### Phase 3: Testing Framework (Requires Testing)
```bash
# Update pytest ecosystem together
uv add --dev "pytest>=9.0.0"
uv add --dev "pytest-cov>=7.0.0"
uv add --dev "inline-snapshot>=0.31.0"

# Run test suite
uv run pytest
```

### Phase 4: CLI Framework (Requires Testing)
```bash
# Update typer - test CLI functionality
uv add "typer>=0.21.0"

# Test CLI commands
uv run git-tree-project-structure-to-yaml --help
```

## Compatibility Matrix

| Package | Python 3.12 | Python 3.13 | Notes |
|---------|-------------|-------------|-------|
| gitpython 3.1.46 | Yes | Yes | |
| pydantic 2.12.5 | Yes | Yes | |
| typer 0.21.1 | Yes | Yes | |
| pytest 9.0.2 | Yes | Yes | Requires 3.9+ |
| ruff 0.14.13 | Yes | Yes | |
| mypy 1.19.1 | Yes | Yes | |

## Deprecated/Unmaintained Package Check

All direct dependencies are actively maintained:

| Package | Last Release | Status |
|---------|--------------|--------|
| gitpython | Recent | Active |
| nutree | Recent | Active |
| pydantic | Recent | Very Active |
| pyyaml | Recent | Active |
| typer | Recent | Very Active |
| pytest | Recent | Very Active |
| ruff | Recent | Very Active |
| mypy | Recent | Very Active |

### Potential Concerns

1. **ty** - Alpha software, may be deprecated or significantly changed
2. **rooster-blue** - Pinned to specific git commit, monitor for updates

## Lock File Update Procedure

After making changes to `pyproject.toml`:

```bash
# Update lock file
uv lock

# Verify no dependency conflicts
uv sync

# Run tests to verify compatibility
uv run pytest

# Run type checks
uv run mypy src/
uv run ruff check src/
```

## Rollback Procedure

If an upgrade causes issues:

```bash
# Revert pyproject.toml changes
git checkout pyproject.toml

# Restore lock file
git checkout uv.lock

# Reinstall previous versions
uv sync
```

## Monitoring Recommendations

1. **Security Alerts**: Enable GitHub Dependabot alerts
2. **Release Notifications**: Watch key repositories (pydantic, typer, pytest)
3. **Periodic Review**: Schedule quarterly dependency review
4. **CI Integration**: Add `uv pip list --outdated` to CI pipeline

## Summary

The project is in good health with no security vulnerabilities. The recommended approach is:

1. **Immediate**: Apply patch updates (Phase 1)
2. **This Sprint**: Update development tools (Phase 2)
3. **Planned**: Schedule pytest 9.x migration with testing (Phase 3)
4. **Planned**: Evaluate typer 0.21.x upgrade (Phase 4)

Total estimated effort: 2-4 hours for all upgrades with testing.
