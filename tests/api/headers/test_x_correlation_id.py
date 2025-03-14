import requests
import pytest
from lib import error_handler, Assertions
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import VALID_ENDPOINTS


CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_correlation_id(
    url,
    bearer_token,
    correlation_id,
    method,
    endpoints
):
    """
    ..py:function:: test_request_with_x_correlation_id

    .. include:: ../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{url}{endpoints}", headers={
        "Authorization": bearer_token.value,
        "x-correlation-id": correlation_id
    })

    error_handler.handle_retry(resp)

    Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
