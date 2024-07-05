import pytest
import uuid
from lib import Assertions, Generators, Helper
from lib.fixtures import *


@pytest.mark.e2e
@pytest.mark.devtest
def test_nhsapp_end_to_end(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end_internal_dev.rst
    """
    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        {"Authorization": bearer_token_internal_dev},
        Generators.generate_send_message_body("nhsapp", "internal-dev")
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth={"Authorization": bearer_token_internal_dev},
        message_id=message_id
    )

    Assertions.assert_get_message_status(
        Helper.get_message(
            nhsd_apim_proxy_url,
            {"Authorization": bearer_token_internal_dev},
            message_id
        ),
        "delivered"
    )


@pytest.mark.e2e
@pytest.mark.uattest
def test_nhsapp_end_to_end_uat(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_nhsapp_end_to_end_uat.rst
    """
    personalisation = str(uuid.uuid1())

    resp = Helper.send_single_message(
        nhsd_apim_proxy_url,
        {"Authorization": bearer_token_internal_dev},
        Generators.generate_send_message_body("nhsapp", "internal-qa", personalisation)
    )

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(
        url=nhsd_apim_proxy_url,
        auth={"Authorization": bearer_token_internal_dev},
        message_id=message_id,
        end_state="sending"
    )

    Assertions.assert_get_message_status(
        Helper.get_message(
            nhsd_apim_proxy_url,
            {"Authorization": bearer_token_internal_dev},
            message_id
        ),
        "sending"
    )

    Helper.nhs_app_login_and_view_message(personalisation)
