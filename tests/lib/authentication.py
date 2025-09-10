import uuid
from time import time, sleep
import os
import jwt
import requests
import json
from .secret import Secret


class AuthenticationCache():
    def __init__(self):
        self.tokens = {}

        # Number of consecutive authentication tests before considering it worked.
        # This is required because apigee might be using load balancing.
        self.consecutive_tests = 4

        # Number of seconds before trying a test again
        self.time_between_tests = 10

        # Number of attempts before giving up. It can take up to 5 minutes for the
        # addition of a product to an application to take effect.
        # time_between_tests * max_tests = 300 seconds = 5 minutes.
        self.max_tests = 30

        # How long the token will stay valid
        self.token_validity = 180

    def generate_authentication(self, env, base_url):

        # For the test_url, note that we don't need a message_id that actually exists in
        # the backend. The test will only check that the API doesn't return a 401,
        # a 404 response means the authentication is working.
        test_url = f"{base_url}/v1/messages/message_id"

        if env in ["internal-dev", "internal-qa", "ref", "ref2"]:
            api_key = os.environ["NON_PROD_API_KEY"]
            private_key = os.environ["NON_PROD_PRIVATE_KEY"]
            url = "https://internal-dev.api.service.nhs.uk/oauth2/token"
            kid = "local"
        elif env == "internal-dev-test-1":
            api_key = os.environ["NON_PROD_API_KEY_TEST_1"]
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
        if env not in self.tokens or latest_token_expiry < int(time()) + 15:
            self.tokens[env] = self.generate_and_test_new_token(api_key, private_key, url, kid, test_url)

        bearer_token = self.tokens[env][0]
        return Secret(bearer_token)

    def generate_and_test_new_token(self, api_key, private_key, url, kid, test_url):
        new_token = None
        valid_auth = False

        for i in range(self.max_tests):
            print(f"Testing new token, attemp #{i+1}")
            if new_token is None:
                new_token = self.generate_new_token(api_key, private_key, url, kid)
                time_since_new_token = int(time())

            if self.test_token(test_url, new_token[0]):
                valid_auth = True
                break

            # The test failed, give apigee some time to update its cache.
            sleep(self.time_between_tests)

            if int(time()) - time_since_new_token > (self.token_validity / 2):
                # Token about to expire, generate a new one
                new_token = None

        if valid_auth:
            print("Token generated successfully")
            return new_token

        print("Could not generate token")
        raise RuntimeError("Could not generate token")

    def generate_new_token(self, api_key, private_key, url, kid):
        pk_pem = None
        with open(private_key, "r") as f:
            pk_pem = f.read()

        token_expiry = int(time()) + self.token_validity

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

        return (f"Bearer {details.get('access_token')}", token_expiry)

    def test_token(self, test_url, token):
        for _ in range(self.consecutive_tests):
            resp = requests.get(
                test_url,
                headers={
                    "Authorization": token,
                    "Accept": "*/*",
                    "Content-Type": "application/json"
                },
            )
            if resp.status_code == 401:
                return False

        return True
