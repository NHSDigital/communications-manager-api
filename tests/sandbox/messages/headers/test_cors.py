import requests
import pytest
from lib import Assertions
from lib.constants import MESSAGES_ENDPOINT

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(nhsd_apim_proxy_url, method):
    """
    .. include :: ../../partials/headers/test_cors_options.rst
    """
    resp = requests.options(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.sandboxtest
@pytest.mark.parametrize("method", TEST_METHODS)
def test_cors(nhsd_apim_proxy_url, method):
    """
    .. include :: ../../partials/headers/test_cors.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
