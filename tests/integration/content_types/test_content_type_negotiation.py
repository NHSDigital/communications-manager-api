import requests
import pytest
from lib import Authentication, Error_Handler
from lib.constants import INT_URL, METHODS

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


@pytest.mark.inttest
@pytest.mark.parametrize("accept_headers", ACCEPT_HEADERS)
@pytest.mark.parametrize("method", METHODS)
def test_application_response_type(accept_headers, method):
    """
    .. py:function:: Test content type negotiation
    """
    resp = getattr(requests, method)(f"{INT_URL}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        **accept_headers.get("headers")
    })

    Error_Handler.handle_retry(resp)

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
