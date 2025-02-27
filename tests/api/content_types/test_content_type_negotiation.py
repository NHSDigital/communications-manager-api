import requests
import pytest
from lib.constants.constants import METHODS, VALID_ENDPOINTS
from lib.fixtures import *  # NOSONAR
from lib import error_handler

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


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("accept_headers", ACCEPT_HEADERS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_application_response_type(url, bearer_token, accept_headers, method, endpoints):
    """
    .. include:: ../partials/content_types/test_application_response_type.rst
    """
    resp = getattr(requests, method)(f"{url}{endpoints}", headers={
        "Authorization": bearer_token.value,
        **accept_headers.get("headers")
    })

    error_handler.handle_retry(resp)

    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
