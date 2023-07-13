import requests
import pytest


CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]
REQUEST_PATH = ["", "/", "/api/v1/send", "/v1/message-batches", "/v1/message-batches/"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


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
    assert resp.headers.get("x-correlation-id") == correlation_id
