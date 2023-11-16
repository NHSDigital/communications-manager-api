import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_200_get_message_valid_accept_headers(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_messages_message_id.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/2WL4QcKGjNHvHFQeKgYbapZJGHK",
        headers={
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
        json=data
    )
    Assertions.assert_200_response_message(resp, "sandbox")
