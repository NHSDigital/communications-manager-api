import requests
import pytest
from lib import Assertions, Generators
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, VALID_MESSAGE_ID
from lib.fixtures import *  # NOSONAR


@pytest.mark.devtest
def test_200_success(url, bearer_token):
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{MESSAGE_RESPONSES_ENDPOINT}/{VALID_MESSAGE_ID}",
        headers=headers
    )

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
    body = resp.json()
    assert "messageId" in body
    assert isinstance(body.get("responses"), list)
