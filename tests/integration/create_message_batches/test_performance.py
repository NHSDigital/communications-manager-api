import requests
import pytest
import uuid
from lib import Assertions, Generators, Authentication
from lib.constants import NUM_MAX_ERRORS, INT_URL

NUM_MESSAGES = 50000
CONTENT_TYPE = "application/json"


@pytest.mark.inttest
def test_create_messages_large_invalid_payload():
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
        "Authorization": f"{Authentication.generate_int_authentication()}"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS


@pytest.mark.inttest
def test_create_messages_large_not_unique_payload():
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
        "Authorization": f"{Authentication.generate_int_authentication()}"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS
