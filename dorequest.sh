#!/bin/bash

BRANCH=comms-pr-751
TOKEN=$(python3 scripts/generate_bearer_token.py 2>/dev/null | cut -d " " -f 3)
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d @request_body.json https://internal-dev.api.service.nhs.uk/${BRANCH}/v1/message-batches