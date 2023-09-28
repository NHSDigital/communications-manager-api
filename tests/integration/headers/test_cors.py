import requests
import pytest
from lib import Assertions, Authentication
from lib.constants import INT_URL


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.inttest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(method):
    """
    .. py:function:: Test OPTIONS CORS headers
    """
    resp = requests.options(f"{INT_URL}", headers={
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
    .. py:function:: Test CORS headers
    """
    resp = getattr(requests, method)(f"{INT_URL}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
