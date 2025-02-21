import requests
import pytest
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.fixtures import *  # NOSONAR


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_200_get_message(url, bearer_token):
    """
    .. include:: ../partials/happy_path/test_200_messages_message_id.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body(url)

    create_message_response = requests.post(f"{url}{MESSAGES_ENDPOINT}", headers=headers, json=data)
    message_id = create_message_response.json().get("data").get("id")

    get_message_response = requests.get(f"{url}{MESSAGES_ENDPOINT}/{message_id}", headers=headers)
    Assertions.assert_200_response_message(get_message_response, url)
