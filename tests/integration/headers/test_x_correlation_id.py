import requests
import pytest
from lib import Error_Handler
from lib.constants.constants import INT_URL, METHODS, VALID_ENDPOINTS
from lib.fixtures import *

CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_correlation_id(bearer_token_int, correlation_id, method, endpoints):
    """
    .. include:: ../../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{endpoints}", headers={
        "Authorization": bearer_token_int,
        "x-correlation-id": correlation_id
    })

    Error_Handler.handle_retry(resp)

    Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
