import requests
import pytest
from lib import Assertions, Generators, error_handler
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT

CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]
VALID_CONTENT_TYPE_HEADERS = ["application/json", "application/vnd.api+json"]


@pytest.mark.devtest
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_missing_accept_header(
    url,
    bearer_token,
    correlation_id,
    content_type
):
    """
    .. include:: ../partials/content_types/test_missing_accept_header.rst
    """
    data = Generators.generate_valid_create_message_batch_body()

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Content-Type": content_type,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token.value,
        },
        json=data
    )

    error_handler.handle_retry(resp)
    Assertions.assert_201_response(resp, data)
