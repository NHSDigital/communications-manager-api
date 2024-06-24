import requests
import pytest
from lib import Error_Handler
from lib.fixtures import *
from lib.constants.constants import VALID_ENDPOINTS


CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_correlation_id(
    nhsd_apim_proxy_url,
    bearer_token_internal_dev,
    correlation_id,
    method,
    endpoints
):
    """
    ..py:function:: test_request_with_x_correlation_id

    .. include:: ../../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        "Authorization": bearer_token_internal_dev,
        "x-correlation-id": correlation_id
    })

    Error_Handler.handle_retry(resp)

    assert resp.headers.get("x-correlation-id") == correlation_id
