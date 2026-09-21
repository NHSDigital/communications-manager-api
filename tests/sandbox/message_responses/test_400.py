import requests
import pytest
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, CORRELATION_IDS, INVALID_MESSAGE_IDS


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("message_id", INVALID_MESSAGE_IDS)
def test_400_invalid_message_id(nhsd_apim_proxy_url, correlation_id, message_id):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGE_RESPONSES_ENDPOINT}/{message_id}",
        headers={
            "X-Correlation-Id": correlation_id,
            "Accept": "application/json"
        }
    )

    assert resp.status_code == 400, f"Response: {resp.status_code}: {resp.text}"
