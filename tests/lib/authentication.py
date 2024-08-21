import uuid
from time import time
import os
import jwt
import requests
import json
from .secret import Secret


class AuthenticationCache():
    def __init__(self):
        self.tokens = {}

    def generate_authentication(self, env):

        if env == "internal-dev":
            api_key = os.environ["NON_PROD_API_KEY"]
            private_key = os.environ["NON_PROD_PRIVATE_KEY"]
            url = "https://internal-dev.api.service.nhs.uk/oauth2/token"
            kid = "local"
        elif env == "int":
            api_key = os.environ.get("INTEGRATION_API_KEY")
            private_key = os.environ.get("INTEGRATION_PRIVATE_KEY")
            url = "https://int.api.service.nhs.uk/oauth2/token"
            kid = "local"
        elif env == "prod":
            api_key = os.environ.get("PRODUCTION_API_KEY")
            private_key = os.environ.get("PRODUCTION_PRIVATE_KEY")
            url = "https://api.service.nhs.uk/oauth2/token"
            kid = "prod-1"
        else:
            raise ValueError("Unknown value: ", env)

        _, latest_token_expiry = self.tokens.get(env, (None, 0))

        # Generate new token if latest token will expire in 15 seconds
        if env not in self.tokens or latest_token_expiry - 15 < int(time()):
            pk_pem = None
            with open(private_key, "r") as f:
                pk_pem = f.read()

            token_expiry = int(time()) + 180

            claims = {
                "sub": api_key,
                "iss": api_key,
                "jti": str(uuid.uuid4()),
                "aud": url,
                "exp": token_expiry,
            }
            additional_headers = {"kid": kid}

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

            self.tokens[env] = (f"Bearer {details.get('access_token')}", token_expiry)

        bearer_token = self.tokens[env][0]
        return Secret(bearer_token)
