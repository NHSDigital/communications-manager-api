#!/bin/bash

# copy the integration collection
echo " "
echo "Downloading integration collection...."
curl -s -X GET "https://api.postman.com/collections/28740466-fbe32763-302e-4a0b-b6e9-3a20f1bde923?access_key=${INTEGRATION_COLLECTION_API_KEY}" | json_pp > postman/CommunicationsManager.Integration.postman_collection.json
echo "done!"

# copy the sandbox collection
echo " "
echo "Downloading sandbox collection...."
curl -s -X GET "https://api.postman.com/collections/28740466-ec078d1e-d4d7-4460-92b9-7d79d51f967a?access_key=${SANDBOX_COLLECTION_API_KEY}" | json_pp > postman/CommunicationsManager.Sandbox.postman_collection.json
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
