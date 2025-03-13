import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_duplicate_message_request(url, bearer_token):
    """
    .. include:: ../partials/duplicate_request/test_422_duplicate_request.rst
    """
    data = Generators.generate_valid_create_message_batch_body(url)
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp_one = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )

    assert resp_one.status_code == 201

    time.sleep(5)

    resp_two = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp_two,
        422,
        Generators.generate_duplicate_batch_request_error(),
        None
    )
