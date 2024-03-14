import pytest
from lib import Assertions, Generators, Helper


@pytest.mark.e2e
@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_nhsapp_end_to_end(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end_internal_dev.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        nhsd_apim_auth_headers,
        Generators.generate_send_message_body("nhsapp", "internal-dev")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth=nhsd_apim_auth_headers,
        message_id=message_id
    )

    Assertions.assert_get_message_status(
        Helper.get_message(nhsd_apim_proxy_url, nhsd_apim_auth_headers, message_id), "delivered")


@pytest.mark.e2e
@pytest.mark.uattest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_nhsapp_end_to_end_uat(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end_uat.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        nhsd_apim_auth_headers,
        Generators.generate_send_message_body("nhsapp", "internal-qa")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth=nhsd_apim_auth_headers,
        message_id=message_id,
        end_state="sending"
    )

    Assertions.assert_get_message_status(
        Helper.get_message(nhsd_apim_proxy_url, nhsd_apim_auth_headers, message_id), "sending")

    Helper.nhs_app_login_and_view_message()
