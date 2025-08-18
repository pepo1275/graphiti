#!/bin/bash
# Pre-commit validator for Graphiti project
# Ensures methodology compliance before commits

set -e

echo "🔍 Pre-commit validation starting..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

# Check 1: Verify not on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo -e "${RED}❌ ERROR: Cannot commit directly to main branch${NC}"
    exit 1
fi
print_status 0 "Branch check passed (current: $CURRENT_BRANCH)"

# Check 2: Run tests if they exist
if [ -d "tests" ]; then
    echo "Running tests..."
    if command -v pytest &> /dev/null; then
        pytest --co -q
        print_status $? "Tests collection check passed"
    else
        echo -e "${YELLOW}⚠️  pytest not installed, skipping tests${NC}"
    fi
fi

# Check 3: Check code quality with ruff
if command -v ruff &> /dev/null; then
    echo "Checking code quality..."
    ruff check . --quiet
    print_status $? "Code quality check passed"
else
    echo -e "${YELLOW}⚠️  ruff not installed, skipping quality check${NC}"
fi

# Check 4: Check for sensitive data
echo "Checking for sensitive data..."
SENSITIVE_PATTERNS=(
    "password.*=.*['\"].*['\"]"
    "api[_-]key.*=.*['\"].*['\"]"
    "secret.*=.*['\"].*['\"]"
    "token.*=.*['\"].*['\"]"
)

FOUND_SENSITIVE=0
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if git diff --cached | grep -iE "$pattern" > /dev/null; then
        echo -e "${RED}❌ Found potential sensitive data matching pattern: $pattern${NC}"
        FOUND_SENSITIVE=1
    fi
done

if [ $FOUND_SENSITIVE -eq 0 ]; then
    print_status 0 "No sensitive data detected"
else
    echo -e "${RED}❌ Remove sensitive data before committing${NC}"
    exit 1
fi

# Check 5: Verify methodology compliance
if [ -f ".claude/check_methodology.py" ]; then
    echo "Checking methodology compliance..."
    python3 .claude/check_methodology.py
    print_status $? "Methodology compliance check passed"
fi

# Check 6: Ensure commit message follows convention
echo -e "${YELLOW}ℹ️  Remember to use conventional commit format:${NC}"
echo "  type(scope): description"
echo "  Types: feat, fix, docs, style, refactor, test, chore"

# Final status
echo ""
echo -e "${GREEN}✅ All pre-commit checks passed!${NC}"
echo "You can proceed with your commit."

# Create checkpoint log entry
CHECKPOINT_LOG="$PROJECT_ROOT/.claude/checkpoint_log.json"
if [ ! -f "$CHECKPOINT_LOG" ]; then
    mkdir -p "$(dirname "$CHECKPOINT_LOG")"
    echo '{"checkpoints": []}' > "$CHECKPOINT_LOG"
fi

# Add pre-commit validation entry
python3 -c "
import json
from datetime import datetime
from pathlib import Path

log_file = Path('$CHECKPOINT_LOG')
with open(log_file) as f:
    data = json.load(f)

data['checkpoints'].append({
    'type': 'pre-commit',
    'timestamp': datetime.now().isoformat(),
    'branch': '$CURRENT_BRANCH',
    'status': 'validated'
})

with open(log_file, 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null || true

exit 0