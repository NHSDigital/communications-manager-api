import requests
import pytest
from lib import Authentication, Error_Handler, Assertions
from lib.constants.constants import INT_URL, METHODS, VALID_ENDPOINTS

CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_correlation_id(correlation_id, method, endpoints):
    """
    .. include:: ../../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "x-correlation-id": correlation_id
    })

    Error_Handler.handle_retry(resp)

    Assertions.assertEquals(resp.headers.get("x-correlation-id"), correlation_id)
