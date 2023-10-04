import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants import *

HEADER_NAME = ["accept", "ACCEPT", "Accept", "AcCePt"]
HEADER_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]


@pytest.mark.prodtest
@pytest.mark.parametrize("accept_header_name", HEADER_NAME)
@pytest.mark.parametrize("accept_header_value", HEADER_VALUE)
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_406(
    accept_header_name,
    accept_header_value,
    request_path,
    correlation_id,
    method,
):
    """
    .. py:function:: Scenario: An API consumer submitting a request with \
        an invalid accept header receives a 406 'Not Acceptable' response

        | **Given** the API consumer provides an invalid accept header
        | **When** the request is submitted
        | **Then** the response is a 406 not acceptable error

    **Asserts**
    - API Recognises headers in case insensitive formats
    - Response returns a 406 'Not Acceptable' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided
    - Response returns the default content type if none is provided

    .. include:: ../../partials/invalid_accept_headers.rst
    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}/{request_path}", headers={
        accept_header_name: accept_header_value,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}",
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        406,
        Generators.generate_not_acceptable_error() if method not in ["options", "head"] else None,
        correlation_id
    )
