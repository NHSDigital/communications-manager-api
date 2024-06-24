import pytest
import os
from lib import Assertions, Helper, Generators
from lib.fixtures import *
from notifications_python_client.notifications import NotificationsAPIClient


@pytest.mark.e2e
@pytest.mark.devtest
def test_email_end_to_end_internal_dev(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_email_end_to_end_internal_dev.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        {"Authorization": bearer_token_internal_dev},
        Generators.generate_send_message_body("email", "internal-dev")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth={"Authorization": bearer_token_internal_dev},
        message_id=message_id
    )

    notifications_client = NotificationsAPIClient(os.environ.get("GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("delivered").get("notifications")

    Assertions.assert_email_gov_uk(gov_uk_response, message_id)


@pytest.mark.e2e
@pytest.mark.uattest
def test_email_end_to_end_uat(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_email_end_to_end_uat.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        {"Authorization": bearer_token_internal_dev},
        Generators.generate_send_message_body("email", "internal-qa")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth={"Authorization": bearer_token_internal_dev},
        message_id=message_id
    )

    notifications_client = NotificationsAPIClient(os.environ.get("UAT_GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("delivered").get("notifications")

    Assertions.assert_email_gov_uk(gov_uk_response, message_id)
