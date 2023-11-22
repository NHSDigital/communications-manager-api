import requests
import pytest
from lib import Assertions, Generators, Error_Handler

CORRELATION_IDS = [None, "19645ac5-b81b-4f05-9630-5c687ad05f71"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_internal_server_error_get(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. include:: ../../partials/test_500_internal_error_prefer.rst
    """
    resp = getattr(requests, method)(nhsd_apim_proxy_url, headers={
        "Prefer": "code=500",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-Correlation-Id": correlation_id
    })

    Error_Handler.handle_504_retry(resp)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_internal_server_error() if method not in ["options", "head"] else None,
        correlation_id
    )
