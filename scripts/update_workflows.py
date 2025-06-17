#!/usr/bin/env python3
"""
Script to update virtool-workflow in workflow repositories and create GitHub PRs.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


WORKFLOW_REPOS = [
    "workflow-build-index",
    "workflow-create-sample",
    "workflow-create-subtraction",
    "workflow-iimi",
    "workflow-nuvs",
    "workflow-pathoscope",
]


def run_command(cmd, cwd=None, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else True
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        if capture_output and hasattr(e, 'stderr') and e.stderr:
            print(f"STDERR: {e.stderr}")
        return None


def get_parent_directory():
    """Navigate to the parent directory of the current repo."""
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    print(f"Moving from {current_dir} to {parent_dir}")
    return parent_dir


def check_repo_exists(repo_path):
    """Check if the repository exists and is a git repo."""
    if not repo_path.exists():
        print(f"Repository {repo_path} does not exist")
        return False
    
    if not (repo_path / ".git").exists():
        print(f"Directory {repo_path} is not a git repository")
        return False
    
    return True


def get_latest_virtool_workflow_version():
    """Get the latest version of virtool-workflow from PyPI."""
    cmd = "pip index versions virtool-workflow --pre"
    result = run_command(cmd)
    if result:
        # Parse the output to get the latest version
        lines = result.split('\n')
        for line in lines:
            if 'Available versions:' in line:
                # Extract the first (latest) version
                versions_line = line.split('Available versions:')[1].strip()
                if versions_line:
                    latest_version = versions_line.split(',')[0].strip()
                    return latest_version
    
    print("Could not determine latest virtool-workflow version")
    return None


def update_virtool_workflow(repo_path, version):
    """Update virtool-workflow in the specified repository."""
    print(f"Updating virtool-workflow to {version} in {repo_path}")
    
    # Check if pyproject.toml exists
    pyproject_path = repo_path / "pyproject.toml"
    if pyproject_path.exists():
        # Read current pyproject.toml
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Update virtool-workflow dependency
        import re
        pattern = r'virtool-workflow\s*=\s*"([^"]*)"'
        match = re.search(pattern, content)
        
        if match:
            old_version = match.group(1)
            replacement = f'virtool-workflow = "{version}"'
            updated_content = re.sub(pattern, replacement, content)
            with open(pyproject_path, 'w') as f:
                f.write(updated_content)
            print(f"Updated pyproject.toml with virtool-workflow = \"{version}\"")
            
            # Run poetry lock to update the lock file
            print("Running poetry lock")
            if not run_command("poetry lock", cwd=repo_path, capture_output=False):
                print("Failed to run poetry lock")
                return None
            
            return old_version
        else:
            print("virtool-workflow dependency not found in pyproject.toml")
            return None
    else:
        print("pyproject.toml not found in repository")
        return None


def create_branch_and_commit(repo_path, version, old_version, custom_message=None):
    """Create a new branch and commit the changes."""
    branch_name = f"virtool-workflow-{version}"
    
    # Delete existing branch if it exists
    run_command(f"git branch -D {branch_name}", cwd=repo_path, capture_output=True)
    
    # Create and checkout new branch
    print(f"Creating branch {branch_name}")
    if not run_command(f"git checkout -b {branch_name}", cwd=repo_path, capture_output=False):
        print(f"Failed to create branch {branch_name}")
        return None
    
    # Add changes
    print("Adding pyproject.toml and poetry.lock")
    if not run_command("git add pyproject.toml poetry.lock", cwd=repo_path, capture_output=False):
        print("Failed to add files")
        return None
    
    # Commit changes
    print("Committing changes")
    if custom_message:
        commit_msg = f"{custom_message}\n\n* Bump virtool-workflow from {old_version} to {version}"
    else:
        commit_msg = f"chore(deps): bump virtool-workflow from {old_version} to {version}"
    
    if not run_command(f'git commit -m "{commit_msg}"', cwd=repo_path, capture_output=False):
        print("Failed to commit changes")
        return None
    
    return branch_name


def push_and_create_pr(repo_path, branch_name, version):
    """Push the branch and create a GitHub PR."""
    # Push the branch with upstream tracking
    print(f"Pushing branch {branch_name}")
    if not run_command(f"git push -u origin {branch_name}", cwd=repo_path, capture_output=False):
        print("Failed to push branch")
        return False
    
    # Create PR using gh CLI
    print("Creating GitHub PR")
    pr_title = f"Update virtool-workflow to {version}"
    pr_body = f"This PR updates the virtool-workflow dependency to version {version}."
    
    pr_cmd = f'gh pr create --title "{pr_title}" --body "{pr_body}"'
    if not run_command(pr_cmd, cwd=repo_path, capture_output=False):
        print("Failed to create PR")
        return False
    
    return True


def process_repository(repo_name, parent_dir, version, custom_message=None):
    """Process a single repository."""
    print(f"\n--- Processing {repo_name} ---")
    
    repo_path = parent_dir / repo_name
    
    if not check_repo_exists(repo_path):
        return False
    
    # Change to repository directory
    original_dir = Path.cwd()
    os.chdir(repo_path)
    
    try:
        # Ensure we're on main branch and up to date
        run_command("git checkout main", cwd=repo_path, capture_output=False)
        run_command("git pull origin main", cwd=repo_path, capture_output=False)
        
        # Update virtool-workflow
        old_version = update_virtool_workflow(repo_path, version)
        if not old_version:
            return False
        
        # Create branch and commit
        branch_name = create_branch_and_commit(repo_path, version, old_version, custom_message)
        if not branch_name:
            return False
        
        # Push and create PR
        if not push_and_create_pr(repo_path, branch_name, version):
            return False
        
        print(f"Successfully created PR for {repo_name}")
        return True
        
    finally:
        # Return to original directory
        os.chdir(original_dir)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Update virtool-workflow in workflow repositories and create GitHub PRs.")
    parser.add_argument("-m", "--message", help="Custom commit message (will be used as title with default message as bullet point)")
    args = parser.parse_args()
    
    if not WORKFLOW_REPOS:
        print("No workflow repositories specified. Please update the WORKFLOW_REPOS list.")
        sys.exit(1)
    
    # Get latest virtool-workflow version
    latest_version = get_latest_virtool_workflow_version()
    if not latest_version:
        print("Could not determine latest virtool-workflow version")
        sys.exit(1)
    
    print(f"Latest virtool-workflow version: {latest_version}")
    
    # Navigate to parent directory
    parent_dir = get_parent_directory()
    
    # Process each repository
    successful_repos = []
    failed_repos = []
    
    for repo_name in WORKFLOW_REPOS:
        if process_repository(repo_name, parent_dir, latest_version, args.message):
            successful_repos.append(repo_name)
        else:
            failed_repos.append(repo_name)
    
    # Summary
    print(f"\n--- Summary ---")
    print(f"Successfully processed: {len(successful_repos)} repositories")
    for repo in successful_repos:
        print(f"  ✓ {repo}")
    
    if failed_repos:
        print(f"Failed to process: {len(failed_repos)} repositories")
        for repo in failed_repos:
            print(f"  ✗ {repo}")


if __name__ == "__main__":
    main()
