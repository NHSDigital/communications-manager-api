import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.constants import CORRELATION_IDS

FORBIDDEN_TOKEN = {"Authorization": "Bearer ClientNotRecognised"}
TRIGGER_425_ROUTING_CONFIG_ID = "d895ade5-0029-4fc3-9fb5-86e1e5370854"


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_425_retry_too_early(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: An API consumer retrying a request while the \
        original request is still being processed receives a 425 error

        | **Given** the API consumer retries a request
        | **When** the original request is still being processed
        | **Then** the response returns a 425 retry too early error

    **Asserts**
    - Response returns a 425 'Retry Too Early' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            "Content-Type": "application/json",
            "X-Correlation-Id": correlation_id,
            "Accept": "*/*",
        },
        json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": TRIGGER_425_ROUTING_CONFIG_ID,
                    "messageBatchReference": str(uuid.uuid1()),
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "9990548609",
                                "dateOfBirth": "2023-01-01",
                            },
                            "personalisation": {},
                        }
                    ],
                },
            }
        },
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp, 425, Generators.generate_retry_too_early_error(), correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_prefer_425_retry_too_early(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: An API consumer wants to test the retry too \
        early error message on the sandbox environment

        | **Given** the API consumer provides a code 425 prefer header
        | **When** the request is submitted
        | **Then** the response returns a 425 retry too early error

    **Asserts**
    - Response returns a 425 'Retry Too Early' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            "Prefer": "code=425",
            "Content-Type": "application/json",
            "X-Correlation-Id": correlation_id,
            "Accept": "*/*",
        },
        json=Generators.generate_valid_create_message_batch_body("sandbox"),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp, 425, Generators.generate_retry_too_early_error(), correlation_id
    )
