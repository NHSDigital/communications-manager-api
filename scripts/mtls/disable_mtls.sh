#!/bin/bash
set -e

help() {
  echo "This script disables mTLS for a specified environment."
  echo ""
  echo "Usage: $0 [environment]"
  echo ""
  echo "Positional Arguments:"
  echo "  environment       Environment identifier (e.g., 'de-gith1')"
  echo ""
  echo "Options:"
  echo "  --help            Show this help message and exit."
  echo ""
  exit 1
}

if [[ "$1" == "--help" ]]; then
  help
fi

environment="$1"
if [ -z "$environment" ]; then
  echo "Environment not specified."
  help
fi

# Check AWS login status
if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo "You must have an active AWS SSO session to run this script."
  exit 1
fi

domain_name="comms-apim.$environment.communications.national.nhs.uk"

echo "Starting: remove mTLS (if set) for environment '$environment' on domain '$domain_name'..."

# Fetch domain status
domain_status=$(aws apigatewayv2 get-domain-name --domain-name "$domain_name" --output json)
if [ $? -ne 0 ]; then
  echo "Failed to get domain status for $domain_name."
  exit 1
fi

# Check if mtls is active
mtls_count=$(echo "$domain_status" | jq '(.MutualTlsAuthentication | length) // 0')

if [ "$mtls_count" -gt 0 ]; then
  mtls_is_enabled=1
else
  mtls_is_enabled=0
fi

# Get domain status message
domain_status_message=$(echo "$domain_status" | jq -r '.DomainNameConfigurations[0].DomainNameStatus')

if [ "$mtls_is_enabled" -eq 1 ] && [ "$domain_status_message" == "AVAILABLE" ]; then
  echo "mTLS is enabled and domain is in AVAILABLE state. Removing mTLS from $domain_name..."

  # Remove mTLS
  if ! aws apigateway update-domain-name \
    --domain-name "$domain_name" \
    --patch-operations op=remove,path=/mutualTlsAuthentication/truststoreUri \
    --no-cli-pager; then
    echo "Failed to remove mTLS from $domain_name."
    exit 1
  fi

  echo "Waiting for mTLS to be completely disabled and status to become AVAILABLE..."

  # Wait for mTLS to be disabled and status to be "AVAILABLE"
  max_attempts=60
  attempts=0
  while [ $attempts -lt $max_attempts ]; do
    sleep 10
    echo ""
    echo -n "Checking..."
    echo ""

    domain_status=$(aws apigatewayv2 get-domain-name --domain-name "$domain_name")
    echo $domain_status

    if [ $? -ne 0 ]; then
      echo "Failed to get domain status for $domain_name."
      continue
    fi

    mtls_count=$(echo "$domain_status" | jq '(.MutualTlsAuthentication | length) // 0')

    if [ "$mtls_count" -gt 0 ]; then
      mtls_is_enabled=1
    else
      mtls_is_enabled=0
    fi

    # Get domain status message
    domain_status_message=$(echo "$domain_status" | jq -r '.DomainNameConfigurations[0].DomainNameStatus')

    if [ "$mtls_is_enabled" -eq 0 ] && [ "$domain_status_message" == "AVAILABLE" ]; then
      printf "\n\nmTLS successfully removed and status is AVAILABLE for %s.\n" "$domain_name"
      break
    fi

    attempts=$((attempts + 1))
  done

  if [ $attempts -eq $max_attempts ]; then
    echo "Timed out waiting for mTLS to be disabled and status to become AVAILABLE."
    exit 1
  fi

elif [ "$mtls_is_enabled" -eq 1 ] && [ "$domain_status_message" == "UPDATING" ]; then
  echo "Domain is in $domain_status_message state for $domain_name. Try again in a few minutes."
  exit 1
else
  echo "mTLS is already disabled for $domain_name. No further action needed."
fi
