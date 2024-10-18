#!/bin/bash

"""
Usage:
scripts/repoint_frontend.sh -h
scripts/repoint_frontend.sh --help 
scripts/repoint_frontend.sh --list-steps
scripts/repoint_frontend.sh 0000 gith1
scripts/repoint_frontend.sh 0000 gith1 --from-step 1
scripts/repoint_frontend.sh 0000 gith1 --only-step 1

When this script is modified the following steps should be taken:
- Check the script works in standard mode
- Check step listing works
- Check starting from a step works
- Check running a step in isolation works
- Check directory requirement is checked and works
- Check AWS login status check works
- Check error is returned on too many positional args

"""

true=0
false=1

# $1: message
info() {
  echo "[ INFO ]: $1."
}

# $1: message, $2: info
error() {
  echo "[ Error ]: $1."

  if [[ -n "$2" ]]; then
    info "$2"
  fi

  exit 1
}

# $1: message, $2: info
exit_on_failure() {
  if [[ $? -ne 0 ]]; then
    error "$1" "$2"
  fi
}

# check if in project root
current_dir=$(basename "$PWD")
if [[ "$current_dir" != "communications-manager-api" ]]; then
  error "you must be in the project root directory to run this script"
fi

# check aws login status
aws sts get-caller-identity > /dev/null 2>&1
exit_on_failure "you must have an active AWS SSO session to run this script"

positional_arg_index=0

handle_positional_arg() {
  case positional_arg_index++ in
    0) ticket_id=$1;;
    1) shortcode=$1;;
    *) error "too many positional arguments"
  esac
}

# FROM_STEP: where to continue execution from, used to skips steps already run
# 0: remove mTLS (if set)
# 1: create new branch for proxy modifications
# 2: modify proxy files
# 3: stage, commit, and push changes
# 4: 

from_step=0
current_step=0
started=$false
single_step=$false
list_steps_only=$false

# sets list_steps_only to true, this is used by check_run_step
list_steps() {
  list_steps_only=$true
  echo "STEPS:"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --from-step) from_step=$2; shift 2;;
        --only-step) from_step=$2; single_step=$true; shift 2;;
        --list-steps) list_steps;;
        -*) error "unknown option: $1" >&2;;
        *) handle_positional_arg;;
    esac
    shift
done

# $1: step description
check_run_step() {
  # if only single step and started, exit now
  if [[$single_step && $started]]; then
    exit 0
  fi

  # if only listing steps, list step and move on (do not run)
  if list_steps_only; then
    echo "$current_step++ $1"
    return $false
  fi

  # if already started, carry on
  if [ started -e $true ]; then
    info "running step: $1"
    return $true
  fi

  # increments current step each time function is called (after access)
  if [$current_step++ -ge $from_step]; then
    
    started=$true
    return $true
  fi

  # step hasn't been reached yet
  info "skipping step: $1"
  return $false
}

# doesn't validate the positional args if only listing steps
if [[ $list_steps_only -e $false ]]; then
  # check if a ticket ID was provided
  if [[ -z "$ticket_id" ]]; then
    error "missing argument: ticket ID (numeric only)" "usage: $0 <ticket ID: 0000> <shortcode: gith1>"
  fi

  # check if a ticket shortcode was provided
  if [[ -z "$shortcode" ]]; then
    error "missing argument: shortcode" "usage: $0 <ticket ID: 0000> <shortcode: gith1>"
  fi
fi

if check_run_step "remove mTLS (if set)"; then
  # check if mTLS set on env
  domain_name="comms-apim.de-$shortcode.communications.national.nhs.uk"
  domain_status=$(aws apigateway get-domain-name --domain-name $domain_name > /dev/null)

  if echo "$domain_status" | jq 'has("mutualTlsAuthentication")' > /dev/null 2>&1; then
    aws apigateway update-domain-name \
      --domain-name  $domain_name \
      --patch-operations op=remove,path=/mutualTlsAuthentication/truststoreUri
  fi
fi

if check_run_step "create new branch for proxy modifications"; then
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  exit_on_failure "failed to get current git branch"

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
  exit_on_failure "failed to checkout branch $new_branch"

  echo ""  # output spacing
fi

if check_run_step "modify proxy files"; then
  python3 scripts/repoint_frontend.py $shortcode
  exit_on_failure "python repoint script failed"

  echo ""  # output spacing
fi

commit_made=$false
if check_run_step "stage, commit, and push changes"; then
  git add proxies
  exit_on_failure "filed to stage changes (git add)"

  git commit -m "CCM-${ticket_id}: repointed frontend" --no-verify  # verify breaks on my machine, will fix this in due course
  exit_on_failure "failed to commit changes (git commit)"

  #git push --set-upstream origin "$new_branch"
  #exit_on_failure "failed to push changes (git push)"
  #commit_made=$true
fi

# wait for mTLS to complete
if check_run_step ""; then

fi

# final output
if [[ commit_made -e $true ]]; then
  echo ""  # output spacing
  echo ""  # output spacing
  echo ""  # output spacing

  pr_url="https://github.com/NHSDigital/communications-manager-api/compare/$current_branch...$new_branch?expand=1"

  echo "Branch $new_branch created, frontend repointed, and changes pushed."
  echo ""  # output spacing
  echo "To create a pull request for this branch, visit the following link:"
  echo "$pr_url"
fi
