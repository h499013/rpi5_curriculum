#!/usr/bin/env bash
# new-project.sh 
# Usage: ./new-project.sh <project-name>

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <project-name>"
    echo "Example: $0 r2-blink"
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="$HOME/rpi/projects/$PROJECT_NAME"

if [ -d "$PROJECT_DIR" ]; then
    echo "Error: $PROJECT_DIR already exists"
    exit 2
fi

echo "Creating $PROJECT_DIR ..."
mkdir -p "$PROJECT_DIR"/{src,test,docs,logs}

# README
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT_NAME

> Started: $(date -Iseconds)

## Description

(TODO)

## Setup

(TODO)

## Run

(TODO)
EOF

# .gitignore
cat > "$PROJECT_DIR/.gitignore" << 'EOF'
__pycache__/
*.pyc
*.pyo
venv/
.venv/
logs/*
!logs/.gitkeep
*.log
*.swp
.vscode/
.idea/
EOF

touch "$PROJECT_DIR/logs/.gitkeep"

# Git init
cd "$PROJECT_DIR"
git init -q
git add .
git commit -q -m "Initial scaffold: $PROJECT_NAME"

echo ""
echo "✓ Created: $PROJECT_DIR"
echo "✓ Git initialized with first commit"
echo ""
echo "Next: cd $PROJECT_DIR"
tree -L 2 "$PROJECT_DIR" 2>/dev/null || find "$PROJECT_DIR" -maxdepth 2 -print
