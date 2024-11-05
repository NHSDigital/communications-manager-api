#!/bin/bash
set -e

current_step=0

# $1: message
info() {
  echo -e "[ INFO  ]: $1"
}

# $1: message
step() {
  echo -e "[ STEP $((current_step++))]: $1"
}

# $1: message
query() {
  read -p "[ QUERY ]: $1: " response
}

error() {
  echo "[ ERROR ]: $1"
  exit 1
}

# check if in project root
current_dir=$(basename "$PWD")
if [[ "$current_dir" != "communications-manager-api" ]]; then
  error "you must be in the project root directory to run this script"
fi

positional_arg_index=0

# shifts positional args from arguments into named vars
handle_positional_arg() {
  case $((positional_arg_index++)) in
    0) ticket_id="$1";;
    1) environment="$1";;
    *) error "too many positional arguments";;
  esac
}

help() {
  echo "This script automates the process of reconfiguring the 'communications-manager-api' APIs to point to a dynamic"
  echo "backend environment in the 'comms-mgr' repository, rather than the default common backend in 'internal-dev'."
  echo ""
  echo "Usage: $0 [ticket ID] [environment]"
  echo ""
  echo "Positional Arguments:"
  echo "  ticket ID         Numeric only (e.g., '0000')"
  echo "  environment       Environment identifier (e.g., 'de-gith1')"
  echo ""
  echo "Options:"
  echo "  --help | -h       Show this help message and exit."
  echo ""
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --help|-h) help; exit 0;;
        -*) error "unknown option: $1" >&2;;
        *) handle_positional_arg "$1";;
    esac
    shift || true
done

# Check AWS login status
if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo "You must have an active AWS SSO session to run this script."
  exit 1
fi

# Check if a ticket ID is provided
if [[ -z "$ticket_id" ]]; then
  error "missing arguments: [ticket ID (numeric only)] [environment]. See '$0 --help'"
fi

# Ensure ticket ID is numeric
if ! [[ "$ticket_id" =~ ^[0-9]+$ ]]; then
  error "Invalid ticket ID: must be numeric only. See '$0 --help' for usage."
fi

# Check if an environment is provided
if [[ -z "$environment" ]]; then
  error "missing argument: [environment]. See '$0 --help'"
fi

info "initial validation passed"

# Step 1: Remove mTLS (if set)
step "Remove mTLS (if set)"
./scripts/mtls/disable_mtls.sh "$environment"

# Step 2: Create new branch for proxy modifications
step "create new branch for proxy modifications"
current_branch=$(git rev-parse --abbrev-ref HEAD)
info "Current branch is: $current_branch"

query "do you want to use this branch? (y/n)"

if [[ "$response" != "y" ]]; then
  error "checkout the branch you want to work with first"
fi

new_branch="CCM-${ticket_id}_REPOINT_DO_NOT_MERGE"
git checkout -b "$new_branch"
info "Switched to new branch: $new_branch"

# Step 3: Modify proxy files
step "modify proxy files"
python3 scripts/repoint-frontend/update_proxy_files.py "$environment"

# Step 4: Stage, commit, and push changes
step "stage, commit, and push changes"

git add proxies
info "Staged changes for proxy files."

git commit -m "CCM-${ticket_id}: repointed frontend" --no-verify
info "Committed changes with message: CCM-${ticket_id}: repointed frontend"

git push --set-upstream origin "$new_branch"
info "Pushed changes to branch: $new_branch"

# final output
echo ""
pr_url="https://github.com/NHSDigital/communications-manager-api/compare/$current_branch...$new_branch?expand=1"
info "Branch $new_branch created, frontend repointed, and changes pushed."
echo ""
info "To create a pull request for this branch, visit the following link:"
info "$pr_url"

