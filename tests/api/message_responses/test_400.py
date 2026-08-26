import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, INVALID_MESSAGE_IDS
from lib.fixtures import *  # NOSONAR


@pytest.mark.devtest
@pytest.mark.parametrize("message_id", INVALID_MESSAGE_IDS)
def test_400_invalid_message_id(url, bearer_token, message_id):
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{MESSAGE_RESPONSES_ENDPOINT}/{message_id}",
        headers=headers
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(
            constants.ERROR_MESSAGE_RESPONSES_INVALID_MESSAGE_ID,
            source={"parameter": "messageId"}
        ),
        None
    )
