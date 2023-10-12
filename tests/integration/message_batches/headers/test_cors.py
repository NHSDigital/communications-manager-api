import requests
import pytest
from lib import Assertions, Authentication
from lib.constants.constants import INT_URL
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.inttest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(method):
    """
    .. include :: ../../partials/headers/test_cors_options.rst
    """
    resp = requests.options(f"{INT_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.inttest
@pytest.mark.parametrize("method", TEST_METHODS)
def test_cors(method):
    """
    .. include :: ../../partials/headers/test_cors.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
