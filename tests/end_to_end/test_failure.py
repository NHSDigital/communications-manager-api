import pytest
import os
from lib import Assertions, Helper, Generators
from lib.fixtures import *  # NOSONAR
from notifications_python_client.notifications import NotificationsAPIClient


@pytest.mark.e2e
@pytest.mark.devtest
def test_invalid_end_to_end_internal_dev(url, bearer_token):
    """
    .. include:: ../../partials/happy_path/test_invalid_end_to_end_internal_dev.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = Helper.send_single_message(
        url, headers, Generators.generate_invalid_send_message_body("email", "internal-dev")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(url=url, headers=headers, message_id=message_id, end_state="failed")

    resp = Helper.get_message(url, headers, message_id)

    Assertions.assert_get_message_status(
        resp,
        "failed",
        "Failed reason: No valid request item plans were generated",
        "MFR_CFGV_0005"
    )

    Assertions.assert_get_message_response_channels(
        resp,
        "failed",
        "Failed reason: Alternative contact detail is malformed",
        "CFR_CLIV_0001",
    )


@pytest.mark.e2e
@pytest.mark.uattest
def test_invalid_end_to_end_uat(url, bearer_token):
    """
    .. include:: ../../partials/happy_path/test_invalid_end_to_end_uat.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = Helper.send_single_message(
        url, headers, Generators.generate_invalid_send_message_body("email", "internal-qa")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(url=url, headers=headers, message_id=message_id, end_state="failed")

    resp = Helper.get_message(url, headers, message_id)

    Assertions.assert_get_message_status(
        resp,
        "failed",
        "Failed reason: No valid request item plans were generated",
        "MFR_CFGV_0005"
    )

    Assertions.assert_get_message_response_channels(
        resp,
        "failed",
        "Failed reason: Alternative contact detail is malformed",
        "CFR_CLIV_0001",
    )
