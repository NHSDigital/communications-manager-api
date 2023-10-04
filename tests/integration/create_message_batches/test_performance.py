import requests
import pytest
import uuid
from lib import Assertions, Generators, Authentication
from lib.constants import NUM_MAX_ERRORS, INT_URL

NUM_MESSAGES = 50000
CONTENT_TYPE = "application/json"


@pytest.mark.inttest
def test_create_messages_large_invalid_payload():
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
    data = Generators.generate_valid_create_message_batch_body("int")

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    for _ in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "not valid",
            },
            "personalisation": {}
        })

    resp = requests.post(f"{INT_URL}/v1/message-batches", headers={
        "Accept": CONTENT_TYPE,
        "Content-Type": CONTENT_TYPE,
        "Authorization": f"{Authentication.generate_authentication('int')}"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS


@pytest.mark.inttest
def test_create_messages_large_not_unique_payload():
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
    data = Generators.generate_valid_create_message_batch_body("int")

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    reference = str(uuid.uuid1())
    for _ in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": reference,
            "recipient": {
                "nhsNumber": "not valid",
            },
            "personalisation": {}
        })

    resp = requests.post(f"{INT_URL}/v1/message-batches", headers={
        "Accept": CONTENT_TYPE,
        "Content-Type": CONTENT_TYPE,
        "Authorization": f"{Authentication.generate_authentication('int')}"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS
