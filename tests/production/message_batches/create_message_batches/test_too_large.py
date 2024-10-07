import requests
import pytest
import uuid
import json
import constants.constants as constants
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT

MESSAGE_LIMIT = 45000
CONTENT_TYPE = "application/json"


@pytest.mark.prodtest
def test_too_many_messages(bearer_token_prod):
    """
    .. include:: ../../partials/too_large/test_too_many_messages.rst
    """

    data = Generators.generate_valid_create_message_batch_body("prod")
    messages = []
    data["data"]["attributes"]["messages"] = messages

    for i in range(MESSAGE_LIMIT+1):
        messages.append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "x"
                }
            })
    # make sure it's less than 6MB to be a fair test
    assert len(json.dumps(data)) < 6000000
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
            "Authorization": bearer_token_prod.value,
            "Accept": CONTENT_TYPE,
            "Content-Type": CONTENT_TYPE
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        413,
        Generators.generate_error(
            constants.ERROR_TOO_MANY_ITEMS,
            source={"pointer": "/data/attributes/messages"}
        ),
        None
    )


@pytest.mark.prodtest
def test_payload_too_large(bearer_token_prod):
    """
    .. include:: ../../partials/too_large/test_payload_too_large.rst
    """

    data = Generators.generate_valid_create_message_batch_body("prod")
    valid_recipient = data["data"]["attributes"]["messages"][0]["recipient"]
    large_personalisation = {'body': 'x'*32}
    messages = []
    data["data"]["attributes"]["messages"] = messages

    for i in range(MESSAGE_LIMIT):
        messages.append({
            "messageReference": str(uuid.uuid1()),
            "recipient": valid_recipient,
            "personalisation": large_personalisation
            })
    # make sure it's more than 6MB to be a fair test
    payload_length = len(json.dumps(data))
    assert payload_length > 6*(1024**2)
    # but less than 10MB to make sure it doesn't fail because apigee didn't accept it
    assert payload_length < 10000000

    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
            "Authorization": bearer_token_prod.value,
            "Accept": CONTENT_TYPE,
            "Content-Type": CONTENT_TYPE
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        413,
        Generators.generate_error(
            constants.ERROR_TOO_LARGE,
            source={"pointer": "/"}
        ),
        None
    )
