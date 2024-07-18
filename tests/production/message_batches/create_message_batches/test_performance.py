import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.constants import PROD_URL, NUM_MAX_ERRORS
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.fixtures import *  # NOSONAR

NUM_MESSAGES = 50000


@pytest.mark.prodtest
def test_create_messages_large_invalid_payload(bearer_token_prod):
    """
    .. include:: ../../partials/performance/test_create_messages_large_valid_payload.rst
    """
    data = Generators.generate_valid_create_message_batch_body()

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

    resp = requests.post(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": bearer_token_prod.value
    }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS


@pytest.mark.prodtest
def test_create_messages_large_not_unique_payload(bearer_token_prod):
    """
    .. include:: ../../partials/performance/test_create_messages_large_not_unique_payload.rst
    """
    data = Generators.generate_valid_create_message_batch_body()

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

    resp = requests.post(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": bearer_token_prod.value
    }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS
