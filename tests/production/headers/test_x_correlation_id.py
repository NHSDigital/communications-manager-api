import requests
import pytest
from lib import Authentication, Error_Handler, Assertions

from lib.constants.constants import METHODS, PROD_URL
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.fixtures import *

CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_request_with_x_correlation_id(
    bearer_token_prod,
    correlation_id,
    method,
):
    """
    .. include:: ../../partials/headers/test_request_with_x_correlation_id.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": bearer_token_prod,
        "x-correlation-id": correlation_id
    })

    Error_Handler.handle_retry(resp)

    Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
