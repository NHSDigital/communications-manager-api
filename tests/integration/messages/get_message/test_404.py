import requests
import pytest
import uuid
from lib import Assertions, Generators, Authentication
from lib.constants.constants import INT_URL
from lib.constants.messages_paths import MESSAGES_ENDPOINT, MESSAGE_ID_NOT_BELONGING_TO_CLIENT


@pytest.mark.inttest
def test_message_id_not_belonging_to_client_id():
    """
    .. include:: ../../partials/not_found/test_message_id_not_belonging_to_client_id.rst
    """
    resp = requests.get(
        f"{INT_URL}{MESSAGES_ENDPOINT}/{MESSAGE_ID_NOT_BELONGING_TO_CLIENT}",
        headers={"Authorization": Authentication.generate_authentication("int")}
        )
    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )


@pytest.mark.inttest
def test_message_id_that_does_not_exist():
    """
    .. include:: ../../partials/not_found/test_message_id_that_does_not_exist.rst
    """
    resp = requests.get(
        f"{INT_URL}{MESSAGES_ENDPOINT}/does_not_exist",
        headers={"Authorization": Authentication.generate_authentication("int")}
        )
    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )
