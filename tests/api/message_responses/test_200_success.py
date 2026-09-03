import os
import requests
import pytest
from lib import Assertions, Generators
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, VALID_MESSAGE_ID
from lib.fixtures import *  # NOSONAR

# ref has no app-response backend; the endpoint is deliberately disabled there
pytestmark = pytest.mark.skipif(
    os.environ.get("API_ENVIRONMENT") == "ref",
    reason="message-responses endpoint is not available in ref"
)


@pytest.mark.devtest
def test_200_success(url, bearer_token):
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{MESSAGE_RESPONSES_ENDPOINT}/{VALID_MESSAGE_ID}",
        headers=headers
    )

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
    body = resp.json()
    assert isinstance(body.get("data"), list)
    assert len(body["data"]) > 0

    first = body["data"][0]
    assert first["type"] == "RecipientResponse"
    assert "id" in first
    assert first["attributes"]["messageId"] == VALID_MESSAGE_ID
