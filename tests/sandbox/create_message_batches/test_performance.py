import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants import NUM_MAX_ERRORS

NUM_MESSAGES = 50000


@pytest.mark.sandboxtest
def test_create_messages_large_valid_payload(nhsd_apim_proxy_url):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        request body containing 50,000 messages receives a 201 response

        | **Given** the API consumer provides a message body of around 50k messages
        | **When** the request is submitted
        | **Then** the response is a 201 success
        | **And** the response takes less than 29 seconds

    **Asserts**
    - Response returns a 201 status code
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    for i in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "9990548609"
            },
            "personalisation": {}
        })

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.sandboxtest
def test_create_messages_large_invalid_payload(nhsd_apim_proxy_url):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        request body containing 50,000 invalid messages receives a 400 status code \
        and response body containing the first 100 instances of errors

        | **Given** the API consumer provides a message body of 50,000 invalid messages
        | **When** the request is submitted
        | **Then** the response is a 400 invalid value error
        | **And** the response body contains 100 errors
        | **And** the response takes less than 29 seconds


    **Asserts**
    - Response returns a 400 'Invalid Value' status code
    - Response returns 100 error message blocks
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    for i in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "not valid",
            },
            "personalisation": {}
        })

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS


@pytest.mark.sandboxtest
def test_create_messages_large_not_unique_payload(nhsd_apim_proxy_url):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        large request body containing 50,000 duplicate messages receives a 400 response

        | **Given** the API consumer provides a message body of 50,000 duplicate messages
        | **When** the request is submitted
        | **Then** the response is a 400 invalid value error
        | **And** the response body contains 100 errors
        | **And** the response takes less than 29 seconds

    **Asserts**
    - Response returns a 400 'Invalid Value' status code
    - Response returns 100 error message blocks
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    reference = str(uuid.uuid1())
    for i in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": reference,
            "recipient": {
                "nhsNumber": "not valid",
            },
            "personalisation": {}
        })

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS
