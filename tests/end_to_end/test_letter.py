import pytest
import os
from lib import Assertions, Generators, Helper
from lib.fixtures import *  # NOSONAR
from notifications_python_client.notifications import NotificationsAPIClient


@pytest.mark.e2e
@pytest.mark.devtest
def test_letter_end_to_end_internal_dev(url, bearer_token):
    """
    .. include:: ../../partials/happy_path/test_letter_end_to_end_internal_dev.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = Helper.send_single_message(
        url,
        headers,
        Generators.generate_send_message_body("letter", "internal-dev"),
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=url,
        headers=headers,
        message_id=message_id,
        end_state="sending",
        poll_time=595,
    )

    notifications_client = NotificationsAPIClient(os.environ.get("GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("received").get(
        "notifications"
    )

    Assertions.assert_letter_gov_uk(gov_uk_response, message_id)


@pytest.mark.e2e
@pytest.mark.uattest
def test_letter_end_to_end_uat(url, bearer_token):
    """
    .. include:: ../../partials/happy_path/test_letter_end_to_end_uat.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = Helper.send_single_message(
        url,
        headers,
        Generators.generate_send_message_body("letter", "internal-qa"),
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=url,
        headers=headers,
        message_id=message_id,
        end_state="sending",
        poll_time=595,
    )

    notifications_client = NotificationsAPIClient(os.environ.get("UAT_GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("received").get(
        "notifications"
    )

    Assertions.assert_letter_gov_uk(gov_uk_response, message_id)
