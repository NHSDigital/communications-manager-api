import requests
import pytest
from lib.constants import CORRELATION_IDS, METHODS, UNEXPECTED_429


REQUEST_PATH = ["", "/", "/api/v1/send", "/v1/message-batches", "/v1/message-batches/"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_request_with_x_correlation_id(
    nhsd_apim_proxy_url,
    request_path,
    correlation_id,
    method
):
    """
    .. py:function:: Scenario: An API consumer submitting a request with to a request with an 'X-Correlation-Id' \
        header receives a response reflecting the X-Correlation-Id value

        | **Given** the API consumer provides an x-correlation-id header
        | **When** the request is submitted
        | **Then** the response is contains an x-correlation-id header

    **Asserts**
    - Response returns a 504 status code
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst

    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": correlation_id
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("x-correlation-id") == correlation_id
