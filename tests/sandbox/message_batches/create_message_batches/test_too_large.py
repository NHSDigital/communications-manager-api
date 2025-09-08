import requests
import pytest
import uuid
import json
import lib.constants.constants as constants
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT

MESSAGE_LIMIT = 45000
CONTENT_TYPE = "application/json"


@pytest.mark.sandboxtest
def test_too_many_messages(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/too_large/test_too_many_messages.rst
    """

    data = Generators.generate_valid_create_message_batch_body("sandbox")
    messages = []
    data["data"]["attributes"]["messages"] = messages

    for _ in range(MESSAGE_LIMIT+1):
        messages.append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "x"
                }
            })
    # make sure it's less than 6MB to be a fair test
    assert len(json.dumps(data)) < 6000000
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
