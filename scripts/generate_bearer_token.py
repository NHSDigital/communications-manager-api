import uuid
from time import time
import os
import jwt
import requests
import json

with open("dev-private.key", "r") as f:
    private_key = f.read()

api_key = os.environ.get("API_KEY")
env = os.environ.get("API_ENVIRONMENT")

claims = {
  "sub": api_key,
  "iss": api_key,
  "jti": str(uuid.uuid4()),
  "aud": f"https://{env}.api.service.nhs.uk/oauth2/token",
  "exp": int(time()) + 180,
}

additional_headers = {"kid": "local"}

j = jwt.encode(
  claims, private_key, algorithm="RS512", headers=additional_headers
)

resp = requests.post(f"https://{env}.api.service.nhs.uk/oauth2/token", headers={
    "Content-Type": "application/x-www-form-urlencoded"
  }, data={
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": j
  }
)

details = json.loads(resp.content)
print(details)
print(f"Token is: {details.get('access_token', 'Unknown')}")
