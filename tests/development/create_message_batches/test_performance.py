import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants import NUM_MAX_ERRORS

NUM_MESSAGES = 50000
CONTENT_TYPE = "application/json"


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_create_messages_large_invalid_payload(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
        ### Description

        Tests the API to ensure that it can handle large invalid payloads.

        A large invalid payload is 50,000 messages where each of them has
        an invalid nhsNumber.


    """
    data = Generators.generate_valid_create_message_batch_body("dev")

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

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        **nhsd_apim_auth_headers,
        "Accept": CONTENT_TYPE,
        "Content-Type": CONTENT_TYPE
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS

test_create_messages_large_invalid_payload.__doc__ = "Create Message Batches - Performance - Test large invalid payloads"


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_create_messages_large_not_unique_payload(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    data = Generators.generate_valid_create_message_batch_body("dev")

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

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        **nhsd_apim_auth_headers,
        "Accept": CONTENT_TYPE,
        "Content-Type": CONTENT_TYPE
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS
