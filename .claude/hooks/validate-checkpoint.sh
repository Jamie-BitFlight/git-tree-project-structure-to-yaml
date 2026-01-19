#!/bin/bash
# Validates checkpoint file structure before writes
# This hook ensures checkpoint updates maintain schema integrity

set -e

# Read input from stdin (tool input JSON)
INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tool_input', {}).get('file_path', ''))" 2>/dev/null || echo "")

# Only validate if writing to checkpoint file
if [[ ! "$FILE_PATH" =~ MODERNIZATION_CHECKPOINT\.md$ ]]; then
    exit 0
fi

# Extract content
CONTENT=$(echo "$INPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tool_input', {}).get('content', ''))" 2>/dev/null || echo "")

# Validate required sections exist
REQUIRED_SECTIONS=(
    "# Brownfield Modernization Checkpoint"
    "## Metadata"
    "## Agent Status"
    "## Completed Tasks"
    "## Pending Tasks"
    "## Next Actions"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! echo "$CONTENT" | grep -q "^$section"; then
        echo "ERROR: Checkpoint validation failed - missing section: $section" >&2
        echo '{"decision": "block", "reason": "Checkpoint missing required section: '"$section"'"}'
        exit 0
    fi
done

# Validate agent status sections have required fields
AGENTS=("Architecture Analyzer" "Dependency Mapper" "Technical Debt Assessor")
for agent in "${AGENTS[@]}"; do
    if echo "$CONTENT" | grep -q "### $agent"; then
        if ! echo "$CONTENT" | grep -A5 "### $agent" | grep -q "Status"; then
            echo "ERROR: Agent '$agent' missing Status field" >&2
            echo '{"decision": "block", "reason": "Agent '"$agent"' missing Status field"}'
            exit 0
        fi
    fi
done

# Validation passed
exit 0
