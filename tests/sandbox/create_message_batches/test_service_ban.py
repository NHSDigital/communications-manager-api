import requests
import pytest
from lib import Assertions, Generators
from lib.constants import CORRELATION_IDS

FORBIDDEN_TOKEN = {
    "Authorization": "Bearer ClientNotRecognised"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_403_service_ban(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer has been banned from the service, \
        when making requests they fail with a service ban response

        | **Given** the API consumer has been banned
        | **When** a request is submitted
        | **Then** the response returns a 403 service ban error

    **Asserts**
    - Response returns a 403 'Service Ban' error
    - Response returns the expected error message body referencing the Authorization header
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
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
    .. py:function:: Scenario: An API consumer wants to test the service ban \
        error message on the sandbox environment

        | **Given** the API consumer provides a code 403.1 prefer header
        | **When** the request is submitted
        | **Then** the response returns a 403 service ban error

    **Asserts**
    - Response returns a 403 'Service Ban' error
    - Response returns the expected error message body referencing the Authorization header
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
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
