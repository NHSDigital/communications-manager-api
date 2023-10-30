import requests
import pytest
from lib import Authentication, Error_Handler
from lib.constants.constants import INT_URL, METHODS, VALID_ENDPOINTS

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
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_application_response_type(accept_headers, method, endpoints):
    """
    .. include:: ../../partials/content_types/test_application_response_type.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        **accept_headers.get("headers")
    })

    Error_Handler.handle_retry(resp)

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
