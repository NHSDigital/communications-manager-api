import os
import requests
import pytest
from lib import Assertions
from lib.constants.constants import INT_URL
from lib.constants.messages_paths import MESSAGES_ENDPOINT, SUCCESSFUL_MESSAGE_IDS
from lib.fixtures import *


@pytest.mark.inttest
@pytest.mark.parametrize('message_ids', SUCCESSFUL_MESSAGE_IDS)
def test_200_get_message(bearer_token_int, message_ids):
    """
    .. include:: ../../partials/happy_path/test_200_messages_message_id.rst
    """
    resp = requests.get(
        f"{INT_URL}{MESSAGES_ENDPOINT}/{message_ids}",
        headers={"Authorization": bearer_token_int}
        )
    Assertions.assert_200_response_message(resp, INT_URL)
    Assertions.assert_get_message_response_channels(resp, "email", "delivered")
