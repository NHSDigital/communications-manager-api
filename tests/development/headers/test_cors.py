import requests
import pytest
from lib import Assertions
from lib.constants.constants import VALID_ENDPOINTS


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]
ORIGIN = "https://my.website"


@pytest.mark.devtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_options(nhsd_apim_proxy_url, method, nhsd_apim_auth_headers, endpoints):
    """
    ..py:function:: test_cors_options

    .. include :: ../../partials/headers/test_cors_options.rst
    """
    resp = requests.options(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, ORIGIN)


@pytest.mark.devtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors(nhsd_apim_proxy_url, method, nhsd_apim_auth_headers, endpoints):
    """
    ..py:function:: test_cors

    .. include :: ../../partials/headers/test_cors.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": ORIGIN
    })

    Assertions.assert_cors_headers(resp, ORIGIN)
