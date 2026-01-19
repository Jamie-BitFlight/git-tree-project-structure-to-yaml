# Modernization Phases

Detailed documentation of each phase in the brownfield modernization process.

---

## Phase 1: Planning & Discovery

**Objective**: Build comprehensive understanding of the current codebase state before making changes.

**Principle**: Never modify what you don't understand. Analysis must be verified before planning begins.

### Subagent: Architecture Analyzer

**Purpose**: Map the current system architecture and identify improvement opportunities.

**Tasks**:
1. Parse all source files using AST analysis
2. Build module dependency graph
3. Identify architectural layers (presentation, business logic, data access)
4. Detect layering violations (e.g., UI directly accessing database)
5. Document component responsibilities
6. Identify coupling hotspots

**Verification Loop**:
```
1. Generate initial architecture diagram
2. Verification questions:
   - Do runtime imports match static analysis?
   - Are there dynamic dependencies via getattr/importlib?
   - Do test imports match production imports?
3. Cross-reference with actual execution traces
4. Correct architecture diagram with verified dependencies
```

**Output Files**:
- `docs/architecture/current-state.md`
- `docs/architecture/dependency-graph.md`
- `docs/architecture/violations.md`

**Checkpoint Update**:
```markdown
### Architecture Analyzer
- **Status**: Completed
- **Last Update**: [timestamp]
- **Findings**:
  - Modules analyzed: 47
  - Architectural violations: 12
  - Coupling hotspots: 3
- **Output Files**: docs/architecture/*.md
```

---

### Subagent: Dependency Mapper

**Purpose**: Audit all external dependencies for security, currency, and compatibility.

**Tasks**:
1. Parse all dependency declaration files (pyproject.toml, requirements.txt, etc.)
2. Cross-reference with lock files for actual resolved versions
3. Check each dependency against:
   - Known vulnerabilities (CVE database)
   - End-of-life status
   - Latest available version
   - Breaking changes in upgrade path
4. Build compatibility matrix for Python version upgrades
5. Identify transitive dependencies that may cause issues

**Verification Loop**:
```
1. Generate dependency inventory
2. Verification:
   - Run: pip-audit for vulnerability check
   - Run: pip list --outdated for version check
   - Compare declared vs locked versions
3. For each vulnerable/outdated package:
   - Check if update has breaking changes
   - Verify compatibility with other dependencies
4. Produce validated upgrade plan
```

**Output Files**:
- `docs/dependencies/inventory.md`
- `docs/dependencies/vulnerabilities.md`
- `docs/dependencies/upgrade-plan.md`

**Checkpoint Update**:
```markdown
### Dependency Mapper
- **Status**: Completed
- **Last Update**: [timestamp]
- **Findings**:
  - Direct dependencies: 24
  - Transitive dependencies: 156
  - Vulnerabilities found: 3 (2 high, 1 medium)
  - Outdated packages: 8
- **Output Files**: docs/dependencies/*.md
```

---

### Subagent: Technical Debt Assessor

**Purpose**: Quantify and prioritize technical debt for remediation.

**Tasks**:
1. Run comprehensive linting (ruff with all rules)
2. Run type checking (mypy strict mode)
3. Measure test coverage
4. Calculate code complexity (cyclomatic, cognitive)
5. Identify code duplication
6. Check for security anti-patterns
7. Assess documentation coverage

**Verification Loop**:
```
1. Run all static analysis tools
2. Categorize findings by:
   - Severity (critical, high, medium, low)
   - Effort to fix (quick, moderate, significant)
   - Risk of change (isolated, moderate, widespread)
3. Prioritize: High severity + low effort + low risk = do first
4. Validate prioritization against historical incident data
```

**Output Files**:
- `docs/technical-debt/inventory.md`
- `docs/technical-debt/prioritized-backlog.md`
- `docs/technical-debt/metrics-baseline.md`

**Checkpoint Update**:
```markdown
### Technical Debt Assessor
- **Status**: Completed
- **Last Update**: [timestamp]
- **Findings**:
  - Lint violations: 234 (47 high priority)
  - Type errors: 89
  - Test coverage: 67%
  - Complexity hotspots: 12 functions above threshold
- **Output Files**: docs/technical-debt/*.md
```

---

## Phase 2: Execution

**Objective**: Implement modernization improvements with continuous validation.

**Principle**: Every change must pass all validation gates. Self-correct on failure.

### Task 2.1: Validation Harness Setup

**Purpose**: Establish automated quality gates that will catch regressions.

**Tasks**:
1. Configure type checking (mypy with strict settings)
2. Configure linting (ruff with project-appropriate rules)
3. Configure test runner with coverage requirements
4. Configure security scanning (bandit)
5. Set up pre-commit hooks
6. Configure CI pipeline with all gates

**Verification**:
```
1. Introduce intentional type error → mypy catches it
2. Introduce intentional lint violation → ruff catches it
3. Break a test → pytest fails the build
4. Introduce security issue → bandit catches it
5. All hooks run on commit attempt
```

**Configuration Files Created**:
- `pyproject.toml` (tool configurations)
- `.pre-commit-config.yaml`
- `.github/workflows/ci.yml`

---

### Task 2.2: Priority Modernization Tasks

**Purpose**: Execute the highest-impact improvements identified in Phase 1.

**Task Selection Criteria**:
1. Fixes security vulnerabilities (highest priority)
2. Resolves breaking dependency issues
3. Reduces critical technical debt
4. Improves test coverage in high-risk areas

**Execution Pattern**:
```
For each task:
1. Create isolated branch
2. Implement change
3. Run validation gates:
   - ruff check src/
   - mypy src/
   - pytest tests/
   - bandit -r src/
4. If any gate fails:
   - Analyze failure
   - Self-correct
   - Re-run gates
   - Max 3 attempts, then mark as blocked
5. If all gates pass:
   - Update checkpoint
   - Commit change
   - Proceed to next task
```

**Checkpoint Update Pattern**:
```markdown
## Completed Tasks
- [x] Fix SQL injection in auth.py:45 (security)
- [x] Upgrade pydantic 1.x → 2.x (dependency)
- [x] Add type hints to core module (quality)

## In Progress
- [ ] Refactor authentication service (Task 2.2.4)
  - Started: [timestamp]
  - Progress: 60% complete
  - Blocked: None
```

---

## Phase 3: Validation & Documentation

**Objective**: Ensure changes are well-tested and documented.

**Principle**: Documentation must be verified against actual code. Claims must be factual.

### Subagent: Test Coverage Improver

**Purpose**: Increase test coverage to target threshold (typically 80%+).

**Tasks**:
1. Identify untested code paths using coverage report
2. Prioritize by:
   - Risk (high-risk code needs tests first)
   - Complexity (complex code more likely to have bugs)
   - Recent changes (new code should be tested)
3. Write tests for uncovered code
4. Ensure tests are meaningful (not just coverage gaming)

**Verification Loop**:
```
1. Generate coverage report
2. For each untested function:
   - Understand function purpose
   - Identify edge cases
   - Write test cases
   - Verify tests actually exercise the code
3. Re-run coverage
4. Verify improvement meets target
```

**Test Quality Checks**:
- Tests have meaningful assertions (not just `assert True`)
- Tests cover edge cases and error paths
- Tests are isolated (no shared state)
- Tests run quickly (< 100ms each for unit tests)

---

### Subagent: Documentation Generator

**Purpose**: Create comprehensive, accurate documentation.

**Tasks**:
1. Generate README for each directory
2. Document each module's purpose
3. Create API documentation
4. Document configuration options
5. Create developer onboarding guide

**Verification Loop**:
```
1. Generate initial documentation
2. Verification:
   - List actual files in directory
   - Compare with documented files
   - Verify all files are documented
3. For each documented function:
   - Verify signature matches actual code
   - Verify description matches behavior
   - Test any code examples
4. Correct any inaccuracies
5. Add missing documentation
```

**Anti-Hallucination Protocol**:
```
Before documenting any claim:
1. Verify via code inspection
2. Verify via test execution (if applicable)
3. Include file:line references
4. If uncertain, mark as "needs verification"

Never document:
- Features that don't exist
- Versions that aren't current
- Configurations that aren't used
- Performance claims without benchmarks
```

**Output Structure**:
```
docs/
├── README.md                 # Project overview
├── ARCHITECTURE.md           # System architecture
├── DEVELOPMENT.md            # Developer guide
├── API.md                    # API documentation
└── directories/
    └── [dir-name]/
        └── README.md         # Per-directory docs
```

---

## Phase Transitions

### Phase 1 → Phase 2 Criteria

- [ ] Architecture analysis complete and verified
- [ ] Dependency audit complete with upgrade plan
- [ ] Technical debt inventory complete and prioritized
- [ ] All Phase 1 agents marked "Completed" in checkpoint
- [ ] Checkpoint committed to version control

### Phase 2 → Phase 3 Criteria

- [ ] Validation harness fully configured and tested
- [ ] All critical/high priority tasks completed
- [ ] All validation gates passing
- [ ] No security vulnerabilities in completed code
- [ ] Checkpoint reflects all completed work

### Phase 3 → Complete Criteria

- [ ] Test coverage meets target threshold
- [ ] All directories have README files
- [ ] Documentation accuracy verified
- [ ] All code examples tested
- [ ] Final checkpoint committed
- [ ] Summary report generated

---

## Parallel Execution Guidelines

### Safe to Run in Parallel

**Phase 1**: All three analyzers can run concurrently
- They only read code, no modifications
- No dependencies between their outputs
- Faster completion with parallel execution

**Phase 3**: Test improver and documentation generator can run concurrently
- Tests and docs are independent concerns
- Both can read the same codebase safely
- Documentation doesn't depend on new tests

### Must Run Sequentially

**Phase 2**: Most execution tasks must be sequential
- Changes may conflict if run in parallel
- Validation gates need stable codebase
- Each change should be committed before next begins

**Exception**: Independent modules can be modernized in parallel if:
- No shared dependencies
- No cross-module changes
- Separate git branches used

### Coordination Protocol

When running parallel agents:
```
1. Each agent writes to its own checkpoint section
2. Main orchestrator aggregates results
3. Conflicts resolved by orchestrator
4. Final checkpoint is single source of truth
```
