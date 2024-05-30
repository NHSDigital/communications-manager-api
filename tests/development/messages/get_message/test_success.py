import requests
import pytest
from lib import Assertions, Authentication
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT, MESSAGE_IDS, CHANNEL_TYPE, CHANNEL_STATUS


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
@pytest.mark.parametrize('message_ids', MESSAGE_IDS)
def test_200_get_message(nhsd_apim_proxy_url, accept_headers, message_ids):
    """
    .. include:: ../../partials/happy_path/test_200_messages_message_id.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/{message_ids}",
        headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_200_get_message_pending_enrichment(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_get_message_pending_enrichment.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/pending_enrichment_request_item_id",
        headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, nhsd_apim_proxy_url)
    Assertions.assert_get_message_status(resp, "pending_enrichment")


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_200_get_message_sending(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_get_message_sending.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/sending_nhsapp_request_item_id",
        headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, nhsd_apim_proxy_url)
    Assertions.assert_get_message_status(resp, "sending")


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_200_get_message_successful(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_get_message_successful.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/successful_letter_request_item_id",
        headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, nhsd_apim_proxy_url)
    Assertions.assert_get_message_status(resp, "delivered")


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_200_get_message_failed(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_get_message_failed.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/exit_code_request_item_id",
        headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, nhsd_apim_proxy_url)
    Assertions.assert_get_message_status(resp, "failed", "Failed reason: patient has exit code")


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_200_get_message_cascade(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_get_message_cascade.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/cascade_sending_all_status_request_item_id",
        headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, nhsd_apim_proxy_url)
    Assertions.assert_get_message_status(resp, "sending")
    Assertions.assert_get_message_response_channels(resp, CHANNEL_TYPE, CHANNEL_STATUS)
