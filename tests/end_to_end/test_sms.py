import requests
import pytest
import time
import os
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from notifications_python_client.notifications import NotificationsAPIClient


@pytest.mark.e2e
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_sms_end_to_end(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_sms_end_to_end.rst
    """
    post_single_message_response = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }, json=Generators.generate_send_message_body("sms")
    )

    Assertions.assert_201_response_messages(post_single_message_response, "internal-dev")

    message_id = post_single_message_response.json().get("data").get("id")
    message_status = None
    end_time = int(time.time()) + 300

    while message_status != 'delivered' and int(time.time()) < end_time:
        get_message_response = requests.get(
            f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/{message_id}",
            headers={
                **nhsd_apim_auth_headers,
                "Accept": "application/vnd.api+json"
            },
        )

        Assertions.assert_200_response_message(get_message_response, "internal-dev")

        message_status = get_message_response.json().get("data").get("attributes").get("messageStatus")
        time.sleep(10)

    if message_status != "delivered":
        raise TimeoutError(f"Request took too long to be processed. Message id: {message_id}")

    notifications_client = NotificationsAPIClient(os.environ.get("GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("delivered").get("notifications")

    Assertions.assert_message_delivered_gov_uk(gov_uk_response, message_id, "sms")
