import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import lib.constants.constants as constants

CORRELATION_IDS = [None, "0f160ae2-9b62-47bf-bdf0-c6a844d59488"]


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_duplicate_message_request(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/duplicate_request/test_422_duplicate_request.rst
    """
    data = Generators.generate_valid_create_message_body("dev")

    resp_one = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
            "X-Correlation-Id": correlation_id
        }, json=data
    )

    assert resp_one.status_code == 201

    time.sleep(5)

    resp_two = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
            "X-Correlation-Id": correlation_id
        }, json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp_two,
        422,
        Generators.generate_duplicate_message_request_error(),
        correlation_id
    )
