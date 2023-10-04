import requests
import pytest
from lib import Authentication
from lib.constants import INT_URL, METHODS, UNEXPECTED_429

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
    .. include:: ../../partials/content_types/test_application_response_type.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        **accept_headers.get("headers")
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
