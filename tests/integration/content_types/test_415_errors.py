import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.constants import INT_URL, CORRELATION_IDS, VALID_ENDPOINTS

CONTENT_TYPE_NAME = ["content-type", "CONTENT_TYPE", "Content_Type", "conTENT_tYpe"]
CONTENT_TYPE_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
METHODS = ["post", "put", "patch"]


@pytest.mark.inttest
@pytest.mark.parametrize("content_type_name", CONTENT_TYPE_NAME)
@pytest.mark.parametrize("content_type_value", CONTENT_TYPE_VALUE)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_415_invalid(
    content_type_name,
    content_type_value,
    correlation_id,
    method,
    endpoints
):
    """
    .. include:: ../../partials/content_types/test_415_invalid.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
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
