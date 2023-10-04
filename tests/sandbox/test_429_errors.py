import requests
import pytest
from lib import Assertions, Generators, Error_Handler

CORRELATION_IDS = [None, "0f160ae2-9b62-47bf-bdf0-c6a844d59488"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_too_many_requests_get(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        429 Prefer header receives a 429 'Quota' response

        | **Given** the API consumer provides a 429 prefer header
        | **When** the request is submitted
        | **Then** the response is a 429 quota error

    **Asserts**
    - Response returns a 429 'Quota' error
    - Response returns 'Retry-After' header
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst

    """
    resp = getattr(requests, method)(nhsd_apim_proxy_url, headers={
        "Prefer": "code=429",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-Correlation-Id": correlation_id
    })

    Error_Handler.handle_504_retry(resp)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error() if method not in ["options", "head"] else None,
        correlation_id
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "5"
