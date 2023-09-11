import json
import os

api_key = os.environ.get("INTEGRATION_API_KEY")
private_key_location = os.environ.get("INTEGRATION_PRIVATE_KEY")
private_key = None


with open(private_key_location, "r") as f:
    private_key = f.read()


dictionary = {
    "id": "c3ec9788-d499-4856-833c-b3c46438a18a",
    "name": "Integration",
    "values": [
        {
            "key": "api_key",
            "value": api_key,
            "type": "secret",
            "enabled": True
        },
        {
            "key": "private_key",
            "value": private_key,
            "type": "secret",
            "enabled": True
        },
        {
            "key": "authorization_header_value",
            "value": "",
            "type": "secret",
            "enabled": True
        },
        {
            "key": "correlation_id",
            "value": "",
            "type": "default",
            "enabled": True
        },
        {
            "key": "mime_type",
            "value": "application/vnd.api+json",
            "type": "default",
            "enabled": True
        },
        {
            "key": "message_batch_reference",
            "value": "",
            "type": "default",
            "enabled": True
        }
    ],
    "_postman_variable_scope": "environment",
    "_postman_exported_at": "2023-08-22T10:21:49.461Z",
    "_postman_exported_using": "Postman/10.17.2-230814-1237"
}

# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("postman/Integration.test.postman_environment.json", "w") as outfile:
    outfile.write(json_object)
