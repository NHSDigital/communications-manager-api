import requests
import pytest
from lib import Assertions, Generators
from lib.constants import CORRELATION_IDS, MESSAGE_BATCHES_ENDPOINT

FORBIDDEN_TOKEN = {
    "Authorization": "Bearer ClientNotRecognised"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_403_service_ban(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/service_ban/test_403_service_ban.rst
    """

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": "banned",
            "Content-Type": "application/json",
            "X-Correlation-Id": correlation_id,
            "Accept": "*/*"
        },
        json=Generators.generate_valid_create_message_batch_body("sandbox")
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_service_ban_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_prefer_403_service_ban(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/service_ban/test_prefer_403_service_ban.rst
    """

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Prefer": "code=403.1",
            "Content-Type": "application/json",
            "X-Correlation-Id": correlation_id,
            "Accept": "*/*"
        },
        json=Generators.generate_valid_create_message_batch_body("sandbox")
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_service_ban_error(),
        correlation_id
    )
