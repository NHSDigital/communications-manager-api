import requests
import pytest
from lib import Assertions


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(nhsd_apim_proxy_url, method):
    """
    .. py:function:: Test OPTIONS CORS response
    """
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.sandboxtest
@pytest.mark.parametrize("method", TEST_METHODS)
def test_cors(nhsd_apim_proxy_url, method):
    """
    .. py:function:: Test CORS response
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
