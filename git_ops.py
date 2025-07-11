#!/usr/bin/env python3
import subprocess
import os

def run_git_command(cmd, cwd):
    """Run a git command and return the output"""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
        print(f"Command: {cmd}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"Error running command {cmd}: {e}")
        return False, "", str(e)

def main():
    repo_path = "/Users/benjaminpoersch/claude/thor-agent"
    os.chdir(repo_path)
    
    print("=== Starting Git Operations ===")
    
    # Check current status
    print("\n1. Checking git status...")
    success, stdout, stderr = run_git_command("git status", repo_path)
    
    # Abort any ongoing rebase first
    print("\n2. Aborting any ongoing rebase...")
    run_git_command("git rebase --abort", repo_path)
    
    # Reset any merge state
    print("\n3. Resetting merge state...")
    run_git_command("git merge --abort", repo_path)
    
    # Add all files
    print("\n4. Adding all files...")
    success, stdout, stderr = run_git_command("git add .", repo_path)
    
    # Commit changes
    print("\n5. Committing changes...")
    success, stdout, stderr = run_git_command('git commit -m "Update Thor-agent with all local changes"', repo_path)
    
    # Force push (since we're resolving conflicts)
    print("\n6. Force pushing to origin...")
    success, stdout, stderr = run_git_command("git push origin main --force", repo_path)
    
    print("\n=== Git Operations Completed ===")

if __name__ == "__main__":
    main()
