#!/usr/bin/env bash

# Note that this will be invoked by the git hook from the repo root, so cd .. isn't required

# These only need to be run once per workstation but are included to try and ensure they are present
./git-secrets --register-aws
./git-secrets --add-provider -- cat nhsd-git-secrets/nhsd-rules-deny.txt

# Scan all files within this repo for this commit
./git-secrets --scan
