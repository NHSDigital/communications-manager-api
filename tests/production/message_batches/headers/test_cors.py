import requests
import pytest
from lib import Assertions, Authentication
from lib.constants.constants import PROD_URL
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(method):
    """
    .. include :: ../../partials/headers/test_cors_options.rst
    """
    resp = requests.options(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.prodtest
@pytest.mark.parametrize("method", TEST_METHODS)
def test_cors(method):
    """
    .. include :: ../../partials/headers/test_cors.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
