import requests
import pytest
from lib import Assertions, Generators

REQUEST_PATH = ["/v1/message-batches"]
METHODS = ["post"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.devtest
@pytest.mark.parametrize("request_path", REQUEST_PATH)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_missing_accept_header(
    nhsd_apim_proxy_url,
    request_path,
    correlation_id,
    method,
    nhsd_apim_auth_headers
):
    data = Generators.generate_valid_create_message_batch_body()

    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id
    })

    if resp.status_code == 429:
        raise AssertionError('Unexpected 429')

    Assertions.assert_201_response(
        resp, data["data"]["attributes"]["messageBatchReference"]
    )
