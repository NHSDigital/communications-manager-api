import requests
import pytest
from lib import Error_Handler
from lib.constants import MESSAGE_BATCHES_ENDPOINT


CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_with_x_correlation_id(
    nhsd_apim_proxy_url,
    correlation_id,
    method,
    nhsd_apim_auth_headers
):
    """
    ..py:function:: test_request_with_x_correlation_id

    .. include:: ../../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **nhsd_apim_auth_headers,
        "x-correlation-id": correlation_id
    })

    Error_Handler.handle_retry(resp)

    assert resp.headers.get("x-correlation-id") == correlation_id
