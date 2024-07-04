import requests
import pytest
from lib import Assertions, Generators, Error_Handler
from lib.fixtures import *
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT

CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]
VALID_CONTENT_TYPE_HEADERS = ["application/json", "application/vnd.api+json"]


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_missing_accept_header(
    nhsd_apim_proxy_url,
    bearer_token_internal_dev,
    correlation_id,
    content_type
):
    """
    .. include:: ../../partials/content_types/test_missing_accept_header.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Content-Type": content_type,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token_internal_dev.value,
        },
        json=data
    )

    Error_Handler.handle_retry(resp)

    Assertions.assert_201_response(
        resp, data["data"]["attributes"]["messageBatchReference"], data["data"]["attributes"]["routingPlanId"]
    )
