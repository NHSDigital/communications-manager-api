import pytest
import uuid
from lib import Assertions, Generators, Helper
from lib.fixtures import *  # NOSONAR


@pytest.mark.e2e
@pytest.mark.devtest
def test_nhsapp_end_to_end(url, bearer_token):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end_internal_dev.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = Helper.send_single_message(
        url,
        headers,
        Generators.generate_send_message_body("nhsapp", "internal-dev")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=url,
        headers=headers,
        message_id=message_id
    )

    Assertions.assert_get_message_status(
        Helper.get_message(
            url,
            headers,
            message_id
        ),
        "delivered"
    )


@pytest.mark.e2e
@pytest.mark.uattest
def test_nhsapp_end_to_end_uat(url, bearer_token):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end_uat.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    personalisation = str(uuid.uuid1())

    resp = Helper.send_single_message(
        url,
        headers,
        Generators.generate_send_message_body("nhsapp", "internal-qa", personalisation)
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=url,
        headers=headers,
        message_id=message_id,
        end_state="sending"
    )

    Assertions.assert_get_message_status(
        Helper.get_message(
            url,
            headers,
            message_id
        ),
        "sending"
    )

    Helper.nhs_app_login_and_view_message(personalisation)
