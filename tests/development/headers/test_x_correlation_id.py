import requests
import pytest
from lib.constants import UNEXPECTED_429


CORRELATION_IDS = [None, "a17669c8-219a-11ee-ba86-322b0407c489"]
REQUEST_PATH = ["", "/", "/api/v1/send", "/v1/message-batches", "/v1/message-batches/"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.devtest
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_with_x_correlation_id(
    nhsd_apim_proxy_url,
    request_path,
    correlation_id,
    method,
    nhsd_apim_auth_headers
):
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "x-correlation-id": correlation_id
    })

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.headers.get("x-correlation-id") == correlation_id
