#!/bin/bash
# Session startup hook for brownfield modernization
# Loads checkpoint state if it exists and provides context for resumption

CHECKPOINT_FILE="${CLAUDE_PROJECT_DIR:-$(pwd)}/MODERNIZATION_CHECKPOINT.md"

# Check if checkpoint exists
if [ ! -f "$CHECKPOINT_FILE" ]; then
    echo "No modernization checkpoint found. Starting fresh."
    echo ""
    echo "To begin brownfield modernization, use: /modernize"
    echo "Or ask: 'Help me modernize this codebase'"
    exit 0
fi

# Checkpoint exists - provide resumption context
echo "=== Brownfield Modernization Checkpoint Found ==="
echo ""

# Extract key information from checkpoint
STATUS=$(grep -m1 "^\*\*Status\*\*:" "$CHECKPOINT_FILE" | sed 's/.*: //' || echo "Unknown")
PHASE=$(grep -m1 "^\*\*Current Phase\*\*:" "$CHECKPOINT_FILE" | sed 's/.*: //' || echo "Unknown")
LAST_UPDATED=$(grep -m1 "^\*\*Last Updated\*\*:" "$CHECKPOINT_FILE" | sed 's/.*: //' || echo "Unknown")

echo "Status: $STATUS"
echo "Current Phase: $PHASE"
echo "Last Updated: $LAST_UPDATED"
echo ""

# Show agent statuses
echo "Agent Statuses:"
grep -A1 "^### " "$CHECKPOINT_FILE" | grep -E "^\*\*Status\*\*:" | head -6 || echo "  (Unable to parse agent statuses)"
echo ""

# Show next actions
echo "Next Actions:"
grep -A5 "^## Next Actions" "$CHECKPOINT_FILE" | grep "^[0-9]\." | head -3 || echo "  (No next actions defined)"
echo ""

echo "To resume modernization, use: /modernize"
echo "To see full checkpoint: cat MODERNIZATION_CHECKPOINT.md"
echo "=============================================="

# Export environment variables for use in session
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export MODERNIZATION_CHECKPOINT_EXISTS=true" >> "$CLAUDE_ENV_FILE"
    echo "export MODERNIZATION_STATUS=\"$STATUS\"" >> "$CLAUDE_ENV_FILE"
    echo "export MODERNIZATION_PHASE=\"$PHASE\"" >> "$CLAUDE_ENV_FILE"
fi

exit 0
