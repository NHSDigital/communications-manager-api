import uuid
from time import time
import os
import jwt
import requests
import json

int_token = None


class Authentication():
    @staticmethod
    def generate_int_authentication():
        global int_token

        if int_token is None:
            api_key = os.environ.get("INTEGRATION_API_KEY")
            private_key = os.environ.get("INTEGRATION_PRIVATE_KEY")

            pk_pem = None
            with open(private_key, "r") as f:
                pk_pem = f.read()

            claims = {
                "sub": api_key,
                "iss": api_key,
                "jti": str(uuid.uuid4()),
                "aud": "https://int.api.service.nhs.uk/oauth2/token",
                "exp": int(time()) + 180,
            }
            additional_headers = {"kid": "local"}

            j = jwt.encode(
                claims, pk_pem, algorithm="RS512", headers=additional_headers
            )

            resp = requests.post("https://int.api.service.nhs.uk/oauth2/token", headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }, data={
                "grant_type": "client_credentials",
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": j
            }
            )
            details = json.loads(resp.content)

            int_token = (f"Bearer {details.get('access_token')}")

        return int_token

    @staticmethod
    def generate_prod_authentication():
        global prod_token

        if prod_token is None:
            api_key = os.environ.get("PRODUCTION_API_KEY")
            private_key = os.environ.get("PRODUCTION_PRIVATE_KEY")

            pk_pem = None
            with open(private_key, "r") as f:
                pk_pem = f.read()

            claims = {
                "sub": api_key,
                "iss": api_key,
                "jti": str(uuid.uuid4()),
                "aud": "https://api.service.nhs.uk/oauth2/token",
                "exp": int(time()) + 180,
            }
            additional_headers = {"kid": "local"}

            j = jwt.encode(
                claims, pk_pem, algorithm="RS512", headers=additional_headers
            )

            resp = requests.post("https://api.service.nhs.uk/oauth2/token", headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }, data={
                "grant_type": "client_credentials",
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": j
            }
            )
            details = json.loads(resp.content)

            prod_token = (f"Bearer {details.get('access_token')}")

        return prod_token
