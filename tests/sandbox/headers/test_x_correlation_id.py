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
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": correlation_id
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("x-correlation-id") == correlation_id
