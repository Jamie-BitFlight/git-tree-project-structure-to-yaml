#!/bin/bash
# Update a specific section of the modernization checkpoint
# Usage: ./update-checkpoint.sh <agent-name> <status> <task> [results]

set -e

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CHECKPOINT_FILE="$PROJECT_ROOT/MODERNIZATION_CHECKPOINT.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

AGENT_NAME="$1"
STATUS="$2"
CURRENT_TASK="$3"
RESULTS="${4:-}"

# Validate inputs
if [ -z "$AGENT_NAME" ] || [ -z "$STATUS" ]; then
    echo "Usage: $0 <agent-name> <status> [task] [results]"
    echo ""
    echo "Agent names:"
    echo "  - Architecture Analyzer"
    echo "  - Dependency Mapper"
    echo "  - Technical Debt Assessor"
    echo "  - Implementation Agent"
    echo "  - Test Coverage Improver"
    echo "  - Documentation Generator"
    echo ""
    echo "Status values:"
    echo "  - Pending"
    echo "  - In Progress"
    echo "  - Completed"
    echo "  - Blocked"
    echo "  - Partial"
    exit 1
fi

# Check if checkpoint exists
if [ ! -f "$CHECKPOINT_FILE" ]; then
    echo "ERROR: No checkpoint file found at $CHECKPOINT_FILE"
    echo "Initialize first with: ./init-checkpoint.sh"
    exit 1
fi

# Create backup
cp "$CHECKPOINT_FILE" "${CHECKPOINT_FILE}.bak"

# Update the Last Updated timestamp in metadata
sed -i "s/^\*\*Last Updated\*\*: .*/\*\*Last Updated\*\*: $TIMESTAMP/" "$CHECKPOINT_FILE"

# Update the agent section using Python for more reliable parsing
python3 << EOF
import re
import sys

checkpoint_file = "$CHECKPOINT_FILE"
agent_name = "$AGENT_NAME"
status = "$STATUS"
current_task = "$CURRENT_TASK" or "N/A"
results = "$RESULTS" or "See output files"
timestamp = "$TIMESTAMP"

with open(checkpoint_file, 'r') as f:
    content = f.read()

# Find and update the agent section
agent_pattern = rf'(### {re.escape(agent_name)}\n)(.*?)(?=\n### |\n---|\Z)'

def update_agent(match):
    header = match.group(1)
    section = match.group(2)

    # Update fields
    section = re.sub(r'\*\*Status\*\*: .*', f'**Status**: {status}', section)
    section = re.sub(r'\*\*Last Update\*\*: .*', f'**Last Update**: {timestamp}', section)
    section = re.sub(r'\*\*Current Task\*\*: .*', f'**Current Task**: {current_task}', section)
    if results:
        section = re.sub(r'\*\*Results Summary\*\*: .*', f'**Results Summary**: {results}', section)

    return header + section

updated_content = re.sub(agent_pattern, update_agent, content, flags=re.DOTALL)

with open(checkpoint_file, 'w') as f:
    f.write(updated_content)

print(f"Updated {agent_name}: {status}")
EOF

echo "Checkpoint updated successfully"
echo "Agent: $AGENT_NAME"
echo "Status: $STATUS"
echo "Task: $CURRENT_TASK"
echo "Timestamp: $TIMESTAMP"
