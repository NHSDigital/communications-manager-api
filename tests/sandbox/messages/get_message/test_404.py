import requests
import pytest
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT

CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
MESSAGE_ID = "blank"


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_message_id_not_found(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/not_found/test_404_not_found_single_method.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/{MESSAGE_ID}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "*/*",
        "Content-Type": "application/json"
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        correlation_id
        )
