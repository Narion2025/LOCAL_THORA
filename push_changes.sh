#!/bin/bash
cd /Users/benjaminpoersch/claude/thor-agent

# Abort any ongoing operations
git rebase --abort 2>/dev/null || true
git merge --abort 2>/dev/null || true

# Clean the working directory
git reset --hard HEAD 2>/dev/null || true

# Add all files
git add .

# Commit with a descriptive message
git commit -m "Complete Thor-agent implementation with resolved conflicts"

# Push to origin
git push origin main

echo "Successfully pushed to repository!"
