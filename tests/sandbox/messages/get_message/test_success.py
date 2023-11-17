import os
import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT


def get_200_message_ids():
    directory_path = os.path.join(os.path.dirname(__file__), '../../../../sandbox/messages')
    return [os.path.splitext(file)[0] for file in os.listdir(directory_path)]


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
@pytest.mark.parametrize('message_ids', get_200_message_ids())
def test_200_get_message_valid_accept_headers(nhsd_apim_proxy_url, accept_headers, message_ids):

    """
    .. include:: ../../partials/happy_path/test_200_messages_message_id.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/{message_ids}",
        headers={
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
    )
    Assertions.assert_200_response_message(resp, "sandbox")
