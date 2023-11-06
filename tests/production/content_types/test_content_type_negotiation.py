import requests
import pytest
from lib import Authentication, Error_Handler, Assertions
from lib.constants.constants import METHODS, PROD_URL, VALID_ENDPOINTS

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


@pytest.mark.prodtest
@pytest.mark.parametrize("accept_headers", ACCEPT_HEADERS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_application_response_type(accept_headers, method, endpoints):
    """
    .. include:: ../../partials/content_types/test_application_response_type.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        **accept_headers.get("headers")
    })

    Error_Handler.handle_retry(resp)

    Assertions.assertEquals(resp.headers.get("Content-Type"), accept_headers.get("expect"))
