#!/bin/bash

# check if in project root
current_dir=$(basename "$PWD")
if [[ "$current_dir" != "communications-manager-api" ]]; then
  echo "Error: You must be in the project root directory to run this script."
  exit 1
fi

# check if a ticket ID was provided as a command-line argument
if [[ -z "$1" ]]; then
  echo "Error: Ticket ID (numeric only) is required."
  echo "Usage: $0 <ticket ID: 0000> <shortcode: gith1>"
  exit 1
fi

if [[ -z "$2" ]]; then
  echo "Error: Shortcode is required."
  echo "Usage: $0 <ticket ID: 0000> <shortcode: gith1>"
  exit 1
fi

ticket_id=$1
shortcode=$2

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ $? -ne 0 ]]; then
  echo "Error: Failed to get current git branch. Exiting."
  exit 1
fi

echo "Current branch is: $current_branch"
read -p "Do you want to use this branch? (y/n): " response

if [[ "$response" != "y" ]]; then
  echo "Checkout the branch you want to work with first."
  exit 1
fi

echo ""  # output spacing

# create and checkout the new branch using the ticket ID
new_branch="CCM-${ticket_id}_REPOINT_DO_NOT_MERGE"
git checkout -b "$new_branch"
if [[ $? -ne 0 ]]; then
  echo "Error: Failed to checkout branch $new_branch. Exiting."
  exit 1
fi

echo ""  # output spacing

python3 scripts/repoint_frontend.py $shortcode
if [[ $? -ne 0 ]]; then
  echo "Error: Python script failed. Exiting."
  exit 1
fi

echo ""  # output spacing

git add proxies  # specified because it keeps trying to add this script whilst I test it!
if [[ $? -ne 0 ]]; then
  echo "Error: Failed to stage changes (git add). Exiting."
  exit 1
fi

git commit -m "CCM-${ticket_id}: repointed frontend" --no-verify
if [[ $? -ne 0 ]]; then
  echo "Error: Failed to stage changes (git commit). Exiting."
  exit 1
fi

git push --set-upstream origin "$new_branch"
if [[ $? -ne 0 ]]; then
  echo "Error: Failed to stage changes (git push). Exiting."
  exit 1
fi

echo ""  # output spacing
echo ""  # output spacing
echo ""  # output spacing

pr_url="https://github.com/NHSDigital/communications-manager-api/compare/$current_branch...$new_branch?expand=1"

echo "Branch $new_branch created, frontend repointed, and changes pushed."
echo ""  # output spacing
echo "To create a pull request for this branch, visit the following link:"
echo "$pr_url"
