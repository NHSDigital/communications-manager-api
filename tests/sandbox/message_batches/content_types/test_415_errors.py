import requests
import pytest
from lib import Assertions, Generators
from lib.constants import MESSAGE_BATCHES_ENDPOINT

CONTENT_TYPE_NAME = ["content-type", "CONTENT_TYPE", "Content_Type", "conTENT_tYpe"]
CONTENT_TYPE_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
METHODS = ["post", "put", "patch"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("content_type_name", CONTENT_TYPE_NAME)
@pytest.mark.parametrize("content_type_value", CONTENT_TYPE_VALUE)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_415_invalid(
    nhsd_apim_proxy_url,
    content_type_name,
    content_type_value,
    correlation_id,
    method
):
    """
    .. include:: ../../partials/content_types/test_415_invalid.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
