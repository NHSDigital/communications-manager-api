import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import METHODS, DEFAULT_CONTENT_TYPE, VALID_ENDPOINTS

HEADER_NAME = ["accept", "AcCePt"]
HEADER_VALUE = ["", "xyz/abc", "application/json; charset=utf-9"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("accept_header_name", HEADER_NAME)
@pytest.mark.parametrize("accept_header_value", HEADER_VALUE)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_406(
    nhsd_apim_proxy_url,
    accept_header_name,
    accept_header_value,
    correlation_id,
    method,
    endpoints
):
    """
    .. include:: ../../partials/content_types/test_406.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{endpoints}", headers={
        accept_header_name: accept_header_value,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        406,
        Generators.generate_not_acceptable_error() if method not in ["options", "head"] else None,
        correlation_id
    )

    assert resp.headers.get("Content-Type") == DEFAULT_CONTENT_TYPE
