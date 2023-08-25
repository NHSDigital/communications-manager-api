import uuid
from time import time
import os
import jwt
import requests
import json

tokens = {}


class Authentication():
    @staticmethod
    def generate_authentication(env="int"):
        global tokens

        if env == "int":
            api_key = os.environ.get("INTEGRATION_API_KEY")
            private_key = os.environ.get("INTEGRATION_PRIVATE_KEY")
            url = "https://int.api.service.nhs.uk/oauth2/token"
        else:
            api_key = os.environ.get("PRODUCTION_API_KEY")
            private_key = os.environ.get("PRODUCTION_PRIVATE_KEY")
            url = "https://api.service.nhs.uk/oauth2/token"

        if tokens.get(env, None) is None:
            pk_pem = None
            with open(private_key, "r") as f:
                pk_pem = f.read()

            claims = {
                "sub": api_key,
                "iss": api_key,
                "jti": str(uuid.uuid4()),
                "aud": url,
                "exp": int(time()) + 180,
            }
            additional_headers = {"kid": "local"}

            j = jwt.encode(
                claims, pk_pem, algorithm="RS512", headers=additional_headers
            )

            resp = requests.post(url, headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }, data={
                "grant_type": "client_credentials",
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": j
            }
            )
            details = json.loads(resp.content)

            tokens[env] = (f"Bearer {details.get('access_token')}")

        return tokens.get(env)
