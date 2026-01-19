#!/bin/bash
# Initialize a new modernization checkpoint file
# Usage: ./init-checkpoint.sh [project-name]

set -e

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CHECKPOINT_FILE="$PROJECT_ROOT/MODERNIZATION_CHECKPOINT.md"
PROJECT_NAME="${1:-$(basename "$PROJECT_ROOT")}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Check if checkpoint already exists
if [ -f "$CHECKPOINT_FILE" ]; then
    echo "ERROR: Checkpoint file already exists at $CHECKPOINT_FILE"
    echo "To start fresh, first remove the existing checkpoint:"
    echo "  rm $CHECKPOINT_FILE"
    exit 1
fi

# Create checkpoint file
cat > "$CHECKPOINT_FILE" << EOF
# Brownfield Modernization Checkpoint

## Metadata

| Field | Value |
|-------|-------|
| **Status** | Planning |
| **Project** | $PROJECT_NAME |
| **Started** | $TIMESTAMP |
| **Last Updated** | $TIMESTAMP |
| **Current Phase** | 1-Planning |
| **Session ID** | ${CLAUDE_SESSION_ID:-manual} |

---

## Progress Summary

**Phase 1: Planning & Discovery**
- [ ] Architecture Analysis
- [ ] Dependency Mapping
- [ ] Technical Debt Assessment

**Phase 2: Execution**
- [ ] Validation Harness Setup
- [ ] Security Fixes
- [ ] Dependency Upgrades
- [ ] Code Quality Improvements

**Phase 3: Validation & Documentation**
- [ ] Test Coverage Improvement
- [ ] Documentation Generation
- [ ] Final Validation

**Overall Progress**: 0/10 tasks complete (0%)

---

## Agent Status

### Architecture Analyzer
- **Status**: Pending
- **Last Update**: Not started
- **Current Task**: Waiting to begin
- **Results Summary**: Awaiting analysis
- **Output Files**: None yet
- **Blockers**: None

### Dependency Mapper
- **Status**: Pending
- **Last Update**: Not started
- **Current Task**: Waiting to begin
- **Results Summary**: Awaiting analysis
- **Output Files**: None yet
- **Blockers**: None

### Technical Debt Assessor
- **Status**: Pending
- **Last Update**: Not started
- **Current Task**: Waiting to begin
- **Results Summary**: Awaiting analysis
- **Output Files**: None yet
- **Blockers**: None

### Implementation Agent
- **Status**: Pending
- **Last Update**: Not started
- **Current Task**: Waiting for Phase 1 completion
- **Results Summary**: N/A
- **Output Files**: None yet
- **Blockers**: Depends on Phase 1

### Test Coverage Improver
- **Status**: Pending
- **Last Update**: Not started
- **Current Task**: Waiting for Phase 2 completion
- **Results Summary**: N/A
- **Output Files**: None yet
- **Blockers**: Depends on Phase 2

### Documentation Generator
- **Status**: Pending
- **Last Update**: Not started
- **Current Task**: Waiting for Phase 2 completion
- **Results Summary**: N/A
- **Output Files**: None yet
- **Blockers**: Depends on Phase 2

---

## Completed Tasks

*No tasks completed yet*

---

## Pending Tasks

### High Priority
- [ ] **Complete Phase 1 Analysis** (Planning)
  - Architecture analysis
  - Dependency mapping
  - Technical debt assessment

### Medium Priority
- [ ] **Set up Validation Harness** (Phase 2)
  - Configure type checking
  - Configure linting
  - Configure testing

### Scheduled
- [ ] **Execute Modernization Tasks** (Phase 2)
- [ ] **Improve Test Coverage** (Phase 3)
- [ ] **Generate Documentation** (Phase 3)

---

## Blockers & Issues

### Open Blockers

*No blockers identified yet*

### Resolved Blockers

*None*

---

## Decisions Made

*No decisions recorded yet*

---

## Metrics

### Code Quality Metrics

| Metric | Baseline | Current | Target |
|--------|----------|---------|--------|
| Test Coverage | Pending | Pending | 80% |
| Type Coverage | Pending | Pending | 90% |
| Lint Violations | Pending | Pending | 0 |
| Security Issues | Pending | Pending | 0 |

### Progress Metrics

| Phase | Tasks | Completed | Blocked | Remaining |
|-------|-------|-----------|---------|-----------|
| Planning | 3 | 0 | 0 | 3 |
| Execution | 4 | 0 | 0 | 4 |
| Validation | 3 | 0 | 0 | 3 |

---

## Next Actions

When starting or resuming this modernization:

1. **Immediate**: Begin Phase 1 analysis with Architecture Analyzer
2. **Parallel**: Run Dependency Mapper concurrently
3. **Parallel**: Run Technical Debt Assessor concurrently
4. **After Phase 1**: Review findings and plan Phase 2

---

## Session History

| Session | Date | Duration | Tasks Completed | Notes |
|---------|------|----------|-----------------|-------|
| 1 | $TIMESTAMP | - | 0 | Checkpoint initialized |

---

## Reference

- **Checklist**: docs/AI_ASSISTED_BROWNFIELD_MODERNIZATION_CHECKLIST.md
- **Skill Definition**: .claude/skills/brownfield-modernization/SKILL.md
- **Phase Details**: .claude/skills/brownfield-modernization/PHASES.md
EOF

echo "Checkpoint initialized at: $CHECKPOINT_FILE"
echo ""
echo "Next steps:"
echo "1. Review the checkpoint structure"
echo "2. Run /modernize to begin Phase 1"
echo "3. Or ask Claude to 'analyze this codebase for modernization'"
