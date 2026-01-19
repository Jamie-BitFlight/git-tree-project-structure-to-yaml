# AI-Assisted Brownfield Modernization Checklist

> A comprehensive guide for systematic, validated AI-assisted modernization of brownfield projects using Chain-of-Verification (CoVe), self-correction loops, and validation harnesses.

## Overview

This checklist enables AI developers to self-correct through continuous validation, produce accurate architectural understanding, generate comprehensive modernization plans, and create navigable documentation that eliminates ambiguity for human development teams.

### Key Principles

1. **Chain-of-Verification (CoVe)**: AI generates initial response → generates verification questions → answers them → produces final verified output
2. **Self-Correction Loops**: AI validates outputs against ground truth (test results, type checks, linting)
3. **Prompt Harnesses**: Structured frameworks that enforce validation steps before accepting AI outputs
4. **Checkpoint-Based Resumption**: Progress tracking enables continuation from last known state

---

## Phase 1: Repository Analysis & Baseline Establishment

### 1.1 Initial Codebase Inventory with Verification Loop

**Best Practice:** Use AST parsing to catalog all code entities, then verify completeness through cross-referencing.

**Example:**
```
Step 1 (Analysis): Parse repository with tree-sitter/AST tools
- Generate inventory: 247 functions, 89 classes, 34 modules

Step 2 (Verification Questions):
- Are there any dynamic imports not captured by static AST?
- Do file counts match directory traversal results?
- Are generated/build files excluded from analysis?

Step 3 (Verification Execution):
- Run: find . -name "*.py" | wc -l → Compare with AST file count
- Check import statements for exec() or __import__() patterns
- Validate .gitignore exclusions applied

Step 4 (Corrected Output):
- Actual inventory: 247 functions, 89 classes, 34 modules, 12 dynamic imports flagged for manual review
```

**Validation Checklist:**
- [ ] AST parser configured for all project languages
- [ ] Dynamic import patterns identified and documented
- [ ] Generated files excluded from analysis
- [ ] File counts verified against directory traversal
- [ ] Results documented in checkpoint file

---

### 1.2 Dependency Graph Construction with CodeQL Validation

**Best Practice:** Build dependency graph, then validate against CodeQL queries for hidden dependencies.

**Example:**
```
Step 1 (Initial Graph): Create dependency map using import analysis
Module A → Module B → Module C

Step 2 (CodeQL Verification):
codeql query run --database=./codeql-db \
  --query="import python \
           from Import i \
           select i.getEnclosingModule(), i.getImportedModule()"

Step 3 (Self-Correction):
- CodeQL reveals: Module A also has runtime dependency on Module D via getattr()
- Updated graph: Module A → [Module B, Module D*] → Module C
- Flag D* as runtime dependency requiring integration testing
```

**Validation Checklist:**
- [ ] Static import analysis completed
- [ ] CodeQL database created for codebase
- [ ] Runtime dependencies identified (getattr, importlib, etc.)
- [ ] Circular dependencies detected and documented
- [ ] Dependency graph exported to visualization format

---

### 1.3 Security & Quality Baseline with Fact-Checking

**Best Practice:** Run CodeQL security queries, verify findings against false-positive database.

**Example:**
```
Step 1 (Scan): codeql analyze --format=sarif-latest
- Result: 23 SQL injection vulnerabilities detected

Step 2 (Verification Loop):
- For each finding, check if parameterized queries exist
- Cross-reference with ORM usage patterns
- Test: Run actual SQL injection attempt in isolated environment

Step 3 (Validated Output):
- 23 findings → 8 true positives, 15 false positives (ORM-protected)
- Document: "8 SQL injection points require parameterization in auth.py:45, users.py:123..."
```

**Validation Checklist:**
- [ ] CodeQL security scan completed
- [ ] Each finding verified for true/false positive status
- [ ] ORM and framework protections documented
- [ ] True positives prioritized by severity
- [ ] Remediation plan created for each true positive

---

### 1.4 Technology Stack Assessment

**Best Practice:** Inventory all technologies, verify versions against official sources.

**Example:**
```
Step 1 (Discovery):
- Package manager files: pyproject.toml, package.json, Cargo.toml
- Runtime configs: Dockerfile, docker-compose.yml
- CI configs: .github/workflows/*.yml

Step 2 (Verification):
- Cross-reference declared versions with lock files
- Check for version mismatches between environments
- Verify compatibility matrices

Step 3 (Validated Inventory):
| Technology | Declared | Lock File | Latest | EOL Status |
|------------|----------|-----------|--------|------------|
| Python     | 3.12     | 3.12.1    | 3.12.1 | Supported  |
| pytest     | ^8.0     | 8.3.5     | 8.3.5  | Current    |
```

**Validation Checklist:**
- [ ] All dependency files identified
- [ ] Lock files present and consistent
- [ ] Version pinning strategy documented
- [ ] EOL/deprecated packages identified
- [ ] Compatibility matrix created

---

## Phase 2: Validation Harness Setup

### 2.1 Type Checking Infrastructure with Self-Correction

**Best Practice:** Implement strict type checking, use failures as ground truth for AI corrections.

**Example:**
```
Step 1 (Setup): Add mypy with strict configuration
[mypy]
strict = true
warn_return_any = true
disallow_untyped_defs = true

Step 2 (AI Adds Types): AI suggests type annotations
def process_data(data):  # Before
def process_data(data: List[Dict[str, Any]]) -> pd.DataFrame:  # After

Step 3 (Validation Loop):
- Run: mypy src/
- Error: "Argument 1 has incompatible type List[Dict[str, str]]"
- AI Self-Correction: Analyze actual data flow
- Corrected: def process_data(data: List[Dict[str, Union[str, int]]]) -> pd.DataFrame:

Step 4 (Verify): mypy passes → Accept change
```

**Configuration Template (pyproject.toml):**
```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
```

**Validation Checklist:**
- [ ] Type checker configured with strict settings
- [ ] Baseline type errors documented
- [ ] Type stubs installed for third-party packages
- [ ] CI pipeline includes type checking gate
- [ ] Type coverage metrics tracked

---

### 2.2 Linting Rules as Validation Gates

**Best Practice:** Configure linters as automatic hallucination detectors.

**Example:**
```
Step 1 (Configure): ruff.toml with comprehensive rules
[lint]
select = ["E", "F", "B", "C4", "SIM", "I", "UP", "PIE", "PGH", "PYI", "RUF"]

Step 2 (AI Refactors Code):
# AI suggests:
def calculate_total(items):
    sum = 0  # Shadows built-in
    for item in items:
        sum += item.price
    return sum

Step 3 (Linting Catches Error):
ruff check src/calculator.py
→ A001: Variable `sum` is shadowing a Python builtin

Step 4 (AI Self-Correction):
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
```

**Configuration Template (pyproject.toml):**
```toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "I",   # isort
    "UP",  # pyupgrade
    "PIE", # flake8-pie
    "PGH", # pygrep-hooks
    "PYI", # flake8-pyi
    "RUF", # ruff-specific rules
]

[tool.ruff.lint.mccabe]
max-complexity = 10
```

**Validation Checklist:**
- [ ] Linter configured with project-appropriate rules
- [ ] Baseline lint errors documented
- [ ] Auto-fix rules enabled where safe
- [ ] CI pipeline includes linting gate
- [ ] Pre-commit hooks configured

---

### 2.3 Test Harness as Ground Truth

**Best Practice:** Existing tests must pass; new code requires tests before acceptance.

**Example:**
```
Step 1 (Baseline): Run existing test suite
pytest tests/ --cov=src
→ 156 passed, 12 failed, 67% coverage

Step 2 (AI Refactors Module):
# AI modernizes authentication.py

Step 3 (Validation Gate):
pytest tests/test_authentication.py
→ 8 passed, 4 failed

Step 4 (Self-Correction Loop):
- AI analyzes failures: "Expected bcrypt, code uses argon2"
- AI checks git history: "Migration to argon2 in commit abc123"
- AI corrects refactoring to preserve argon2
- Rerun: 12 passed, 0 failed → Accept change

Step 5 (New Test Requirement):
- AI adds new feature: rate limiting
- Validation gate: "No tests found for rate_limiter.py"
- AI generates tests before feature accepted
```

**Validation Checklist:**
- [ ] Test suite runs successfully
- [ ] Coverage baseline established
- [ ] Coverage thresholds configured
- [ ] Test isolation verified (no shared state)
- [ ] CI pipeline includes test gate with coverage reporting

---

### 2.4 Pre-Commit Validation Harness

**Best Practice:** Implement automated validation before any code is committed.

**Configuration Template (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.10
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest
        entry: pytest tests/ -x -q
        language: system
        pass_filenames: false
        always_run: true

      - id: security-scan
        name: Security Scan (bandit)
        entry: bandit -r src/ -ll
        language: system
        pass_filenames: false
```

**Validation Flow:**
1. Developer commits code
2. Pre-commit hook triggers all checks
3. Any failure blocks commit
4. Developer sees specific error
5. Developer fixes issue
6. Retry commit → Success only when all checks pass

**Validation Checklist:**
- [ ] Pre-commit hooks installed
- [ ] All validation tools configured as hooks
- [ ] Hooks tested locally
- [ ] Team onboarded to pre-commit workflow
- [ ] CI validates pre-commit configuration

---

## Phase 3: Architecture Documentation with Verification

### 3.1 System Architecture Mapping with Cross-Validation

**Best Practice:** Generate architecture diagrams, validate against actual runtime behavior.

**Example:**
```
Step 1 (Static Analysis): AI analyzes imports and class relationships
Generated architecture:
[Web Layer] → [Service Layer] → [Data Layer]

Step 2 (Verification Questions):
- Does runtime behavior match static structure?
- Are there circular dependencies?
- Do deployment boundaries align with logical boundaries?

Step 3 (Runtime Validation):
- Add logging to trace actual call paths
- Run integration tests with call graph profiling
- Result: Service Layer directly calls Database in 3 locations (bypasses Data Layer)

Step 4 (Corrected Architecture):
[Web Layer] → [Service Layer] ⇄ [Data Layer]
                ↓ (3 legacy paths - marked for refactoring)
            [Database]
```

**Validation Checklist:**
- [ ] Static architecture diagram generated
- [ ] Runtime call paths traced and documented
- [ ] Architectural violations identified
- [ ] Layering rules documented
- [ ] Refactoring priorities established

---

### 3.2 Component Relationship Documentation with Fact-Checking

**Best Practice:** Document each component's purpose, validate against actual usage.

**Example:**
```
Step 1 (AI Documentation):
"UserService: Handles user authentication and profile management"

Step 2 (Verification):
- Grep codebase: grep -r "UserService" --include="*.py"
- Find actual usage: Also handles email notifications, password resets, session management

Step 3 (Self-Correction):
"UserService: Manages user lifecycle including authentication, profile management,
session handling, password resets, and user-related email notifications.
Note: Email functionality should be extracted to NotificationService (see issue #234)"

Step 4 (Cross-Reference):
- Check issue tracker: Issue #234 exists and confirms planned refactoring
- Validate: Documentation now matches reality + planned improvements
```

**Validation Checklist:**
- [ ] All components documented with purpose
- [ ] Usage patterns verified via code search
- [ ] Responsibilities accurately described
- [ ] Technical debt noted with issue references
- [ ] Dependencies between components mapped

---

### 3.3 Data Flow Documentation

**Best Practice:** Document data flows, validate against actual database queries and API calls.

**Example:**
```
Step 1 (AI Documents Data Flow):
User Registration: Form → API → UserService → Database

Step 2 (Verification):
- Trace actual request path with logging
- Check for middleware, validators, event handlers
- Result: Missing EmailService call, missing audit logging

Step 3 (Corrected Flow):
User Registration:
  Form → [Validation Middleware] → API → UserService
       → [AuditLogger] → Database
       → [EmailService] → Email Provider
```

**Validation Checklist:**
- [ ] Critical data flows documented
- [ ] Request paths traced end-to-end
- [ ] Middleware and interceptors included
- [ ] Side effects documented (logging, notifications)
- [ ] Error paths documented

---

## Phase 4: Modernization Planning with Validation

### 4.1 Task Breakdown with Dependency Validation

**Best Practice:** Generate task list, validate dependencies through build simulation.

**Example:**
```
Step 1 (AI Task Generation):
Task 1: Upgrade Python 3.7 → 3.11
Task 2: Migrate unittest → pytest
Task 3: Add type hints
Task 4: Update dependencies

Step 2 (Dependency Verification):
- Question: Can we upgrade Python before updating dependencies?
- Simulate: Create test branch, attempt Python upgrade
- Result: 12 dependencies incompatible with Python 3.11

Step 3 (Corrected Task Order):
Task 1: Audit dependencies for Python 3.11 compatibility
Task 2: Update/replace incompatible dependencies
Task 3: Upgrade Python 3.7 → 3.11
Task 4: Migrate unittest → pytest (benefits from Python 3.11 features)
Task 5: Add type hints (use Python 3.11 syntax)

Step 4 (Validation):
- Each task includes rollback plan
- Each task has acceptance criteria with automated tests
```

**Validation Checklist:**
- [ ] Tasks ordered by dependency
- [ ] Each task has clear acceptance criteria
- [ ] Rollback plan documented for each task
- [ ] Dependencies verified through simulation
- [ ] Blockers identified upfront

---

### 4.2 Risk Assessment with Historical Validation

**Best Practice:** Identify high-risk changes, validate risk level against similar past changes.

**Example:**
```
Step 1 (AI Risk Assessment):
"Refactoring authentication system: Medium Risk"

Step 2 (Verification Questions):
- What was the impact of previous auth changes?
- How many systems depend on current auth implementation?
- What is test coverage for auth module?

Step 3 (Historical Analysis):
- Git log: Last auth change (2 years ago) caused 3-day outage
- Dependency scan: 47 modules import authentication
- Coverage: 34% (below project average of 67%)

Step 4 (Corrected Risk Assessment):
"Refactoring authentication system: HIGH RISK
- Previous auth changes caused production outages
- 47 dependent modules require regression testing
- Test coverage must increase to 90% before refactoring
- Requires feature flag for gradual rollout
- Mitigation: 6-phase rollout with 2-week parallel run period"
```

**Risk Assessment Matrix:**
| Factor | Low | Medium | High | Critical |
|--------|-----|--------|------|----------|
| Dependencies | <5 | 5-20 | 20-50 | >50 |
| Test Coverage | >80% | 60-80% | 40-60% | <40% |
| Past Incidents | None | Minor | Outage | Data Loss |
| Rollback Time | <1min | <1hr | <1day | >1day |

**Validation Checklist:**
- [ ] All tasks risk-assessed
- [ ] Historical incidents reviewed
- [ ] Dependency count verified
- [ ] Test coverage measured
- [ ] Mitigation strategies documented

---

### 4.3 Modernization Roadmap Creation

**Best Practice:** Create phased roadmap, validate feasibility with proof-of-concept.

**Example:**
```
Step 1 (AI Roadmap):
Phase 1: Infrastructure modernization
Phase 2: Code quality improvements
Phase 3: Architecture refactoring
Phase 4: Performance optimization

Step 2 (Feasibility Verification):
- For each phase, identify smallest demonstrable change
- Implement proof-of-concept in isolated branch
- Validate assumptions and identify unknowns

Step 3 (Validated Roadmap):
Phase 1: Infrastructure (PoC: Dockerize single service - verified)
  - Milestone 1.1: Container all services
  - Milestone 1.2: CI/CD pipeline
  - Milestone 1.3: Infrastructure as Code
Phase 2: Quality (PoC: Add types to core module - verified)
  - Milestone 2.1: Type checking infrastructure
  - Milestone 2.2: Linting standardization
  - Milestone 2.3: Test coverage improvement
```

**Validation Checklist:**
- [ ] Phases logically ordered
- [ ] Each phase has proof-of-concept
- [ ] Dependencies between phases documented
- [ ] Success criteria defined per milestone
- [ ] Rollback points identified

---

## Phase 5: CI/CD Pipeline Development with Validation

### 5.1 Pipeline Design with Failure Simulation

**Best Practice:** Design pipeline stages, validate by simulating failure scenarios.

**Example:**
```
Step 1 (AI Pipeline Design):
stages:
  - lint
  - test
  - build
  - deploy

Step 2 (Verification Questions):
- What happens if linting fails but tests pass?
- Can we deploy if build succeeds but tests are skipped?
- How do we handle flaky tests?

Step 3 (Failure Simulation):
- Introduce intentional lint error → Pipeline should stop
- Skip test stage → Pipeline should fail
- Test: 1 flaky test fails → Entire deployment blocked

Step 4 (Corrected Pipeline):
stages:
  - lint (blocking)
  - security-scan (blocking)
  - unit-tests (blocking, retry flaky tests 3x)
  - integration-tests (blocking)
  - build (blocking)
  - smoke-tests (blocking)
  - deploy-staging (manual approval)
  - deploy-production (manual approval + 4-eyes)

validation:
  - All stages must explicitly pass (no skips allowed)
  - Flaky tests isolated and tracked in separate job
```

**GitHub Actions Template:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: ruff check src/
      - name: Format Check
        run: ruff format --check src/

  security:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - name: Security Scan
        run: bandit -r src/ -ll

  test:
    runs-on: ubuntu-latest
    needs: security
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: pytest tests/ --cov=src --cov-fail-under=80

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: python -m build

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: Deploy to Staging
        run: echo "Deploy to staging"
```

**Validation Checklist:**
- [ ] All pipeline stages defined
- [ ] Failure scenarios tested
- [ ] Stage dependencies correct
- [ ] Flaky test handling configured
- [ ] Manual approval gates configured

---

### 5.2 Docker Build Optimization with Validation

**Best Practice:** Create Docker images, validate build reproducibility and layer caching.

**Example:**
```
Step 1 (AI Dockerfile):
FROM python:3.11
COPY . /app
RUN pip install -r requirements.txt

Step 2 (Verification):
- Build twice: Compare image hashes
- Result: Different hashes (non-reproducible)
- Check: pip installs latest versions, not pinned

Step 3 (Self-Correction):
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app
WORKDIR /app

Step 4 (Validation):
- Build twice: Hashes match ✓
- Test layer caching: Change source code, only final layer rebuilds ✓
- Verify: docker history shows optimized layers ✓
```

**Optimized Dockerfile Template:**
```dockerfile
# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application code
COPY src/ ./src/

# Non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

CMD ["python", "-m", "src.main"]
```

**Validation Checklist:**
- [ ] Dockerfile uses multi-stage build
- [ ] Dependencies installed before code copy
- [ ] Build is reproducible (same hash)
- [ ] Layer caching verified
- [ ] Security: non-root user, minimal base image

---

## Phase 6: Review Cycles & Hallucination Detection

### 6.1 Code Review with Fact-Checking Protocol

**Best Practice:** AI-generated code must pass multi-stage verification before human review.

**Example:**
```
Step 1 (AI Generates Code):
def fetch_user_data(user_id: int) -> Dict:
    """Fetches user data from database."""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query).fetchone()

Step 2 (Automated Verification Gates):
Gate 1 - Linting: ✓ Passes
Gate 2 - Type Checking: ✓ Passes
Gate 3 - Security Scan (CodeQL): ✗ FAILS
  → SQL injection vulnerability detected

Step 3 (AI Self-Correction):
def fetch_user_data(user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches user data from database using parameterized query."""
    query = "SELECT * FROM users WHERE id = ?"
    result = db.execute(query, (user_id,)).fetchone()
    return dict(result) if result else None

Step 4 (Re-verification):
Gate 1 - Linting: ✓ Passes
Gate 2 - Type Checking: ✓ Passes
Gate 3 - Security Scan: ✓ Passes
Gate 4 - Unit Tests: ✓ New tests pass
→ Now ready for human review
```

**Validation Checklist:**
- [ ] All automated gates passed
- [ ] Security scan clean
- [ ] Type checking passes
- [ ] Tests added/updated
- [ ] Ready for human review

---

### 6.2 Documentation Accuracy Validation

**Best Practice:** Cross-reference documentation claims against actual code behavior.

**Example:**
```
Step 1 (AI Documentation):
"The caching layer uses Redis with a 1-hour TTL for all user queries."

Step 2 (Verification Protocol):
- Grep for Redis config: grep -r "REDIS" config/
- Check TTL settings: grep -r "ttl\|expire" src/cache/
- Find actual values: TTL varies by query type (5min to 24hrs)

Step 3 (Self-Correction):
"The caching layer uses Redis with variable TTL based on data type:
- User profile queries: 1 hour (3600s)
- User preferences: 24 hours (86400s)
- Session data: 5 minutes (300s)
Configuration: config/cache_settings.py:15-23"

Step 4 (Validation):
- Code reference check: File and line numbers correct ✓
- Value verification: TTL values match code ✓
```

**Validation Checklist:**
- [ ] All claims verified against code
- [ ] Line number references correct
- [ ] Configuration values accurate
- [ ] Edge cases documented
- [ ] Version/date stamps included

---

### 6.3 Hallucination Detection Checklist

**Best Practice:** Apply systematic checks for common AI hallucination patterns.

**Detection Protocol:**

| Category | Hallucination Example | Verification Method |
|----------|----------------------|---------------------|
| Dependency | "This project uses FastAPI" | `grep -r "fastapi" requirements.txt` |
| Version | "Upgraded to PostgreSQL 14" | Check docker-compose.yml |
| Feature | "Authentication supports OAuth2" | `grep -r "oauth" src/` |
| Performance | "Optimized query reduces load time by 50%" | Run benchmark tests |
| Coverage | "Added tests bring coverage to 85%" | `pytest --cov=src` |
| API | "The endpoint accepts JSON body" | Check route definition |
| Config | "Environment variable DATABASE_URL" | Check .env.example |

**Verification Commands:**
```bash
# Dependency verification
grep -r "package-name" pyproject.toml requirements.txt

# Feature verification
grep -r "feature-keyword" src/

# Configuration verification
grep -r "CONFIG_VAR" .env.example config/

# API verification
grep -r "@router\|@app" src/api/

# Test coverage verification
pytest --cov=src --cov-report=term-missing
```

**Validation Rule:** Any claim must be verifiable through:
- Code inspection
- Test execution
- Benchmark measurement
- Documentation cross-reference

**Validation Checklist:**
- [ ] Dependency claims verified
- [ ] Version claims verified
- [ ] Feature claims verified
- [ ] Performance claims benchmarked
- [ ] Coverage claims measured

---

## Phase 7: Comprehensive Documentation Generation

### 7.1 Per-Directory README with Validation

**Best Practice:** Generate contextual README for each directory, validate against actual directory contents.

**Example:**
```
Step 1 (AI Generates): src/services/README.md
"# Services Layer
Contains business logic services.

## Files:
- user_service.py: User management
- auth_service.py: Authentication"

Step 2 (Verification):
- List actual files: ls src/services/
  → user_service.py, auth_service.py, email_service.py, payment_service.py

Step 3 (Self-Correction):
"# Services Layer

Contains business logic services that orchestrate data access and implement
core application functionality.

## Architecture
Services follow the dependency injection pattern and are registered in `__init__.py`.

## Files

### user_service.py
**Purpose**: User lifecycle management including registration, profile updates,
and account deletion.
**Key Classes**: `UserService`
**Dependencies**: `UserRepository`, `EmailService`

### auth_service.py
**Purpose**: Authentication and authorization using JWT tokens.
**Key Classes**: `AuthService`, `TokenManager`
**Dependencies**: `UserRepository`, `Redis`

### email_service.py
**Purpose**: Email notification delivery via SendGrid API.
**Key Classes**: `EmailService`
**Dependencies**: `SendGrid`, `TemplateEngine`

### payment_service.py
**Purpose**: Payment processing integration with Stripe.
**Key Classes**: `PaymentService`, `StripeAdapter`
**Dependencies**: `stripe`, `PaymentRepository`

## Testing
Run service tests: `pytest tests/services/ -v`
Coverage requirement: >80% for all services"

Step 4 (Validation):
- File count matches: ✓
- Import statements verified: ✓
- Test command works: ✓
```

**README Template:**
```markdown
# [Directory Name]

## Purpose
[One paragraph describing what this directory contains and why]

## Architecture
[How components in this directory relate to each other]

## Files

### [filename.ext]
**Purpose**: [What this file does]
**Key Classes/Functions**: [Main exports]
**Dependencies**: [What it imports]
**Usage Example**:
```python
from module import Component
component = Component()
```

## Testing
```bash
pytest tests/[directory]/ -v
```

## Related Documentation
- [Link to related docs]
```

**Validation Checklist:**
- [ ] All files in directory documented
- [ ] File purposes accurate
- [ ] Dependencies correctly listed
- [ ] Code examples work
- [ ] Test commands execute successfully

---

### 7.2 File-Level Purpose Documentation with Cross-Validation

**Best Practice:** Document each file's purpose, validate against imports and usage.

**Example:**
```
Step 1 (AI Documents): src/utils/validators.py
"Purpose: Input validation utilities"

Step 2 (Deep Verification):
- Analyze imports: What does this file import?
  → re, typing, email_validator
- Analyze exports: What do other files import from this?
  → validate_email, validate_phone, validate_password, sanitize_input
- Check usage: grep -r "from utils.validators import" src/
  → Used in: forms.py, api/endpoints.py, services/user_service.py

Step 3 (Comprehensive Documentation):
"# validators.py

## Purpose
Provides input validation and sanitization utilities used across the application
to ensure data integrity and security.

## Key Functions

### validate_email(email: str) -> bool
Validates email format using RFC 5322 standards.
**Used by**: User registration (forms.py:45), API endpoints (api/endpoints.py:123)

### validate_phone(phone: str, country_code: str = 'US') -> str
Validates and normalizes phone numbers to E.164 format.
**Used by**: User profile updates (services/user_service.py:234)

### sanitize_input(text: str, allow_html: bool = False) -> str
Removes potentially dangerous characters and optionally strips HTML.
**Security**: Prevents XSS attacks

## Dependencies
- email-validator: ^2.0.0
- re: standard library

## Testing
Tests: tests/utils/test_validators.py
Coverage: 94%"
```

**Validation Checklist:**
- [ ] All exports documented
- [ ] Usage locations verified
- [ ] Dependencies accurate
- [ ] Security implications noted
- [ ] Test coverage measured

---

### 7.3 Navigation-Optimized Documentation Structure

**Best Practice:** Ensure every directory visible in GitHub has a README.

**Directory Audit Process:**
```
Step 1 (Audit):
find . -type d -not -path '*/\.*' | while read dir; do
  if [ ! -f "$dir/README.md" ]; then
    echo "Missing: $dir/README.md"
  fi
done

Step 2 (Generate Missing):
For each missing README:
- Analyze directory contents
- Generate contextual documentation
- Validate against actual files
- Create README.md

Step 3 (Verify Navigation):
- Clone repo fresh
- Navigate through GitHub UI
- Verify each directory shows README
- Check all links work
```

**Validation Checklist:**
- [ ] Every directory has README.md
- [ ] READMEs visible in GitHub UI
- [ ] Cross-references link correctly
- [ ] No broken links
- [ ] Consistent formatting across docs

---

## Phase 8: Continuous Validation Loop

### 8.1 Documentation Drift Detection

**Best Practice:** Automatically detect when code changes make documentation inaccurate.

**Implementation:**
```python
# scripts/detect_doc_drift.py

import ast
import re
from pathlib import Path

def extract_function_signatures(python_file: Path) -> dict[str, str]:
    """Extract function signatures from Python file."""
    tree = ast.parse(python_file.read_text())
    signatures = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            signatures[node.name] = f"{node.name}({', '.join(args)})"
    return signatures

def extract_documented_signatures(readme: Path) -> dict[str, str]:
    """Extract function signatures documented in README."""
    content = readme.read_text()
    pattern = r'###\s+(\w+)\(([^)]*)\)'
    return {m.group(1): f"{m.group(1)}({m.group(2)})"
            for m in re.finditer(pattern, content)}

def check_drift(src_dir: Path, docs_dir: Path) -> list[str]:
    """Check for documentation drift."""
    drifts = []
    for py_file in src_dir.rglob("*.py"):
        readme = docs_dir / py_file.parent.name / "README.md"
        if readme.exists():
            code_sigs = extract_function_signatures(py_file)
            doc_sigs = extract_documented_signatures(readme)
            for name, sig in code_sigs.items():
                if name in doc_sigs and doc_sigs[name] != sig:
                    drifts.append(f"Drift: {py_file}:{name} - {doc_sigs[name]} → {sig}")
    return drifts
```

**CI Integration:**
```yaml
- name: Check Documentation Drift
  run: python scripts/detect_doc_drift.py
  continue-on-error: false
```

**Validation Checklist:**
- [ ] Drift detection script created
- [ ] CI job configured
- [ ] Alert mechanism in place
- [ ] Auto-fix or PR creation configured
- [ ] Regular audit scheduled

---

### 8.2 Checkpoint-Based Progress Tracking

**Best Practice:** Maintain checkpoint file for resumable AI sessions.

**Checkpoint Schema:**
```markdown
# Modernization Checkpoint

**Status**: [Planning | Executing | Validating | Complete]
**Last Updated**: 2026-01-19T14:30:00Z
**Session**: [session-id]

## Current Phase
**Phase**: [1-Planning | 2-Execution | 3-Validation]
**Progress**: X/Y tasks complete

## Agent Status

### Architecture Analyzer
- **Status**: [Pending | In Progress | Completed | Blocked]
- **Last Update**: [timestamp]
- **Current Task**: [description]
- **Results**: [summary]

### Dependency Mapper
- **Status**: [Pending | In Progress | Completed | Blocked]
- **Last Update**: [timestamp]
- **Results**: [summary]

## Completed Tasks
- [x] Task 1: Description
- [x] Task 2: Description

## Pending Tasks
- [ ] Task 3: Description
- [ ] Task 4: Description

## Blockers
- Blocker 1: [description, impact, resolution]

## Decisions Made
- Decision 1: [what and why]

## Next Actions
1. [immediate action]
2. [following action]
```

**Validation Checklist:**
- [ ] Checkpoint file schema defined
- [ ] Update hooks configured
- [ ] Validation on write
- [ ] Git commit on progress
- [ ] Resume capability tested

---

### 8.3 Automated Regression Prevention

**Best Practice:** Ensure modernization changes don't introduce regressions.

**Implementation:**
```yaml
# .github/workflows/regression-check.yml
name: Regression Check

on:
  pull_request:
    branches: [main]

jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get Changed Files
        id: changed
        run: |
          echo "files=$(git diff --name-only origin/main...HEAD | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: Run Affected Tests
        run: |
          pytest tests/ --co -q | grep -F "${{ steps.changed.outputs.files }}" | xargs pytest

      - name: Coverage Comparison
        run: |
          # Get baseline coverage
          git checkout origin/main
          pytest --cov=src --cov-report=json -q
          mv coverage.json baseline.json

          # Get PR coverage
          git checkout -
          pytest --cov=src --cov-report=json -q

          # Compare
          python scripts/compare_coverage.py baseline.json coverage.json
```

**Validation Checklist:**
- [ ] Regression tests automated
- [ ] Coverage comparison enabled
- [ ] Performance benchmarks tracked
- [ ] API compatibility verified
- [ ] Database migration tested

---

## Quick Reference: Validation Commands

### Static Analysis
```bash
# Type checking
mypy src/ --strict

# Linting
ruff check src/

# Security scan
bandit -r src/ -ll

# Complexity check
radon cc src/ -a -s
```

### Testing
```bash
# Unit tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Integration tests
pytest tests/integration/ -v

# Performance tests
pytest tests/performance/ --benchmark-only
```

### Documentation Verification
```bash
# Check all links
linkchecker docs/

# Verify code examples
python -m doctest docs/**/*.md

# Check README coverage
find src -type d -exec test -f {}/README.md \; -print
```

### Dependency Analysis
```bash
# Security vulnerabilities
pip-audit

# Outdated packages
pip list --outdated

# Dependency tree
pipdeptree
```

---

## Appendix: Tool Configuration Templates

### A. Complete pyproject.toml
```toml
[project]
name = "project-name"
version = "0.1.0"
requires-python = ">=3.12"

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "B", "C4", "SIM", "I", "UP", "PIE", "PGH", "RUF"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-fail-under=80"

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]
```

### B. Complete .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.10
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: [-ll, -r, src/]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/ -x -q --no-header
        language: system
        pass_filenames: false
        always_run: true
```

### C. GitHub Actions CI Template
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install ruff mypy bandit
      - run: ruff check src/
      - run: ruff format --check src/
      - run: mypy src/ --strict
      - run: bandit -r src/ -ll

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e ".[dev]"
      - run: pytest tests/ --cov=src --cov-fail-under=80
```

---

## Summary

This checklist provides a systematic approach to AI-assisted brownfield modernization with built-in validation at every step. Key principles:

1. **Never trust initial AI output** - Always verify through automated tools
2. **Use tests as ground truth** - If tests fail, the change is wrong
3. **Document with references** - Every claim must be traceable to code
4. **Checkpoint progress** - Enable resumption from any point
5. **Automate validation** - CI/CD should catch what humans miss

By following this checklist, AI developers can produce accurate, validated modernization work while human developers can trust the outputs and efficiently review changes.
