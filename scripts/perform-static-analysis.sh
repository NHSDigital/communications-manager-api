#!/bin/bash

set -e

# Script to perform static analysis of the repository content and upload the
# report to SonarCloud.
#
# Usage:
#   $ ./perform-static-analysis.sh
#
# Expects:
#   BRANCH_NAME=branch-name # Branch to report on
#   SONAR_TOKEN=token       # SonarCloud token
#
# Options:
#   VERBOSE=true  # Show all the executed commands, default is `false`

# ==============================================================================

# SEE: https://hub.docker.com/r/sonarsource/sonar-scanner-cli/tags, use the `linux/amd64` os/arch
image_version=5.0.1@sha256:494ecc3b5b1ee1625bd377b3905c4284e4f0cc155cff397805a244dee1c7d575

# ==============================================================================

function main() {

  cd $(git rev-parse --show-toplevel)
  create-report
}

function create-report() {

  docker run --rm --platform linux/amd64 \
    --volume $PWD:/usr/src \
    sonarsource/sonar-scanner-cli:$image_version \
      -Dproject.settings=/usr/src/scripts/config/sonar-scanner.properties \
      -Dsonar.branch.name="${BRANCH_NAME:-$(git rev-parse --abbrev-ref HEAD)}" \
      -Dsonar.token="$(echo $SONAR_TOKEN)"
}

function is_arg_true() {

  if [[ "$1" =~ ^(true|yes|y|on|1|TRUE|YES|Y|ON)$ ]]; then
    return 0
  else
    return 1
  fi
}

# ==============================================================================

is_arg_true "$VERBOSE" && set -x

main $*

exit 0
