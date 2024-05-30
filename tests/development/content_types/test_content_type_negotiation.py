import requests
import pytest
from lib.constants.constants import METHODS, VALID_ENDPOINTS
from lib.fixtures import *
from lib import Error_Handler

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
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_application_response_type(nhsd_apim_proxy_url, bearer_token_internal_dev, accept_headers, method, endpoints):
    """
    .. include:: ../../partials/content_types/test_application_response_type.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        "Authorization": bearer_token_internal_dev,
        **accept_headers.get("headers")
    })

    Error_Handler.handle_retry(resp)

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
