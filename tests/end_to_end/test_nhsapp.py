import pytest
import os
from lib import Assertions, Generators, Helper


@pytest.mark.e2e
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_nhsapp_end_to_end(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        nhsd_apim_auth_headers,
        Generators.generate_send_message_body("nhsapp")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth=nhsd_apim_auth_headers,
        message_id=message_id
    )

    Assertions.assert_get_message_status(
        Helper.get_message(nhsd_apim_proxy_url, nhsd_apim_auth_headers, message_id), "delivered")
