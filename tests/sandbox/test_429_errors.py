import requests
import pytest
from lib import Assertions, Generators, error_handler

CORRELATION_IDS = [None, "0f160ae2-9b62-47bf-bdf0-c6a844d59488"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_too_many_requests_get(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. include:: ../../partials/timeouts/test_too_many_requests_get.rst
    """
    resp = getattr(requests, method)(nhsd_apim_proxy_url, headers={
        "Prefer": "code=429",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-Correlation-Id": correlation_id
    })

    error_handler.handle_504_retry(resp)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error() if method not in ["options", "head"] else None,
        correlation_id
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "5"
