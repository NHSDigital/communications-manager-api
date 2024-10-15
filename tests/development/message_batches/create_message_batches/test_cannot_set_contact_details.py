import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.constants.constants import CORRELATION_IDS


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_400_cannot_set_contact_details(nhsd_apim_proxy_url, bearer_token_internal_dev_test_1, correlation_id):
    """
    .. include:: ../../partials/validation/test_not_permitted_to_use_contact_details.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"][
        "nhsNumber"
    ] = constants.VALID_NHS_NUMBER
    data["data"]["attributes"]["messages"][0]["recipient"][
        "contactDetails"
    ] = {
        "sms": "07777777777",
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev_test_1.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
            "X-Correlation-Id": correlation_id,
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(
            constants.ERROR_CANNOT_SET_CONTACT_DETAILS,
            source={
                "pointer": "/data/attributes/messages/0/recipient/contactDetails"
                }
                ),
        correlation_id
    )
