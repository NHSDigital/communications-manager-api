import requests
import pytest
from lib import Authentication
from lib.constants import INT_URL, METHODS, UNEXPECTED_429

CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]
REQUEST_PATH = ["", "/", "/api/v1/send", "/v1/message-batches", "/v1/message-batches/"]


@pytest.mark.inttest
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_request_with_x_correlation_id(
    request_path,
    correlation_id,
    method,
):
    resp = getattr(requests, method)(f"{INT_URL}{request_path}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "x-correlation-id": correlation_id
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("x-correlation-id") == correlation_id
