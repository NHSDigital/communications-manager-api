import requests
import pytest
from lib import Assertions, Generators
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, CORRELATION_IDS, BAD_GATEWAY_MESSAGE_ID


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_502_bad_gateway(nhsd_apim_proxy_url, correlation_id):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGE_RESPONSES_ENDPOINT}/{BAD_GATEWAY_MESSAGE_ID}",
        headers={
            "X-Correlation-Id": correlation_id,
            "Accept": "application/json"
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        502,
        Generators.generate_bad_gateway_error(),
        correlation_id
    )
