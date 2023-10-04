import requests
import pytest
from lib.constants import METHODS, UNEXPECTED_429

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
    .. include:: ../../partials/content_types/test_application_response_type.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
