import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import GLOBAL_ROUTING_CONFIGURATION_SMS


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_too_large_personalisation(url, bearer_token):
    """
    .. include:: ../partials/validation/test_too_large_personalisation.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["routingPlanId"] = GLOBAL_ROUTING_CONFIGURATION_SMS
    data["data"]["attributes"]["personalisation"] = {
        'sms_body': 'x'*919
    }

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_personalisation_error(
            "Total personalisation length of 919 exceeding the maximum length of 918",
            "/data/attributes/personalisation"),
        None
    )
