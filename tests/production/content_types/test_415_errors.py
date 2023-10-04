import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants import *

CONTENT_TYPE_NAME = ["content-type", "CONTENT_TYPE", "Content_Type", "conTENT_tYpe"]
CONTENT_TYPE_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]
METHODS = ["post", "put", "patch"]


@pytest.mark.prodtest
@pytest.mark.parametrize("content_type_name", CONTENT_TYPE_NAME)
@pytest.mark.parametrize("content_type_value", CONTENT_TYPE_VALUE)
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_415_invalid(
    content_type_name,
    content_type_value,
    request_path,
    correlation_id,
    method
):
    """
    .. py:function:: Scenario: An API consumer submitting a request with \
        an invalid content type receives a 415 'Unsupported Media' response

        | **Given** the API consumer provides an invalid content type header
        | **When** the request is submitted
        | **Then** the response is a 415 unsupported media error

    **Asserts**
    - API Recognises headers in case insensitive formats
    - Response returns a 415 'Unsupported Media' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided
    - Response returns the default content type if none is provided

    .. include:: ../../partials/invalid_content_type_headers.rst
    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{request_path}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        415,
        Generators.generate_unsupported_media_error(),
        correlation_id
    )
