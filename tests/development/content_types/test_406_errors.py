import requests
import pytest
from lib import Assertions, Generators
from lib.constants import DEFAULT_CONTENT_TYPE

HEADER_NAME = ["accept", "ACCEPT", "Accept", "AcCePt"]
HEADER_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.devtest
@pytest.mark.parametrize("accept_header_name", HEADER_NAME)
@pytest.mark.parametrize("accept_header_value", HEADER_VALUE)
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406(
    nhsd_apim_proxy_url,
    accept_header_name,
    accept_header_value,
    request_path,
    correlation_id,
    method,
    nhsd_apim_auth_headers
):
    """
    .. py:function:: Test 406 responses
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
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
