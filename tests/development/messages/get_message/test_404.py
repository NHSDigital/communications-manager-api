import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_message_id_not_belonging_to_client_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/not_found/test_message_id_not_belonging_to_client_id.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/successful_email_other_owner",
        headers=nhsd_apim_auth_headers
    )
    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_message_id_that_does_not_exist(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/not_found/test_message_id_that_does_not_exist.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/does_not_exist",
        headers=nhsd_apim_auth_headers
    )
    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )
