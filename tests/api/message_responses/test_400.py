import os
import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_responses_paths import MESSAGE_RESPONSES_ENDPOINT, INVALID_MESSAGE_IDS, VALID_MESSAGE_ID
from lib.fixtures import *  # NOSONAR

# ref has no app-response backend; the endpoint is deliberately disabled there
pytestmark = pytest.mark.skipif(
    os.environ.get("API_ENVIRONMENT") == "ref",
    reason="message-responses endpoint is not available in ref"
)


@pytest.mark.devtestonly
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


@pytest.mark.devtestonly
@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization(
    access="healthcare_worker",
    level="aal3",
    login_form={"username": "656005750104"},
    authentication="separate",
)
def test_403_user_token(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGE_RESPONSES_ENDPOINT}/{VALID_MESSAGE_ID}",
        headers=nhsd_apim_auth_headers
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_forbidden_error(),
        None
    )
