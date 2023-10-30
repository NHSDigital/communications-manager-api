import requests
import pytest
from lib import Assertions, Authentication
from lib.constants.constants import INT_URL, VALID_ENDPOINTS


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.inttest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_cors_options(method, endpoints):
    """
    .. include :: ../../partials/headers/test_cors_options.rst
    """
    resp = requests.options(f"{INT_URL}{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.inttest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_cors(method, endpoints):
    """
    .. include :: ../../partials/headers/test_cors.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
