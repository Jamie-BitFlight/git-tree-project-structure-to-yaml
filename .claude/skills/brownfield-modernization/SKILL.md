---
name: brownfield-modernization
description: Orchestrate concurrent agents through brownfield modernization phases with checkpoint-based resumable workflows. Use when starting a modernization initiative, resuming from a checkpoint, or coordinating modernization across multiple components.
---

# Brownfield Modernization Skill

## Overview

This skill manages the entire lifecycle of a brownfield modernization project by:

1. **Initializing checkpoints** - Creates a resumable progress document
2. **Spawning concurrent subagents** - Each specializes in a modernization aspect
3. **Aggregating progress** - Updates checkpoint with agent results
4. **Enabling resumption** - Agents can pick up from last checkpoint state

## When This Skill Activates

Claude will automatically use this skill when the user:

- Asks to "modernize" or "upgrade" a codebase
- Mentions "brownfield" project work
- Requests concurrent agent orchestration
- Wants to resume from a checkpoint
- Needs systematic codebase analysis and improvement

## Core Workflow

### 1. Checkpoint Detection

```python
# Pseudo-code for checkpoint handling
if exists("MODERNIZATION_CHECKPOINT.md"):
    checkpoint = parse_checkpoint()
    if checkpoint.status == "Complete":
        offer_new_modernization_or_review()
    else:
        resume_from_checkpoint(checkpoint)
else:
    initialize_new_checkpoint()
    start_phase_1()
```

### 2. Agent Spawning Pattern

Spawn agents using the Task tool with specific subagent types:

```
# Concurrent exploration agents (Phase 1)
Task(subagent_type="Explore", prompt="Analyze architecture...")
Task(subagent_type="Explore", prompt="Map dependencies...")
Task(subagent_type="Explore", prompt="Assess technical debt...")

# Implementation agents (Phase 2)
Task(subagent_type="general-purpose", prompt="Set up validation harness...")
Task(subagent_type="general-purpose", prompt="Execute modernization tasks...")

# Documentation agents (Phase 3)
Task(subagent_type="general-purpose", prompt="Generate documentation...")
```

### 3. Validation Loop

Every agent output goes through validation:

```
1. Agent produces output
2. Run validation gates (lint, type-check, test, security)
3. If any gate fails:
   - Feed error back to agent
   - Agent self-corrects
   - Re-run validation
4. If all gates pass:
   - Accept output
   - Update checkpoint
   - Proceed to next task
```

### 4. Checkpoint Updates

After each significant action:

```markdown
## Agent Status

### [Agent Name]
- **Status**: Completed
- **Last Update**: 2026-01-19T15:30:00Z
- **Task Completed**: Analyzed 47 modules, found 12 architectural violations
- **Output Files**: docs/architecture-analysis.md
```

## Phases

### Phase 1: Planning & Discovery

**Goal**: Understand the current state of the codebase

**Concurrent Agents**:
- Architecture Analyzer
- Dependency Mapper
- Technical Debt Assessor

**Deliverables**:
- Architecture diagram and analysis
- Dependency upgrade plan
- Technical debt inventory with priorities

**Duration**: Agents work concurrently, typically completes in one session

### Phase 2: Execution

**Goal**: Implement modernization improvements

**Sequential Tasks** (with validation gates):
1. Set up validation harness (type checking, linting, testing)
2. Execute highest-priority modernization tasks
3. Validate each change before proceeding

**Deliverables**:
- Configured validation tools
- Modernized code with passing tests
- Updated dependencies

**Duration**: Multiple sessions, checkpoint enables resumption

### Phase 3: Validation & Documentation

**Goal**: Ensure quality and document everything

**Concurrent Agents**:
- Test Coverage Improver
- Documentation Generator

**Deliverables**:
- Improved test coverage (target: 80%+)
- Per-directory README files
- Updated API documentation

**Duration**: Agents work concurrently, typically completes in one session

## Self-Correction Patterns

### Pattern 1: Lint Failure Correction

```
Agent output: def foo(x): return x+1
Lint error: E225 missing whitespace around operator
Self-correction: def foo(x): return x + 1
```

### Pattern 2: Type Check Correction

```
Agent output: def process(data: list) -> dict:
Type error: Missing type parameters
Self-correction: def process(data: list[str]) -> dict[str, Any]:
```

### Pattern 3: Test Failure Correction

```
Agent output: Changed authentication from bcrypt to argon2
Test failure: Expected bcrypt hash format
Analysis: Check git history for intentional bcrypt usage
Self-correction: Preserve bcrypt, update only non-auth code
```

### Pattern 4: Hallucination Detection

```
Agent claim: "Project uses FastAPI"
Verification: grep -r "fastapi" requirements.txt → Not found
Self-correction: Remove incorrect claim, verify actual framework
```

## Integration with Checklist

This skill works in conjunction with the comprehensive checklist at:
`docs/AI_ASSISTED_BROWNFIELD_MODERNIZATION_CHECKLIST.md`

The checklist provides:
- Detailed validation procedures
- Configuration templates
- Example verification loops
- Tool configuration guides

## Resumption Protocol

When resuming from a checkpoint:

1. **Read checkpoint file** completely
2. **Identify current phase** and active tasks
3. **Check agent statuses**:
   - `Completed`: Skip, use results
   - `In Progress`: Resume from last known state
   - `Blocked`: Report blocker, attempt resolution or skip
   - `Pending`: Start fresh
4. **Verify environment** hasn't changed (dependencies, configs)
5. **Continue orchestration** from appropriate point

## Error Recovery

### Agent Timeout
- Save partial progress to checkpoint
- Mark agent as "Partial"
- Allow manual retry or skip

### Validation Gate Persistent Failure
- After 3 self-correction attempts, mark as "Blocked"
- Document the issue in checkpoint
- Escalate to human developer

### External Service Failure
- Retry with exponential backoff
- If persistent, document and continue with other tasks

## Usage

Users can invoke this skill by:

1. Using the slash command: `/modernize`
2. Asking Claude directly: "Help me modernize this brownfield codebase"
3. Requesting specific phases: "Run Phase 2 of the modernization"
4. Checking status: "What's the current modernization status?"
