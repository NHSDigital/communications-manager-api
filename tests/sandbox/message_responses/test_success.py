import requests
import pytest
from lib import Assertions
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, CORRELATION_IDS, VALID_MESSAGE_ID


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_200_success(nhsd_apim_proxy_url, correlation_id):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGE_RESPONSES_ENDPOINT}/{VALID_MESSAGE_ID}",
        headers={
            "X-Correlation-Id": correlation_id,
            "Accept": "application/json"
        }
    )

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
    body = resp.json()
    assert isinstance(body.get("data"), list)
    assert len(body["data"]) > 0

    first = body["data"][0]
    assert first["type"] == "RecipientResponse"
    assert "id" in first

    attributes = first["attributes"]
    assert attributes["messageId"] == VALID_MESSAGE_ID
    assert "messageReference" in attributes
    assert "code" in attributes
    assert "channel" in attributes
    assert "channelStatus" in attributes
    assert "cascadeType" in attributes
    assert "authoredAt" in attributes
    assert "timestamp" in attributes

    Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
