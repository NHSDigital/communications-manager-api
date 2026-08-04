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
    assert body.get("messageId") == VALID_MESSAGE_ID
    assert isinstance(body.get("responses"), list)
    assert len(body["responses"]) > 0

    first = body["responses"][0]
    assert "responseId" in first
    assert "messageReference" in first
    assert "code" in first
    assert "channel" in first
    assert "channelStatus" in first
    assert "authoredAt" in first

    Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
