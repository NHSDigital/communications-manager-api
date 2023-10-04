import requests
import pytest
from lib import Assertions, Generators
from lib.constants import UNEXPECTED_429

REQUEST_PATH = "/v1/message-batches"
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]
VALID_CONTENT_TYPE_HEADERS = ["application/json", "application/vnd.api+json"]


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_missing_accept_header(
    nhsd_apim_proxy_url,
    correlation_id,
    content_type,
    nhsd_apim_auth_headers
):
    """
    .. py:function:: Scenario: An API consumer submitting a request without an accept header \
        receives a successful response

        | **Given** the API consumer does not provide an accept header
        | **When** the request is submitted
        | **Then** the response returned is successful

    **Asserts**
    - Response returns a 201 success

    .. include:: ../../partials/valid_accept_headers.rst
    .. include:: ../../partials/methods.rst

    """
    data = Generators.generate_valid_create_message_batch_body("dev")

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{REQUEST_PATH}",
        headers={
            "Content-Type": content_type,
            "X-Correlation-Id": correlation_id,
            **nhsd_apim_auth_headers,
        },
        json=data
    )

    if resp.status_code == 429:
        raise UNEXPECTED_429

    Assertions.assert_201_response(
        resp, data["data"]["attributes"]["messageBatchReference"]
    )
