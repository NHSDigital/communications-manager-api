#!/bin/bash

: '
Usage:
scripts/repoint_frontend.sh -h
scripts/repoint_frontend.sh --help 
scripts/repoint_frontend.sh --list-steps
scripts/repoint_frontend.sh 0000 gith1
scripts/repoint_frontend.sh 0000 gith1 --from-step 1
scripts/repoint_frontend.sh 0000 gith1 --only-step 1

When this script is modified the following steps should be taken:
- Check the script works in standard mode              scripts/repoint_frontend.sh 0000 gith1
- Check step listing works                             scripts/repoint_frontend.sh --list-steps
- Check starting from a step works                     scripts/repoint_frontend.sh 0000 gith1 --from-step 1
- Check running a step in isolation works              scripts/repoint_frontend.sh --only-step 2
- Check directory requirement is checked and works     cd scripts && scripts/repoint_frontend.sh --list-steps
- Check AWS login status check works                   aws sso logout && scripts/repoint_frontend.sh
- Check error is returned on too many positional args  scripts/repoint_frontend.sh 0000 gith1 invalid
- 
'

true=0
false=1

# $1: message
info() {
  echo -e "[ INFO  ]: $1"
}

# $1: message
info_overwrite() {
  echo -n -e "\r[ INFO  ]: $1"
}

# $1: lines
info_multiline() {
  while IFS= read -r line; do
    info "$line"
  done <<< "$1"
}

# $1: message
step() {
  echo -e "[ STEP  ]: $1"
}

# $1: message
query() {
  read -p "[ QUERY ]: $1: " response
}

# $1: message, $2: info
error() {
  echo -e "[ ERROR ]: $1"

  if [[ -n "$2" ]]; then
    info "$2"
  fi

  exit 1
}

# $1: message
warn() {
  echo -e "[ WARN  ]: $1"
}

spacer() {
  echo ""
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

# shifts positional args from arguments into named vars
handle_positional_arg() {
  case $((positional_arg_index++)) in
    0) ticket_id="$1";;
    1) shortcode="$1";;
    *) error "too many positional arguments"
  esac
}

# FROM_STEP: where to continue execution from, used to skips steps already run
# 0: remove mTLS (if set)
# 1: create new branch for proxy modifications
# 2: modify proxy files
# 3: stage, commit, and push changes
# 4: await domainName available status (or timeout)

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
        *) handle_positional_arg "$1";;
    esac
    shift || true
done

# $1: step description
check_run_step() {
  # if only single step and started, exit now
  if [[ $single_step -eq $true && $started -eq $true ]]; then
    exit 0
  fi

  # if only listing steps, list step and move on (do not run)
  if [ $list_steps_only -eq $true ]; then
    echo "  $((current_step++)): $1"
    #current_step=$current_step
    return $false
  fi

  # if already started, carry on
  if [ $started -eq $true ]; then
    spacer
    step "running: $1"
    return $true
  fi

  # increments current step each time function is called (after access)
  if [ $((current_step++)) -ge $from_step ]; then
    spacer
    step "running: $1"
    started=$true
    return $true
  fi

  # step hasn't been reached yet
  spacer
  step "skipping: $1"
  return $false
}

# doesn't validate the positional args if only listing steps
if [[ $list_steps_only -eq $false ]]; then
  # check if a ticket ID was provided
  if [[ -z "$ticket_id" ]]; then
    error "missing argument: ticket ID (numeric only)" "usage: $0 <ticket ID: 0000> <shortcode: gith1>"
  fi

  # check if a ticket shortcode was provided
  if [[ -z "$shortcode" ]]; then
    error "missing argument: shortcode" "usage: $0 <ticket ID: 0000> <shortcode: gith1>"
  fi
fi

info "initial validation passed"

if check_run_step "remove mTLS (if set)"; then
  # check if mTLS set on env
  domain_name="comms-apim.de-$shortcode.communications.national.nhs.uk"
  domain_status=$(aws apigateway get-domain-name --domain-name $domain_name)

  if echo "$domain_status" | jq -re 'has("mutualTlsAuthentication")' > /dev/null 2>&1; then
    aws apigateway update-domain-name \
      --domain-name  $domain_name \
      --patch-operations op=remove,path=/mutualTlsAuthentication/truststoreUri
  fi
fi

if check_run_step "create new branch for proxy modifications"; then
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  exit_on_failure "failed to get current git branch"

  repsonse=""
  info "current branch is: $current_branch"
  query "do you want to use this branch? (y/n)"
  
  if [[ "$response" != "y" ]]; then
    error "checkout the branch you want to work with first"
  fi

  # create and checkout the new branch using the ticket ID
  new_branch="CCM-${ticket_id}_REPOINT_DO_NOT_MERGE"
  git checkout -b "$new_branch"
  exit_on_failure "failed to checkout branch $new_branch"
fi

if check_run_step "modify proxy files"; then
  output=$(python3 scripts/repoint_frontend.py $shortcode 2>&1)
  exit_on_failure "python repoint script failed" "\n $output"
  info_multiline "$output"
fi

commit_made=$false
if check_run_step "stage, commit, and push changes"; then
  git add proxies
  exit_on_failure "filed to stage changes (git add)"
  
  git commit -m "CCM-${ticket_id}: repointed frontend" --no-verify  # verify breaks on my machine, will fix this in due course
  exit_on_failure "failed to commit changes (git commit)"

  git push --set-upstream origin "$new_branch"
  exit_on_failure "failed to push changes (git push)"
  commit_made=$true
fi

# wait for mTLS update to complete
if check_run_step "mTLS update - await domainName available status (or timeout)"; then
  start_time=$(date +%s)
  domain_name_available=$false
  timeout_seconds=300
  domain_name="comms-apim.de-$shortcode.communications.national.nhs.uk"

  # timeout set to 300 seconds /5 minutes
  while [ $(( $(date +%s) - start_time )) -lt $timeout_seconds ]; do
    info_overwrite "waiting for available status (timeout in $(($timeout_seconds - ($(date +%s) - $start_time))) seconds)"

    domain_status=$(aws apigateway get-domain-name --domain-name $domain_name)
    exit_on_failure "aws sso session may have expired"

    domain_name_status=$( echo "$domain_status" | jq -er '.domainNameStatus')

    if [[ $domain_name_status == "AVAILABLE" ]]; then
      domain_name_available=$true
      echo ""  # prevents the previous info being overwritten
      info_overwrite "mTLS update has completed"
      break
    fi

    sleep 1
  done
  echo ""  # prevents the previous info being overwritten

  if [[ $domain_name_available -eq $false ]]; then 
    warn "timeout reached before domain name became available - mTLS update is likely still processing"
  fi
fi

# final output
if [[ $commit_made -eq $true ]]; then
  echo ""  # output spacing

  pr_url="https://github.com/NHSDigital/communications-manager-api/compare/$current_branch...$new_branch?expand=1"

  info "Branch $new_branch created, frontend repointed, and changes pushed."
  echo ""  # output spacing
  info "To create a pull request for this branch, visit the following link:"
  info "$pr_url"
fi
