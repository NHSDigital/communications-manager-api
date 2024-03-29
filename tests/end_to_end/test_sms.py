import pytest
import os
from lib import Assertions, Generators, Helper
from notifications_python_client.notifications import NotificationsAPIClient


@pytest.mark.e2e
@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_sms_end_to_end_internal_dev(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_sms_end_to_end_internal_dev.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        nhsd_apim_auth_headers,
        Generators.generate_send_message_body("sms", "internal-dev")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth=nhsd_apim_auth_headers,
        message_id=message_id
    )

    notifications_client = NotificationsAPIClient(os.environ.get("GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("delivered").get("notifications")

    Assertions.assert_sms_gov_uk(gov_uk_response, message_id)


@pytest.mark.e2e
@pytest.mark.uattest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_sms_end_to_end_uat(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_sms_end_to_end_uat.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        nhsd_apim_auth_headers,
        Generators.generate_send_message_body("sms", "internal-qa")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth=nhsd_apim_auth_headers,
        message_id=message_id
    )

    notifications_client = NotificationsAPIClient(os.environ.get("UAT_GUKN_API_KEY"))
    gov_uk_response = notifications_client.get_all_notifications("delivered").get("notifications")

    Assertions.assert_sms_gov_uk(gov_uk_response, message_id)
