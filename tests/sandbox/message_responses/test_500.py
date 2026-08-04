import requests
import pytest
from lib import Assertions, Generators
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, CORRELATION_IDS, TOO_MANY_RESPONSES_MESSAGE_ID


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_500_too_many_responses(nhsd_apim_proxy_url, correlation_id):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGE_RESPONSES_ENDPOINT}/{TOO_MANY_RESPONSES_MESSAGE_ID}",
        headers={
            "X-Correlation-Id": correlation_id,
            "Accept": "application/json"
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_internal_server_error(),
        correlation_id
    )
