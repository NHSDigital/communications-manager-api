import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import lib.constants.constants as constants


@pytest.mark.devtest
def test_400_cannot_set_contact_details(nhsd_apim_proxy_url, bearer_token_internal_dev_test_1):
    """
    .. include:: ../../partials/validation/test_not_permitted_to_use_contact_details.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = constants.VALID_NHS_NUMBER
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "sms": "07777777777",
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev_test_1.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(
            constants.ERROR_CANNOT_SET_CONTACT_DETAILS,
            source={
                "pointer": "/data/attributes/recipient/contactDetails"
                }
                ),
        correlation_id
    )
