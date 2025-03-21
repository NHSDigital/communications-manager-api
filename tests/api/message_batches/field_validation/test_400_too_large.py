import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import GLOBAL_ROUTING_CONFIGURATION_SMS
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
def test_too_large_personalisation(url, bearer_token):
    """
    .. include:: ../partials/validation/test_too_large_personalisation.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["routingPlanId"] = GLOBAL_ROUTING_CONFIGURATION_SMS
    data["data"]["attributes"]["messages"][0]["personalisation"] = {
        'sms_body': 'x'*919
    }
    while len(data["data"]["attributes"]["messages"]) > 1:
        del data["data"]["attributes"]["messages"][1]

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_personalisation_error(
            "Total personalisation length of 919 exceeding the maximum length of 918",
            "/data/attributes/messages/0/personalisation"),
        None
    )
