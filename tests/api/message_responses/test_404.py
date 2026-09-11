import os
import requests
import pytest
from lib import Assertions, Generators
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, NOT_FOUND_MESSAGE_ID
from lib.fixtures import *  # NOSONAR

# ref has no app-response backend; the endpoint is deliberately disabled there
pytestmark = pytest.mark.skipif(
    os.environ.get("API_ENVIRONMENT") == "ref",
    reason="message-responses endpoint is not available in ref"
)


@pytest.mark.devtest
def test_404_not_found(url, bearer_token):
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{MESSAGE_RESPONSES_ENDPOINT}/{NOT_FOUND_MESSAGE_ID}",
        headers=headers
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )
