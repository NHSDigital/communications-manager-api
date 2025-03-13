import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT

CORRELATION_IDS = [None, "0f160ae2-9b62-47bf-bdf0-c6a844d59488"]


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_duplicate_message_request(url, bearer_token):
    """
    .. include:: /partials/duplicate_request/test_422_duplicate_request.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")

    resp_one = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    assert resp_one.status_code == 201

    time.sleep(5)

    resp_two = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp_two,
        422,
        Generators.generate_duplicate_message_request_error(),
        None
    )
