import pytest
import os
from lib import Assertions, Generators, Helper
from notifications_python_client.notifications import NotificationsAPIClient


@pytest.mark.e2e
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_letter_end_to_end(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_letter_end_to_end.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        nhsd_apim_auth_headers,
        Generators.generate_send_message_body("letter")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth=nhsd_apim_auth_headers,
        message_id=message_id,
        end_state="sending",
        poll_time=595
    )

    notifications_client = NotificationsAPIClient(os.environ.get("GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("received").get("notifications")

    Assertions.assert_letter_gov_uk(gov_uk_response, message_id)
