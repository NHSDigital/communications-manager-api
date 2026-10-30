#!/bin/bash
set -e

help() {
  echo "This script disables client certificate verification for a specified environment."
  echo ""
  echo "It is primarily called by repoint_frontend.sh as part of the process for reconfiguring"
  echo "the communications-manager-api APIs to point to a dynamic backend."
  echo ""
  echo "Usage: $0 [environment]"
  echo ""
  echo "Positional Arguments:"
  echo "  environment       Environment identifier (e.g., 'de-gith1')"
  echo ""
  echo "Options:"
  echo "  --help            Show this help message and exit."
  echo ""
}

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  help
  exit 1
fi

environment="$1"
if [ -z "$environment" ]; then
  echo "missing argument: [environment]. See '$0 --help'"
  exit 1
fi

# Check AWS login status
if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo "You must have an active AWS SSO session to run this script."
  exit 1
fi

# Get the AWS account ID
account_id=$(aws sts get-caller-identity --query "Account" --output text)

# Check if the account ID matches dev or dev 2
if [[ "$account_id" != "257995483745" && "$account_id" != "637423498933" ]]; then
  echo "This script can only be run in a dev or dev 2 account. Current account ID is $account_id."
  exit 1
fi

function_name="comms-$environment-api-oa3-commsapi-apim-authorizer-lambda"
variable_name="CLIENT_CERTIFICATE_VERIFICATION_MODE"
variable_value="OFF"

echo "Starting: set $variable_name=$variable_value for environment '$environment' on lambda '$function_name'..."

# Fetch current environment variables
if ! current_variables=$(aws lambda get-function-configuration \
  --function-name "$function_name" \
  --query "Environment.Variables" \
  --output json); then
  echo "Failed to get configuration for $function_name."
  exit 1
fi

current_value=$(echo "$current_variables" | jq -r --arg name "$variable_name" '(. // {})[$name] // empty')

if [ "$current_value" == "$variable_value" ]; then
  echo "$variable_name is already $variable_value for $function_name. No further action needed."
  exit 0
fi

echo "$variable_name is currently '${current_value:-unset}'. Setting to $variable_value on $function_name..."

# Lambda replaces the whole variable set on update, so existing variables must be merged in
updated_environment=$(echo "$current_variables" | jq -c \
  --arg name "$variable_name" \
  --arg value "$variable_value" \
  '{Variables: ((. // {}) + {($name): $value})}')

if ! aws lambda update-function-configuration \
  --function-name "$function_name" \
  --environment "$updated_environment" \
  --no-cli-pager >/dev/null; then
  echo "Failed to update $variable_name on $function_name."
  exit 1
fi

echo "Waiting for $function_name update to complete..."

if ! aws lambda wait function-updated-v2 --function-name "$function_name"; then
  echo "Timed out waiting for $function_name update to complete."
  exit 1
fi

printf "\n\n%s successfully set to %s for %s.\n" "$variable_name" "$variable_value" "$function_name"
