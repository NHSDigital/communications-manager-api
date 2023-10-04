import requests
import pytest
from lib.constants import METHODS, UNEXPECTED_429

DEFAULT_CONTENT_TYPE = "application/vnd.api+json"
ACCEPT_HEADERS = [
    {
        "headers": {
            "Accept": DEFAULT_CONTENT_TYPE
        },
        "expect": DEFAULT_CONTENT_TYPE
    },
    {
        "headers": {
            "Accept": "*/*"
        },
        "expect": DEFAULT_CONTENT_TYPE
    },
    {
        "headers": {
            "Accept": "application/json"
        },
        "expect": "application/json"
    }
]


@pytest.mark.devtest
@pytest.mark.parametrize("accept_headers", ACCEPT_HEADERS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_application_response_type(nhsd_apim_proxy_url, accept_headers, method, nhsd_apim_auth_headers):
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
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
