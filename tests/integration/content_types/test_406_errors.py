import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.constants import CORRELATION_IDS, METHODS, INT_URL, DEFAULT_CONTENT_TYPE, VALID_ENDPOINTS

HEADER_NAME = ["accept", "ACCEPT", "Accept", "AcCePt"]
HEADER_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]


@pytest.mark.inttest
@pytest.mark.parametrize("accept_header_name", HEADER_NAME)
@pytest.mark.parametrize("accept_header_value", HEADER_VALUE)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_406(
    accept_header_name,
    accept_header_value,
    correlation_id,
    method,
    endpoints
):
    """
    .. include:: ../../partials/content_types/test_406.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{endpoints}", headers={
        accept_header_name: accept_header_value,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('int')}"
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        406,
        Generators.generate_not_acceptable_error() if method not in ["options", "head"] else None,
        correlation_id
    )

    assert resp.headers.get("Content-Type") == DEFAULT_CONTENT_TYPE
