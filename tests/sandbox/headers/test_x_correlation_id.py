import requests
import pytest
from lib.constants.constants import CORRELATION_IDS, METHODS, VALID_ENDPOINTS
from lib import error_handler, Assertions


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_correlation_id(
    nhsd_apim_proxy_url,
    correlation_id,
    method,
    endpoints
):
    """
    .. include:: ../../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        "x-correlation-id": correlation_id
    })

    error_handler.handle_retry(resp)

    Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
