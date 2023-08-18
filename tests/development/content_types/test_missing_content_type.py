import requests
import pytest

HEADER_NAME = ["", "accept", "ACCEPT", "Accept", "AcCePt"]
HEADER_VALUE = [""]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.devtest
@pytest.mark.parametrize("accept_header_name", HEADER_NAME)
@pytest.mark.parametrize("accept_header_value", HEADER_VALUE)
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_missing_accept_header(
    nhsd_apim_proxy_url,
    accept_header_name,
    accept_header_value,
    request_path,
    correlation_id,
    method,
    nhsd_apim_auth_headers
):
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-Id": correlation_id
    })

    assert resp.status_code == 201
