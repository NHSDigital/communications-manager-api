#!/bin/bash

# copy the integration collection
echo " "
echo "Downloading integration collection...."
curl -s -X GET "https://api.postman.com/collections/41628342-9c132bcd-f76f-448f-a58c-ba38c5d64d4f?access_key=${INTEGRATION_COLLECTION_API_KEY}" | json_pp > postman/NhsNotify.Integration.postman_collection.json
echo "done!"

# copy the sandbox collection
echo " "
echo "Downloading sandbox collection...."
curl -s -X GET "https://api.postman.com/collections/41628342-33dcc9d0-8ccc-4756-8ccb-237fd78337f5?access_key=${SANDBOX_COLLECTION_API_KEY}" | json_pp > postman/NhsNotify.Sandbox.postman_collection.json
echo "done!"

# ensure we notify that the environments need to be exported manually
echo " "
echo "==========================================="
echo "EXPORT ENVIRONMENTS "
echo " "
echo "Ensure you export the relevant environments"
echo "manually using the postman app. "
echo " "
echo "These are not exported automatically!"
echo "==========================================="
