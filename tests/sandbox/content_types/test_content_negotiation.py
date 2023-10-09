import requests
import pytest
from lib.constants import METHODS
from lib import Error_Handler

ACCEPT_HEADERS = [
    {
        "headers": {
            "Accept": "application/vnd.api+json"
        },
        "expect": "application/vnd.api+json"
    },
    {
        "headers": {
            "Accept": "*/*"
        },
        "expect": "application/vnd.api+json"
    },
    {
        "headers": {
            "Accept": "application/json"
        },
        "expect": "application/json"
    }
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("accept_headers", ACCEPT_HEADERS)
@pytest.mark.parametrize("method", METHODS)
def test_application_response_type(nhsd_apim_proxy_url, accept_headers, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a valid accept header \
        receives a response containing the expected accept header

        | **Given** the API consumer provides a valid accept header
        | **When** the request is submitted
        | **Then** the response returned is in the format requested

    **Asserts**
    - Response returns the expected accept header

    .. include:: ../../partials/valid_accept_headers.rst
    .. include:: ../../partials/methods.rst

    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))

    Error_Handler.handle_retry(resp)

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
