---
description: Orchestrate AI-assisted brownfield modernization with concurrent agents and checkpoint tracking
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
---

# Brownfield Modernization Orchestrator

You are orchestrating a brownfield modernization process using AI-assisted development with Chain-of-Verification (CoVe), self-correction loops, and validation harnesses.

## Overview

This command spawns multiple specialized agents to work concurrently through a brownfield modernization process, with checkpoint-based progress tracking for resumability.

## Initialization

First, check if a checkpoint file exists:

```bash
cat MODERNIZATION_CHECKPOINT.md 2>/dev/null || echo "NO_CHECKPOINT"
```

### If No Checkpoint Exists

1. Read the modernization checklist: `docs/AI_ASSISTED_BROWNFIELD_MODERNIZATION_CHECKLIST.md`
2. Initialize a new checkpoint file using the schema in `.claude/skills/brownfield-modernization/CHECKPOINT_SCHEMA.md`
3. Begin Phase 1: Repository Analysis

### If Checkpoint Exists

1. Parse the checkpoint to determine current state
2. Identify which agents were active and their last status
3. Resume from the appropriate phase and task

## Agent Orchestration

Spawn specialized agents concurrently using the Task tool:

### Phase 1: Planning & Discovery (Concurrent Agents)

1. **Architecture Analyzer** (`subagent_type: Explore`)
   - Analyze codebase structure
   - Document component relationships
   - Identify architectural patterns and violations

2. **Dependency Mapper** (`subagent_type: Explore`)
   - Scan all dependency files
   - Check for vulnerabilities and outdated packages
   - Create upgrade compatibility matrix

3. **Technical Debt Assessor** (`subagent_type: Explore`)
   - Run linting and type checking
   - Identify code quality issues
   - Prioritize technical debt items

### Phase 2: Execution (Sequential with Validation)

1. **Validation Harness Setup** (`subagent_type: general-purpose`)
   - Configure type checking, linting, testing
   - Establish baseline metrics

2. **Implementation Agent** (`subagent_type: general-purpose`)
   - Execute modernization tasks
   - Self-correct based on validation failures

### Phase 3: Validation & Documentation (Concurrent)

1. **Test Coverage Improver** (`subagent_type: general-purpose`)
   - Add missing tests
   - Improve coverage metrics

2. **Documentation Generator** (`subagent_type: general-purpose`)
   - Generate per-directory READMEs
   - Validate documentation accuracy

## Checkpoint Updates

After each agent completes a task:

1. Update the `MODERNIZATION_CHECKPOINT.md` file with:
   - Agent status change
   - Task completion
   - Any blockers encountered
   - Next actions

2. Commit checkpoint changes:
   ```bash
   git add MODERNIZATION_CHECKPOINT.md
   git commit -m "chore: update modernization checkpoint - [agent] completed [task]"
   ```

## Validation Gates

Before accepting any agent output:

1. **Linting Gate**: `ruff check src/`
2. **Type Checking Gate**: `mypy src/`
3. **Test Gate**: `pytest tests/ -x`
4. **Security Gate**: `bandit -r src/ -ll`

If any gate fails, the agent must self-correct before proceeding.

## Usage Examples

```
/modernize                    # Start or resume modernization
/modernize status            # Show current checkpoint status
/modernize phase1            # Run Phase 1: Planning & Discovery
/modernize phase2            # Run Phase 2: Execution
/modernize phase3            # Run Phase 3: Validation & Documentation
/modernize reset             # Reset checkpoint (start fresh)
```

## Error Handling

If an agent encounters a blocker:

1. Document the blocker in the checkpoint
2. Mark the agent as "Blocked"
3. Continue with other agents if possible
4. Report blockers to the human developer for resolution

## Completion

When all phases are complete:

1. Generate final modernization report
2. Update checkpoint status to "Complete"
3. Create summary of all changes made
4. List any remaining manual tasks for human developers
