import requests
import pytest
from lib import Assertions
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import VALID_ENDPOINTS


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]
ORIGIN = "https://my.website"


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_cors_options(url, bearer_token, method, endpoints):
    """
    ..py:function:: test_cors_options

    .. include :: ../partials/headers/test_cors_options.rst
    """
    resp = requests.options(f"{url}{endpoints}", headers={
        "Authorization": bearer_token.value,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, ORIGIN)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_cors(url, bearer_token, method, endpoints):
    """
    ..py:function:: test_cors

    .. include :: ../partials/headers/test_cors.rst
    """
    resp = getattr(requests, method)(f"{url}{endpoints}", headers={
        "Authorization": bearer_token.value,
        "Accept": "*/*",
        "Origin": ORIGIN
    })

    Assertions.assert_cors_headers(resp, ORIGIN)
