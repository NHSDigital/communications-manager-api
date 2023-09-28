import requests
import pytest
from lib import Authentication
from lib.constants import *

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
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.prodtest
@pytest.mark.parametrize("accept_headers", ACCEPT_HEADERS)
@pytest.mark.parametrize("method", METHODS)
def test_application_response_type(accept_headers, method):
    """
    .. py:function:: Test content type negotiation
    """
    resp = getattr(requests, method)(f"{PROD_URL}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        **accept_headers.get("headers")
    })

    if resp.status_code == 429:
        raise AssertionError('Unexpected 429')

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
