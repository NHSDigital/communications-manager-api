import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.devtest
def test_duplicate_message_request(
    nhsd_apim_proxy_url,
    bearer_token_internal_dev
):
    """
    .. include:: ../../partials/duplicate_request/test_422_duplicate_request.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")

    resp_one = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )

    assert resp_one.status_code == 201

    time.sleep(5)

    resp_two = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp_two,
        422,
        Generators.generate_duplicate_batch_request_error(),
        correlation_id
    )
