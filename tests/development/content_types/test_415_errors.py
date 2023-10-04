import requests
import pytest
from lib import Assertions, Generators

CONTENT_TYPE_NAME = ["content-type", "CONTENT_TYPE", "Content_Type", "conTENT_tYpe"]
CONTENT_TYPE_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]
METHODS = ["post", "put", "patch"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.devtest
@pytest.mark.parametrize("content_type_name", CONTENT_TYPE_NAME)
@pytest.mark.parametrize("content_type_value", CONTENT_TYPE_VALUE)
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_415_invalid(
    nhsd_apim_proxy_url,
    content_type_name,
    content_type_value,
    request_path,
    correlation_id,
    method,
    nhsd_apim_auth_headers
):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        content type header receives a 415 'Unsupported Media' response

        | **Given** the API consumer provides an invalid content type header
        | **When** the request is submitted
        | **Then** the response is a 415 unsupported media error

    **Asserts**
    - Response returns a 415 'Unsupported Media' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/invalid_content_type_headers.rst
    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
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
