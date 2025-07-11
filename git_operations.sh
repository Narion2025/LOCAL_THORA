#!/bin/bash

# Navigate to repository
cd /Users/benjaminpoersch/claude/thor-agent

# Check current status
echo "=== Current Git Status ==="
git status

echo -e "\n=== Checking for conflicts ==="
# Check if there are any conflict markers in README.md
if grep -q "<<<<<<< HEAD\|=======" README.md 2>/dev/null; then
    echo "Conflicts found in README.md"
    
    # Show the conflicted file
    echo -e "\n=== Current README.md content ==="
    cat README.md
    
    # Resolve conflict by keeping our local version (the L_Thor_M content)
    echo "# L_Thor_M" > README.md
    echo "Local Thor Maschine - AI to control your computer" >> README.md
    
    echo -e "\n=== Resolved README.md content ==="
    cat README.md
    
    # Add the resolved file
    git add README.md
    
    echo -e "\n=== Added resolved README.md ==="
else
    echo "No conflicts found in README.md"
fi

# Complete any ongoing merge/rebase
if [ -d ".git/rebase-merge" ]; then
    echo -e "\n=== Continuing rebase ==="
    git rebase --continue
elif [ -f ".git/MERGE_HEAD" ]; then
    echo -e "\n=== Committing merge ==="
    git commit -m "Resolve README.md conflict"
fi

# Check status again
echo -e "\n=== Status after conflict resolution ==="
git status

# Add all files and commit
echo -e "\n=== Adding all files ==="
git add .

echo -e "\n=== Committing changes ==="
git commit -m "Update Thor-agent with all local changes"

echo -e "\n=== Final status before push ==="
git status

# Push to origin
echo -e "\n=== Pushing to origin ==="
git push origin main

echo -e "\n=== Operation completed ==="
