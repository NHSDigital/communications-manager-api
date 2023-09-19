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
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
