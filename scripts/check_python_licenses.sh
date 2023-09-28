#!/bin/bash
set -euo pipefail

LICENSES=$(poetry run pip-licenses)
INCOMPATIBLE_LIBS=$(echo "$LICENSES" | grep 'GPL' | grep -v 'LGPL' || true)

# CCM-1813
#
# Allowing docutils as part of sphinx - this is not shipped as part of the
# software but is utilised for generating our documentation before it is
# checked into the repository.

INCOMPATIBLE_LIBS=$(echo $INCOMPATIBLE_LIBS | grep -v 'docutils' || true)

if [[ -z $INCOMPATIBLE_LIBS ]]; then
    exit 0
else
    echo "The following libraries were found which are not compatible with this project's license:"
    echo "$INCOMPATIBLE_LIBS"
    exit 1
fi