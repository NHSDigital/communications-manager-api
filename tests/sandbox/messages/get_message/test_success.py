import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT

VALID_ROUTING_PLAN_ID = [
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c",
    "b402cd20-b62a-4357-8e02-2952959531c8",
    "936e9d45-15de-4a95-bb36-ae163c33ae53",
    "9ba00d23-cd6f-4aca-8688-00abc85a7980"
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_201_message_batch_valid_accept_headers(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_200_messages_message_id.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/2WL4TEpohhdATmtxTxvqPyUIOx5",
        headers={
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
        json=data
    )
    Assertions.assert_200_response_message(resp, "sandbox")
